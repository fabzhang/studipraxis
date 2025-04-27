import streamlit as st
from backend.services.data_service import DataService

# Coordinates for major hospitals in Hamburg
HAMBURG_COORDINATES = {
    "Universitätsklinikum Hamburg-Eppendorf (UKE)": (53.5897, 9.9756),
    "Asklepios Klinik St. Georg": (53.5553, 10.0114),
    "Asklepios Klinik Barmbek": (53.5869, 10.0406),
    "Asklepios Klinik Altona": (53.5511, 9.9357),
    "Asklepios Klinik Wandsbek": (53.5731, 10.0853),
    "Asklepios Klinik Harburg": (53.4603, 9.9833),
    "Marienkrankenhaus": (53.5511, 9.9357),
    "Evangelisches Krankenhaus Alsterdorf": (53.6103, 10.0133),
    "Krankenhaus Tabea": (53.5511, 9.9357),
    "Krankenhaus Rissen": (53.5833, 9.7500)
}

st.set_page_config(
    page_title="Klinik Login - studiPraxis",
    page_icon="🔐"
)

st.markdown("### Klinik Login")

# Initialize session state for hospital
if 'hospital_id' not in st.session_state:
    st.session_state.hospital_id = None

def login():
    data_service = DataService()
    
    with st.form("login_form"):
        email = st.text_input("E-Mail")
        password = st.text_input("Passwort", type="password")
        
        submitted = st.form_submit_button("Anmelden")
        if submitted:
            try:
                hospital = data_service.authenticate_hospital(email, password)
                if hospital:
                    st.session_state.hospital_id = hospital.id
                    st.success("Login erfolgreich!")
                    st.switch_page("pages/8_Hospital_Dashboard.py")
                else:
                    st.error("Ungültige E-Mail oder Passwort.")
            except Exception as e:
                st.error(f"Ein Fehler ist aufgetreten: {str(e)}")

def register():
    st.markdown("### Neue Klinik registrieren")
    
    with st.form("register_form"):
        name = st.text_input("Klinikname")
        email = st.text_input("E-Mail")
        password = st.text_input("Passwort", type="password")
        confirm_password = st.text_input("Passwort bestätigen", type="password")
        location = st.text_input("Standort")
        
        # Add coordinates selection
        st.markdown("### Standort")
        st.info("Bitte wählen Sie die Klinik aus der Liste oder geben Sie die Koordinaten manuell ein.")
        
        # Hospital selection for coordinates
        selected_hospital = st.selectbox(
            "Klinik auswählen",
            ["Manuelle Eingabe"] + list(HAMBURG_COORDINATES.keys())
        )
        
        if selected_hospital == "Manuelle Eingabe":
            col1, col2 = st.columns(2)
            with col1:
                latitude = st.number_input("Breitengrad", value=53.5503, format="%.4f")
            with col2:
                longitude = st.number_input("Längengrad", value=9.9937, format="%.4f")
        else:
            latitude, longitude = HAMBURG_COORDINATES[selected_hospital]
            st.info(f"Koordinaten für {selected_hospital}: {latitude}, {longitude}")
        
        submitted = st.form_submit_button("Registrieren")
        if submitted:
            if password != confirm_password:
                st.error("Die Passwörter stimmen nicht überein.")
                return
            
            try:
                data_service = DataService()
                hospital = data_service.create_hospital_account(
                    name=name,
                    email=email,
                    password=password,
                    location=location,
                    latitude=latitude,
                    longitude=longitude
                )
                st.success("Registrierung erfolgreich! Bitte melden Sie sich an.")
            except Exception as e:
                st.error(f"Ein Fehler ist aufgetreten: {str(e)}")

# Create tabs for login and register
tab1, tab2 = st.tabs(["Login", "Registrieren"])

with tab1:
    login()

with tab2:
    register() 