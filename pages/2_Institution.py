import streamlit as st

st.set_page_config(
    page_title="Für Institutionen - studiPraxis",
    page_icon="🏥"
)

st.markdown("### Für Institutionen")
st.write("StudiPraxis.de bietet Kliniken, Praxen und Forschungseinrichtungen die Möglichkeit, motivierte Medizinstudierende für Assistenzstellen zu gewinnen.")

with st.expander("Was bringt Ihnen die Plattform?"):
    st.markdown("""
    - Direkte Reichweite an Studierende nach Fachinteressen und Verfügbarkeit
    - Zeitersparnis durch strukturierte Profile und Kontaktaufnahme
    - Rechtlich sichere Gestaltung von Werkstudentenverträgen möglich
    """)

# Create two columns for the buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Klinik anmelden", use_container_width=True, key="hospital_login"):
        st.switch_page("pages/7_Hospital_Login.py")

with col2:
    if st.button("Neue Klinik registrieren", use_container_width=True, key="hospital_register"):
        st.switch_page("pages/7_Hospital_Login.py") 