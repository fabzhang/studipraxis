import streamlit as st

st.set_page_config(
    page_title="Student - studiPraxis",
    page_icon="🧑‍🎓"
)

st.markdown("### Willkommen bei studiPraxis!")

# Check if user is logged in
if 'student_id' not in st.session_state or not st.session_state.student_id:
    st.info("Bitte melden Sie sich an oder registrieren Sie sich, um fortzufahren.")
    
    # Create two columns for the buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Anmelden", use_container_width=True):
            st.switch_page("pages/9_Student_Login.py")
    
    with col2:
        if st.button("Registrieren", use_container_width=True):
            st.switch_page("pages/9_Student_Login.py")
else:
    # User is logged in, show dashboard options
    st.success("Sie sind angemeldet!")
    
    # Create two columns for the buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Positionen durchsuchen", use_container_width=True):
            st.switch_page("pages/3_Positionen.py")
    
    with col2:
        if st.button("Profil bearbeiten", use_container_width=True):
            st.switch_page("pages/4_Profile.py")

with st.expander("Was bedeutet eine Anstellung als Werkstudent*in?"):
    st.markdown("""
    - Maximal 20 Stunden pro Woche während des Semesters
    - Du bleibst in der Regel familien- und studienversichert
    - Ein fairer Lohn für praktische Mitarbeit
    - Möglichkeit, Fachbereiche frühzeitig kennenzulernen
    """) 