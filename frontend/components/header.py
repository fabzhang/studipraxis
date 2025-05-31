import streamlit as st

def header():
    """
    Display the studiPraxis header with consistent styling across all pages.
    """
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #15396b;'>studiPraxis.de</h1>
        <p style='font-size: 1.2rem;'>Praxiserfahrung. Einfach vermittelt.</p>
    </div>
    """, unsafe_allow_html=True) 