import streamlit as st
from frontend.components.footer import footer

st.set_page_config(
    page_title="AGB - studiPraxis",
    page_icon="📜"
)

st.markdown("## Allgemeine Geschäftsbedingungen")

st.markdown("""
### §1 Geltungsbereich

Diese Allgemeinen Geschäftsbedingungen (AGB) gelten für die Nutzung der Plattform Studipraxis.de.

### §2 Leistungsbeschreibung

Studipraxis.de vermittelt Medizinstudierende an medizinische Einrichtungen für Werkstudententätigkeiten.

### §3 Registrierung und Nutzerkonto

1. Die Registrierung erfolgt durch Ausfüllen des Registrierungsformulars
2. Der Nutzer verpflichtet sich, wahrheitsgemäße Angaben zu machen
3. Jeder Nutzer darf nur ein Konto erstellen

### §4 Pflichten der Nutzer

1. Wahrheitsgemäße Angaben
2. Aktuelle Daten
3. Sorgfältiger Umgang mit Zugangsdaten

### §5 Haftung

1. Studipraxis.de haftet nicht für die Richtigkeit der Nutzerangaben
2. Die Haftung ist auf Vorsatz und grobe Fahrlässigkeit beschränkt

### §6 Datenschutz

Die Datenschutzerklärung ist Bestandteil dieser AGB.

### §7 Änderungen der AGB

Studipraxis.de behält sich vor, diese AGB jederzeit zu ändern.

### §8 Schlussbestimmungen

1. Es gilt deutsches Recht
2. Gerichtsstand ist Hamburg
""")

# Add footer
footer() 