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

if st.button("Position ausschreiben", use_container_width=True, key="post_position"):
    st.switch_page("pages/6_Institution_Form.py") 