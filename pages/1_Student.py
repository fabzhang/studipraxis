import streamlit as st

st.set_page_config(
    page_title="Für Studierende - studiPraxis",
    page_icon="🧑‍🎓"
)

st.markdown("### Für Studierende")
st.write("Als Medizinstudent*in kannst du über studiPraxis.de passende Stellenangebote finden, die praktische Erfahrungen ermöglichen und dich gleichzeitig finanziell unterstützen.")

with st.expander("Was bedeutet eine Anstellung als Werkstudent*in?"):
    st.markdown("""
    - Maximal 20 Stunden pro Woche während des Semesters
    - Du bleibst in der Regel familien- und studienversichert
    - Ein fairer Lohn für praktische Mitarbeit
    - Möglichkeit, Fachbereiche frühzeitig kennenzulernen
    """)

# Create two columns for the buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Stellenangebote durchsuchen", use_container_width=True, key="search_positions"):
        st.switch_page("pages/3_Positionen.py")

with col2:
    if st.button("Profil erstellen", use_container_width=True, key="create_profile"):
        st.switch_page("pages/5_Student_Form.py") 