# Jeux de données de démonstration — 100 % SYNTHÉTIQUES

Ces fichiers sont produits par des tirages pseudo-aléatoires avec une graine fixe (`2031`) ; ils ne représentent aucun ouvrage réel, aucune campagne d’essais ni aucune base de prix.

- `scenarios_poutres_FICTIFS.csv` : 4 500 poutres rectangulaires simplement appuyées sous charge uniforme, sans charge ponctuelle. Formules : M=qL²/8 ; f=5qL⁴/(384EI), avec E en GPa converti en kN/m² et I=bh³/12.
- `scenarios_semelles_FICTIFS.csv` : 4 500 semelles carrées fictives sous charge verticale centrée. A=N/(qadm−24h), poids volumique fictif 24 kN/m³. Aucune vérification géotechnique détaillée.

**Utilisation :** exercices d'analyse de données, régression et tests de cohérence. **Interdit de les présenter comme des observations réelles ou une validation réglementaire.**
