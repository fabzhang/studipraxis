import streamlit as st
from frontend.components.footer import footer
from frontend.components.header import header

st.set_page_config(
    page_title="Who We Are - studiPraxis",
    page_icon="👥"
)

# Add header
header()

st.markdown("## Who We Are")

st.markdown("""
### Unsere Mission

Studipraxis.de wurde mit der Mission gegründet, die Verbindung zwischen Medizinstudierenden und medizinischen Einrichtungen zu revolutionieren. Wir glauben daran, dass praktische Erfahrungen während des Studiums essentiell für die Entwicklung zukünftiger Ärzte sind.

### Unser Team

Unser Team besteht aus erfahrenen Medizinern, Softwareentwicklern und Unternehmern, die gemeinsam an der Vision arbeiten, die medizinische Ausbildung zu verbessern.

### Unsere Werte

- **Innovation**: Wir entwickeln kontinuierlich neue Lösungen für die Herausforderungen im Gesundheitswesen
- **Qualität**: Wir setzen höchste Standards für unsere Vermittlungsdienstleistungen
- **Transparenz**: Wir fördern offene Kommunikation zwischen allen Beteiligten
- **Nachhaltigkeit**: Wir arbeiten an langfristigen Lösungen für die medizinische Ausbildung

### Unsere Geschichte

Studipraxis.de wurde 2023 gegründet und hat sich seitdem zu einer der führenden Plattformen für die Vermittlung von Medizinstudierenden entwickelt.

### Unsere Ziele

- Verbesserung der praktischen Ausbildung von Medizinstudierenden
- Erleichterung des Zugangs zu relevanten Praxiserfahrungen
- Förderung der Vernetzung zwischen Studierenden und medizinischen Einrichtungen
- Beitrag zur Qualitätsverbesserung in der medizinischen Ausbildung
""")

# Add footer
footer() 