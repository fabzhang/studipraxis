import streamlit as st

def footer():
    """
    Display a footer at the bottom of the page with links to important pages.
    Uses Streamlit's native components for better compatibility.
    """
    # Add spacing before footer
    st.markdown("<br>" * 3, unsafe_allow_html=True)
    
    # Create a container for the footer
    footer_container = st.container()
    
    with footer_container:
        # Add a horizontal line
        st.markdown("---")
        
        # Create columns for the links
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # Add links in each column
        with col1:
            st.markdown("[Kontakt](/pages/12_Kontakt.py)")
        with col2:
            st.markdown("[AGB](/pages/13_AGB.py)")
        with col3:
            st.markdown("[Datenschutz](/pages/14_Datenschutz.py)")
        with col4:
            st.markdown("[Impressum](/pages/15_Impressum.py)")
        with col5:
            st.markdown("[Über uns](/pages/16_Who_We_Are.py)")
        
        # Add copyright text
        st.markdown(
            "<div style='text-align: center; color: #666; font-size: 0.8em;'>© 2024 studiPraxis. Alle Rechte vorbehalten.</div>",
            unsafe_allow_html=True
        ) 