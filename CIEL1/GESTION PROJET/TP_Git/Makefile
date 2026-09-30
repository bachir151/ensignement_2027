# Génère la version élève et la version corrigée du TP (2 passes pour \pageref{LastPage})
all: TP_Git_debutant.pdf TP_Git_debutant_corrige.pdf

TP_Git_debutant.pdf: tp_git.tex
	pdflatex -interaction=nonstopmode -jobname=TP_Git_debutant tp_git.tex
	pdflatex -interaction=nonstopmode -jobname=TP_Git_debutant tp_git.tex

TP_Git_debutant_corrige.pdf: tp_git.tex
	pdflatex -interaction=nonstopmode -jobname=TP_Git_debutant_corrige "\def\CORRIGE{}\input{tp_git.tex}"
	pdflatex -interaction=nonstopmode -jobname=TP_Git_debutant_corrige "\def\CORRIGE{}\input{tp_git.tex}"

clean:
	rm -f *.aux *.log *.out *.toc

.PHONY: all clean
