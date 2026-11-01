# DIMENSIA — Structural Engineering Studio (V1)

Application Streamlit pédagogique de **calcul mécanique des poutres**, de **pré-dimensionnement des semelles centrées**, de **comparaison de sections** et de **simulation probabiliste**.

## Installation

Python 3.11 ou 3.12 recommandé.

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Dans le navigateur, l'application affiche normalement `http://localhost:8501`.

## Modules

- Vue générale : indicateurs et graphique de moments.
- Analyse des poutres : poutre simplement appuyée ou console, charge répartie uniforme et charge ponctuelle, réactions, efforts tranchants, moments, flèches, CSV et PDF.
- Semelles : charge verticale centrée et pression moyenne, prise en compte facultative du poids propre.
- Optimisation : comparaison de sections rectangulaires selon volume, flèche et seuil de moment **défini par l'utilisateur**.
- Probabilités : distribution lognormale d'une charge répartie, simulation de dépassement d'un seuil de moment, estimation de l'erreur Monte-Carlo.
- Comprendre : formules, hypothèses, limites.

## Exemples de contrôle

Poutre simplement appuyée, L=5 m, q=20 kN/m, sans charge ponctuelle : RA=RB=50 kN, Mmax=62,5 kN·m, |V|max=50 kN.

## IMPORTANT : limites et normes

**Cette première version n'implémente PAS le dimensionnement réglementaire des armatures BAEL 91 révisé 99 ni Eurocode 2.** Ces normes demandent des vérifications spécifiques qui ne sont pas représentées par les seuls efforts et flèches.

- Hypothèses poutres : Euler-Bernoulli, comportement élastique linéaire, inertie constante, petites déformations, appuis idéalisés, charges statiques.
- Le module semelle ne vérifie ni tassement, ni poinçonnement, ni flexion, ni excentricité, ni ferraillage.
- Le module optimisation compare uniquement des candidats selon des critères fournis, sans résistance de section en béton armé calculée.
- La probabilité de dépassement d'un seuil de moment n'est **pas** une probabilité de ruine structurale ni une vérification de fiabilité normative.
- Le logiciel ne constitue pas une note de calcul de construction certifiée.

## Tests

```bash
python -m unittest discover -s tests -v
```

Neuf tests automatisés passent pour les formules et sorties des moteurs de calcul. **L'interface Streamlit et le rendu navigateur n'ont pas été exécutés dans cet environnement** car Streamlit n'y est pas installé.

## Déploiement

Pour Streamlit Community Cloud : placer `app.py`, `requirements.txt`, le dossier `dimensia/` et `.streamlit/` à la racine d'un dépôt GitHub. Définir `app.py` comme fichier d'entrée. Ne pas mettre seulement `app.py` : les modules du dossier `dimensia` sont nécessaires.

## Jeux de données inclus (pour l'enseignement)

Le dossier `exemples/` contient **9 000 scénarios synthétiques** avec unités et formules documentées dans `PROVENANCE.md`. Ils peuvent servir à analyser les distributions, les corrélations et la sensibilité des modèles, mais **ne sont pas des données de terrain**.

La taille du ZIP est supérieure à 40 Ko grâce à ces données utiles, et non par ajout de fichiers de remplissage.

## Extensions de la version enrichie

Cette édition ajoute trois modules réels (sans modifier les hypothèses de calcul précédentes) :

1. **Explorateur de données** : import CSV/XLSX jusqu'à 12 Mo, affichage des observations brutes, documentation manuelle de la source/date/unités, audit des valeurs manquantes, statistiques descriptives, histogrammes et régression linéaire exploratoire. Les fichiers fournis dans `exemples/` sont **synthétiques**.
2. **Combinaisons de charges** : charge combinée obtenue par coefficients saisis manuellement ; aucune revendication de conformité à une combinaison BAEL ou EC2.
3. **Caractéristiques des sections** : aires, inerties et modules de résistance géométriques de rectangles pleins, cercles pleins et rectangles creux centrés.

Les 14 tests unitaires valident les modules de calcul et de traitement des données. Ils ne constituent pas une validation réglementaire. Les données d'exemple sont volumineuses pour permettre une exploration statistique substantielle, non pour simuler des relevés de chantier réels.
