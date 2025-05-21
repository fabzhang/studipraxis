import streamlit as st
from frontend.components.footer import footer

st.set_page_config(
    page_title="Kontakt - studiPraxis",
    page_icon="📧"
)

st.markdown("## Kontakt")

st.markdown("""
### Haben Sie Fragen? Wir sind für Sie da!

**E-Mail:** kontakt@studipraxis.de  
**Telefon:** +49 (0) 40 123456789  
**Adresse:**  
Studipraxis GmbH  
Musterstraße 123  
20144 Hamburg

### Öffnungszeiten
Montag - Freitag: 9:00 - 17:00 Uhr

### Kontaktformular
""")

with st.form("contact_form"):
    name = st.text_input("Name")
    email = st.text_input("E-Mail")
    subject = st.selectbox("Betreff", [
        "Allgemeine Anfrage",
        "Technischer Support",
        "Feedback",
        "Sonstiges"
    ])
    message = st.text_area("Nachricht")
    
    submitted = st.form_submit_button("Nachricht senden")
    if submitted:
        st.success("Vielen Dank für Ihre Nachricht! Wir werden uns in Kürze bei Ihnen melden.")

# Add footer
footer() 