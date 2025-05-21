import streamlit as st
from frontend.components.footer import footer

st.set_page_config(
    page_title="Impressum - studiPraxis",
    page_icon="ℹ️"
)

st.markdown("## Impressum")

st.markdown("""
### Angaben gemäß § 5 TMG

Studipraxis.de  
Musterstraße 123  
12345 Hamburg

### Kontakt

Telefon: +49 (0) 123 456789  
E-Mail: info@studipraxis.de

### Verantwortlich für den Inhalt nach § 55 Abs. 2 RStV

Max Mustermann  
Musterstraße 123  
12345 Hamburg

### EU-Streitschlichtung

Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung (OS) bereit.

### Verbraucherstreitschlichtung/Universalschlichtungsstelle

Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.

### Haftung für Inhalte

Als Diensteanbieter sind wir gemäß § 7 Abs.1 TMG für eigene Inhalte auf diesen Seiten nach den allgemeinen Gesetzen verantwortlich.

### Haftung für Links

Unser Angebot enthält Links zu externen Websites Dritter, auf deren Inhalte wir keinen Einfluss haben.

### Urheberrecht

Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen dem deutschen Urheberrecht.
""")

# Add footer
footer() 