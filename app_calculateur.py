import streamlit as st
from datetime import datetime, date
import pandas as pd
import re
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from pathlib import Path
import streamlit.components.v1 as components
from streamlit_javascript import st_javascript
import st_yled

# Config de la page
st.set_page_config(page_title="Simulateur ECLAT", page_icon="🎵", layout="wide")

# Sidebar
st.sidebar.title("Musiques Tangentes")
logo_url = "https://raw.githubusercontent.com/musiquestangentes/calculateur-eclat-app/refs/heads/main/logo_2025_celine_queguiner.png"
st.sidebar.image(logo_url, width=300)

# Navigation principale
modules = [
    "Accueil",
    "Lire sa fiche de paie",
    "Coefficient, valeur du point d'indice et salaire de base",
    "Heures lissées",
    "Primes",
    "Vérificateur d'heures",
    "🧮 Simulateur complet",
    "🔗 Liens utiles"
]
module = st.sidebar.radio("Navigation", modules, index=0)

# ACCUEIL

if module == "Accueil":
    st.title("Simulateur de paie - Musiques Tangentes")
    st.image(logo_url, width=400)
    st.write("""
    **Cet outil vous permet de comprendre les éléments de votre fiche de paie et de calculer vos heures et primes.**
    
    Utilisez le menu à gauche pour naviguer entre les différents modules :
    - Définitions : Coefficient, valeur du point d'indice et salaire de base  
    - Lire sa fiche de paie : schéma interactif  
    - Heures lissées  
    - Primes  
    - Vérification de son nombre d'heures réelles annuelles  
    - Simulateur complet   
    - Liens utiles
    """)


# PAGE 1: LIRE SA FICHE DE PAIE
elif module == "Lire sa fiche de paie":
    st.title("Comprendre sa fiche de paie")

    st.write("Passez la souris sur les blocs pour plus d'infos et cliquez pour naviguer.")

    svg_code = """
    <svg width="900" height="700" style="font-family:sans-serif;">
    <style>
        .block { fill:#f9f9f9; stroke:#333; stroke-width:1; cursor:pointer; }
        .block:hover { fill:#cce6ff; }
        .text { font-size:14px; }
        .header { font-size:20px; font-weight:bold; }
        .subheader { font-size:16px; fill:#333; }
        .tooltip { font-size:16px; pointer-events:none; fill:#333; }
    </style>

    <!-- Titre -->
    <text x="450" y="30" text-anchor="middle" class="header">BULLETIN DE PAIE</text>
    <text x="450" y="55" text-anchor="middle" class="subheader">Période : 01/09/2025 - 30/09/2025</text>

    <!-- Blocs gauche -->
    <rect x="50" y="80" width="200" height="40" class="block" id="bloc_employeur"/>
    <text x="55" y="105" class="text">Employeur : Association XYZ</text>

    <rect x="50" y="130" width="200" height="40" class="block" id="bloc_convention"/>
    <text x="55" y="155" class="text">Convention collective : ECLAT</text>

    <rect x="50" y="180" width="200" height="40" class="block" id="bloc_qualification"/>
    <text x="55" y="205" class="text">Qualification - coefficient</text>

    <!-- Blocs droite -->
    <rect x="300" y="80" width="200" height="40" class="block" id="bloc_emploi"/>
    <text x="305" y="105" class="text">Emploi</text>

    <rect x="300" y="130" width="200" height="40" class="block" id="bloc_salarie"/>
    <text x="305" y="155" class="text">Salarié-e</text>

    <!-- Tableau salaire -->
    <text x="50" y="250" class="text" font-weight="bold">Désignation</text>
    <text x="300" y="250" class="text" font-weight="bold">Base</text>
    <text x="400" y="250" class="text" font-weight="bold">Taux</text>
    <text x="500" y="235" class="text" font-weight="bold">Montant</text>
    <text x="500" y="250" class="text">Part salarié</text>
    <text x="650" y="250" class="text">Part employeur</text>

    <rect x="50" y="260" width="500" height="30" class="block" id="ligne_base"/>
    <text x="55" y="280" class="text">Salaire de base</text>
    <text x="300" y="280" class="text">2500 €</text>
    <text x="400" y="280" class="text">100%</text>
    <text x="500" y="280" class="text">2500 €</text>
    <text x="650" y="280" class="text">2500 €</text>

    <rect x="50" y="300" width="500" height="30" class="block" id="ligne_prime"/>
    <text x="55" y="320" class="text">Prime ancienneté</text>
    <text x="300" y="320" class="text">250 €</text>
    <text x="400" y="320" class="text">2%</text>
    <text x="500" y="320" class="text">250 €</text>
    <text x="650" y="320" class="text">250 €</text>

    <rect x="50" y="340" width="500" height="30" class="block" id="ligne_cotis"/>
    <text x="55" y="360" class="text">Cotisations sociales</text>
    <text x="500" y="360" class="text">-500 €</text>
    <text x="650" y="360" class="text">-500 €</text>

    <rect x="50" y="380" width="500" height="30" class="block" id="ligne_net"/>
    <text x="55" y="400" class="text">Net à payer</text>
    <text x="500" y="400" class="text">2350 €</text>

    <text id="tooltip" x="50" y="450" class="tooltip">Passez la souris sur un élément pour voir le détail</text>

    <script>
        const tooltip = document.getElementById('tooltip');
        function showTooltip(msg){ tooltip.textContent = msg; }

        const mapping = {
        "bloc_employeur":"Coefficient, valeur du point d'indice et salaire de base",
        "bloc_convention":"Coefficient, valeur du point d'indice et salaire de base",
        "bloc_qualification":"Coefficient, valeur du point d'indice et salaire de base",
        "bloc_emploi":"Primes",
        "bloc_salarie":"🧮 Simulateur complet",
        "ligne_base":"Coefficient, valeur du point d'indice et salaire de base",
        "ligne_prime":"Primes",
        "ligne_cotis":"🔗 Liens utiles",
        "ligne_net":"🧮 Simulateur complet"
        };

        Object.keys(mapping).forEach(id=>{
        const elem = document.getElementById(id);
        if(elem){
            elem.addEventListener('mouseover', ()=>showTooltip(mapping[id]));
            elem.addEventListener('mouseout', ()=>showTooltip('Passez la souris sur un élément pour voir le détail'));
            elem.addEventListener('click', ()=>window.parent.postMessage({func:'selectModule', module: mapping[id]}, '*'));
        }
        });
    </script>
    </svg>
    """

    components.html(svg_code, height=500, scrolling=True)

# PAGE 2: COEFFICIENT ET SALAIRE DE BASE

elif module == "Coefficient, valeur du point d'indice et salaire de base":
    st.title("Coefficient et salaire de base")
    url_grille = "https://www.legifrance.gouv.fr/conv_coll/article/KALIARTI000048471347#KALIARTI000048471347"
    url_valpoint = "http://legifrance.gouv.fr/conv_coll/article/KALIARTI000050362519#KALIARTI000050362519"
    url_salaire = "https://www.legifrance.gouv.fr/conv_coll/id/KALIARTI000046098173/?idConteneur=KALICONT000005635177"
    
    st.info("""
    **Coefficient :** Renvoie à la grille de classification de la convention collective ECLAT.  
    Les professeur·e·s sont rattaché·e·s par défaut au groupe B de niveau 2, 
    qui correspond au coefficient 265. Musiques Tangentes rattache ses profs au **groupe D, 
    coefficient 305**, dont le salaire de base est plus élevé.
    """)
    st.success("Nb : Le coefficient conventionnel de base, indiqué sur les bulletins de paie, est de 305 mais le coefficient réel sur " \
    "lequel est indexé les paies des profs de Musiques Tangentes est de 367,03 (voir \"prime différentielle\"). Il est donc " \
    "plus élevé que le coefficient maximal de la catégorie Techniciens et agents de maîtrise et s'approche de la catégorie Cadres.")
    st.caption(f"[Lien Légifrance - Grille de classification]({url_grille})")
    st.divider()
    st.info("""
    **Valeur du point d'indice** : Valeur fixée par la convention collective ECLAT.  
    Au 1er janvier 2025, la valeur du point d'indice est de 7,15€.
    """)
    st.caption(f"[Lien Légifrance - Valeur du point d'indice]({url_valpoint})")
    st.divider()
    st.info("""
    Le **salaire de base conventionnel** correspond à la rémunération d’un·e professeur·e à temps plein ECLAT.  
    Il est calculé en multipliant les heures hebdomadaires lissées par la valeur du point d’indice et le coefficient, puis en divisant 
    le tout par 24 afin de ramener le résultat à la quotité ETP, c’est-à-dire la fraction du temps plein effectuée.
    """)
    with st.expander("Formule"):
        st.latex("\\text{Salaire de base} = \\frac{\\text{Heures hebdo lissées} \\times \\text{valeur du point d'indice} \\times \\text{coefficient}}{24}")
    st.caption(f"[Lien Légifrance - Salaire conventionnel]({url_salaire})")

# PAGE 3: HEURES LISSEES

elif module == "Heures lissées":
    st.title("Calcul des heures lissées")

    url_modulation = "https://www.legifrance.gouv.fr/conv_coll/id/KALIARTI000027717752?idConteneur=KALICONT000005635177&origin=list"
    url_etp = "https://www.legifrance.gouv.fr/conv_coll/article/KALIARTI000043234742?utm_"

    st.info("Le **lissage** permet de compenser le creux d'heures pendant les vacances scolaires.")
    with st.expander("Formules"):
        st.latex("\\text{Heures mensuelles lissées} = \\frac{(\\text{Heures annuelles} + 10\\% \\text{ CP})}{12}")
        st.latex("\\text{Heures hebdomadaires lissées} = \\frac{\\text{Heures mensuelles lissées}}{(52 / 12)}")
    st.caption(f"[Lien Légifrance - Modulation et annualisation]({url_modulation})")

    st.divider()
    st.info("**L'équivalent temps plein - ETP - **permet de comparer les heures des profs (temps plein fixé à 24h/semaine par la convention collective ECLAT) à un temps plein classique (35h/semaine).")
    with st.expander("Formule"):
        st.latex("\\text{Heures mensuelles ETP} = \\frac{\\text{Heures hebdo lissées} \\times \\text{151,67}}{24}")
    st.caption(f"[Lien Légifrance - Temps plein professeur]({url_etp})")
    
    st.divider()
    st.write("**Calculateur :**")
    heures_annuelles_reelles = st.number_input(
        "Heures annuelles réellement effectuées (de septembre à août) :", min_value=0.0, step=0.5
    )

    if heures_annuelles_reelles > 0:
        heures_avec_cp = heures_annuelles_reelles * 1.10
        heures_mensuelles = heures_avec_cp / 12
        heures_hebdo = heures_mensuelles / (52/12)
        heures_mensuelles_etp = (heures_hebdo * ((35 * 52)/12)) / 24

        st.markdown("### Résultats")
        st.write(f"- Heures annuelles + 10% CP : **{heures_avec_cp:.2f} h**")
        st.write(f"- Heures mensuelles lissées : **{heures_mensuelles:.2f} h/mois**")
        st.write(f"- Heures hebdomadaires lissées : **{heures_hebdo:.2f} h/semaine**")
        st.write(f"- Heures mensuelles ETP : **{heures_mensuelles_etp:.2f} h**")


# PAGE 4: PRIMES

elif module == "Primes":
    st.title("Calcul des primes")

    st.info("La **prime d'ancienneté** est calculée sur la base du nombre d'années d'ancienneté. Elle commence à N+1. On compte 2 points par année d'ancienneté.")
    st.info("La **prime différentielle** a été mise en place afin que tou·te·s les salarié·e·s soient sur un pied d'égalité en termes de " \
    "rémunération, quelle que soit leur ancienneté.")
    st.caption("Le coefficient différentiel a été fixé lors de la mise en place de la convention collective actuelle, en 2021. " \
    "Est prise en compte la valeur de point d'indice en vigueur à l'époque : 6,32€.")
    with st.expander("Formules"):
        st.latex("\\text{Prime d'ancienneté} = \\frac{\\text{Heures hebdo lissées} \\times \\text{valeur du point d'indice} \\times (\\text{ancienneté} \\times 2)}{24}")
        st.latex("\\text{Prime différentielle} = \\frac{\\text{valeur max entre 0 et} \\text{(62.03 - (}\\text{ancienneté} \\times 2)) \\times \\text{6.32} \\times \\text{heures hebdo lissées}}{24}")
    
    st.divider()
    st.write("**Calculateur :**")
    date_entree = st.date_input(
        "Date d'entrée dans l'école :", min_value=date(1980,1,1), max_value=date.today()
    )
    heures_lissees = st.number_input("Heures hebdomadaires lissées :", min_value=0.0, step=0.5)
    valeur_point = 7.15
    st.caption(f"Valeur du point d'indice au 1er janvier 2025 : {valeur_point} €.")

    # Ancienneté
    today = datetime.today().date()
    anciennete = today.year - date_entree.year - ((today.month, today.day) < (date_entree.month, date_entree.day))

    if heures_lissees > 0:
        prime_anciennete = heures_lissees * valeur_point * (anciennete * 2) / 24
        prime_diff = max(0, (62.03 - (anciennete * 2))) * 6.32 * heures_lissees / 24

        st.markdown("### Résultats")
        st.write(f"- Ancienneté calculée : **{anciennete} ans**")
        st.write(f"- Prime d’ancienneté : **{prime_anciennete:.2f} €**")
        st.write(f"- Prime différentielle : **{prime_diff:.2f} €**")


# PAGE 5: VERIFICATEUR HEURES ANNUELLES

elif module == "Vérificateur d'heures":
    
    def hhmm_to_decimal(hhmm):
        """Convertit '03:30' en nombre décimal d’heures"""
        hh, mm = hhmm.strip().split(":")
        return int(hh) + int(mm)/60

    def parse_fichier_multi_profs(fichier_txt):
        """
        Retourne :
        heures_profs = { "Prénom NOM": [(date, heures), ...], ... }
        total_annuels = { "Prénom NOM": total_annee, ... }
        """
        heures_profs = {}
        total_annuels = {}
        lines = fichier_txt.splitlines()
        current_prof = None
        heures_courantes = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if not re.match(r"\d{2}-\d{2}-\d{4}", line) and not line.startswith("Total"):
                if current_prof is not None:
                    heures_profs[current_prof] = heures_courantes
                    total_annuels[current_prof] = sum(h for _, h in heures_courantes)
                current_prof = line
                heures_courantes = []

            match = re.match(r"(\d{2}-\d{2}-\d{4})\s+total jour\s*:\s*(\d{2}:\d{2})", line)
            if match:
                date_str, hhmm = match.groups()
                heures_courantes.append((date_str, hhmm_to_decimal(hhmm)))

            elif line.startswith("Total Période"):
                match_total = re.search(r"([\d,\.]+)", line)
                if match_total:
                    total_annuel = float(match_total.group(1).replace(",", "."))
                    total_annuels[current_prof] = total_annuel

        if current_prof is not None:
            heures_profs[current_prof] = heures_courantes
            if current_prof not in total_annuels:
                total_annuels[current_prof] = sum(h for _, h in heures_courantes)

        return heures_profs, total_annuels

    # Lecture backend
    DATA_FILE = Path(__file__).parent / "heures_2526.txt"

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        contenu = f.read()

    heures_profs, total_annuels = parse_fichier_multi_profs(contenu)

    st.title("Vérificateur heures annuelles réelles")

    prof_selectionne = st.selectbox("Sélectionnez votre nom :", list(heures_profs.keys()))

    if prof_selectionne:
        data_semaine = heures_profs[prof_selectionne]
        dates = [d for d, _ in data_semaine]
        heures = [h for _, h in data_semaine]
        total_annuel = total_annuels[prof_selectionne]

        st.markdown(f"### Total annuel : **{total_annuel:.2f} h**")

        # Tableau avec dates réelles     
        df_heures = pd.DataFrame({
            "Date": dates,
            "Heures": heures
        })
        jours_fr = {
            "Monday": "Lundi",
            "Tuesday": "Mardi",
            "Wednesday": "Mercredi",
            "Thursday": "Jeudi",
            "Friday": "Vendredi",
            "Saturday": "Samedi",
            "Sunday": "Dimanche"
        }
        df_heures['Jour'] = df_heures['Date'].apply(
            lambda x: jours_fr[datetime.strptime(x, "%d-%m-%Y").strftime("%A")]
        )
        df_heures = df_heures[['Jour', 'Date', 'Heures']]
        st.dataframe(df_heures, use_container_width=True)

        # Export PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph(f"Relevé heures annuelles - {prof_selectionne}", styles["Title"]))
        story.append(Spacer(1,12))
        story.append(Paragraph(f"Total annuel : {total_annuel:.2f} h", styles["Normal"]))
        story.append(Spacer(1,12))

        for date_str, h in data_semaine:
            story.append(Paragraph(f"{date_str} : {h:.2f} h", styles["Normal"]))

        doc.build(story)
        pdf_data = buffer.getvalue()

        st.download_button(
            label="Télécharger le PDF récapitulatif",
            data=pdf_data,
            file_name=f"heures_{prof_selectionne.replace(' ','_')}.pdf",
            mime="application/pdf"
        )


# PAGE 6: SIMULATEUR COMPLET

elif module == "🧮 Simulateur complet":
    st.title("🧮 Simulateur complet")
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
        prime_diff = max(0, (62.03 - (anciennete * 2))) * 6.32 * heures_hebdo / 24

        # Salaire brut
        salaire_base = (heures_hebdo * valeur_point * 300) / 24
        salaire_brut_total = salaire_base + prime_anciennete + prime_diff

        # Heures réelles mensuelles
        coef_etp_par_heure_reelle = 1.36
        heures_mensuelles_reelles = heures_mensuelles_etp / coef_etp_par_heure_reelle
        taux_horaire_brut_reel = salaire_brut_total / heures_mensuelles_reelles

        st.markdown("### Résultats")
        st.write(f"- Heures mensuelles lissées : **{heures_mensuelles:.2f} h/mois**")
        st.write(f"- Heures hebdomadaires lissées : **{heures_hebdo:.2f} h/semaine**")
        st.write(f"- Heures mensuelles ETP : **{heures_mensuelles_etp:.2f} h**")
        st.write(f"- Ancienneté : **{anciennete} ans**")
        st.write(f"- Prime d’ancienneté : **{prime_anciennete:.2f} €**")
        st.write(f"- Prime différentielle : **{prime_diff:.2f} €**")
        st.write(f"- Salaire brut total estimé : **{salaire_brut_total:.2f} €**")
        st.write(f"- Taux horaire brut réel : **{taux_horaire_brut_reel:.2f} €/h**")

        # Export PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("Simulation de salaire - Convention ECLAT", styles["Title"]))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Heures annuelles réelles : {heures_annuelles:.2f} h", styles["Normal"]))
        story.append(Paragraph(f"Heures mensuelles lissées : {heures_mensuelles:.2f} h/mois", styles["Normal"]))
        story.append(Paragraph(f"Heures hebdomadaires lissées : {heures_hebdo:.2f} h/semaine", styles["Normal"]))
        story.append(Paragraph(f"Heures mensuelles ETP : {heures_mensuelles_etp:.2f} h", styles["Normal"]))
        story.append(Paragraph(f"Heures mensuelles réelles (équivalentes) : {heures_mensuelles_reelles:.2f} h", styles["Normal"]))
        story.append(Paragraph(f"Ancienneté : {anciennete} ans", styles["Normal"]))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Salaire de base : {salaire_base:.2f} €", styles["Normal"]))
        story.append(Paragraph(f"Prime d’ancienneté : {prime_anciennete:.2f} €", styles["Normal"]))
        story.append(Paragraph(f"Prime différentielle : {prime_diff:.2f} €", styles["Normal"]))
        story.append(Paragraph(f"<b>Salaire brut total : {salaire_brut_total:.2f} €</b>", styles["Heading2"]))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Taux horaire brut réel : {taux_horaire_brut_reel:.2f} €/h", styles["Normal"]))

        doc.build(story)
        pdf_data = buffer.getvalue()

        st.download_button(
            label="📄 Télécharger le PDF récapitulatif",
            data=pdf_data,
            file_name="simulation_eclat.pdf",
            mime="application/pdf"
        )


# PAGE 7: LIENS UTILES

elif module == "🔗 Liens utiles":
    st.title("🔗 Liens utiles")
    
    st.write("### 1. Textes et avenants")
    url_eclat = "https://www.legifrance.gouv.fr/conv_coll/id/KALICONT000005635177"
    st.markdown(f"- [Convention collective ECLAT - IDCC 1518]({url_eclat})")

    st.write("### 2. Formules")

    with st.expander("Salaire de base"):
        st.latex("\\text{Salaire de base} = \\frac{\\text{Heures hebdo lissées} \\times \\text{valeur du point d'indice} \\times \\text{coefficient}}{24}")
    with st.expander("Heures mensuelles lissées"):
         st.latex("\\text{Heures mensuelles lissées} = \\frac{\\text{Heures annuelles} + 10\\% \\text{ CP}}{12}")
    with st.expander("Heures hebdomadaires lissées"):
        st.latex("\\text{Heures hebdomadaires lissées} = \\frac{\\text{Heures mensuelles lissées}}{\\frac{52}{12}}")
    with st.expander("Heures mensuelles ETP"):
        st.latex("\\text{Heures mensuelles ETP} = \\frac{\\text{Heures hebdo lissées} \\times \\text{151,67}}{24}")
    with st.expander("Prime d'ancienneté"): 
        st.latex("\\text{Prime d'ancienneté} = \\frac{\\text{Heures hebdo lissées} \\times \\text{valeur du point d'indice} \\times (\\text{ancienneté} \\times 2)}{24}")
    with st.expander("Prime différentielle"):
        st.latex("\\text{Prime différentielle} = \\frac{\\text{valeur max entre 0 et} \\text{(62.03 - (}\\text{ancienneté} \\times 2)) \\times \\text{6.32} \\times \\text{heures hebdo lissées}}{24}")