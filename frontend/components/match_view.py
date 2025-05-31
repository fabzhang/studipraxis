import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from backend.services.data_service import DataService
from shared.types import HospitalProfile, Position, Match
from datetime import datetime
from form_options import INTEREST_FIELDS, PRAXIS_SKILLS, STUDY_YEAR_OPTIONS
import uuid

# Toggle for additional filters
SHOW_ADDITIONAL_FILTERS = False  # Set to True to show year and requirements filters

def create_map(hospitals, positions, selected_department="Alle Abteilungen"):
    # Create a map centered on Hamburg
    m = folium.Map(location=[53.5511, 9.9937], zoom_start=12)
    
    # Create markers for hospitals with positions
    for hospital in hospitals:
        # Get positions for this hospital
        hospital_positions = [p for p in positions if p.hospital_id == hospital.id]
        
        # Filter by department if selected
        if selected_department != "All":
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
    """Display available positions with filtering options."""
    st.header("🔍 Browse Assistantship Positions")
    
    # Check if user is logged in
    if 'student_id' not in st.session_state or not st.session_state.student_id:
        st.warning("Bitte melden Sie sich an, um sich auf Positionen zu bewerben oder sie zu speichern.")
    
    # Add refresh button
    if st.button("🔄 Aktualisieren"):
        st.rerun()
    
    data_service = DataService()
    positions = data_service.get_positions()
    
    if not positions:
        st.info("No positions available yet.")
        return
    
    # Filter by department - use all INTEREST_FIELDS options
    selected_department = st.selectbox(
        "Filter by Department",
        ["All"] + INTEREST_FIELDS,
        help="Filter positions by department"
    )
    
    # Additional filters (only shown if SHOW_ADDITIONAL_FILTERS is True)
    selected_year = "All"
    selected_requirements = []
    if SHOW_ADDITIONAL_FILTERS:
        # Filter by minimum year - use all STUDY_YEAR_OPTIONS
        selected_year = st.selectbox(
            "Filter by Minimum Year",
            ["All"] + STUDY_YEAR_OPTIONS,
            help="Filter positions by minimum study year required"
        )
        
        # Filter by requirements - use all PRAXIS_SKILLS options
        selected_requirements = st.multiselect(
            "Filter by Requirements",
            options=PRAXIS_SKILLS,
            help="Filter positions by required skills/certifications"
        )
    
    # Create and display the interactive map
    m = create_map(data_service.get_hospitals(), positions, selected_department)
    folium_static(m)
    
    # Add legend or help text
    st.markdown("""
    💡 **Karten-Tipps:**
    - Klicken Sie auf die Marker für Details
    - Hoven Sie über die Marker für eine Schnellübersicht
    - Nutzen Sie +/- zum Zoomen
    """)
    
    # Display positions
    st.markdown("### Verfügbare Positionen")
    for position in positions:
        # Apply filters
        if selected_department != "All" and position.department != selected_department:
            continue
        
        if SHOW_ADDITIONAL_FILTERS:
            if selected_year != "All" and STUDY_YEAR_OPTIONS.index(position.min_year) > STUDY_YEAR_OPTIONS.index(selected_year):
                continue
            
            if selected_requirements and not all(req in position.requirements for req in selected_requirements):
                continue
        
        # Get hospital info
        hospital = data_service.get_hospital(position.hospital_id)
        if not hospital:
            continue
        
        # Create expander for position details
        with st.expander(f"{position.title} - {hospital.name}"):
            st.markdown(f"**Hospital:** {hospital.name}")
            st.markdown(f"**Department:** {position.department}")
            st.markdown(f"**Location:** {hospital.location}")
            st.markdown(f"**Description:** {position.description}")
            st.markdown(f"**Requirements:** {', '.join(position.requirements)}")
            st.markdown(f"**Minimum Year:** {position.min_year}")
            
            # Display stipend based on format
            if position.stipend:
                if position.stipend == "Bezahlung nach Tarifvertrag":
                    st.markdown(f"💰 {position.stipend}")
                else:
                    st.markdown(f"💰 {position.stipend}€/Stunde")
            
            # Add save/apply buttons if user is logged in as student
            if 'student_id' in st.session_state and st.session_state.student_id:
                # Check if position is already saved or applied
                existing_match = data_service.get_match_by_student_and_position(
                    st.session_state.student_id,
                    position.id
                )
                
                # Create two columns for the buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    if existing_match and existing_match.status == 'applied':
                        st.success("✅ Bewerbung eingereicht")
                        if st.button("Bewerbung zurückziehen", key=f"unapply_{position.id}"):
                            data_service.update_match_status(existing_match.id, 'saved')
                            st.success("Bewerbung zurückgezogen!")
                            st.rerun()
                    else:
                        if st.button("Jetzt bewerben", key=f"apply_{position.id}"):
                            if existing_match:
                                # Update existing match to applied
                                data_service.update_match_status(existing_match.id, 'applied')
                            else:
                                # Create new match as applied
                                new_match = Match(
                                    id=str(uuid.uuid4()),
                                    student_id=st.session_state.student_id,
                                    position_id=position.id,
                                    status='applied',
                                    created_at=datetime.now(),
                                    updated_at=datetime.now()
                                )
                                data_service.create_match(new_match)
                            st.success("Bewerbung erfolgreich eingereicht!")
                            st.rerun()
                
                with col2:
                    if existing_match and existing_match.status == 'saved':
                        st.success("💾 Position gespeichert")
                        if st.button("Aus gespeicherten entfernen", key=f"unsave_{position.id}"):
                            data_service.delete_match(existing_match.id)
                            st.success("Position aus gespeicherten entfernt!")
                            st.rerun()
                    else:
                        if st.button("Position speichern", key=f"save_{position.id}"):
                            if existing_match:
                                # Update existing match to saved
                                data_service.update_match_status(existing_match.id, 'saved')
                            else:
                                # Create new match as saved
                                new_match = Match(
                                    id=str(uuid.uuid4()),
                                    student_id=st.session_state.student_id,
                                    position_id=position.id,
                                    status='saved',
                                    created_at=datetime.now(),
                                    updated_at=datetime.now()
                                )
                                data_service.create_match(new_match)
                            st.success("Position erfolgreich gespeichert!")
                            st.rerun() 