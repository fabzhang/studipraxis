import streamlit as st
from backend.services.data_service import DataService
from shared.types import StudentProfile

def student_view():
    st.header("👥 Browse Student Profiles")
    
    # Get all students
    data_service = DataService()
    students = data_service.get_students()
    
    if not students:
        st.info("No student profiles available yet.")
        return
    
    # Handle conversion for sorting to prevent type comparison errors
    def get_year_for_sorting(student):
        """Convert year to sortable value, handling both string and int formats"""
        year = student.year
        if isinstance(year, int):
            return year
        elif isinstance(year, str):
            # For string years like "Vorklinik - 1. Jahr", extract numeric part
            # This is a simple approach, might need refinement
            for part in year.split():
                if part.isdigit():
                    return int(part)
            # If no numeric part found, put at the end of the sort
            return 999
        return 0

    # Filter by study year safely
    years_set = set()
    for student in students:
        if isinstance(student.year, int):
            years_set.add(str(student.year))
        else:
            years_set.add(student.year)
    
    years = sorted(years_set, key=lambda y: int(y) if y.isdigit() else 999)  # Sort numerically if possible
    selected_year = st.selectbox("Filter by Study Year", ["All"] + years)
    
    # Filter by interests
    all_interests = set()
    for student in students:
        all_interests.update(student.interests)
    
    selected_interest = st.selectbox("Filter by Interest Area", ["All"] + sorted(list(all_interests)))
    
    # Display filtered students
    for student in students:
        # Apply filters
        if selected_year != "All":
            # Handle both string and int year formats
            student_year = str(student.year) if isinstance(student.year, int) else student.year
            if student_year != selected_year:
                continue
                
        if selected_interest != "All" and selected_interest not in student.interests:
            continue
        
        # Display student year in a consistent format
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
        
        st.subheader(f"Medical Student - {display_year}")
        st.markdown(f"**Name:** {student.name}")
        
        if student.interests:
            st.markdown("**Interests:**")
            for interest in student.interests:
                st.markdown(f"- {interest}")
        
        st.markdown(f"**Availability:** {student.availability}")
        
        if student.certifications:
            st.markdown("**Certifications:**")
            for cert in student.certifications:
                st.markdown(f"- {cert}")
        
        st.markdown("---") 