import streamlit as st
import random
import time

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="QCM Gestion Financière", page_icon="📊", layout="centered")
# --- STYLE PERSONNALISÉ (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stProgress > div > div > div > div { background-color: #4CAF50; }
    .question-box { background-color: #0000000; padding: 20px; border-radius: 10px; border-left: 5px solid #007BFF; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# [cite_start]--- DONNÉES (Questions basées sur le document [cite: 1, 44, 77]) ---
if 'questions' not in st.session_state:
    questions = [
        # --- CHAPITRE 1 : CHARGES FIXES ET VARIABLES ---
        {
            "theme": "Ch.1 - Nature des Charges",
            "question": "Quels éléments composent précisément les charges de structure (fixes) ?",
            "options": ["La structure de production (amortissements, loyers)", "La structure humaine (rémunérations fixes, charges sociales)", "La structure financière (intérêts des emprunts)", "Les achats de matières premières et marchandises", "Les commissions des OTA (Online Travel Agency)"],
            "answers": ["La structure de production (amortissements, loyers)", "La structure humaine (rémunérations fixes, charges sociales)", "La structure financière (intérêts des emprunts)"],
            "explication": "Les charges fixes sont liées à l'existence de la structure (production, humaine, financière) et ne dépendent pas du volume d'activité immédiat."
        },
        {
            "theme": "Ch.1 - Charges Variables",
            "question": "Quelles affirmations sont vraies concernant les charges opérationnelles (variables) ?",
            "options": ["Elles varient proportionnellement avec l'activité", "Elles incluent les consommables et les commissions", "Elles restent stables jusqu'à un certain niveau d'activité", "Elles sont déduites du CA pour obtenir la MSCV", "Les amortissements en font partie"],
            "answers": ["Elles varient proportionnellement avec l'activité", "Elles incluent les consommables et les commissions", "Elles sont déduites du CA pour obtenir la MSCV"],
            "explication": "Les charges variables (achats, commissions) fluctuent selon les ventes, contrairement aux charges de structure."
        },
        {
            "theme": "Ch.1 - Analyse de la MSCV",
            "question": "Que représente concrètement la Marge sur Coûts Variables (MSCV) ?",
            "options": ["Le bénéfice net final de l'entreprise", "Ce que l'activité dégage avant de couvrir les charges fixes", "La part de CA non consommée par les coûts variables", "Si MSCV < Charges Fixes, l'entreprise dégage une perte", "Elle se calcule par : CA - Charges Fixes"],
            "answers": ["Ce que l'activité dégage avant de couvrir les charges fixes", "La part de CA non consommée par les coûts variables", "Si MSCV < Charges Fixes, l'entreprise dégage une perte"],
            "explication": "La MSCV (CA - CV) est l'indicateur clé : elle doit être assez grande pour éponger les charges fixes et créer un bénéfice."
        },
        # --- CHAPITRE 2 : LE SEUIL DE RENTABILITÉ ---
        {
            "theme": "Ch.2 - Seuil de Rentabilité (SR)",
            "question": "Comment définit-on précisément le Seuil de Rentabilité ?",
            "options": ["C'est le chiffre d'affaires critique", "C'est le montant de CA où le résultat est égal à zéro", "C'est le niveau d'activité où l'on couvre l'intégralité des charges", "C'est la date de rentabilité", "C'est le point où MSCV = Charges Fixes"],
            "answers": ["C'est le chiffre d'affaires critique", "C'est le montant de CA où le résultat est égal à zéro", "C'est le niveau d'activité où l'on couvre l'intégralité des charges", "C'est le point où MSCV = Charges Fixes"],
            "explication": "Au SR, l'entreprise ne fait ni bénéfice ni perte. Toute vente supplémentaire après le SR génère du profit."
        },
        {
            "theme": "Ch.2 - Point Mort (PM) et Sécurité",
            "question": "Concernant le Point Mort et la Marge de Sécurité :",
            "options": ["Le PM est une date calculée sur une base de 360 jours", "PM = (Seuil de Renta / CA HT) x 360", "Marge de sécurité = CA - Seuil de Rentabilité", "Plus la marge de sécurité est faible, plus le risque est faible", "Le point mort s'exprime en euros"],
            "answers": ["Le PM est une date calculée sur une base de 360 jours", "PM = (Seuil de Renta / CA HT) x 360", "Marge de sécurité = CA - Seuil de Rentabilité"],
            "explication": "Le PM donne le moment de l'année où l'on devient rentable. La marge de sécurité mesure l'éloignement par rapport au danger (perte)."
        },
        {
            "theme": "Ch.2 - Chiffre d'Affaires Cible (CAC)",
            "question": "Quelle formule permet de calculer le CA nécessaire pour atteindre un bénéfice souhaité ?",
            "options": ["CAC = (Résultat visé + Charges Fixes) / TMSCV", "CAC = SR + Résultat visé", "CAC = (Charges Fixes / TMSCV) + Résultat visé", "Elle permet de prévoir l'activité pour un objectif précis", "CAC = MSCV / CA"],
            "answers": ["CAC = (Résultat visé + Charges Fixes) / TMSCV", "Elle permet de prévoir l'activité pour un objectif précis"],
            "explication": "Pour viser un bénéfice, on l'ajoute aux charges fixes à couvrir dans le calcul du seuil."
        },
        # --- CHAPITRE 3 : LES SOLDES INTERMÉDIAIRES DE GESTION (SIG) ---
        {
            "theme": "Ch.3 - Marge Commerciale et Production",
            "question": "Quelles sont les spécificités de la Marge Commerciale et de la Production ?",
            "options": ["Marge commerciale = Ventes Mses - Coût d'achat des Mses vendues", "La production de l'exercice inclut la production stockée et immobilisée", "La marge commerciale est aussi appelée Marge Brute", "La production de l'exercice concerne toutes les entreprises", "La production stockée peut impacter le solde de production"],
            "answers": ["Marge commerciale = Ventes Mses - Coût d'achat des Mses vendues", "La production de l'exercice inclut la production stockée et immobilisée", "La marge commerciale est aussi appelée Marge Brute", "La production stockée peut impacter le solde de production"],
            "explication": "La marge est pour le négoce (revente), la production pour la création. Note : la production ne concerne que les entreprises de production."
        },
        {
            "theme": "Ch.3 - Valeur Ajoutée (VA)",
            "question": "Que mesure précisément la Valeur Ajoutée ?",
            "options": ["La richesse réelle créée par l'entreprise", "Le poids économique de l'entreprise", "VA = (Marge commerciale + Production) - Consommations en provenance des tiers", "Le bénéfice distribuable aux actionnaires", "La différence entre le CA et les charges de personnel"],
            "answers": ["La richesse réelle créée par l'entreprise", "Le poids économique de l'entreprise", "VA = (Marge commerciale + Production) - Consommations en provenance des tiers"],
            "explication": "La VA montre ce que l'entreprise a apporté de plus aux matières et services achetés à l'extérieur."
        },
        {
            "theme": "Ch.3 - Excédent Brut d'Exploitation (EBE)",
            "question": "L'EBE est un indicateur fondamental car :",
            "options": ["Il est indépendant de la politique d'amortissement", "Il est indépendant du mode de financement (intérêts)", "Il mesure la performance économique brute de l'exploitation", "EBE = VA + Subventions - Impôts/Taxes - Charges de personnel", "Il prend en compte le résultat exceptionnel"],
            "answers": ["Il est indépendant de la politique d'amortissement", "Il est indépendant du mode de financement (intérêts)", "Il mesure la performance économique brute de l'exploitation", "EBE = VA + Subventions - Impôts/Taxes - Charges de personnel"],
            "explication": "L'EBE est le 'poumon' financier de l'activité, avant les choix comptables et financiers."
        },
        {
            "theme": "Ch.3 - REX et RCAI",
            "question": "Comment se forment le Résultat d'Exploitation (REX) et le Courant (RCAI) ?",
            "options": ["REX = EBE - Dotations aux amortissements + Reprises", "Le REX tient compte de la politique d'investissement", "RCAI = REX + Produits financiers - Charges financières", "Le RCAI mesure l'impact de l'endettement", "Le RCAI inclut les amendes et pénalités exceptionnelles"],
            "answers": ["REX = EBE - Dotations aux amortissements + Reprises", "Le REX tient compte de la politique d'investissement", "RCAI = REX + Produits financiers - Charges financières", "Le RCAI mesure l'impact de l'endettement"],
            "explication": "Le REX intègre l'usure du matériel (amortissements). Le RCAI y ajoute le coût de l'argent (intérêts)."
        },
        {
            "theme": "Ch.3 - Résultat Net (RN)",
            "question": "Concernant le calcul final du Résultat Net :",
            "options": ["RN = RCAI + Résultat exceptionnel - Participation - Impôts", "Le résultat exceptionnel concerne les opérations non récurrentes", "Le RN est le seul indicateur de la richesse créée", "Il est le solde final disponible pour les dividendes ou réserves", "Le résultat exceptionnel découle directement du RCAI"],
            "answers": ["RN = RCAI + Résultat exceptionnel - Participation - Impôts", "Le résultat exceptionnel concerne les opérations non récurrentes", "Il est le solde final disponible pour les dividendes ou réserves"],
            "explication": "Le RN est la 'dernière ligne'. Le résultat exceptionnel est calculé à part car il ne dépend pas de l'activité courante."
        },
        # --- COMPLÉMENTS ---
        {
            "theme": "Ch.1 - Formules du Taux",
            "question": "Comment calcule-t-on le Taux de Marge sur Coûts Variables (TMSCV) ?",
            "options": ["TMSCV = (MSCV / CA HT) * 100", "TMSCV = (CA HT / MSCV) * 100", "TMSCV = (Marge Brute / CA HT) * 100", "C'est la part de chaque euro de CA qui sert à couvrir les charges fixes", "Il reste constant quel que soit le niveau de CA (si les conditions d'exploitation ne changent pas)"],
            "answers": ["TMSCV = (MSCV / CA HT) * 100", "C'est la part de chaque euro de CA qui sert à couvrir les charges fixes", "Il reste constant quel que soit le niveau de CA (si les conditions d'exploitation ne changent pas)"],
            "explication": "Le TMSCV est un ratio. Si ton TMSCV est de 30%, cela signifie que pour 100€ de ventes, il te reste 30€ pour payer tes loyers et salaires fixes."
        },
        {
            "theme": "Ch.2 - Indice de Sécurité",
            "question": "À quoi correspond l'Indice de Sécurité (IS) ?",
            "options": ["IS = (Marge de sécurité / CA HT) * 100", "Il exprime le pourcentage de baisse de CA supportable sans faire de perte", "Plus il est proche de 100%, plus l'entreprise est risquée", "C'est le montant minimum de trésorerie en banque", "Il permet de comparer la solidité de deux entreprises de tailles différentes"],
            "answers": ["IS = (Marge de sécurité / CA HT) * 100", "Il exprime le pourcentage de baisse de CA supportable sans faire de perte", "Il permet de comparer la solidité de deux entreprises de tailles différentes"],
            "explication": "L'indice de sécurité transforme la marge de sécurité (€) en pourcentage (%), ce qui est plus parlant pour l'analyse."
        },
        {
            "theme": "Ch.3 - La Production de l'exercice",
            "question": "De quoi se compose précisément la Production de l'exercice ?",
            "options": ["La production vendue (au prix de vente HT)", "La production stockée (au coût de production)", "La production immobilisée (travaux faits par l'entreprise pour elle-même)", "La marge commerciale sur les produits fabriqués", "Les achats de matières premières"],
            "answers": ["La production vendue (au prix de vente HT)", "La production stockée (au coût de production)", "La production immobilisée (travaux faits par l'entreprise pour elle-même)"],
            "explication": "La production de l'exercice est la somme de ces trois éléments. Attention, elle ne concerne que les entreprises qui fabriquent quelque chose."
        },
        {
            "theme": "Ch.3 - La Production Stockée",
            "question": "Que signifie une 'Production Stockée' négative dans les SIG ?",
            "options": ["L'entreprise a vendu plus que ce qu'elle a produit durant l'année", "Il y a eu un déstockage (on a pisé dans les réserves)", "L'entreprise est forcément en perte", "Cela vient diminuer la valeur du solde 'Production de l'exercice'", "C'est impossible, un stock est toujours positif"],
            "answers": ["L'entreprise a vendu plus que ce qu'elle a produit durant l'année", "Il y a eu un déstockage (on a pisé dans les réserves)", "Cela vient diminuer la valeur du solde 'Production de l'exercice'"],
            "explication": "Si le stock final est plus petit que le stock initial, la variation est négative. On a vendu des produits fabriqués les années précédentes."
        },
        {
            "theme": "Ch.3 - Répartition de la VA",
            "question": "Comment est répartie la Valeur Ajoutée (VA) selon les SIG ?",
            "options": ["Au personnel (salaires et charges sociales)", "À l'État (impôts et taxes)", "Aux prêteurs / banques (intérêts)", "À l'entreprise elle-même (autofinancement via l'EBE et les amortissements)", "Aux clients (remises et rabais)"],
            "answers": ["Au personnel (salaires et charges sociales)", "À l'État (impôts et taxes)", "Aux prêteurs / banques (intérêts)", "À l'entreprise elle-même (autofinancement via l'EBE et les amortissements)"],
            "explication": "La VA est la richesse créée. Elle est ensuite 'mangée' par les différents acteurs (salariés, État, banques) avant qu'il ne reste le profit."
        }
    ]
    random.shuffle(questions)
    st.session_state.questions = questions
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.feedback = None

# --- BARRE LATÉRALE (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Paramètres & Infos")
    st.info("**Rappel :** Uniquement sur les chapitres 1, 2 et 3.\n\n**Auteur :** Par LV")
    st.divider()
    st.warning("⚠️ PS : Toute personne utilisant ce QCM me doit un verre.")
    if st.button("Réinitialiser le Quiz"):
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.feedback = None
        random.shuffle(st.session_state.questions)
        st.rerun()

# --- ZONE PRINCIPALE ---
# Barre de progression
total_q = len(st.session_state.questions)
progress = (st.session_state.index) / total_q
st.progress(progress)

if st.session_state.index < total_q:
    q = st.session_state.questions[st.session_state.index]
    
    # Bloc Question
    st.markdown(f"### QUESTION {st.session_state.index + 1}/{total_q} (Gestion Financière)")
    st.markdown(f"**Thème :** `{q['theme']}`")
    
    with st.container():
        st.markdown(f"""<div class="question-box"><h4>{q['question']}</h4></div>""", unsafe_allow_html=True)
        
        # Options
        selected = []
        for opt in q['options']:
            if st.checkbox(opt, key=f"{st.session_state.index}_{opt}"):
                selected.append(opt)

    # Validation
    if st.button("Valider la réponse"):
        correct = sorted(q['answers'])
        user_choice = sorted(selected)
        
        if user_choice == correct:
            st.session_state.feedback = ("success", "✅ CORRECT !")
            st.session_state.score += 1
        else:
            st.session_state.feedback = ("error", f"❌ INCORRECT\n\nLes bonnes réponses étaient :\n" + "\n".join([f"- {a}" for a in correct]))

    # Affichage du Feedback et de l'explication
    if st.session_state.feedback:
        type_f, msg_f = st.session_state.feedback
        if type_f == "success": st.success(msg_f)
        else: st.error(msg_f)
        
        with st.expander("💡Rappel de cours", expanded=True):
            st.info(q['explication'])
        
        if st.button("Question suivante ➡️"):
            st.session_state.index += 1
            st.session_state.feedback = None
            st.rerun()

else:
    # --- BILAN FINAL ---
    st.balloons()
    st.header("🏆 Bilan de l'examen")
    score = st.session_state.score
    
    col1, col2 = st.columns(2)
    col1.metric("Score Final", f"{score} / {total_q}")
    col2.metric("Taux de réussite", f"{(score/total_q)*100:.0f}%")

    if score/total_q >= 0.8:
        st.success("Excellent ! Vous maîtrisez les concepts de rentabilité.")
    elif score/total_q >= 0.5:
        st.warning("Résultats corrects, mais revoyez les formules des SIG.")
    else:
        st.error("Attention : Les bases du compte différentiel sont à relire.")

    if st.button("Recommencer"):
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.feedback = None
        st.rerun()




