import streamlit as st
from frontend.components.match_view import match_view

st.set_page_config(
    page_title="Alle Positionen - studiPraxis",
    page_icon="🔍"
)

st.markdown("### Alle Positionen")
match_view() 