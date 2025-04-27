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
    
    # Filter by study year
    years = sorted(set(s.year for s in students))
    selected_year = st.selectbox("Filter by Study Year", ["All"] + [str(y) for y in years])
    
    # Filter by interests
    all_interests = set()
    for student in students:
        all_interests.update(student.interests)
    
    selected_interest = st.selectbox("Filter by Interest Area", ["All"] + sorted(list(all_interests)))
    
    # Display filtered students
    for student in students:
        # Apply filters
        if selected_year != "All" and student.year != int(selected_year):
            continue
        if selected_interest != "All" and selected_interest not in student.interests:
            continue
        
        st.subheader(f"Medical Student - Year {student.year}")
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