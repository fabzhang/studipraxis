import streamlit as st
from backend.services.data_service import DataService
from form_options import LANGUAGE_OPTIONS, UNIVERSITY_OPTIONS, INTEREST_FIELDS, PRAXIS_SKILLS, STUDY_YEAR_OPTIONS

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
                    st.switch_page("pages/3_Student_Dashboard.py")
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
        year = st.selectbox("Studienjahr", STUDY_YEAR_OPTIONS)
        
        # Language selection
        language = st.multiselect(
            "Sprachen",
            options=LANGUAGE_OPTIONS,
            help="Wählen Sie die Sprachen, die Sie sprechen."
        )
        # University selection
        university = st.selectbox(
            "Universität",
            options=[u["name"] for u in UNIVERSITY_OPTIONS],
            help="Wählen Sie Ihre Universität."
        )
        # Use multiselect for specialty interests
        st.markdown("#### Fachinteressen")
        st.info("Wählen Sie Ihre Fachinteressen aus der Liste aus. Sie können mehrere auswählen.")
        interests = st.multiselect(
            "Fachinteressen",
            options=INTEREST_FIELDS,
            help="Wählen Sie die Fachgebiete, die Sie interessieren."
        )
        
        # Replace availability with praxiserfahrungen
        st.markdown("#### Praxiserfahrungen")
        st.info("Beschreiben Sie Ihre bisherigen Praxiserfahrungen (z.B. Famulaturen, Praktika, etc.)")
        praxiserfahrungen = st.text_area(
            "Praxiserfahrungen",
            help="Beschreiben Sie Ihre bisherigen Praxiserfahrungen im medizinischen Bereich."
        )
        
        # Use multiselect for certifications/skills
        st.markdown("#### Praxis-Skills/Zertifizierungen")
        st.info("Wählen Sie Ihre Praxis-Skills und Zertifizierungen aus der Liste aus. Sie können mehrere auswählen.")
        certifications = st.multiselect(
            "Praxis-Skills/Zertifizierungen",
            options=PRAXIS_SKILLS,
            help="Wählen Sie die Skills/Zertifizierungen, die Sie besitzen."
        )
        
        submitted = st.form_submit_button("Registrieren")
        if submitted:
            if password != confirm_password:
                st.error("Die Passwörter stimmen nicht überein.")
                return
            # Store form data for preview
            st.session_state.new_student = {
                "name": name,
                "email": email,
                "password": password,
                "year": year,
                "language": language,
                "university": university,
                "interests": interests,
                "praxiserfahrungen": praxiserfahrungen,
                "certifications": certifications
            }
            st.session_state.show_student_preview = True
            st.rerun()

    # Show preview and confirm step
    if st.session_state.get("show_student_preview") and 'new_student' in st.session_state:
        st.markdown("---")
        st.markdown(f"# Medical Student - Year {st.session_state.new_student['year']}")
        st.markdown(f"**Name:** {st.session_state.new_student['name']}")
        st.markdown(f"**Universität:** {st.session_state.new_student['university']}")
        st.markdown(f"**Sprachen:** {', '.join(st.session_state.new_student['language']) if st.session_state.new_student['language'] else 'Keine Angabe'}")
        st.markdown("**Fachinteressen:**")
        for interest in st.session_state.new_student['interests']:
            st.markdown(f"- {interest}")
        st.markdown("**Praxiserfahrungen:**")
        st.markdown(st.session_state.new_student['praxiserfahrungen'])
        st.markdown("**Praxis-Skills/Zertifizierungen:**")
        for cert in st.session_state.new_student['certifications']:
            st.markdown(f"- {cert}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Bestätigen und registrieren", key="confirm_register_student"):
                try:
                    data_service = DataService()
                    student = data_service.create_student_account(
                        name=st.session_state.new_student['name'],
                        email=st.session_state.new_student['email'],
                        password=st.session_state.new_student['password'],
                        year=st.session_state.new_student['year'],
                        interests=st.session_state.new_student['interests'],
                        praxiserfahrungen=st.session_state.new_student['praxiserfahrungen'],
                        certifications=st.session_state.new_student['certifications'] if st.session_state.new_student['certifications'] else None
                    )
                    st.success("Registrierung erfolgreich! Bitte melden Sie sich an.")
                    del st.session_state.new_student
                    st.session_state.show_student_preview = False
                except Exception as e:
                    st.error(f"Ein Fehler ist aufgetreten: {str(e)}")
        with col2:
            if st.button("Abbrechen", key="cancel_register_student"):
                del st.session_state.new_student
                st.session_state.show_student_preview = False
                st.rerun()

# Create tabs for login and registration
tab1, tab2 = st.tabs(["Anmelden", "Registrieren"])

with tab1:
    login()

with tab2:
    register() 