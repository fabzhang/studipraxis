import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="studiPraxis.de",
    layout="wide",
    page_icon="💡",
    initial_sidebar_state="expanded"
)

# Load and display logo
logo = Image.open("studipraxis_logo.png")

# Center-aligned header
st.markdown("""
<div style='text-align: center;'>
    <h1 style='color: #1e8e5a;'>studiPraxis.de</h1>
    <p style='font-size: 1.2rem;'>Praxiserfahrung. Einfach vermittelt.</p>
</div>
""", unsafe_allow_html=True)

# Create two columns for the buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Ich bin Student*in", use_container_width=True, key="student_main"):
        st.switch_page("pages/1_Student.py")

with col2:
    if st.button("Ich bin eine Institution", use_container_width=True, key="institution_main"):
        st.switch_page("pages/2_Institution.py")

# Default landing page content
st.markdown("""
### Willkommen bei studiPraxis.de

Wählen Sie oben aus, ob Sie Student*in oder Institution sind, um fortzufahren.
""")
