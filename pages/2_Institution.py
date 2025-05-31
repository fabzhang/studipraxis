import streamlit as st
from frontend.components.footer import footer
from frontend.components.header import header

st.set_page_config(
    page_title="Für Institutionen - studiPraxis",
    page_icon="🏥"
)

# Add header
header()

st.markdown("### Für Institutionen")
st.write("StudiPraxis.de bietet Kliniken, Praxen und Forschungseinrichtungen die Möglichkeit, motivierte Medizinstudierende für Assistenzstellen zu gewinnen.")

# Create two columns for the buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Klinik anmelden", use_container_width=True, key="hospital_login"):
        st.switch_page("pages/7_Hospital_Login.py")

with col2:
    if st.button("Neue Klinik registrieren", use_container_width=True, key="hospital_register"):
        st.switch_page("pages/7_Hospital_Login.py")

st.markdown("""
## 🏥 Medizinstudierende zur Unterstützung Ihrer Einrichtung

Mit **Studipraxis** finden Sie qualifizierte, engagierte Medizinstudierende für flexible Werkstudententätigkeiten – **schnell und unkompliziert vermittelt**.

**💡 So profitieren Sie von der Zusammenarbeit:**

- 🗂️ Entlastung bei administrativen Aufgaben, Rezeption & Telefon
- 💉 Unterstützung bei Blutabnahmen, EKG, Infusionen & Dokumentation
- 🩺 Assistenz im OP oder bei Untersuchungen (je nach Kenntnisstand)
- 🚑 Mithilfe in der Notaufnahme, im Praxis- oder Stationsalltag
- 🤝 Frühzeitiger Kontakt zu zukünftigen Ärzt:innen und Fachkräften
- 💶 Günstige Anstellung durch Werkstudentenstatus (geringe Abgaben)

Egal ob Praxis, Klinik oder MVZ – unsere Studierenden möchten Erfahrung sammeln und helfen dort, wo Ihr Team Unterstützung braucht.

**🌟 Warum Studipraxis für Ihre Einrichtung?**

- ✔️ Zugriff auf motivierten medizinischen Nachwuchs
- ✔️ Entlastung für Ihr Team – besonders bei Personalengpässen
- ✔️ Schnelle, unkomplizierte Abwicklung
- ✔️ Plattform speziell für Medizinstudierende
- ✔️ Nur verifizierte Nutzer*innen
- ✔️ 100 % DSGVO-konform

**Jetzt registrieren und die Vorteile sichern!**
""")
if st.button("Mehr Informationen anzeigen", key="info_btn_hospital"):
    st.switch_page("pages/11_Institution_Info.py")

# Add footer at the bottom
footer() 