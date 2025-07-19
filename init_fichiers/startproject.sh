#!/bin/bash
echo "Création d'un environnement virtuel..."
python3 -m venv env
source env/bin/activate

echo "Installation des dépendances..."
pip install -r requirements.txt

echo "Création du projet Django avec Wagtail..."
wagtail start formation_wushu .

echo "Configuration initiale terminée."
