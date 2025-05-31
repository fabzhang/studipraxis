import streamlit as st
from frontend.components.student_form import student_form

st.set_page_config(
    page_title="Profil erstellen - studiPraxis",
    page_icon="📝"
)

st.markdown("### Profil erstellen")
student_form() 