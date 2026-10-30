# TP — Prédire le mot suivant avec des bigrammes (n = 2)

## Objectif

Créer en Python un petit système d'aide à la saisie qui prédit **le prochain mot** à partir d'un corpus de **13 phrases françaises**. Ce TP suit exactement le cheminement demandé :

**Phrases → tokens → bigrammes → comptes et probabilités → prédictions**

Le programme utilise **uniquement le dernier mot saisi** comme contexte et retourne **au maximum trois mots**.

## Fichiers du projet

```text
TP_Bigrammes_GitHub/
├── README.md                     # Présentation du TP et explication des résultats
├── TP_Bigrammes_Enonce.pdf       # Énoncé fourni par l'enseignant
├── dataset_bigrammes.json        # Corpus de 13 phrases et 6 tests
├── TP_Bigrammes_Colab.ipynb      # Notebook pédagogique à ouvrir dans Google Colab
├── tp_bigrammes.py              # Solution Python, commentée pour débutants
└── resultats/
    ├── resultats.txt             # Affichage des 6 tests
    ├── resultats.csv             # Top-3 et probabilités, format tableur
    └── comptes_bigrammes.csv     # Tous les bigrammes observés et leurs comptes
```

> Les deux fichiers `dataset_bigrammes.json` et `dataset_bigrammes(1).json` fournis initialement étaient identiques : une seule copie suffit.

## Exécution dans Google Colab

1. Ouvrir [Google Colab](https://colab.research.google.com/).
2. Importer le notebook `TP_Bigrammes_Colab.ipynb` (**Fichier → Importer un notebook**).
3. Dans la barre latérale **Fichiers**, déposer `dataset_bigrammes.json`.
4. Exécuter les cellules **dans l'ordre**, de haut en bas.

Le notebook utilise seulement les bibliothèques standard de Python : **aucune installation n'est nécessaire**.

## Exécution sur un ordinateur

Placer `tp_bigrammes.py` et `dataset_bigrammes.json` dans le même dossier puis exécuter :

```bash
python tp_bigrammes.py
```

## Comment fonctionne le modèle ?

**1. Tokenisation.** `"Le guide prépare"` devient `['le', 'guide', 'prépare']`. Les majuscules et la ponctuation sont ignorées.

**2. Bigrammes.** Un bigramme contient deux mots consécutifs : `(le, guide)`, `(guide, prépare)`, etc. Un marqueur `DEBUT` est ajouté avant chaque phrase pour apprendre les premiers mots.

**3. Comptage.** Le programme compte les mots observés après chaque contexte : après `prépare`, il a vu `une` **4 fois**, `un` **2 fois**, et `le` **1 fois**.

**4. Probabilité.** On calcule :

```text
P(mot suivant | contexte) = nombre du bigramme / total après ce contexte
```

Exemple : `P(une | prépare) = 4 / 7 = 57,14 %`.

**5. Prédiction.** On garde le dernier token de la saisie. Les propositions sont triées **par probabilité décroissante**, puis **par ordre alphabétique si elles sont ex æquo**. On affiche au maximum les trois premières.

**Cas particuliers :** une saisie vide utilise `DEBUT`. Un contexte jamais rencontré donne une liste vide et affiche le message demandé dans l'énoncé.

## Résultats des 6 tests

| Saisie | Contexte | Top des mots suivants | Meilleure prédiction |
|---|---|---|---|
| `le guide prépare` | `prépare` | une (57,14 %) ; un (28,57 %) ; le (14,29 %) | **une** |
| `la classe prépare` | `prépare` | une (57,14 %) ; un (28,57 %) ; le (14,29 %) | **une** |
| `le musée propose` | `propose` | un (50 %) ; une (50 %) | **un** |
| `le musée` | `musée` | propose (50 %) ; pour (25 %) ; puis (25 %) | **propose** |
| `astronaute` | `astronaute` | Aucune prédiction : contexte non observé. | — |
| `""` | `DEBUT` | le (61,54 %) ; la (30,77 %) ; les (7,69 %) | **le** |

**Pourquoi `le guide prépare` et `la classe prépare` donnent-ils le même résultat ?** Parce que le dernier mot est `prépare` dans les deux cas. Un bigramme ne regarde pas les mots précédents.

**Pourquoi seulement deux résultats après `propose` ?** Parce que le corpus ne contient que deux mots suivants différents pour ce contexte : `un` et `une`. À probabilité égale, `un` passe avant `une` par ordre alphabétique.

## Conclusion

Ce TP montre comment construire une aide à la saisie simple avec des bigrammes. Le modèle fonctionne pour les contextes vus dans le corpus, mais il ne comprend pas le sens des phrases et ne peut pas prédire après un mot inconnu. Ces tests illustrent le fonctionnement du modèle ; ils ne mesurent pas ses performances sur de nouveaux textes.
