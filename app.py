import streamlit as st
from hospital_form import hospital_form
from student_form import student_form
from match_view import match_view
from student_view import student_view
from PIL import Image

# Initialize session state for navigation
if 'menu' not in st.session_state:
    st.session_state.menu = "Startseite"

st.set_page_config(
    page_title="Hospital-Student Match",
    layout="wide",
    page_icon="💡",
    initial_sidebar_state="expanded"
)

# Use session state for the menu selection
menu = st.sidebar.radio("Navigation", 
    ["Startseite", "Für Studierende", "Für Institutionen", "Alle Positionen", "Student*innen Profile"],
    key="menu"
)

# Load and display logo
logo = Image.open("studipraxis_logo.png")

# Center-aligned header
st.markdown("""
<div style='text-align: center;'>
    <h1 style='color: #1e8e5a;'>studiPraxis.de</h1>
    <p style='font-size: 1.2rem;'>Praxiserfahrung. Einfach vermittelt.</p>
</div>
""", unsafe_allow_html=True)

if menu == "Startseite":
    # Create two columns for the buttons
    col1, col2 = st.columns(2)

    with col1:
        student_button = st.button("Ich bin Student*in", use_container_width=True)

    with col2:
        institution_button = st.button("Ich bin eine Institution", use_container_width=True)

    # Content based on button selection
    if student_button:
        st.markdown("### Für Studierende")
        st.write("Als Medizinstudent*in kannst du über studiPraxis.de passende Stellenangebote finden, die praktische Erfahrungen ermöglichen und dich gleichzeitig finanziell unterstützen.")
        
        with st.expander("Was bedeutet eine Anstellung als Werkstudent*in?"):
            st.markdown("""
            - Maximal 20 Stunden pro Woche während des Semesters
            - Du bleibst in der Regel familien- und studienversichert
            - Ein fairer Lohn für praktische Mitarbeit
            - Möglichkeit, Fachbereiche frühzeitig kennenzulernen
            """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Stellenangebote durchsuchen"):
                st.session_state.menu = "Alle Positionen"
                st.experimental_rerun()
        
        with col2:
            if st.button("Profil erstellen"):
                st.session_state.menu = "Für Studierende"
                st.experimental_rerun()

    elif institution_button:
        st.markdown("### Für Institutionen")
        st.write("StudiPraxis.de bietet Kliniken, Praxen und Forschungseinrichtungen die Möglichkeit, motivierte Medizinstudierende für Assistenzstellen zu gewinnen.")
        
        with st.expander("Was bringt Ihnen die Plattform?"):
            st.markdown("""
            - Direkte Reichweite an Studierende nach Fachinteressen und Verfügbarkeit
            - Zeitersparnis durch strukturierte Profile und Kontaktaufnahme
            - Rechtlich sichere Gestaltung von Werkstudentenverträgen möglich
            """)
        
        if st.button("Position ausschreiben"):
            st.switch_page("Hospitals: Post Position")

    else:
        # Default landing page content
        st.markdown("""
        ### Willkommen bei studiPraxis.de
        
        Wählen Sie oben aus, ob Sie Student*in oder Institution sind, um fortzufahren.
        """)

elif menu == "Für Studierende":
    st.markdown("### Für Studierende")
    st.write("Als Medizinstudent*in kannst du über studiPraxis.de passende Stellenangebote finden, die praktische Erfahrungen ermöglichen und dich gleichzeitig finanziell unterstützen.")
    
    with st.expander("Was bedeutet eine Anstellung als Werkstudent*in?"):
        st.markdown("""
        - Maximal 20 Stunden pro Woche während des Semesters
        - Du bleibst in der Regel familien- und studienversichert
        - Ein fairer Lohn für praktische Mitarbeit
        - Möglichkeit, Fachbereiche frühzeitig kennenzulernen
        """)
    student_form()

elif menu == "Für Institutionen":
    st.markdown("### Für Institutionen")
    st.write("StudiPraxis.de bietet Kliniken, Praxen und Forschungseinrichtungen die Möglichkeit, motivierte Medizinstudierende für Assistenzstellen zu gewinnen.")
    
    with st.expander("Was bringt Ihnen die Plattform?"):
        st.markdown("""
        - Direkte Reichweite an Studierende nach Fachinteressen und Verfügbarkeit
        - Zeitersparnis durch strukturierte Profile und Kontaktaufnahme
        - Rechtlich sichere Gestaltung von Werkstudentenverträgen möglich
        """)
    hospital_form()

elif menu == "Alle Positionen":
    match_view()

elif menu == "Student*innen Profile":
    student_view()
