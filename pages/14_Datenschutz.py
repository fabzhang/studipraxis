import streamlit as st
from frontend.components.footer import footer
from frontend.components.header import header

st.set_page_config(
    page_title="Datenschutzerklärung - studiPraxis",
    page_icon="🔒"
)

# Add header
header()

st.markdown("## Datenschutzerklärung")

st.markdown("""
### 1. Datenschutz auf einen Blick

#### Allgemeine Hinweise
Die folgenden Hinweise geben einen einfachen Überblick darüber, was mit Ihren personenbezogenen Daten passiert, wenn Sie diese Website besuchen.

#### Datenerfassung auf dieser Website
Die Datenverarbeitung auf dieser Website erfolgt durch den Websitebetreiber.

### 2. Allgemeine Hinweise und Pflichtinformationen

#### Datenschutz
Die Betreiber dieser Seiten nehmen den Schutz Ihrer persönlichen Daten sehr ernst.

#### Hinweis zur verantwortlichen Stelle
Die verantwortliche Stelle für die Datenverarbeitung auf dieser Website ist:
Studipraxis.de
Musterstraße 123
12345 Hamburg

### 3. Datenerfassung auf dieser Website

#### Cookies
Die Internetseiten verwenden teilweise so genannte Cookies.

#### Server-Log-Dateien
Der Provider der Seiten erhebt und speichert automatisch Informationen in so genannten Server-Log-Dateien.

### 4. Soziale Medien

#### Datenschutzerklärung für die Nutzung von LinkedIn
Wir nutzen auf unserer Website Komponenten des Netzwerks LinkedIn.

### 5. Newsletter

#### Newsletterdaten
Wenn Sie den auf der Website angebotenen Newsletter beziehen möchten, benötigen wir von Ihnen eine E-Mail-Adresse.

### 6. Plugins und Tools

#### Google Analytics
Diese Website nutzt Funktionen des Webanalysedienstes Google Analytics.
""")

# Add footer
footer() 