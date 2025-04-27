import streamlit as st
from backend.services.data_service import DataService

st.set_page_config(
    page_title="Student Login - studiPraxis",
    page_icon="🔐"
)

st.markdown("### Student Login")

# Initialize session state for student
if 'student_id' not in st.session_state:
    st.session_state.student_id = None

def login():
    data_service = DataService()
    
    with st.form("login_form"):
        email = st.text_input("E-Mail")
        password = st.text_input("Passwort", type="password")
        
        submitted = st.form_submit_button("Anmelden")
        if submitted:
            try:
                student = data_service.authenticate_student(email, password)
                if student:
                    st.session_state.student_id = student.id
                    st.success("Login erfolgreich!")
                    st.switch_page("pages/3_Positionen.py")
                else:
                    st.error("Ungültige E-Mail oder Passwort.")
            except Exception as e:
                st.error(f"Ein Fehler ist aufgetreten: {str(e)}")

def register():
    st.markdown("### Neues Studentenprofil erstellen")
    
    with st.form("register_form"):
        name = st.text_input("Name")
        email = st.text_input("E-Mail")
        password = st.text_input("Passwort", type="password")
        confirm_password = st.text_input("Passwort bestätigen", type="password")
        year = st.selectbox("Studienjahr", ["1", "2", "3", "4", "5", "6"])
        interests = st.text_area("Interessengebiete (eine pro Zeile)")
        availability = st.text_input("Verfügbarkeit (z.B. Sommer 2025)")
        certifications = st.text_area("Zertifizierungen (optional, eine pro Zeile)")
        
        submitted = st.form_submit_button("Registrieren")
        if submitted:
            if password != confirm_password:
                st.error("Die Passwörter stimmen nicht überein.")
                return
            
            try:
                # Convert interests and certifications to lists
                interests_list = [i.strip() for i in interests.split("\n") if i.strip()]
                certifications_list = [c.strip() for c in certifications.split("\n") if c.strip()]
                
                data_service = DataService()
                student = data_service.create_student_account(
                    name=name,
                    email=email,
                    password=password,
                    year=int(year),
                    interests=interests_list,
                    availability=availability,
                    certifications=certifications_list if certifications_list else None
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