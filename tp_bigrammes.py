"""TP : prédire le mot suivant avec des bigrammes (n = 2).

Utilisation : python tp_bigrammes.py
Aucune bibliothèque externe n'est nécessaire.
"""

# ===== 1. IMPORTER LES OUTILS =====

import json  # Pour lire les données enregistrées dans le fichier JSON.
import re  # Pour séparer une phrase en mots (tokenisation).
from pathlib import Path  # Pour retrouver le fichier JSON à côté de ce script.

# Retrouve le dossier qui contient ce programme.
DOSSIER = Path(__file__).resolve().parent

# Donne le chemin complet du fichier contenant les phrases.
FICHIER_JSON = DOSSIER / "dataset_bigrammes.json"

# Ouvre le fichier JSON en indiquant que le texte peut contenir des accents.
with open(FICHIER_JSON, "r", encoding="utf-8") as fichier:
    donnees = json.load(fichier)  # Convertit le JSON en dictionnaire Python.


# ===== 2. DECOUPER UNE PHRASE EN MOTS =====

def tokeniser(texte):
    """Renvoie les mots en minuscules, sans ponctuation."""
    texte = texte.lower()  # "Le Musée" devient "le musée".
    tokens = re.findall(r"\b\w+\b", texte)  # Extrait les mots dans une liste.
    return tokens  # Exemple : ["le", "guide", "prépare"].


# ===== 3. COMPTER LES BIGRAMMES =====

comptes = {}  # Dictionnaire : contexte -> {mot_suivant: nombre}.

# Prend chaque phrase d'apprentissage présente dans le JSON.
for phrase in donnees["phrases_apprentissage"]:
    tokens = tokeniser(phrase["texte"])  # Transforme la phrase en mots.
    tokens = ["DEBUT"] + tokens  # Ajoute un début pour les saisies vides.

    # i va de 0 jusqu'à l'avant-dernier mot de la phrase.
    for i in range(len(tokens) - 1):
        contexte = tokens[i]  # Mot de gauche dans le bigramme.
        mot_suivant = tokens[i + 1]  # Mot de droite dans le bigramme.

        # Crée un dictionnaire vide pour un nouveau contexte.
        if contexte not in comptes:
            comptes[contexte] = {}

        # Commence le comptage d'un nouveau mot suivant à zéro.
        if mot_suivant not in comptes[contexte]:
            comptes[contexte][mot_suivant] = 0

        # Ajoute une occurrence du couple (contexte, mot_suivant).
        comptes[contexte][mot_suivant] += 1


# ===== 4. CALCULER LES PROBABILITES ET PREDIRE =====

def predire(saisie):
    """Renvoie le contexte et les trois meilleures prédictions."""
    tokens = tokeniser(saisie)  # Découpe la saisie de l'utilisateur.

    # S'il n'y a aucun mot, on prédit le début d'une phrase.
    if len(tokens) == 0:
        contexte = "DEBUT"
    else:
        contexte = tokens[-1]  # Sinon, on garde SEULEMENT le dernier mot.

    # Un mot jamais observé ne peut pas donner de prédiction.
    if contexte not in comptes:
        return contexte, []  # Une liste vide signifie « aucune prédiction ».

    # Compte combien de mots apparaissent après ce contexte au total.
    total = sum(comptes[contexte].values())
    resultats = []  # Liste de couples (mot, probabilité).

    # Parcourt tous les mots trouvés après le contexte.
    for mot, nombre in comptes[contexte].items():
        probabilite = nombre / total  # Formule : fréquence du mot / total.
        resultats.append((mot, probabilite))  # Enregistre le résultat.

    # Trie d'abord par probabilité décroissante (-x[1]).
    # En cas d'égalité, trie par ordre alphabétique (x[0]).
    resultats.sort(key=lambda x: (-x[1], x[0]))

    return contexte, resultats[:3]  # Garde au maximum les trois premiers.


# ===== 5. TESTER AVEC LES SIX SAISIES DU FICHIER =====

# Ce bloc ne s'exécute que lorsque l'on lance ce fichier Python directement.
if __name__ == "__main__":
    # Lit les six exemples de saisie prévus dans l'énoncé.
    for saisie in donnees["saisies_a_tester"]:
        contexte, top3 = predire(saisie)  # Appelle notre fonction de prédiction.

        print("\nSaisie :", repr(saisie))  # repr() montre aussi la chaîne vide ''.
        print("Contexte retenu :", contexte)  # Montre le mot utilisé comme contexte.

        if not top3:  # Vrai lorsque la liste de prédictions est vide.
            print("Aucune prédiction : contexte non observé.")
        else:
            # Affiche chaque mot et sa probabilité.
            for mot, probabilite in top3:
                print(f"  {mot} : {probabilite:.4f} ({probabilite:.2%})")

            # Le premier élément est la meilleure prédiction.
            print("Meilleure prédiction :", top3[0][0])
