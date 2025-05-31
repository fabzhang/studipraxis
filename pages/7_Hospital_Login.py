import streamlit as st
from backend.services.data_service import DataService
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError
import time

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

# List of Hamburg hospitals with addresses
HAMBURG_HOSPITALS = [
    {"name": "Universitätsklinikum Hamburg-Eppendorf (UKE)", "address": "Martinistraße 52, 20246 Hamburg"},
    {"name": "Asklepios Klinik Altona", "address": "Paul-Ehrlich-Straße 1, 22763 Hamburg"},
    {"name": "Asklepios Klinik Barmbek", "address": "Rübenkamp 220, 22307 Hamburg"},
    {"name": "Asklepios Klinik Harburg", "address": "Eißendorfer Pferdeweg 52, 21075 Hamburg"},
    {"name": "Asklepios Klinik St. Georg", "address": "Lohmühlenstraße 5, 20099 Hamburg"},
    {"name": "Asklepios Klinik Wandsbek", "address": "Alphonsstraße 14, 22043 Hamburg"},
    {"name": "Asklepios Klinik Nord – Heidberg", "address": "Tangstedter Landstraße 400, 22417 Hamburg"},
    {"name": "Asklepios Klinik Nord – Ochsenzoll", "address": "Langenhorner Chaussee 560, 22419 Hamburg"},
    {"name": "HELIOS ENDO-Klinik Hamburg", "address": "Holstenstraße 2, 22767 Hamburg"},
    {"name": "HELIOS Mariahilf Klinik Hamburg", "address": "Stader Straße 203c, 21075 Hamburg"},
    {"name": "Israelitisches Krankenhaus Hamburg", "address": "Orchideenstieg 14, 22297 Hamburg"},
    {"name": "Katholisches Kinderkrankenhaus Wilhelmstift", "address": "Liliencronstraße 130, 22149 Hamburg"},
    {"name": "Kath. Marienkrankenhaus Hamburg", "address": "Alfredstraße 9, 22087 Hamburg"},
    {"name": "Evangelisches Krankenhaus Alsterdorf", "address": "Elisabeth-Flügge-Straße 1, 22337 Hamburg"},
    {"name": "Ev. Amalie Sieveking Krankenhaus", "address": "Haselkamp 33, 22359 Hamburg"},
    {"name": "Krankenhaus Jerusalem", "address": "Moorkamp 2–6, 20357 Hamburg"},
    {"name": "Facharztklinik Hamburg", "address": "Martinistraße 78, 20251 Hamburg"},
    {"name": "Schön Klinik Hamburg Eilbek", "address": "Dehnhaide 120, 22081 Hamburg"},
    {"name": "Krankenhaus Tabea", "address": "Kösterbergstraße 32, 22587 Hamburg"},
    {"name": "Bundeswehrkrankenhaus Hamburg", "address": "Lesserstraße 180, 22049 Hamburg"}
]

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

def get_coordinates(address, max_retries=3, timeout=10):
    """
    Get coordinates for an address using Nominatim with retries and better error handling.
    
    Args:
        address (str): The address to geocode
        max_retries (int): Maximum number of retry attempts
        timeout (int): Timeout in seconds for each request
    
    Returns:
        tuple: (latitude, longitude) or None if geocoding fails
    """
    geolocator = Nominatim(
        user_agent="studipraxis",
        timeout=timeout
    )
    
    for attempt in range(max_retries):
        try:
            location = geolocator.geocode(address)
            if location:
                return location.latitude, location.longitude
            
            # If no location found, try with "Hamburg, Germany" appended
            if "Hamburg" not in address:
                location = geolocator.geocode(f"{address}, Hamburg, Germany")
                if location:
                    return location.latitude, location.longitude
            
            st.warning(f"Adresse nicht gefunden (Versuch {attempt + 1}/{max_retries})")
            time.sleep(1)  # Wait 1 second between retries
            
        except (GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError) as e:
            st.warning(f"Geocoding-Fehler (Versuch {attempt + 1}/{max_retries}): {str(e)}")
            time.sleep(1)  # Wait 1 second between retries
            
        except Exception as e:
            st.error(f"Unerwarteter Fehler bei der Geocodierung: {str(e)}")
            return None
    
    st.error("Die Adresse konnte nach mehreren Versuchen nicht in Koordinaten umgewandelt werden.")
    return None

def register():
    st.markdown("### Neue Klinik registrieren")
    
    with st.form("register_form"):
        name = st.text_input("Klinikname")
        email = st.text_input("E-Mail")
        password = st.text_input("Passwort", type="password")
        confirm_password = st.text_input("Passwort bestätigen", type="password")
        
        # Add hospital selection
        st.markdown("### Standort")
        st.info("Bitte wählen Sie die Klinik aus der Liste oder geben Sie eine neue Adresse ein.")
        
        # Hospital selection
        selected_hospital = st.selectbox(
            "Klinik auswählen",
            ["Manuelle Eingabe"] + [h["name"] for h in HAMBURG_HOSPITALS]
        )
        
        if selected_hospital == "Manuelle Eingabe":
            location = st.text_input("Adresse eingeben")
        else:
            # Get the address for the selected hospital
            hospital = next((h for h in HAMBURG_HOSPITALS if h["name"] == selected_hospital), None)
            location = hospital["address"]
            st.info(f"Adresse: {location}")
        
        submitted = st.form_submit_button("Registrieren")
        if submitted:
            if password != confirm_password:
                st.error("Die Passwörter stimmen nicht überein.")
                return
            
            # Get coordinates for the address
            coordinates = get_coordinates(location)
            if not coordinates:
                st.error("Die Adresse konnte nicht in Koordinaten umgewandelt werden. Bitte überprüfen Sie die Adresse.")
                return
            
            latitude, longitude = coordinates
            
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