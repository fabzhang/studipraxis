import streamlit as st
from data_storage import load_data, save_data

STUDENTS_FILE = "student_data.json"

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
            data = load_data(STUDENTS_FILE)
            data.append({
                "name": name,
                "year": year,
                "interests": interests,
                "availability": availability,
                "certifications": certifications
            })
            save_data(STUDENTS_FILE, data)
            st.success("Profile submitted successfully!")
