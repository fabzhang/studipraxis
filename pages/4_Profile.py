import streamlit as st
from student_view import student_view

st.set_page_config(
    page_title="Student*innen Profile - studiPraxis",
    page_icon="👥"
)

st.markdown("### Student*innen Profile")
student_view() 