import streamlit as st
from PIL import Image
from frontend.components.footer import footer

st.set_page_config(
    page_title="studiPraxis.de",
    layout="wide",
    page_icon="💡",
    initial_sidebar_state="expanded"
)

# Load and display logo
logo = Image.open("studipraxis_logo.png")

# Center-aligned header
st.markdown("""
<div style='text-align: center;'>
    <h1 style='color: #15396b;'>studiPraxis.de</h1>
    <p style='font-size: 1.2rem;'>Praxiserfahrung. Einfach vermittelt.</p>
</div>
""", unsafe_allow_html=True)

# Create two columns for the buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Ich bin Student*in", use_container_width=True, key="student_main"):
        st.switch_page("pages/1_Student.py")

with col2:
    if st.button("Ich bin eine Institution", use_container_width=True, key="institution_main"):
        st.switch_page("pages/2_Institution.py")

# Default landing page content
st.markdown("""
<div style='margin-top:2em; margin-bottom:2em;'>
    <h3 style='color:#15396b;'>Warum Studipraxis?</h3>
    <ul style='font-size:1.1rem; line-height:1.7;'>
        <li><b>Schnell, unkompliziert und kostenlos</b> für Studierende</li>
        <li><b>Zugang zu exklusiven Werkstudentenstellen</b> in der Medizin</li>
        <li><b>Individuelle Suchoptionen</b> für deine Präferenzen</li>
        <li>Auf Wunsch <b>proaktive Kontaktaufnahme</b> durch potentielle Arbeitgeber</li>
        <li><b>Absolute Datenkontrolle:</b> Du entscheidest, wer dein Profil sieht</li>
        <li><b>Flexible Jobs</b>, die wirklich zu deinem Studium und deinem Lebensstil passen</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Add footer at the bottom
footer()
