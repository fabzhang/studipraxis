import streamlit as st
from backend.services.data_service import DataService
from form_options import INTEREST_FIELDS, PRAXIS_SKILLS, STUDY_YEAR_OPTIONS

# Hamburg coordinates for reference
HAMBURG_COORDINATES = {
    "UKE": (53.5897, 9.9756),
    "St. Georg": (53.5553, 10.0114),
    "Barmbek": (53.5869, 10.0406),
    "Altona": (53.5503, 9.9333),
    "Wandsbek": (53.5731, 10.0853),
    "Marienkrankenhaus": (53.5503, 9.9333),
    "Albertinen": (53.5731, 9.9333),
    "Israelitisches": (53.5731, 9.9333)
}

def hospital_form():
    """Form for hospitals to create new positions."""
    with st.form("position_form"):
        st.markdown("### Neue Position erstellen")
        
        # Department selection
        department = st.selectbox(
            "Department",
            options=INTEREST_FIELDS,
            help="Wählen Sie das Department aus, in dem die Position angeboten wird."
        )
        
        # Title
        title = st.text_input(
            "Titel der Position",
            help="Geben Sie einen aussagekräftigen Titel für die Position ein."
        )
        
        # Description
        description = st.text_area(
            "Beschreibung",
            help="Beschreiben Sie die Position und die zu erwartenden Aufgaben."
        )
        
        # Requirements
        requirements = st.multiselect(
            "Anforderungen",
            options=PRAXIS_SKILLS,
            help="Wählen Sie die erforderlichen Fähigkeiten und Zertifizierungen aus."
        )
        
        # Minimum year
        min_year = st.selectbox(
            "Minimales Studienjahr",
            options=STUDY_YEAR_OPTIONS,
            help="Wählen Sie das minimale Studienjahr, das für die Position erforderlich ist."
        )
        
        # Stipend
        stipend = st.text_input(
            "Vergütung",
            value="Bezahlung nach Tarifvertrag",
            help="Geben Sie 'Bezahlung nach Tarifvertrag' ein oder einen Stundenlohn in Euro (z.B. '15')"
        )
        
        # Submit button
        submitted = st.form_submit_button("Position erstellen")
        
        if submitted:
            if not title or not description or not requirements:
                st.error("Bitte füllen Sie alle Pflichtfelder aus.")
                return
            
            try:
                data_service = DataService()
                position = {
                    "hospital_id": st.session_state.hospital_id,
                    "department": department,
                    "title": title,
                    "description": description,
                    "requirements": requirements,
                    "min_year": min_year,
                    "stipend": stipend
                }
                data_service.add_position(position)
                st.success("Position erfolgreich erstellt!")
                st.rerun()
            except Exception as e:
                st.error(f"Ein Fehler ist aufgetreten: {str(e)}")

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