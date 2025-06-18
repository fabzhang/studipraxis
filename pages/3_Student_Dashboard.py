import streamlit as st
from frontend.components.match_view import match_view
from backend.services.data_service import DataService
from form_options import INTEREST_FIELDS, PRAXIS_SKILLS, STUDY_YEAR_OPTIONS
#from shared.categories import MEDICAL_SPECIALTIES, MEDICAL_CERTIFICATIONS
from frontend.components.footer import footer
from frontend.components.header import header

st.set_page_config(
    page_title="Student Dashboard - studiPraxis",
    page_icon="🔍"
)

# Add header
header()

# Compatibility helpers for old data formats
def get_year_index(year_value):
    """Handle both string and integer year values for backward compatibility"""
    if isinstance(year_value, int):
        # Map old numeric years (1-6) to positions in the new STUDY_YEAR_OPTIONS
        # This is an approximation - adjust the mapping as needed
        year_mapping = {
            1: 0,  # "Vorklinik - 1. Jahr"
            2: 1,  # "Vorklinik - 2. Jahr"
            3: 2,  # "Klinik - 3. Jahr"
            4: 3,  # "Klinik - 4. Jahr"
            5: 4,  # "Klinik - 5. Jahr"
            6: 5,  # "Praktisches Jahr (PJ)"
        }
        return year_mapping.get(year_value, 0)
    elif year_value in STUDY_YEAR_OPTIONS:
        return STUDY_YEAR_OPTIONS.index(year_value)
    return 0

def get_compatible_defaults(old_values, new_options):
    """Return only the values that exist in the new options list"""
    if not old_values:
        return []
    # Create a set of lowercase option values for case-insensitive matching
    lowercase_options = {opt.lower(): opt for opt in new_options}
    result = []
    
    for val in old_values:
        # Direct match
        if val in new_options:
            result.append(val)
        # Case-insensitive match
        elif val.lower() in lowercase_options:
            result.append(lowercase_options[val.lower()])
        # Skip values that don't exist in new options
    
    return result

# Check if user is logged in
if 'student_id' in st.session_state and st.session_state.student_id:
    data_service = DataService()
    
    # Get applied and saved positions
    applied_matches = data_service.get_applied_positions_for_student(st.session_state.student_id)
    saved_matches = data_service.get_saved_positions_for_student(st.session_state.student_id)
    
    # Get current student profile
    student = data_service.get_student(st.session_state.student_id)
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Alle Positionen", "Bewerbungen", "Gespeicherte Positionen", "Mein Profil", "Informationen für Studierende"])
    
    with tab1:
        st.markdown("### Alle Positionen")
        match_view()
    
    with tab2:
        st.markdown("### Meine Bewerbungen")
        if not applied_matches:
            st.info("Sie haben sich noch auf keine Positionen beworben.")
        else:
            for match in applied_matches:
                position = data_service.get_position(match.position_id)
                if position:
                    hospital = data_service.get_hospital(position.hospital_id)
                    if hospital:
                        with st.expander(f"{position.title} - {hospital.name}"):
                            st.markdown(f"**Hospital:** {hospital.name}")
                            st.markdown(f"**Department:** {position.department}")
                            st.markdown(f"**Location:** {hospital.location}")
                            st.markdown(f"**Description:** {position.description}")
                            st.markdown(f"**Requirements:** {', '.join(position.requirements)}")
                            if position.stipend:
                                if position.stipend == "Bezahlung nach Tarifvertrag":
                                    st.markdown(f"💰 {position.stipend}")
                                else:
                                    st.markdown(f"💰 {position.stipend}€/Stunde")
                            
                            # Add action buttons
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("Bewerbung zurückziehen", key=f"unapply_{match.id}"):
                                    data_service.update_match_status(match.id, 'saved')
                                    st.success("Bewerbung zurückgezogen!")
                                    st.rerun()
                            with col2:
                                if st.button("Position speichern", key=f"save_from_applied_{match.id}"):
                                    data_service.update_match_status(match.id, 'saved')
                                    st.success("Position erfolgreich gespeichert!")
                                    st.rerun()
    
    with tab3:
        st.markdown("### Gespeicherte Positionen")
        if not saved_matches:
            st.info("Sie haben noch keine Positionen gespeichert.")
        else:
            for match in saved_matches:
                position = data_service.get_position(match.position_id)
                if position:
                    hospital = data_service.get_hospital(position.hospital_id)
                    if hospital:
                        with st.expander(f"{position.title} - {hospital.name}"):
                            st.markdown(f"**Hospital:** {hospital.name}")
                            st.markdown(f"**Department:** {position.department}")
                            st.markdown(f"**Location:** {hospital.location}")
                            st.markdown(f"**Description:** {position.description}")
                            st.markdown(f"**Requirements:** {', '.join(position.requirements)}")
                            if position.stipend:
                                if position.stipend == "Bezahlung nach Tarifvertrag":
                                    st.markdown(f"💰 {position.stipend}")
                                else:
                                    st.markdown(f"💰 {position.stipend}€/Stunde")
                            
                            # Add action buttons
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("Jetzt bewerben", key=f"apply_saved_{match.id}"):
                                    data_service.update_match_status(match.id, 'applied')
                                    st.success("Bewerbung erfolgreich eingereicht!")
                                    st.rerun()
                            with col2:
                                if st.button("Aus gespeicherten entfernen", key=f"unsave_{match.id}"):
                                    data_service.delete_match(match.id)
                                    st.success("Position aus gespeicherten entfernt!")
                                    st.rerun()
    
    with tab4:
        st.markdown("### Mein Profil")
        if student:
            logout_placeholder = st.empty()
            if logout_placeholder.button("🚪 Logout", use_container_width=True):
                if st.session_state.get("confirm_logout"):
                    # Actually log out
                    st.session_state.clear()
                    st.switch_page("pages/9_Student_Login.py")
                else:
                    st.session_state.confirm_logout = True
                    st.warning("Sind Sie sicher, dass Sie sich abmelden möchten? Klicken Sie erneut auf 'Logout' zum Bestätigen.")
            else:
                st.session_state.confirm_logout = False
                
            # Display the year properly, handling both string and int formats
            display_year = student.year
            if isinstance(student.year, int) and 1 <= student.year <= 6:
                # Map old numeric years to appropriate display text
                year_map = {
                    1: "Vorklinik - 1. Jahr",
                    2: "Vorklinik - 2. Jahr",
                    3: "Klinik - 3. Jahr",
                    4: "Klinik - 4. Jahr",
                    5: "Klinik - 5. Jahr",
                    6: "Praktisches Jahr (PJ)"
                }
                display_year = year_map.get(student.year, f"Jahr {student.year}")
                
            st.markdown(f"# Medical Student - {display_year}")
            st.markdown(f"**Name:** {student.name}")
            st.markdown("**Interests:**")
            for interest in student.interests:
                st.markdown(f"- {interest}")
            st.markdown("**Praxiserfahrungen:**")
            st.markdown(student.praxiserfahrungen if hasattr(student, 'praxiserfahrungen') else "Keine Angabe")
            st.markdown("**Certifications:**")
            if student.certifications:
                for cert in student.certifications:
                    st.markdown(f"- {cert}")
            else:
                st.markdown("Keine Zertifizierungen angegeben.")
            # Edit profile form
            with st.expander("Profil bearbeiten"):
                with st.form("edit_profile_form"):
                    new_name = st.text_input("Name", value=student.name)
                    
                    # Handle year selection, with backward compatibility
                    year_index = get_year_index(student.year)
                    new_year = st.selectbox("Studienjahr", STUDY_YEAR_OPTIONS, index=year_index)
                    
                    # Filter interests for compatibility with new options
                    compatible_interests = get_compatible_defaults(student.interests, INTEREST_FIELDS)
                    
                    # For older profiles, also show the old options as a fallback
                    if len(compatible_interests) < len(student.interests):
                        st.warning("Einige Ihrer alten Fachinteressen entsprechen nicht den neuen Optionen. " 
                                 "Bitte wählen Sie neue Optionen aus der Liste.")
                    
                    new_interests = st.multiselect(
                        "Fachinteressen", 
                        options=INTEREST_FIELDS, 
                        default=compatible_interests
                    )
                    
                    # Replace availability with praxiserfahrungen
                    st.markdown("#### Praxiserfahrungen")
                    st.info("Beschreiben Sie Ihre bisherigen Praxiserfahrungen (z.B. Famulaturen, Praktika, etc.)")
                    new_praxiserfahrungen = st.text_area(
                        "Praxiserfahrungen",
                        value=student.praxiserfahrungen if hasattr(student, 'praxiserfahrungen') else "",
                        help="Beschreiben Sie Ihre bisherigen Praxiserfahrungen im medizinischen Bereich."
                    )
                    
                    # Filter certifications for compatibility with new options
                    compatible_certs = get_compatible_defaults(student.certifications, PRAXIS_SKILLS)
                    
                    # Show warning if there are incompatible certifications
                    if student.certifications and len(compatible_certs) < len(student.certifications):
                        st.warning("Einige Ihrer alten Zertifizierungen entsprechen nicht den neuen Optionen. "
                                 "Bitte wählen Sie neue Optionen aus der Liste.")
                    
                    new_certifications = st.multiselect(
                        "Praxis-Skills/Zertifizierungen", 
                        options=PRAXIS_SKILLS, 
                        default=compatible_certs
                    )
                    
                    submitted = st.form_submit_button("Profil aktualisieren")
                    if submitted:
                        try:
                            # Update student profile
                            student.name = new_name
                            # Always store as string format now
                            student.year = new_year
                            student.interests = new_interests
                            student.praxiserfahrungen = new_praxiserfahrungen
                            student.certifications = new_certifications if new_certifications else None
                            data_service.update_student(student)
                            st.success("Profil erfolgreich aktualisiert!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Ein Fehler ist aufgetreten: {str(e)}")
        else:
            st.error("Studentenprofil nicht gefunden.")
    
    with tab5:
        st.markdown("""
        <div style='margin-top:1em; margin-bottom:1em;'>
        <h3 style='color:#15396b;'>Was bedeutet es, Werkstudent zu sein?</h3>
        <p>Werkstudent*innen sind Studierende, die neben ihrem Studium bei einem Arbeitgeber unter bestimmten Voraussetzungen beschäftigt sind. Die wichtigste Voraussetzung ist, dass dein Schwerpunkt auf deinem Studium bleibt. Dies wird sichergestellt, indem deine Arbeitszeit grundsätzlich auf <b>20 Stunden pro Woche</b> begrenzt ist.</p>
        <p>Es gibt jedoch Ausnahmen, die wir weiter unten erklären.</p>
        <h4>Welche Voraussetzungen musst du mitbringen?</h4>
        <p>Die maximale Anzahl Semester in denen du als Werkstudent*in arbeiten darfst beträgt 25. Außerdem darfst du dich nicht in einem Urlaubssemester befinden.</p>
        <h4>Wie ist die Arbeitszeit geregelt?</h4>
        <p>Als Werkstudent*in gilt grundsätzlich ein wöchentliches Limit von 20 Arbeitsstunden.</p>
        <p>Du darfst diese Grenze jedoch <b>in bis zu 26 Wochen pro Jahr überschreiten</b>, wenn:</p>
        <ul>
            <li>die Mehrarbeit abends, nachts, am Wochenende oder in den Semesterferien erfolgt,</li>
            <li>der Zeitraum im Voraus bekannt ist,</li>
            <li>und innerhalb eines Zeitjahres die 26-Wochen-Grenze eingehalten wird.</li>
        </ul>
        <h4>Warum ein Werkstudentenjob über Studipraxis?</h4>
        <ol>
            <li><b>Praxiserfahrung sammeln – Werde fit für deinen Berufsstart</b>
                <ul>
                    <li>Sicherer Umgang mit Patient*innen</li>
                    <li>Basisfertigkeiten wie Blutabnahmen, Infusionen legen, Anamnesegespräche führen</li>
                    <li>Assistenz im OP und bei Untersuchungen</li>
                    <li>Mitarbeit im Stations- und Praxisbetrieb</li>
                    <li>Verständnis für Teamabläufe in Kliniken und Praxen entwickeln</li>
                </ul>
                <p>Diese Erfahrungen geben dir Sicherheit im späteren Berufsleben und verschaffen dir einen klaren Vorteil bei Bewerbungen für Famulaturen, Hospitationen oder deine Assistenzarztstelle – und natürlich für dein PJ, falls dort keine zentrale Bewerbung erfolgt.</p>
            </li>
            <li><b>Geld verdienen – Studiere sorgenfreier</b>
                <ul>
                    <li>Faire Vergütung durch tarifnahe oder marktgerechte Stundenlöhne</li>
                    <li>Flexible Arbeitszeiten, angepasst an dein Studium</li>
                    <li>Keine Nebenjobs mehr außerhalb deines Fachgebiets</li>
                    <li>Attraktiver Status für Arbeitgeber durch reduzierte Sozialabgaben</li>
                </ul>
                <p>Du arbeitest nicht nur sinnvoll nebenbei, sondern baust aktiv an deiner Zukunft.</p>
            </li>
            <li><b>Krankenversicherung – Sicher abgesichert</b>
                <ul>
                    <li><b>Unter 25 Jahre:</b> Möglichst weiterhin familienversichert, wenn dein Einkommen unter der Geringfügigkeitsgrenze (556 €/Monat, 2025) bleibt</li>
                    <li><b>Über der Geringfügigkeitsgrenze:</b> Günstige werkstudentische Versicherung bei einer Krankenkasse deiner Wahl</li>
                    <li>Reduzierte Abgaben: Keine Beiträge zur Kranken-, Pflege- oder Arbeitslosenversicherung, nur Rentenbeiträge</li>
                    <li>Fester Beitragssatz: Dein Krankenkassenbeitrag bleibt unabhängig von deinem Einkommen konstant</li>
                    <li>Freie Wahl zwischen gesetzlicher und (freiwilliger) privater Krankenversicherung</li>
                    <li>Ab deinem 30. Lebensjahr darfst du zwar weiter als Werkstudent*in arbeiten, musst dich aber Eigenständig im Regeltarif krankenversichern</li>
                </ul>
                <p>So bist du auch finanziell bestens abgesichert – und kannst dich voll auf dein Studium konzentrieren.</p>
            </li>
            <li><b>Netzwerk aufbauen – Kontakte für deine medizinische Karriere</b>
                <ul>
                    <li>Knüpfe früh Kontakte zu Ärzt:innen, Praxisinhaber:innen und Klinikleitungen</li>
                    <li>Sichere dir Empfehlungsschreiben und Kontakte für später</li>
                    <li>Stärke dein berufliches Profil durch positive praktische Erfahrungen</li>
                </ul>
                <p>Ein gutes Netzwerk öffnet dir viele Wege für deine Karriere.</p>
            </li>
            <li><b>Spaß haben – Medizin erleben, bevor es richtig losgeht</b>
                <ul>
                    <li>Setze dein Wissen in der Praxis um</li>
                    <li>Erlebe Teamarbeit und echte Erfolge im Alltag</li>
                    <li>Motiviere dich durch Erfahrungen, die dich durch Prüfungszeiten tragen</li>
                </ul>
            </li>
        </ol>
        <p style='font-weight:bold; color:#15396b;'>Medizin erleben statt nur lernen – das ist Studipraxis.</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("### Alle Positionen")
    match_view() 

# Add footer at the bottom
footer() 