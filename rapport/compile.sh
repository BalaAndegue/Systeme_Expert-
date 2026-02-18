#!/bin/bash
# ============================================================
#  Script de compilation du rapport LaTeX
#  Usage: cd rapport/ && bash compile.sh
# ============================================================

echo "=== Compilation du rapport LaTeX ==="
echo "Vérification des dépendances..."

# Vérifier pdflatex
if ! command -v pdflatex &> /dev/null; then
    echo "ERREUR: pdflatex non trouvé. Installez TexLive:"
    echo "  sudo apt-get install texlive-full"
    exit 1
fi

# Vérifier bibtex
if ! command -v bibtex &> /dev/null; then
    echo "ERREUR: bibtex non trouvé."
    exit 1
fi

echo "Compilation en cours (4 passes)..."

# Passe 1
pdflatex -interaction=nonstopmode -shell-escape rapport_main.tex > /dev/null 2>&1
echo "  [1/4] Première passe..."

# Bibliographie
bibtex rapport_main > /dev/null 2>&1
echo "  [2/4] Bibliographie..."

# Passe 2 (pour références)
pdflatex -interaction=nonstopmode -shell-escape rapport_main.tex > /dev/null 2>&1
echo "  [3/4] Deuxième passe..."

# Passe 3 (pour table des matières)
pdflatex -interaction=nonstopmode -shell-escape rapport_main.tex > /dev/null 2>&1
echo "  [4/4] Troisième passe..."

if [ -f "rapport_main.pdf" ]; then
    echo ""
    echo "=== SUCCÈS ==="
    echo "Rapport généré : rapport_main.pdf"
    echo "Taille : $(du -h rapport_main.pdf | cut -f1)"
    # Ouvrir le PDF si possible
    if command -v xdg-open &> /dev/null; then
        xdg-open rapport_main.pdf &
    fi
else
    echo "ERREUR: La compilation a échoué."
    echo "Consultez rapport_main.log pour les détails."
    exit 1
fi

# Nettoyage des fichiers temporaires
echo "Nettoyage des fichiers temporaires..."
rm -f *.aux *.log *.toc *.lof *.lot *.bbl *.blg *.out *.fls *.fdb_latexmk
echo "Terminé."
