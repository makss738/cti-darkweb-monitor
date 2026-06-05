# Architecture du projet CTI Dark Web Monitor

## Objectif
Détection automatique de fuites de données sur le Dark Web.

## Pipeline
1. Crawler Tor
2. Scraping HTML
3. Extraction texte + liens
4. Analyse OSINT (regex + NLP)
5. Stockage des données
6. Génération Obsidian
7. Analyse RAG
8. Dashboard Streamlit

## Contraintes
- anonymat via Tor
- gestion des sites instables .onion
- limitation des faux positifs
