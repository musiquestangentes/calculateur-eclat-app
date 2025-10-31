import streamlit as st
from datetime import datetime, date

# Config de la page
st.set_page_config(page_title="Simulateur ECLAT", page_icon="🎵", layout="wide")

# Sidebar
st.sidebar.title("Musiques Tangentes")
logo_url = "https://raw.githubusercontent.com/musiquestangentes/calculateur-eclat-app/refs/heads/main/logo_2025_celine_queguiner.png"
st.sidebar.image(logo_url, width=300)

# Navigation principale
modules = [
    "Accueil",
    "Coefficient et salaire de base",
    "Heures lissées",
    "Primes",
    "Simulateur complet",
    "Saisie des heures par semaine"
]
module = st.sidebar.radio("Navigation", modules, index=0)


# ACCUEIL

if module == "Accueil":
    st.title("Bienvenue sur le simulateur de paie - Musiques Tangentes")
    st.write("""
    Cet outil vous permet de comprendre les éléments de votre fiche de paie et de calculer vos heures et primes.
    
    Utilisez le menu à gauche pour naviguer entre les différents modules :
    - Coefficient et salaire de base  
    - Heures lissées  
    - Primes  
    - Simulateur complet  
    - Saisie des heures par semaine
    """)
    st.image(logo_url, width=400)


# PAGE 1: COEFFICIENT ET SALAIRE DE BASE

elif module == "Coefficient et salaire de base":
    st.title("Coefficient et salaire de base")
    url_grille = "https://www.legifrance.gouv.fr/conv_coll/article/KALIARTI000048471347#KALIARTI000048471347"
    
    st.info("""
    **Coefficient :** Renvoie à la grille de classification de la convention collective ECLAT.  
    Les professeur·e·s sont rattaché·e·s par défaut au groupe A de niveau 1, mais Musiques Tangentes rattache ses profs au **groupe D (coefficient 300)**.
    """)
    st.markdown("Nb : Le coefficient réel utilisé pour les paies des profs est de 362,03 (voir prime différentielle).")
    st.markdown(f"[>> Lien Légifrance - Grille de classification]({url_grille})")
    st.divider()
    st.info("Le **salaire de base conventionnel** est obtenu en multipliant le coefficient par la valeur du point d'indice.")


# PAGE 2: HEURES LISSEES

elif module == "Heures lissées":
    st.title("Calcul des heures lissées")
    heures_annuelles = st.number_input(
        "Heures annuelles réellement effectuées (de septembre à août) :", min_value=0.0, step=0.5
    )

    if heures_annuelles > 0:
        heures_avec_cp = heures_annuelles * 1.10
        heures_mensuelles = heures_avec_cp / 12
        heures_hebdo = heures_mensuelles / (52/12)
        heures_mensuelles_etp = (heures_hebdo * ((35 * 52)/12)) / 24

        st.markdown("### Résultats")
        st.write(f"- Heures annuelles + 10% CP : **{heures_avec_cp:.2f} h**")
        st.write(f"- Heures mensuelles lissées : **{heures_mensuelles:.2f} h/mois**")
        st.write(f"- Heures hebdomadaires lissées : **{heures_hebdo:.2f} h/semaine**")

        st.info("Le lissage compense le creux d'heures pendant les vacances scolaires.")
        st.markdown("*Formules :*")
        st.latex("\\text{Heures mensuelles lissées} = \\frac{(\\text{Heures annuelles} + 10\\% \\text{ CP})}{12}")
        st.latex("\\text{Heures hebdomadaires lissées} = \\frac{\\text{Heures mensuelles lissées}}{(52 / 12)}")

        st.divider()
        st.info("L'équivalent temps plein - ETP - permet de comparer les heures des profs (temps plein fixée à 24h/semaine par la convention collective ECLAT) à un temps plein classique (35h/semaine).")
        st.write(f"- Heures mensuelles ETP : **{heures_mensuelles_etp:.2f} h**")
        st.markdown("*Formule :*")
        st.latex("\\text{Heures mensuelles ETP} = \\frac{\\text{{Heures hebdo lissées} \\times \\text{151,67}}}{(24)}")


# PAGE 3: PRIMES

elif module == "Primes":
    st.title("Calcul des primes")
    date_entree = st.date_input(
        "Date d'entrée dans l'école :", min_value=date(1980,1,1), max_value=date.today()
    )
    heures_lissees = st.number_input("Heures hebdomadaires lissées :", min_value=0.0, step=0.5)
    valeur_point = 7.15
    st.write(f"Valeur du point d'indice au 1er janvier 2025 : {valeur_point} €.")

    # Ancienneté
    today = datetime.today().date()
    anciennete = today.year - date_entree.year - ((today.month, today.day) < (date_entree.month, date_entree.day))

    if heures_lissees > 0:
        prime_anciennete = heures_lissees * valeur_point * (anciennete * 2) / 24
        prime_diff = max(0, (62.03 - (anciennete * 2))) * valeur_point * heures_lissees / 24

        st.markdown("### Résultats")
        st.write(f"- Ancienneté calculée : **{anciennete} ans**")
        st.write(f"- Prime d’ancienneté : **{prime_anciennete:.2f} €**")
        st.write(f"- Prime différentielle : **{prime_diff:.2f} €**")

        st.markdown("*Formules :*")
        st.latex("\\text{Prime d'ancienneté} = \\frac{\\text{heures hebdo lissées} \\times \\text{valeur du point d'indice} \\times (\\text{ancienneté} \\times 2)}{24}")
        st.latex("\\text{Prime différentielle} = \\frac{\\max(0, 62.03 - (\\text{ancienneté} \\times 2)) \\times \\text{valeur du point d'indice} \\times \\text{heures hebdo lissées}}{24}")

# PAGE 4: SIMULATEUR COMPLET

elif module == "Simulateur complet":
    st.title("Simulateur complet")
    heures_annuelles = st.number_input("Heures annuelles réellement effectuées :", min_value=0.0, step=0.5)
    date_entree = st.date_input("Date d'entrée dans l'école :", min_value=date(1980,1,1), max_value=date.today())

    if heures_annuelles > 0:
        # Heures lissées
        heures_avec_cp = heures_annuelles * 1.10
        heures_mensuelles = heures_avec_cp / 12
        heures_hebdo = heures_mensuelles / (52/12)
        heures_mensuelles_etp = (heures_hebdo * ((35 * 52)/12)) / 24

        # Ancienneté & primes
        valeur_point = 7.15
        today = datetime.today().date()
        anciennete = today.year - date_entree.year - ((today.month, today.day) < (date_entree.month, date_entree.day))
        prime_anciennete = heures_hebdo * valeur_point * (anciennete * 2) / 24
        prime_diff = max(0, (62.03 - (anciennete * 2))) * valeur_point * heures_hebdo / 24

        st.markdown("### Résultats")
        st.write(f"- Heures mensuelles lissées : **{heures_mensuelles:.2f} h/mois**")
        st.write(f"- Heures hebdomadaires lissées : **{heures_hebdo:.2f} h/semaine**")
        st.write(f"- Heures mensuelles ETP : **{heures_mensuelles_etp:.2f} h**")
        st.write(f"- Ancienneté : **{anciennete} ans**")
        st.write(f"- Prime d’ancienneté : **{prime_anciennete:.2f} €**")
        st.write(f"- Prime différentielle : **{prime_diff:.2f} €**")
