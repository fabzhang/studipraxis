import streamlit as st
from data_storage import load_data

HOSPITALS_FILE = "hospital_data.json"

def match_view():
    st.header("🔍 Browse Assistantship Positions")
    data = load_data(HOSPITALS_FILE)

    if not data:
        st.info("No positions available yet.")
        return

    # Optional: Filter by department
    departments = sorted(set(d["department"] for d in data if d["department"]))
    selected_department = st.selectbox("Filter by Department", ["All"] + departments)

    for entry in data:
        if selected_department != "All" and entry["department"] != selected_department:
            continue

        st.subheader(entry["title"])
        st.markdown(f"**Hospital:** {entry['hospital_name']}")
        st.markdown(f"**Department:** {entry['department']}")
        st.markdown(f"**Location:** {entry['location']}")
        st.markdown(f"**Duration:** {entry['duration']}")
        st.markdown(f"**Description:** {entry['description']}")
        st.markdown(f"**Requirements:** {entry['requirements']}")
        if entry["stipend"]:
            st.markdown(f"💰 **Stipend:** {entry['stipend']}")
        st.markdown("---")
