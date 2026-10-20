# Compilation des supports CIEL2 réseau (LuaLaTeX).
#   make            -> tous les chapitres, versions élève + prof/corrigé
#   make 03         -> un chapitre (02, 03, 04 ou 05)
#   make verif      -> contrôle arithmétique des adresses (Python ipaddress)
#   make png        -> rendu PNG de tous les PDF (build/png, contrôle visuel)
#   make clean      -> fichiers auxiliaires ; make distclean -> + PDF
# Chaque NOM.tex de <chapitre>/cours/ ou <chapitre>/tp/ donne
#   <chapitre>/pdf/NOM.pdf          version élève
#   <chapitre>/pdf/NOM-prof.pdf     version professeur (cours)
#   <chapitre>/pdf/NOM-corrige.pdf  corrigé (TP, TD, évaluations)

LATEX := lualatex -interaction=nonstopmode -halt-on-error -file-line-error
ROOT  := $(CURDIR)
BUILD := $(ROOT)/build
CHAPS := 02 03 04 05
DEPS  := $(wildcard $(ROOT)/commun/*.sty $(ROOT)/commun/icones/*.tex)
export TEXINPUTS := $(ROOT)/commun//:

.PHONY: all $(CHAPS) verif png clean distclean
all: $(CHAPS)

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

# rules <chapitre> <source>
define rules
$(1): $(dir $(2))../pdf/$(basename $(notdir $(2))).pdf $(dir $(2))../pdf/$(basename $(notdir $(2)))-$(3).pdf
$(dir $(2))../pdf/$(basename $(notdir $(2))).pdf: $(2) $(DEPS)
	$$(call compile,$(2),$(basename $(notdir $(2))),0)
$(dir $(2))../pdf/$(basename $(notdir $(2)))-$(3).pdf: $(2) $(DEPS)
	$$(call compile,$(2),$(basename $(notdir $(2)))-$(3),1)
endef

$(foreach c,$(CHAPS),\
  $(foreach s,$(wildcard $(ROOT)/$(c)-*/cours/*.tex),$(eval $(call rules,$(c),$(s),prof)))\
  $(foreach s,$(wildcard $(ROOT)/$(c)-*/tp/*.tex),$(eval $(call rules,$(c),$(s),corrige))))

verif:
	python3 $(ROOT)/commun/verif_adressage.py

png:
	@mkdir -p $(BUILD)/png
	@for f in $(ROOT)/0*/pdf/*.pdf; do \
	  pdftoppm -r 60 -png $$f $(BUILD)/png/$$(basename $$f .pdf); done
	@echo "  PNG dans build/png"

clean:
	rm -rf $(BUILD)

distclean: clean
	rm -f $(ROOT)/0*/pdf/*.pdf
