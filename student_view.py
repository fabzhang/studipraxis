import streamlit as st
from data_storage import load_data

STUDENTS_FILE = "student_data.json"

def student_view():
    st.header("👥 Browse Student Profiles")
    data = load_data(STUDENTS_FILE)

    if not data:
        st.info("No student profiles available yet.")
        return

    # Filter by study year
    years = sorted(set(d["year_of_study"] for d in data if d.get("year_of_study")))
    selected_year = st.selectbox("Filter by Study Year", ["All"] + years)

    # Filter by interests/departments
    # Split the interests string into a list if it's a string
    all_interests = set()
    for d in data:
        interests = d.get("interests", "")
        if isinstance(interests, str):
            # Split by comma and strip whitespace
            interests_list = [i.strip() for i in interests.split(",")]
            all_interests.update(interests_list)
    
    selected_interest = st.selectbox("Filter by Interest Area", ["All"] + sorted(list(all_interests)))

    for entry in data:
        # Convert interests to list if it's a string
        entry_interests = entry.get("interests", "")
        if isinstance(entry_interests, str):
            entry_interests = [i.strip() for i in entry_interests.split(",")]
        
        # Convert certifications to list if it's a string
        entry_certs = entry.get("certifications", "")
        if isinstance(entry_certs, str):
            entry_certs = [c.strip() for c in entry_certs.split(",")]

        # Apply filters
        if selected_year != "All" and entry.get("year_of_study") != selected_year:
            continue
        if selected_interest != "All" and selected_interest not in entry_interests:
            continue

        st.subheader(f"Medical Student - Year {entry.get('year_of_study', 'N/A')}")
        st.markdown(f"**Name:** {entry.get('name', 'N/A')}")
        st.markdown(f"**Study Year:** {entry.get('year_of_study', 'N/A')}")
        
        if entry_interests:
            st.markdown("**Interests:**")
            for interest in entry_interests:
                if interest:  # Only show non-empty interests
                    st.markdown(f"- {interest}")
        
        st.markdown(f"**Availability:** {entry.get('availability', 'N/A')}")
        
        if entry_certs:
            st.markdown("**Certifications:**")
            for cert in entry_certs:
                if cert:  # Only show non-empty certifications
                    st.markdown(f"- {cert}")
        
        st.markdown("---") 