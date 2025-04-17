import streamlit as st
import pandas as pd
from backend.services.data_service import DataService
from shared.types import HospitalProfile

def map_view():
    st.header("🏥 Kliniken in Hamburg")
    
    # Get all hospitals
    data_service = DataService()
    hospitals = data_service.get_hospitals()
    
    if not hospitals:
        st.info("Keine Kliniken verfügbar.")
        return
    
    # Convert to DataFrame for st.map
    df = pd.DataFrame([
        {
            'name': h.name,
            'department': h.department,
            'title': h.title,
            'lat': h.latitude,
            'lon': h.longitude
        }
        for h in hospitals
    ])
    
    # Create two columns: map and details
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display the map
        st.map(df)
        
        # Add some sample hospitals in Hamburg (you can replace these with real data)
        st.markdown("""
        ### Wichtige Kliniken in Hamburg:
        - Universitätsklinikum Hamburg-Eppendorf (UKE)
        - Asklepios Klinik St. Georg
        - Asklepios Klinik Barmbek
        - Asklepios Klinik Altona
        - Asklepios Klinik Wandsbek
        - Marienkrankenhaus
        - Albertinen-Krankenhaus
        - Israelitisches Krankenhaus
        """)
    
    with col2:
        # Display hospital details when a marker is clicked
        st.markdown("### Verfügbare Positionen")
        
        # Group by hospital name
        hospital_groups = {}
        for hospital in hospitals:
            if hospital.name not in hospital_groups:
                hospital_groups[hospital.name] = []
            hospital_groups[hospital.name].append(hospital)
        
        # Display each hospital's positions
        for hospital_name, positions in hospital_groups.items():
            with st.expander(f"🏥 {hospital_name}"):
                for pos in positions:
                    st.markdown(f"""
                    **{pos.title}**
                    - Abteilung: {pos.department}
                    - Dauer: {pos.duration}
                    - Standort: {pos.location}
                    """)
                    if pos.stipend:
                        st.markdown(f"💰 Stipendium: {pos.stipend}€")
                    st.markdown("---") 