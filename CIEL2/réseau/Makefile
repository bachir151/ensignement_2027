# Compilation des supports CIEL2 réseau (LuaLaTeX).
#   make            -> tous les chapitres, versions élève + prof/corrigé
#   make ospf       -> une thématique (subnetting-vlsm, ospf, wireshark-transport)
#   make verif      -> contrôle arithmétique des adresses (Python ipaddress)
#   make png        -> rendu PNG de tous les PDF (build/png, contrôle visuel)
#   make clean      -> fichiers auxiliaires ; make distclean -> + PDF
# Chaque NOM.tex de <thème>/cours/ ou <thème>/tp/ donne
#   <thème>/pdf/NOM.pdf          version élève
#   <thème>/pdf/NOM-prof.pdf     version professeur (cours)
#   <thème>/pdf/NOM-corrige.pdf  corrigé (TP, TD, évaluations)

LATEX := lualatex -interaction=nonstopmode -halt-on-error -file-line-error
ROOT  := $(CURDIR)
BUILD := $(ROOT)/build
THEMES := subnetting-vlsm ospf wireshark-transport
DEPS  := $(wildcard $(ROOT)/commun/*.sty $(ROOT)/commun/icones/*.tex)
export TEXINPUTS := $(ROOT)/commun//:

.PHONY: all $(THEMES) verif png clean distclean
all: $(THEMES)

# compile <source> <jobname> <0|1> : deux passes (LastPage, numéros de diapos)
define compile
	@mkdir -p $(BUILD) $(dir $@)
	@echo "  LUALATEX  $(notdir $@)"
	@cd $(dir $(1)) && for i in 1 2; do \
	  $(LATEX) -output-directory=$(BUILD) -jobname=$(2) \
	    "\def\cielcorrige{$(3)}\input{$(notdir $(1))}" > $(BUILD)/$(2).stdout 2>&1 \
	  || { grep -A3 -E "^!|:[0-9]+:" $(BUILD)/$(2).log | head -n 20; exit 1; }; done
	@grep -E "^(Overfull|Underfull)" $(BUILD)/$(2).log | sed 's/^/    /' || true
	@cp $(BUILD)/$(2).pdf $@
	@printf "    %s pages\n" "$$(pdfinfo $@ 2>/dev/null | awk '/^Pages/{print $$2}')"
endef

# rules <thème> <source> <suffixe>
define rules
$(1): $(dir $(2))../pdf/$(basename $(notdir $(2))).pdf $(dir $(2))../pdf/$(basename $(notdir $(2)))-$(3).pdf
$(dir $(2))../pdf/$(basename $(notdir $(2))).pdf: $(2) $(DEPS)
	$$(call compile,$(2),$(basename $(notdir $(2))),0)
$(dir $(2))../pdf/$(basename $(notdir $(2)))-$(3).pdf: $(2) $(DEPS)
	$$(call compile,$(2),$(basename $(notdir $(2)))-$(3),1)
endef

$(foreach t,$(THEMES),\
  $(foreach s,$(wildcard $(ROOT)/$(t)/cours/*.tex),$(eval $(call rules,$(t),$(s),prof)))\
  $(foreach s,$(wildcard $(ROOT)/$(t)/tp/*.tex),$(eval $(call rules,$(t),$(s),corrige))))

verif:
	python3 $(ROOT)/commun/verif_adressage.py

png:
	@mkdir -p $(BUILD)/png
	@for f in $(foreach t,$(THEMES),$(wildcard $(ROOT)/$(t)/pdf/*.pdf)); do \
	  pdftoppm -r 60 -png $$f $(BUILD)/png/$$(basename $$f .pdf); done
	@echo "  PNG dans build/png"

clean:
	rm -rf $(BUILD)

distclean: clean
	rm -f $(foreach t,$(THEMES),$(ROOT)/$(t)/pdf/*.pdf)
