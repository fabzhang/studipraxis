import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from backend.services.data_service import DataService
from shared.types import HospitalProfile

def create_map(hospitals, selected_department="Alle Abteilungen"):
    # Create a map centered on Hamburg
    m = folium.Map(location=[53.5511, 9.9937], zoom_start=12)
    
    # Create markers for filtered hospitals
    for hospital in hospitals:
        if selected_department != "Alle Abteilungen" and hospital.department != selected_department:
            continue
            
        # Count positions in this hospital for this department
        positions_count = len([h for h in hospitals 
                             if h.name == hospital.name 
                             and (selected_department == "Alle Abteilungen" 
                                 or h.department == selected_department)])
        
        # Create popup content
        popup_html = f"""
        <div style='width: 200px'>
            <h4>{hospital.name}</h4>
            <b>Abteilung:</b> {hospital.department}<br>
            <b>Position:</b> {hospital.title}<br>
            <b>Dauer:</b> {hospital.duration}<br>
            {'<b>Vergütung:</b> ' + str(hospital.stipend) + '€/Monat<br>' if hospital.stipend else ''}
            <b>Verfügbare Stellen:</b> {positions_count}
        </div>
        """
        
        # Add marker with popup
        folium.Marker(
            [hospital.latitude, hospital.longitude],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{hospital.name} ({positions_count} {'Position' if positions_count == 1 else 'Positionen'})",
            icon=folium.Icon(color='green', icon='info-sign')
        ).add_to(m)
    
    return m

def match_view():
    st.header("🔍 Browse Assistantship Positions")
    
    # Add refresh button
    if st.button("🔄 Aktualisieren"):
        st.experimental_rerun()
    
    # Get all hospitals
    data_service = DataService()
    hospitals = data_service.get_hospitals()
    
    if not hospitals:
        st.info("Keine Positionen verfügbar.")
        return
    
    # Create two columns: map and filter
    col1, col2 = st.columns([2, 1])
    
    with col2:
        # Department filter
        departments = sorted(set(d.department for d in hospitals if d.department))
        selected_department = st.selectbox(
            "Nach Abteilung filtern",
            ["Alle Abteilungen"] + departments,
            key="department_filter"
        )
    
    with col1:
        # Create and display the interactive map
        m = create_map(hospitals, selected_department)
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
    for entry in hospitals:
        if selected_department != "Alle Abteilungen" and entry.department != selected_department:
            continue

        # Create a container for each position
        with st.container():
            # Use columns for the condensed view
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"### {entry.title}")
                st.markdown(f"🏥 {entry.name}")
            
            with col2:
                st.markdown(f"**Abteilung:** {entry.department}")
            
            with col3:
                st.markdown(f"⏱️ {entry.duration}")
                if entry.stipend:
                    st.markdown(f"💰 {entry.stipend}€/Monat")

            # Expandable details section
            with st.expander("Mehr Details anzeigen"):
                st.markdown("#### Position Details")
                
                # Create two columns for details
                detail_col1, detail_col2 = st.columns(2)
                
                with detail_col1:
                    st.markdown("##### Standort")
                    st.markdown(f"📍 {entry.location}")
                    
                    st.markdown("##### Beschreibung")
                    st.markdown(entry.description)
                
                with detail_col2:
                    st.markdown("##### Anforderungen")
                    for req in entry.requirements:
                        st.markdown(f"✓ {req}")
                    
                    if entry.stipend:
                        st.markdown("##### Vergütung")
                        st.markdown(f"💰 {entry.stipend}€ pro Monat")

            # Add a subtle divider between positions
            st.markdown("---")

    # Add some spacing at the bottom
    st.markdown("<br>", unsafe_allow_html=True)

    # Display all positions below the map
    st.markdown("### Alle Positionen")
    for entry in hospitals:
        if selected_department != "Alle Abteilungen" and entry.department != selected_department:
            continue

        st.subheader(entry.title)
        st.markdown(f"**Hospital:** {entry.name}")
        st.markdown(f"**Department:** {entry.department}")
        st.markdown(f"**Location:** {entry.location}")
        st.markdown(f"**Duration:** {entry.duration}")
        st.markdown(f"**Description:** {entry.description}")
        st.markdown(f"**Requirements:** {', '.join(entry.requirements)}")
        if entry.stipend:
            st.markdown(f"💰 **Stipend:** {entry.stipend}€")
        st.markdown("---") 