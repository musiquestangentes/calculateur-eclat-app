import streamlit as st
from datetime import datetime, date

st.set_page_config(page_title="Musiques Tangentes - Simulateur simplifié", page_icon="🎵", layout="wide")
st.sidebar.title("Musiques Tangentes")
logo_url = "https://raw.githubusercontent.com/musiquestangentes/calculateur-eclat-app/refs/heads/main/logo_2025_celine_queguiner.png"
st.image(logo_url, width=500)
page = st.sidebar.radio("Choisir un module :", ["Coefficient et salaire de base", "Heures lissées", "Primes", "Simulateur complet"])

valeur_point = 7.01

# PAGE 1 : COEFFICIENT ET SALAIRE DE BASE
if page == "Coefficient et salaire de base":
    st.title("Coefficient et salaire de base")

    url_grille = "https://www.legifrance.gouv.fr/conv_coll/article/KALIARTI000048471347#KALIARTI000048471347"
    st.info("**Coefficient :** Renvoie à la grille de classification de la convention collective ECLAT 1518, composée de groupes nommés par des lettres correspondant chacune à un coefficient et à une catégorie socioprofessionnelle.\n\n" \
    "Les professeur·e·s sont rattaché·e·s par défaut au groupe A de niveau 1 (Ouvriers et employés), qui correspond au coefficient 247. Musiques Tangentes rattache ses profs au **groupe D** (Techniciens, agents de maîtrise), **coefficient 300**, dont le salaire de base est plus élevé.\n")
    st.markdown("Nb : Le coefficient conventionnel de base, indiqué sur les bulletins de paie, est de 300 mais le coefficient réel sur lequel est indexé les paies des profs de Musiques Tangentes est de 362,03 (voir « prime différentielle » dans l'onglet \"Primes\"). Il est donc plus élevé que le coefficient maximal de la catégorie Techniciens et agents de maîtrise et s'approche de la catégorie Cadres.")
    st.markdown("[>> Lien Légifrance - Grille de classification](%s)" % url_grille)
    st.divider()
    st.info("Le **salaire de base conventionnel** est obtenu en multipliant le coefficient par la valeur du point d'indice (voir page \"Primes\").")

# PAGE 2 : HEURES LISSEES ET ETP
if page == "Heures lissées":
    st.title("Calcul des heures lissées")

    heures_annuelles = st.number_input("Heures annuelles réellement effectuées (de septembre à août):", min_value=0.0, step=0.5)

    if heures_annuelles > 0:
        heures_avec_cp = heures_annuelles * 1.10
        heures_mensuelles = heures_avec_cp / 12
        heures_hebdo = heures_mensuelles / (52/12)
        heures_mensuelles_etp = (heures_hebdo * ((35 * 52)/12)) / 24

        st.markdown("### Résultats")
        st.write(f"- Heures annuelles + 10% de congés payés (CP) : **{heures_avec_cp:.2f} h**")
        st.write(f"- Heures mensuelles lissées : **{heures_mensuelles:.2f} h/mois**")
        st.write(f"- Heures hebdomadaires lissées : **{heures_hebdo:.2f} h/semaine**")

        st.info("Le lissage permet de compenser le creux d'heures pendant les vacances scolaires.")
        st.markdown("*Formules :*")
        st.latex("\\text{Heures mensuelles lissées} = \\frac{(\\text{Heures annuelles} + 10\\% \\text{ CP})}{12}")
        st.latex("\\text{Heures hebdomadaires lissées} = \\frac{\\text{Heures mensuelles lissées}}{(52 / 12)}")

        st.divider()
        st.info("L'équivalent temps plein - ETP - permet de comparer les heures des profs (temps plein à 24h/semaine d'après la convention collective ECLAT) à un temps plein classique (35h/semaine).")
        st.write(f"- Heures mensuelles ETP (affichées sur la fiche de paie) : **{heures_mensuelles_etp:.2f} h**")
        st.markdown("*Formule :*")
        st.latex("\\text{Heures mensuelles ETP} = \\frac{(\\text{Heures hebdo lissées} \\times \\text{ 151,67})}{24}")


# PAGE 3 : PRIMES
elif page == "Primes":
    st.title("Calcul des primes")

    date_entree = st.date_input(
    "Date d'entrée dans l'école :",
    min_value=date(1980, 1, 1),
    max_value=date.today()
    )
    heures_lissees = st.number_input("Heures hebdomadaires lissées :", min_value=0.0, step=0.5)
    valeur_point = 7.15
    url_valpoint = "https://www.legifrance.gouv.fr/conv_coll/article/KALIARTI000050362519#KALIARTI000050362519"
    st.write("Valeur du point d'indice au 1er janvier 2025 : 7,15 €.")
    st.markdown("[>> Lien Légifrance - Valeur du point d'indice](%s)" % url_valpoint)

    today = datetime.today().date()
    anciennete = today.year - date_entree.year - ((today.month, today.day) < (date_entree.month, date_entree.day))

    if heures_lissees > 0:
        prime_anciennete = heures_lissees * valeur_point * (anciennete * 2) / 24
        prime_diff = max(0, (62.03 - (anciennete * 2))) * valeur_point * heures_lissees / 24

        st.markdown("### Résultats")
        st.write(f"- Ancienneté calculée : **{anciennete} ans**")
        st.write(f"- Prime d’ancienneté : **{prime_anciennete:.2f}**")
        st.write(f"- Prime différentielle : **{prime_diff:.2f}**")

        st.info("La prime d’ancienneté démarre à partir de la 2ème année (N+1).")
        st.info("La prime différentielle a été mise en place afin que tou·te·s les salarié·e·s soient sur un pied d'égalité en termes de rémunération, quelle que soit leur ancienneté.")
        st.markdown("*Formules :*")
        st.latex("\\text{Prime d'ancienneté} = \\frac{\\text{heures hebdo lissées} \\times \\text{valeur du point d'indice} \\times (\\text{nombre d'années d'ancienneté} \\times 2)}{24}")
        st.latex("\\text{Prime différentielle} = \\frac{\\text{valeur max entre 0 et (62,03 - (\\text{nombre d'années d'ancienneté} \\times 2))} \\times \\text{valeur du point d'indice} \\times (\\text{heures hebdo lissées})}{24}")

    else:
        st.warning("Veuillez entrer vos heures lissées pour afficher le calcul.")


# PAGE 4 : SIMULATEUR COMPLET
elif page == "Simulateur complet":
    st.title("Simulateur complet")