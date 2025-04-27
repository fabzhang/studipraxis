import streamlit as st
from frontend.components.match_view import match_view
from backend.services.data_service import DataService

st.set_page_config(
    page_title="Alle Positionen - studiPraxis",
    page_icon="🔍"
)

# Check if user is logged in
if 'student_id' in st.session_state and st.session_state.student_id:
    data_service = DataService()
    
    # Get applied and saved positions
    applied_matches = data_service.get_applied_positions_for_student(st.session_state.student_id)
    saved_matches = data_service.get_saved_positions_for_student(st.session_state.student_id)
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Alle Positionen", "Bewerbungen", "Gespeicherte Positionen"])
    
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
                            st.markdown(f"**Abteilung:** {position.department}")
                            st.markdown(f"**Standort:** {hospital.location}")
                            st.markdown(f"**Dauer:** {position.duration}")
                            if position.stipend:
                                st.markdown(f"**Vergütung:** {position.stipend}€/Monat")
                            st.markdown("**Beschreibung:**")
                            st.markdown(position.description)
                            st.markdown("**Anforderungen:**")
                            for req in position.requirements:
                                st.markdown(f"- {req}")
    
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
                            st.markdown(f"**Abteilung:** {position.department}")
                            st.markdown(f"**Standort:** {hospital.location}")
                            st.markdown(f"**Dauer:** {position.duration}")
                            if position.stipend:
                                st.markdown(f"**Vergütung:** {position.stipend}€/Monat")
                            st.markdown("**Beschreibung:**")
                            st.markdown(position.description)
                            st.markdown("**Anforderungen:**")
                            for req in position.requirements:
                                st.markdown(f"- {req}")
                            
                            # Add apply button
                            if st.button("Jetzt bewerben", key=f"apply_saved_{position.id}"):
                                data_service.update_match_status(match.id, 'applied')
                                st.success("Bewerbung erfolgreich eingereicht!")
                                st.rerun()
else:
    st.markdown("### Alle Positionen")
    match_view() 