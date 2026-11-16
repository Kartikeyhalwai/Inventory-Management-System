"""
app.py
------
Main application controller for the Garment Inventory Tracker.
Coordinates sidebar navigation, database initialization, and page rendering.

To run:
    streamlit run app.py
"""

import streamlit as st
import database

# Configure Streamlit page layout and metadata
st.set_page_config(
    page_title="MYI ~ Manage Your Inventory",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure database and demo records are initialized on startup
database.init_db()

# Load sub-page modules
from pages import dashboard, add_garment, view_inventory, update_garment, delete_garment


def main():
    # Application Title in Main Area
    st.title("MYI ~ Manage Your Inventory")
    st.caption("Internal Apparel Inventory Management & Record Organization System")

    # Sidebar Header
    st.sidebar.markdown("### 👔 Navigation")
    st.sidebar.caption("Apparel Analyst Workspace")

    # Required 5 Navigation Options
    nav_options = [
        "1. Dashboard",
        "2. Add Garment",
        "3. View Inventory",
        "4. Update Garment",
        "5. Delete Garment"
    ]

    selected_page = st.sidebar.radio(
        "Select Operation:",
        options=nav_options,
        index=0
    )

    st.sidebar.markdown("---")

    # Quick System Status in Sidebar
    metrics = database.get_dashboard_metrics()
    st.sidebar.markdown("#### 📦 Quick Stock Overview")
    st.sidebar.text(f"Total SKUs:  {metrics['total_registered']}")
    st.sidebar.text(f"Total Units: {metrics['total_quantity']:,}")
    st.sidebar.text(f"Categories:  {metrics['total_categories']}")
    st.sidebar.caption("Database: SQLite (`garment_inventory.db`)")

    st.sidebar.markdown("---")
    st.sidebar.caption("MYI ~ Manage Your Inventory")

    # Render selected view
    if selected_page == "1. Dashboard":
        dashboard.render()
    elif selected_page == "2. Add Garment":
        add_garment.render()
    elif selected_page == "3. View Inventory":
        view_inventory.render()
    elif selected_page == "4. Update Garment":
        update_garment.render()
    elif selected_page == "5. Delete Garment":
        delete_garment.render()


if __name__ == "__main__":
    main()
