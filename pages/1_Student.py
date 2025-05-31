import streamlit as st
from frontend.components.footer import footer
from frontend.components.header import header

st.set_page_config(
    page_title="Student - studiPraxis",
    page_icon="🧑‍🎓"
)

# Add header
header()

st.markdown("### Willkommen bei studiPraxis!")

# Check if user is logged in
if 'student_id' not in st.session_state or not st.session_state.student_id:
    st.info("Bitte melden Sie sich an oder registrieren Sie sich, um fortzufahren.")
    
    # Create two columns for the buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Anmelden", use_container_width=True):
            st.switch_page("pages/9_Student_Login.py")
    
    with col2:
        if st.button("Registrieren", use_container_width=True):
            st.switch_page("pages/9_Student_Login.py")
else:
    # User is logged in, show dashboard options
    st.success("Sie sind angemeldet!")
    
    # Create two columns for the buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Positionen durchsuchen", use_container_width=True):
            st.switch_page("pages/3_Student_Dashboard.py")
    
    with col2:
        if st.button("Profil bearbeiten", use_container_width=True):
            st.switch_page("pages/4_Profile.py")

st.markdown("""
<div style='margin-top:1em; margin-bottom:1em;'>
<h3>🚀 Starte jetzt deine Zukunft!</h3>
<p>Registriere dich kostenlos auf <b>Studipraxis.de</b> und finde noch heute die passende Stelle, die dein Studium und deine Karriere nach vorne bringt!</p>
<h4>🎓 Dein Sprungbrett in die Medizinwelt – mit Studipraxis</h4>
<p>Sammle echte Praxiserfahrung, verdiene Geld neben dem Studium, baue dein medizinisches Netzwerk auf – und hab dabei auch noch Spaß!</p>
<p>Mit Studipraxis findest du flexible Werkstudentenjobs in Praxen, Kliniken und medizinischen Einrichtungen, die perfekt zu deinem Studienalltag passen.</p>
<b>Deine Vorteile auf einen Blick:</b>
<ul style='font-size:1.1rem; line-height:1.7;'>
    <li>✔ Frühzeitig praktische Erfahrung sammeln</li>
    <li>✔ Faire Bezahlung und flexible Arbeitszeiten</li>
    <li>✔ Sicher und günstig krankenversichert bleiben</li>
    <li>✔ Wichtige Kontakte für deine Zukunft knüpfen</li>
    <li>✔ Werde ein Teammitglied echter medizinischer Teams</li>
</ul>
<p style='font-weight:bold; color:#15396b;'>Dein Studium. Deine Karriere. Dein Job.</p>
</div>
""", unsafe_allow_html=True)
if st.button("Mehr Informationen", key="info_btn_student"):
    st.switch_page("pages/10_Student_Info.py")

# Add footer at the bottom
footer() 