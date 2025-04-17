import streamlit as st
from hospital_form import hospital_form

st.set_page_config(
    page_title="Position ausschreiben - studiPraxis",
    page_icon="📋"
)

st.markdown("### Position ausschreiben")
hospital_form() 