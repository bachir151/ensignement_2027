#!/usr/bin/env python3
"""Arithmetic checks for the CIEL2 "fil rouge" addressing plan.

Usage:
    python3 commun/verif_adressage.py [theme_dir ...]

Checks performed:
  1. The VLSM plan itself: alignment, inclusion in 192.168.10.0/24,
     no overlap, gateway = last usable address.
  2. Every Cisco config in <chapter>/packet-tracer/*.txt:
     interface addresses inside a plan network, never network/broadcast,
     no duplicates, both ends of each /30 in the same subnet, router
     sub-interface = gateway of its VLAN, static-route next hops on a
     connected network, DHCP pools and exclusions consistent,
     switch default-gateway in the SVI subnet.
  3. Every IPv4 literal found in <chapter>/**/*.tex: each a.b.c.d/p is
     either a network address or a usable host of that prefix; each
     192.168.10.x belongs to a plan network (or is flagged as free space).
Exit status is non-zero if any error is found.
"""
import ipaddress as ia
import pathlib
import re
import sys

PLAN = {  # name: (network, gateway or None)
    "VLAN10 Production": ("192.168.10.0/25", "192.168.10.126"),
    "VLAN20 Administration": ("192.168.10.128/26", "192.168.10.190"),
    "VLAN30 Invites": ("192.168.10.192/27", "192.168.10.222"),
    "R1-R2": ("192.168.10.224/30", None),
    "R2-FW": ("192.168.10.228/30", None),
}
BLOCK = ia.ip_network("192.168.10.0/24")
OUTSIDE_OK = [ia.ip_network("203.0.113.0/24"), ia.ip_network("0.0.0.0/0")]

errors = []


def err(msg):
    errors.append(msg)
    print("  ERREUR :", msg)


def check_plan():
    print("== Plan VLSM")
    nets = {k: ia.ip_network(v[0]) for k, v in PLAN.items()}  # strict=True: alignment
    for name, net in nets.items():
        if not net.subnet_of(BLOCK):
            err(f"{name} {net} hors de {BLOCK}")
        hosts = list(net.hosts())
        gw = PLAN[name][1]
        if gw and ia.ip_address(gw) != hosts[-1]:
            err(f"{name}: passerelle {gw} != derniere utilisable {hosts[-1]}")
        print(f"  {name:24} {str(net):20} masque {net.netmask}  "
              f"{hosts[0]} - {hosts[-1]}  diff {net.broadcast_address}  "
              f"{len(hosts)} utilisables")
    items = list(nets.items())
    for i, (a, na) in enumerate(items):
        for b, nb in items[i + 1:]:
            if na.overlaps(nb):
                err(f"chevauchement {a} {na} / {b} {nb}")
    used = sum(n.num_addresses for n in nets.values())
    free = list(BLOCK.address_exclude(nets["VLAN10 Production"]))
    for n in list(nets.values())[1:]:
        free = [f for x in free for f in (x.address_exclude(n) if n.subnet_of(x) else [x])]
    print(f"  utilise {used}/256, libre : {', '.join(map(str, sorted(free)))}")
    return nets


def plan_net_of(addr, nets):
    for name, n in nets.items():
        if addr in n:
            return name, n
    return None, None


def check_configs(chapter, nets):
    files = sorted((chapter / "packet-tracer").glob("*.txt"))
    if not files:
        return
    print(f"== Configurations {chapter.name}/packet-tracer")
    seen = {}
    connected = {}  # device -> list of interface networks
    for f in files:
        dev = f.stem
        text = f.read_text()
        connected[dev] = []
        itf = None
        for line in text.splitlines():
            s = line.strip()
            if s.startswith("interface "):
                itf = s.split(None, 1)[1]
            m = re.match(r"ip address (\S+) (\S+)$", s)
            if m and itf:
                i = ia.ip_interface(f"{m[1]}/{m[2]}")
                connected[dev].append(i.network)
                where = f"{dev} {itf} {i}"
                if i.ip in seen:
                    err(f"adresse dupliquee {i.ip}: {seen[i.ip]} / {where}")
                seen[i.ip] = where
                if i.network.prefixlen < 32 and i.ip in (i.network.network_address, i.network.broadcast_address):
                    err(f"{where}: adresse reseau ou diffusion")
                if i.ip in BLOCK:
                    name, n = plan_net_of(i.ip, nets)
                    if n is None or n != i.network:
                        err(f"{where}: masque/reseau incoherent avec le plan ({n})")
                    gw = PLAN.get(name, (None, None))[1] if name else None
                    m10 = re.search(r"\.(\d+)$", itf)
                    if m10 and gw and str(i.ip) != gw:
                        err(f"{where}: sous-interface != passerelle {gw}")
                    if m10 and "encapsulation dot1Q " + m10[1] not in text:
                        err(f"{where}: encapsulation dot1Q {m10[1]} absente")
                    if m10 and not name.startswith("VLAN" + m10[1]):
                        err(f"{where}: VLAN {m10[1]} associe au reseau {name}")
                print(f"  ok {where}")
        # default gateway of switches
        for gw in re.findall(r"ip default-gateway (\S+)", text):
            g = ia.ip_address(gw)
            if not any(g in n for n in connected[dev]):
                err(f"{dev}: default-gateway {gw} hors des SVI")
            else:
                print(f"  ok {dev} default-gateway {gw}")
        # DHCP
        excl = [(ia.ip_address(a), ia.ip_address(b or a)) for a, b in
                re.findall(r"ip dhcp excluded-address (\S+)(?: (\S+))?", text)]
        for pool, net, mask, gw in re.findall(
                r"ip dhcp pool (\S+)\n network (\S+) (\S+)\n default-router (\S+)", text):
            n = ia.ip_network(f"{net}/{mask}")
            g = ia.ip_address(gw)
            if n not in nets.values():
                err(f"{dev} pool {pool}: {n} pas dans le plan")
            if g not in n or not any(n.supernet_of(c) or n == c for c in connected[dev]):
                err(f"{dev} pool {pool}: passerelle {g} incoherente")
            if not any(lo <= g <= hi for lo, hi in excl):
                err(f"{dev} pool {pool}: passerelle {g} non exclue")
            free = [h for h in n.hosts() if not any(lo <= h <= hi for lo, hi in excl)]
            print(f"  ok {dev} pool {pool} {n}: {free[0]} - {free[-1]} ({len(free)} baux)")
        for lo, hi in excl:
            if plan_net_of(lo, nets)[1] != plan_net_of(hi, nets)[1]:
                err(f"{dev}: exclusion {lo}-{hi} a cheval sur deux reseaux")
    # static routes, once every device is known
    for f in files:
        dev = f.stem
        for net, mask, nh in re.findall(r"ip route (\S+) (\S+) (\S+)", f.read_text()):
            dst = ia.ip_network(f"{net}/{mask}")  # strict: host bits must be zero
            h = ia.ip_address(nh)
            if not any(h in c for c in connected[dev]):
                err(f"{dev}: next hop {nh} hors reseau connecte")
            if h not in seen:
                err(f"{dev}: next hop {nh} n'est l'adresse d'aucun equipement")
            print(f"  ok {dev} route {dst} via {nh} ({seen.get(h, '?')})")


IP_RE = re.compile(r"(?<![\d.])(\d{1,3}(?:\.\d{1,3}){3})(?:\s*/\s*(\d{1,2}))?(?![\d.])")


def check_tex(chapter, nets):
    texs = sorted(chapter.rglob("*.tex"))
    if not texs:
        return
    print(f"== Litteraux IPv4 dans {chapter.name}/**/*.tex")
    count = 0
    for t in texs:
        for ln, line in enumerate(t.read_text().splitlines(), 1):
            if line.lstrip().startswith("%"):
                continue
            for m in IP_RE.finditer(line):
                ip, pfx = m[1], m[2]
                where = f"{t.relative_to(chapter)}:{ln} {m[0]}"
                try:
                    a = ia.ip_address(ip)
                except ValueError:
                    err(f"{where}: adresse invalide")
                    continue
                count += 1
                if pfx:
                    i = ia.ip_interface(f"{ip}/{pfx}")
                    if int(pfx) < 31 and a == i.network.broadcast_address:
                        err(f"{where}: diffusion ecrite avec un prefixe")
                if a in BLOCK:
                    name, n = plan_net_of(a, nets)
                    if n is None:
                        print(f"  info {where}: espace libre du plan")
                    elif pfx and int(pfx) != n.prefixlen and a != BLOCK.network_address:
                        err(f"{where}: prefixe /{pfx} != {n} du plan")
    print(f"  {count} litteraux controles")


def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    nets = check_plan()
    chapters = [pathlib.Path(p).resolve() for p in sys.argv[1:]] or sorted(d for d in root.iterdir()
                                                                 if (d / "cours").is_dir() or (d / "tp").is_dir())
    for c in chapters:
        check_configs(c, nets)
        check_tex(c, nets)
    print(f"== {len(errors)} erreur(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
