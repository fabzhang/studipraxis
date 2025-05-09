import streamlit as st
from backend.services.data_service import DataService
from shared.types import StudentProfile

def student_form():
    st.header("🧑‍🎓 Submit Your Student Profile")
    
    with st.form("student_form"):
        name = st.text_input("Name")
        year = st.selectbox("Year of Study", ["1", "2", "3", "4", "5", "6"])
        interests = st.text_area("Specialty Interests (e.g., Surgery, Pediatrics)")
        availability = st.text_input("Availability (e.g., Summer 2025)")
        certifications = st.text_input("Certifications (optional)")

        submitted = st.form_submit_button("Submit Profile")
        if submitted:
            try:
                # Create student profile
                student = StudentProfile(
                    id="",  # Will be generated by the service
                    name=name,
                    year=int(year),
                    interests=[i.strip() for i in interests.split(",") if i.strip()],
                    availability=availability,
                    certifications=[c.strip() for c in certifications.split(",") if c.strip()] if certifications else None,
                    created_at=None,  # Will be set by the service
                    updated_at=None   # Will be set by the service
                )
                
                # Save using data service
                data_service = DataService()
                saved_student = data_service.create_student(student)
                
                st.success("Profile submitted successfully!")
                st.balloons()
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}") 