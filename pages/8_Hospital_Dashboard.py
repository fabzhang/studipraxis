import streamlit as st
from backend.services.data_service import DataService
from shared.types import Position
from form_options import INTEREST_FIELDS, PRAXIS_SKILLS, STUDY_YEAR_OPTIONS
from datetime import datetime
from shared.utils import generate_mailto_link

st.set_page_config(
    page_title="Klinik Dashboard - studiPraxis",
    page_icon="🏥"
)

# Check if user is logged in
if 'hospital_id' not in st.session_state or not st.session_state.hospital_id:
    st.error("Bitte melden Sie sich an, um auf das Dashboard zuzugreifen.")
    st.stop()

# Initialize data service
data_service = DataService()

# Get hospital profile
hospital = data_service.get_hospital(st.session_state.hospital_id)
if not hospital:
    st.error("Klinik nicht gefunden.")
    st.stop()

st.markdown(f"### Willkommen, {hospital.name}!")

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["Positionen verwalten", "Bewerbungen", "Profil", "Informationen für Arbeitgeber"])

with tab1:
    st.markdown("#### Positionen verwalten")
    
    # Add new position form
    with st.expander("Neue Position hinzufügen"):
        with st.form("new_position_form"):
            # Use selectbox for department (using INTEREST_FIELDS)
            st.markdown("#### Abteilung")
            st.info("Wählen Sie die Abteilung aus der Liste aus.")
            department = st.selectbox(
                "Abteilung",
                options=INTEREST_FIELDS,
                help="Wählen Sie die Abteilung für die Position."
            )
            
            title = st.text_input("Positionstitel")
            description = st.text_area("Beschreibung")
            
            # Use multiselect for requirements (using PRAXIS_SKILLS)
            st.markdown("#### Anforderungen")
            st.info("Wählen Sie die erforderlichen Praxis-Skills aus der Liste aus.")
            requirements = st.multiselect(
                "Anforderungen",
                options=PRAXIS_SKILLS,
                help="Wählen Sie die erforderlichen Praxis-Skills für die Position."
            )
            
            # Add minimum study year requirement
            st.markdown("#### Mindeststudienjahr")
            st.info("Wählen Sie das erforderliche Mindeststudienjahr aus.")
            min_year = st.selectbox(
                "Mindeststudienjahr",
                options=STUDY_YEAR_OPTIONS,
                help="Wählen Sie das erforderliche Mindeststudienjahr für die Position."
            )
            
            stipend = st.text_input(
                "Vergütung",
                value="Bezahlung nach Tarifvertrag",
                help="Geben Sie 'Bezahlung nach Tarifvertrag' ein oder einen Stundenlohn in Euro (z.B. '15')"
            )
            
            submitted = st.form_submit_button("Position hinzufügen")
            if submitted:
                st.session_state.new_position = {
                    "department": department,
                    "title": title,
                    "description": description,
                    "requirements": requirements,
                    "min_year": min_year,
                    "stipend": stipend
                }
                st.session_state.show_modal = True
                st.rerun()

    # Inline preview fallback if modal is not available
    if st.session_state.get("show_modal") and 'new_position' in st.session_state:
        st.markdown("---")
        st.markdown("## Vorschau der neuen Position")
        pos = st.session_state.new_position
        # Header row
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.markdown(f"### {pos['title']}")
            st.markdown(f"🏥 {hospital.name}")
        with col2:
            st.markdown(f"**Abteilung:** {pos['department']}")
            st.markdown(f"**Mindeststudienjahr:** {pos['min_year']}")
        with col3:
            if pos['stipend']:
                if pos['stipend'] == "Bezahlung nach Tarifvertrag":
                    st.markdown(f"💰 {pos['stipend']}")
                else:
                    st.markdown(f"💰 {pos['stipend']}€/Stunde")
        st.markdown("---")
        # Details section
        st.markdown("#### Position Details")
        detail_col1, detail_col2 = st.columns(2)
        with detail_col1:
            st.markdown("##### Standort")
            st.markdown(f"📍 {hospital.location}")
            st.markdown("##### Beschreibung")
            st.markdown(pos['description'])
        with detail_col2:
            st.markdown("##### Anforderungen")
            for req in pos['requirements']:
                st.markdown(f"- {req}")
            if pos['stipend']:
                st.markdown("##### Vergütung")
                st.markdown(f"💰 {pos['stipend']}€ pro Monat")
        # Confirmation buttons at the bottom
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Bestätigen und hinzufügen", key="confirm_add_position"):
                try:
                    position = Position(
                        id="",  # Will be generated by service
                        hospital_id=hospital.id,
                        department=pos['department'],
                        title=pos['title'],
                        description=pos['description'],
                        requirements=pos['requirements'],
                        min_year=pos['min_year'],
                        stipend=pos['stipend'],
                        created_at=None,  # Will be set by service
                        updated_at=None   # Will be set by service
                    )
                    data_service.create_position(position)
                    st.success("Position erfolgreich hinzugefügt!")
                    del st.session_state.new_position
                    st.session_state.show_modal = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Ein Fehler ist aufgetreten: {str(e)}")
        with col2:
            if st.button("Abbrechen", key="cancel_add_position"):
                del st.session_state.new_position
                st.session_state.show_modal = False
                st.rerun()
    
    # List existing positions
    st.markdown("#### Aktuelle Positionen")
    positions = data_service.get_positions(hospital.id)
    
    if not positions:
        st.info("Noch keine Positionen vorhanden.")
    else:
        for position in positions:
            with st.expander(f"{position.title} - {position.department}"):
                # Show edit form if this position is being edited
                if st.session_state.get("editing_position") == position.id:
                    with st.form(f"edit_position_form_{position.id}"):
                        st.markdown("#### Position bearbeiten")
                        
                        # Department selection
                        new_department = st.selectbox(
                            "Abteilung",
                            options=INTEREST_FIELDS,
                            index=INTEREST_FIELDS.index(position.department) if position.department in INTEREST_FIELDS else 0,
                            help="Wählen Sie die Abteilung für die Position."
                        )
                        
                        # Title and description
                        new_title = st.text_input("Positionstitel", value=position.title)
                        new_description = st.text_area("Beschreibung", value=position.description)
                        
                        # Requirements - filter out any requirements that are not in PRAXIS_SKILLS
                        valid_requirements = [req for req in position.requirements if req in PRAXIS_SKILLS]
                        new_requirements = st.multiselect(
                            "Anforderungen",
                            options=PRAXIS_SKILLS,
                            default=valid_requirements,
                            help="Wählen Sie die erforderlichen Praxis-Skills für die Position."
                        )
                        
                        # Minimum year
                        new_min_year = st.selectbox(
                            "Mindeststudienjahr",
                            options=STUDY_YEAR_OPTIONS,
                            index=STUDY_YEAR_OPTIONS.index(position.min_year) if position.min_year in STUDY_YEAR_OPTIONS else 0,
                            help="Wählen Sie das erforderliche Mindeststudienjahr für die Position."
                        )
                        
                        # Stipend
                        new_stipend = st.text_input(
                            "Vergütung",
                            value=position.stipend,
                            help="Geben Sie 'Bezahlung nach Tarifvertrag' ein oder einen Stundenlohn in Euro (z.B. '15')"
                        )
                        
                        # Form buttons
                        col1, col2 = st.columns(2)
                        with col1:
                            save_button = st.form_submit_button("Änderungen speichern")
                        with col2:
                            cancel_button = st.form_submit_button("Abbrechen")
                        
                        if save_button:
                            try:
                                updated_position = Position(
                                    id=position.id,
                                    hospital_id=position.hospital_id,
                                    department=new_department,
                                    title=new_title,
                                    description=new_description,
                                    requirements=new_requirements,
                                    min_year=new_min_year,
                                    stipend=new_stipend,
                                    created_at=position.created_at,
                                    updated_at=datetime.now()
                                )
                                data_service.update_position(updated_position)
                                st.success("Position erfolgreich aktualisiert!")
                                del st.session_state.editing_position
                                st.rerun()
                            except Exception as e:
                                st.error(f"Ein Fehler ist aufgetreten: {str(e)}")
                        
                        if cancel_button:
                            del st.session_state.editing_position
                            st.rerun()
                else:
                    # Display position details
                    st.markdown(f"**Beschreibung:** {position.description}")
                    st.markdown(f"**Mindeststudienjahr:** {position.min_year}")
                    if position.stipend:
                        if position.stipend == "Bezahlung nach Tarifvertrag":
                            st.markdown(f"**Vergütung:** {position.stipend}")
                        else:
                            st.markdown(f"**Vergütung:** {position.stipend}€/Stunde")
                    st.markdown("**Anforderungen:**")
                    for req in position.requirements:
                        st.markdown(f"- {req}")
                    
                    # Edit and delete buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Bearbeiten", key=f"edit_{position.id}"):
                            st.session_state.editing_position = position.id
                            st.rerun()
                    with col2:
                        if st.button("Löschen", key=f"delete_{position.id}"):
                            if st.session_state.get(f"confirm_delete_{position.id}"):
                                data_service.delete_position(position.id)
                                st.success("Position gelöscht!")
                                st.rerun()
                            else:
                                st.session_state[f"confirm_delete_{position.id}"] = True
                                st.warning("Klicken Sie erneut auf 'Löschen' um zu bestätigen.")

with tab2:
    st.markdown("#### Bewerbungen")
    
    # Get all positions with applications
    positions = data_service.get_positions(hospital.id)
    has_applications = False
    
    for position in positions:
        applications = data_service.get_applications_for_position(position.id)
        if applications:
            has_applications = True
            st.markdown(f"### {position.title} - {position.department}")
            st.markdown(f"**Anzahl Bewerbungen:** {len(applications)}")
            
            for application in applications:
                student = data_service.get_student(application.student_id)
                if student:
                    with st.expander(f"Bewerbung von {student.name}"):
                        st.markdown(f"**Name:** {student.name}")
                        st.markdown(f"**Studienjahr:** {student.year}")
                        st.markdown(f"**Verfügbarkeit:** {student.availability}")
                        st.markdown("**Interessen:**")
                        for interest in student.interests:
                            st.markdown(f"- {interest}")
                        if student.certifications:
                            st.markdown("**Zertifizierungen:**")
                            for cert in student.certifications:
                                st.markdown(f"- {cert}")
                        
                        # Application actions
                        col1, col2 = st.columns(2)
                        with col1:
                            # Generate mailto link for contacting the student
                            subject = f"Bewerbung bei {hospital.name} - {position.title}"
                            body = f"""Hallo {student.name},

vielen Dank für Ihr Interesse an der Position "{position.title}" in unserer Einrichtung.

Wir würden uns freuen, mit Ihnen in Kontakt zu treten und mehr über Ihre Erfahrungen und Motivation zu erfahren.

Mit freundlichen Grüßen
{hospital.name}"""
                            
                            mailto_link = generate_mailto_link(student.email, subject, body)
                            if st.button("📧 Kontakt aufnehmen", key=f"contact_{application.id}"):
                                st.markdown(f'<a href="{mailto_link}" target="_blank">E-Mail öffnen</a>', unsafe_allow_html=True)
                        with col2:
                            if st.button("Ablehnen", key=f"reject_{application.id}"):
                                data_service.update_match_status(application.id, 'rejected')
                                st.success("Bewerbung abgelehnt!")
                                st.rerun()
    
    if not has_applications:
        st.info("Noch keine Bewerbungen vorhanden.")

with tab3:
    st.markdown("#### Profil")
    logout_placeholder = st.empty()
    if logout_placeholder.button("🚪 Logout", use_container_width=True):
        if st.session_state.get("confirm_logout_hospital"):
            st.session_state.clear()
            st.switch_page("pages/7_Hospital_Login.py")
        else:
            st.session_state.confirm_logout_hospital = True
            st.warning("Sind Sie sicher, dass Sie sich abmelden möchten? Klicken Sie erneut auf 'Logout' zum Bestätigen.")
    else:
        st.session_state.confirm_logout_hospital = False
    st.markdown(f"**Name:** {hospital.name}")
    st.markdown(f"**E-Mail:** {hospital.email}")
    st.markdown(f"**Standort:** {hospital.location}")
    
    # Edit profile form
    with st.expander("Profil bearbeiten"):
        with st.form("edit_profile_form"):
            new_name = st.text_input("Neuer Name", value=hospital.name)
            new_location = st.text_input("Neuer Standort", value=hospital.location)
            
            submitted = st.form_submit_button("Profil aktualisieren")
            if submitted:
                try:
                    data_service.update_hospital(
                        hospital.id,
                        name=new_name,
                        location=new_location
                    )
                    st.success("Profil erfolgreich aktualisiert!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Ein Fehler ist aufgetreten: {str(e)}")

with tab4:

    st.markdown("**[Jetzt kostenlos registrieren und ein Stellenangebot aufgeben]**")

    st.markdown("""
    ### Ihre Vorteile auf einen Blick
    - **Fachlich interessiert:** Medizinstudent:innen bringen Grundverständnis und hohe Motivation mit – perfekt für unterstützende Tätigkeiten im Alltag.
    - **Flexibel einsetzbar:** Ob zur Urlaubsvertretung, in Stoßzeiten oder für einfache medizinische Aufgaben – Werkstudierende entlasten Ihr Personal.
    - **Rechtlich abgesichert:** Der Werkstudentenstatus ist klar geregelt: Günstige Abgaben für Sie – und volle Sicherheit für beide Seiten.
    """)

    st.markdown("""
    ### Was Medizinstudierende in Ihrer Einrichtung übernehmen können
    - Patientenaufnahme und -betreuung
    - Blutabnahmen, Infusionen und Injektionen (nach Einarbeitung)
    - Unterstützung bei der Dokumentation und administrativen Aufgaben
    - Assistenz bei Untersuchungen und OP-Vorbereitungen
    - Assistenz im OP
    - Mitarbeit in der Notaufnahme / ZNA bei der Ersteinschätzung von Patient:innen
    - Mithilfe in Funktionsbereichen (z. B. EKG, Labor, Sprechstundenassistenz)
    - Telefon- und Empfangstätigkeiten
    - Pflegerische Maßnahmen
    - Nachtwachen
    
    *CAVE: Alle Einsätze erfolgen im Rahmen der Vorerfahrung und unter ärztlicher oder fachlicher Anleitung und Supervision.*
    """)

    st.markdown("""
    ### So funktioniert's – in 3 Schritten
    1. **Kostenfrei registrieren:** Erstellen Sie ein Arbeitgeberprofil – in wenigen Minuten.
    2. **Stellenanzeige veröffentlichen:** Beschreiben Sie, wen Sie suchen und wann Sie Unterstützung brauchen.
    3. **Bewerbungen erhalten oder aktiv selber suchen:** Medizinstudierende bewerben sich direkt – oder Sie finden passende Profile über die Plattform.
    """)

    st.markdown("""
    ### Warum Studipraxis für Ihre Einrichtung?
    - ✔️ Zugriff auf motivierten medizinischen Nachwuchs
    - ✔️ Entlastung für Ihr Team – besonders bei Personalengpässen
    - ✔️ Schnelle, unkomplizierte Abwicklung
    - ✔️ Plattform speziell für Medizinstudierende
    - ✔️ Nur verifizierte Nutzer:innen
    - ✔️ 100 % DSGVO-konform
    """)

    st.markdown("**Bereit für Unterstützung durch motivierte Studierende?**\n\nStarten Sie jetzt und veröffentlichen Sie Ihre erste Stellenanzeige – kostenlos.\n\n**[Jetzt Arbeitgeberprofil erstellen]**")

    st.markdown("---")
    st.markdown("## Häufig gestellte Fragen (FAQ) für Arbeitgeber")

    with st.expander("Was genau ist ein Werkstudent bzw. eine Werkstudentin?"):
        st.markdown("""
        Werkstudent:innen sind immatrikulierte Studierende, die neben dem Studium in Teilzeit bei einem Arbeitgeber arbeiten. Wichtig ist: **Das Studium bleibt der Hauptfokus** – deshalb dürfen Werkstudent:innen in der Regel nicht mehr als 20 Stunden pro Woche während der Vorlesungszeit arbeiten.

        Diese Form der Anstellung ist rechtlich klar geregelt und bietet **Vorteile für beide Seiten**:
        - Studierende gewinnen praktische Erfahrung in ihrem Fachgebiet.
        - Arbeitgeber profitieren von motivierter Unterstützung – bei gleichzeitig geringeren Sozialabgaben.
        """)
    with st.expander("Wie viele Stunden dürfen Werkstudent:innen pro Woche arbeiten?"):
        st.markdown("""
        Grundsätzlich gilt:

        **Max. 20 Stunden pro Woche während der Vorlesungszeit.**

        Aber: Es gibt **Ausnahmen**, die besonders im medizinischen Bereich relevant sind. In **bis zu 26 Wochen pro Jahr** dürfen Werkstudent:innen auch **mehr als 20 Stunden pro Woche arbeiten**, **wenn**:
        - die Mehrarbeit außerhalb der Vorlesungszeit (abends, nachts, Wochenende oder in den Semesterferien) stattfindet,
        - der Zeitraum vorher absehbar ist,
        - die Jahresarbeitszeitregel eingehalten wird.

        Das bedeutet für Sie: **Flexible Einsatzplanung ist möglich – auch über das 20-Stunden-Limit hinaus**, wenn die Rahmenbedingungen stimmen.
        """)
    with st.expander("Welche Aufgaben dürfen Werkstudent:innen übernehmen?"):
        st.markdown("""
        Medizinstudierende dürfen alle Aufgaben übernehmen, die ihrem Kenntnisstand und Ausbildungsstand entsprechen – z. B.:
        - Patientenkontakt (z. B. Aufnahme, Betreuung)
        - Blutabnahmen, Infusionen, einfache technische Tätigkeiten (nach Einarbeitung)
        - Dokumentationshilfe, administrative Abläufe
        - Assistenz im OP oder bei Untersuchungen
        - Unterstützung in der Notaufnahme (z. B. Ersteinschätzung, administrative Entlastung)
        - Pflegerische Maßnahmen
        - Nachtwachen
        
        Sie ergänzen Ihr Team sinnvoll und entlasten bei Routineaufgaben.
        """)
    with st.expander("Welche Lohn- und Versicherungskosten fallen an?"):
        st.markdown("""
        Werkstudent*innen sind in einem **besonderen sozialversicherungsrechtlichen Status**:
        - **Keine Beiträge zur Kranken-, Pflege- und Arbeitslosenversicherung**
        - **Nur Beiträge zur Rentenversicherung (ca. 9,3 % Arbeitgeberanteil)**
        - Geringere Lohnnebenkosten als bei regulären Teilzeitkräften
        - Stundenlohn ist frei verhandelbar aber sollte sich an Berufsgruppen üblichen Tarifen orientieren (i. d. R. 15–20 € je nach Einsatzgebiet und Qualifikation)

        **Fazit:** Werkstudent:innen sind **kosteneffizient einsetzbar**, rechtlich abgesichert – und gleichzeitig hoch motiviert.
        """)
    with st.expander("Wie läuft die Vermittlung über Studipraxis ab?"):
        st.markdown("""
        1. **Kostenlos registrieren**
        2. **Stellenangebot erstellen** – mit Angabe von Einsatzzeit, Aufgaben und Wünschen
        3. **Bewerbungen erhalten** oder passende Kandidat*innen direkt anfragen
        4. **Direkt in Kontakt treten** und Anstellung eigenständig umsetzen

        → Sie behalten die Kontrolle – wir liefern Ihnen den Zugang zu geeigneten Kandidat*innen.
        """)
    with st.expander("Wer kann Studierende anstellen?"):
        st.markdown("""
        Grundsätzlich jede medizinische Einrichtung:
        - Einzel- oder Gemeinschaftspraxen
        - Kliniken und Krankenhäuser
        - MVZs (Medizinische Versorgungszentren)
        - Pflege- und Rehaeinrichtungen
        - Forschungseinrichtungen mit medizinischem Schwerpunkt

        Wichtig ist nur: Die Anstellung erfolgt **im Rahmen einer offiziellen, angemeldeten Werkstudententätigkeit**.
        """)
    with st.expander("Was kostet Studipraxis für Arbeitgeber?"):
        st.markdown("""
        Aktuell ist die Nutzung für Arbeitgeber in der Startphase **kostenfrei**.

        Langfristig planen wir transparente Modelle – z. B. mit Abrechnung für die Stellenangebote oder mit Premium-Optionen für mehr Sichtbarkeit.

        Sie haben also **kein Risiko** – und können die Plattform ganz einfach testen.
        """) 