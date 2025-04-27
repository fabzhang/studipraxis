import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from backend.services.data_service import DataService
from shared.types import HospitalProfile, Position, Match
from datetime import datetime

def create_map(hospitals, positions, selected_department="Alle Abteilungen"):
    # Create a map centered on Hamburg
    m = folium.Map(location=[53.5511, 9.9937], zoom_start=12)
    
    # Create markers for hospitals with positions
    for hospital in hospitals:
        # Get positions for this hospital
        hospital_positions = [p for p in positions if p.hospital_id == hospital.id]
        
        # Filter by department if selected
        if selected_department != "Alle Abteilungen":
            hospital_positions = [p for p in hospital_positions if p.department == selected_department]
        
        if not hospital_positions:
            continue
            
        # Create popup content
        popup_html = f"""
        <div style='width: 200px'>
            <h4>{hospital.name}</h4>
            <b>Standort:</b> {hospital.location}<br>
            <b>Verfügbare Stellen:</b> {len(hospital_positions)}
        </div>
        """
        
        # Add marker with popup
        folium.Marker(
            [hospital.latitude, hospital.longitude],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{hospital.name} ({len(hospital_positions)} {'Position' if len(hospital_positions) == 1 else 'Positionen'})",
            icon=folium.Icon(color='green', icon='info-sign')
        ).add_to(m)
    
    return m

def match_view():
    st.header("🔍 Browse Assistantship Positions")
    
    # Check if user is logged in
    if 'student_id' not in st.session_state or not st.session_state.student_id:
        st.warning("Bitte melden Sie sich an, um sich auf Positionen zu bewerben oder sie zu speichern.")
    
    # Add refresh button
    if st.button("🔄 Aktualisieren"):
        st.rerun()
    
    # Get all hospitals and positions
    data_service = DataService()
    hospitals = data_service.get_hospitals()
    positions = data_service.get_positions()
    
    if not positions:
        st.info("Keine Positionen verfügbar.")
        return
    
    # Create two columns: map and filter
    col1, col2 = st.columns([2, 1])
    
    with col2:
        # Department filter
        departments = sorted(set(p.department for p in positions if p.department))
        selected_department = st.selectbox(
            "Nach Abteilung filtern",
            ["Alle Abteilungen"] + departments,
            key="department_filter"
        )
    
    with col1:
        # Create and display the interactive map
        m = create_map(hospitals, positions, selected_department)
        folium_static(m)
        
        # Add legend or help text
        st.markdown("""
        💡 **Karten-Tipps:**
        - Klicken Sie auf die Marker für Details
        - Hovern Sie über die Marker für eine Schnellübersicht
        - Nutzen Sie +/- zum Zoomen
        """)

    # Display all positions with a cleaner layout
    st.markdown("### Verfügbare Positionen")

    # Create a grid layout for positions
    for position in positions:
        if selected_department != "Alle Abteilungen" and position.department != selected_department:
            continue

        # Get hospital info
        hospital = next((h for h in hospitals if h.id == position.hospital_id), None)
        if not hospital:
            continue

        # Create a container for each position
        with st.container():
            # Use columns for the condensed view
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"### {position.title}")
                st.markdown(f"🏥 {hospital.name}")
            
            with col2:
                st.markdown(f"**Abteilung:** {position.department}")
            
            with col3:
                st.markdown(f"⏱️ {position.duration}")
                if position.stipend:
                    st.markdown(f"💰 {position.stipend}€/Monat")

            # Expandable details section
            with st.expander("Mehr Details anzeigen"):
                st.markdown("#### Position Details")
                
                # Create two columns for details
                detail_col1, detail_col2 = st.columns(2)
                
                with detail_col1:
                    st.markdown("##### Standort")
                    st.markdown(f"📍 {hospital.location}")
                    
                    st.markdown("##### Beschreibung")
                    st.markdown(position.description)
                
                with detail_col2:
                    st.markdown("##### Anforderungen")
                    for req in position.requirements:
                        st.markdown(f"✓ {req}")
                    
                    if position.stipend:
                        st.markdown("##### Vergütung")
                        st.markdown(f"💰 {position.stipend}€ pro Monat")
                
                # Action buttons
                if 'student_id' in st.session_state and st.session_state.student_id:
                    # Check if student has already applied or saved this position
                    student_id = st.session_state.student_id
                    existing_match = data_service.get_match_by_student_and_position(student_id, position.id)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if existing_match and existing_match.status == 'applied':
                            st.success("✓ Bewerbung eingereicht")
                        elif existing_match and existing_match.status == 'saved':
                            if st.button("Jetzt bewerben", key=f"apply_{position.id}"):
                                data_service.update_match_status(existing_match.id, 'applied')
                                st.success("Bewerbung erfolgreich eingereicht!")
                                st.rerun()
                        else:
                            if st.button("Jetzt bewerben", key=f"apply_{position.id}"):
                                match = Match(
                                    id="",  # Will be generated by service
                                    student_id=student_id,
                                    position_id=position.id,
                                    status='applied',
                                    created_at=datetime.now(),
                                    updated_at=datetime.now()
                                )
                                data_service.create_match(match)
                                st.success("Bewerbung erfolgreich eingereicht!")
                                st.rerun()
                    
                    with col2:
                        if existing_match and existing_match.status == 'saved':
                            st.success("✓ Position gespeichert")
                        elif existing_match and existing_match.status == 'applied':
                            if st.button("Position speichern", key=f"save_{position.id}"):
                                data_service.update_match_status(existing_match.id, 'saved')
                                st.success("Position erfolgreich gespeichert!")
                                st.rerun()
                        else:
                            if st.button("Position speichern", key=f"save_{position.id}"):
                                match = Match(
                                    id="",  # Will be generated by service
                                    student_id=student_id,
                                    position_id=position.id,
                                    status='saved',
                                    created_at=datetime.now(),
                                    updated_at=datetime.now()
                                )
                                data_service.create_match(match)
                                st.success("Position erfolgreich gespeichert!")
                                st.rerun()

            # Add a subtle divider between positions
            st.markdown("---")

    # Add some spacing at the bottom
    st.markdown("<br>", unsafe_allow_html=True)

    # Display all positions below the map
    st.markdown("### Alle Positionen")
    for position in positions:
        if selected_department != "Alle Abteilungen" and position.department != selected_department:
            continue

        # Get hospital info
        hospital = next((h for h in hospitals if h.id == position.hospital_id), None)
        if not hospital:
            continue

        st.subheader(position.title)
        st.markdown(f"**Hospital:** {hospital.name}")
        st.markdown(f"**Department:** {position.department}")
        st.markdown(f"**Location:** {hospital.location}")
        st.markdown(f"**Duration:** {position.duration}")
        st.markdown(f"**Description:** {position.description}")
        st.markdown(f"**Requirements:** {', '.join(position.requirements)}")
        if position.stipend:
            st.markdown(f"💰 **Stipend:** {position.stipend}€")
        st.markdown("---") 