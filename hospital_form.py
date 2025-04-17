import streamlit as st
from data_storage import load_data, save_data

HOSPITALS_FILE = "hospital_data.json"

def hospital_form():
    st.header("🏥 Submit Assistantship Position")
    with st.form("hospital_form"):
        hospital_name = st.text_input("Hospital Name")
        department = st.text_input("Department")
        title = st.text_input("Position Title")
        description = st.text_area("Description")
        duration = st.text_input("Duration (e.g., 3 months)")
        requirements = st.text_input("Requirements")
        location = st.text_input("Location")
        stipend = st.text_input("Stipend (optional)")

        submitted = st.form_submit_button("Submit Position")
        if submitted:
            data = load_data(HOSPITALS_FILE)
            data.append({
                "hospital_name": hospital_name,
                "department": department,
                "title": title,
                "description": description,
                "duration": duration,
                "requirements": requirements,
                "location": location,
                "stipend": stipend
            })
            save_data(HOSPITALS_FILE, data)
            st.success("Position submitted successfully!")
