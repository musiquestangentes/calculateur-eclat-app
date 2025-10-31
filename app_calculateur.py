import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Musiques Tangentes - Simulateur simplifié", page_icon="🎵")

st.sidebar.title("Musiques Tangentes")
page = st.sidebar.radio("Choisir un module :", ["Heures lissées", "Primes"])

valeur_point = 7.01

# PAGE 1 : HEURES LISSEES
if page == "Heures lissées":
    st.title("Calcul des heures lissées")

    heures_annuelles = st.number_input("Heures annuelles réellement effectuées :", min_value=0.0, step=0.5)

    if heures_annuelles > 0:
        heures_avec_cp = heures_annuelles * 1.10
        heures_mensuelles = heures_avec_cp / 12
        heures_hebdo = heures_mensuelles / (52/12)

        st.markdown("### Résultats")
        st.write(f"- Heures annuelles + 10% de congés payés (CP) : **{heures_avec_cp:.2f} h**")
        st.write(f"- Heures mensuelles lissées : **{heures_mensuelles:.2f} h/mois**")
        st.write(f"- Heures hebdomadaires lissées : **{heures_hebdo:.2f} h/semaine**")

        st.info("Le lissage permet de compenser le creux d'heures pendant les vacances scolaires.")
        st.markdown("*Formules :*")
        st.latex("\\text{Heures mensuelles lissées} = \\frac{\\text{Heures mensuelles lissées + 10% CP}}{(12)}")
        st.latex("\\text{Heures hebdomadaires lissées} = \\frac{\\text{Heures mensuelles lissées}}{(52 / 12)}")

# PAGE 2 : PRIMES
elif page == "Primes":
    st.title("Calcul des primes")

    date_entree = st.date_input("Date d’entrée dans l’école :")
    heures_lissees = st.number_input("Heures hebdomadaires lissées :", min_value=0.0, step=0.5)
    valeur_point = st.number_input("Valeur du point d’indice (€) :", value=7.01, step=0.01)

    today = datetime.today().date()
    anciennete = today.year - date_entree.year - ((today.month, today.day) < (date_entree.month, date_entree.day))

    if heures_lissees > 0:
        prime_anciennete = heures_lissees * valeur_point * (anciennete * 2) / 24
        prime_diff = max(0, (62.03 - (anciennete * 2))) * valeur_point * heures_lissees / 24

        st.markdown("### Résultats")
        st.write(f"- Ancienneté calculée : **{anciennete} an(s)**")
        st.write(f"- Prime d’ancienneté : **{prime_anciennete:.2f} €**")
        st.write(f"- Prime différentielle : **{prime_diff:.2f} €**")

        st.info("La prime d’ancienneté démarre à partir de la 2ème année (N+1).")
        st.markdown("*Formule :*")
        st.latex("\\text{Prime d'ancienneté} = \\frac{\\text{heures hebdo lissées} \\times {valeur du point d'indice} \\times {(nombre d'années d'ancienneté \\times 2}{(24)}")
        st.info("La prime différentielle a été mise en place afin que tou·te·s les salarié·e·s soient sur un pied d'égalité en termes de rémunération, quelle que soit leur ancienneté.")
        st.latex("\\text{Prime différentielle} = \\frac{\\text{valeur maximale entre 0 et (62,03 - (années d'ancienneté \\times 2))}{(52 / 12)}")
    else:
        st.warning("Veuillez entrer vos heures lissées pour afficher le calcul.")
