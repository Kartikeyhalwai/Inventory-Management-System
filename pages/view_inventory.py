"""
pages/view_inventory.py
-----------------------
Inventory inspection page:
- Displays all registered garments in an organized table.
- Provides search by Garment ID and Garment Name.
- Provides multi-attribute filtering by Type, Size, Colour, and Fabric.
- Shows live inventory statistics for the filtered records.
- Enables CSV export of the inventory dataset (both filtered view and full catalog).
"""

from datetime import datetime
import streamlit as st
import pandas as pd
import database


def render():
    st.subheader("📋 Garment Inventory Records")
    st.markdown("Browse, search, and filter the complete garment catalog. Filtered records can be exported as a CSV report.")

    # Retrieve all inventory data from SQLite
    df = database.get_all_garments_df()

    if df.empty:
        st.info("The inventory is currently empty. Use the 'Add Garment' page to register items.")
        return

    # Fetch existing unique values for dynamic filter dropdowns
    filter_opts = database.get_filter_options()

    # Search and Filter section
    with st.expander("🔍 Search and Filter Options", expanded=True):
        col_search1, col_search2 = st.columns(2)

        with col_search1:
            search_id = st.text_input(
                "Search by Garment ID",
                placeholder="e.g. DEMO-TSH or TSH-001",
                help="Enter full or partial Garment ID."
            ).strip().lower()

        with col_search2:
            search_name = st.text_input(
                "Search by Garment Name",
                placeholder="e.g. Classic, Denim, Silk, Linen",
                help="Enter full or partial garment name."
            ).strip().lower()

        col_f1, col_f2, col_f3, col_f4 = st.columns(4)

        with col_f1:
            type_options = ["All"] + filter_opts["types"]
            selected_type = st.selectbox("Garment Type", options=type_options, index=0)

        with col_f2:
            size_options = ["All"] + filter_opts["sizes"]
            selected_size = st.selectbox("Size", options=size_options, index=0)

        with col_f3:
            colour_options = ["All"] + filter_opts["colours"]
            selected_colour = st.selectbox("Colour", options=colour_options, index=0)

        with col_f4:
            fabric_options = ["All"] + filter_opts["fabrics"]
            selected_fabric = st.selectbox("Fabric", options=fabric_options, index=0)

    # Apply filters to DataFrame
    filtered_df = df.copy()

    if search_id:
        filtered_df = filtered_df[filtered_df["garment_id"].astype(str).str.lower().str.contains(search_id, na=False)]

    if search_name:
        filtered_df = filtered_df[filtered_df["garment_name"].astype(str).str.lower().str.contains(search_name, na=False)]

    if selected_type != "All":
        filtered_df = filtered_df[filtered_df["garment_type"] == selected_type]

    if selected_size != "All":
        filtered_df = filtered_df[filtered_df["size"] == selected_size]

    if selected_colour != "All":
        filtered_df = filtered_df[filtered_df["colour"] == selected_colour]

    if selected_fabric != "All":
        filtered_df = filtered_df[filtered_df["fabric"] == selected_fabric]

    # Display KPI summaries for current view
    total_records = len(df)
    filtered_count = len(filtered_df)
    total_filtered_units = int(filtered_df["quantity"].sum()) if not filtered_df.empty else 0

    col_stat1, col_stat2, col_stat3 = st.columns(3)
    col_stat1.metric("Total Catalog SKUs", total_records)
    col_stat2.metric("Matching Records", filtered_count)
    col_stat3.metric("Total Units in View", f"{total_filtered_units:,}")

    # Export Buttons Row
    col_exp1, col_exp2, _ = st.columns([1, 1, 2])
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    with col_exp1:
        filtered_csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export Current View (CSV)",
            data=filtered_csv,
            file_name=f"garment_inventory_filtered_{timestamp}.csv",
            mime="text/csv",
            use_container_width=True,
            help="Download the currently filtered records as a CSV spreadsheet."
        )

    with col_exp2:
        full_csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📦 Export Full Inventory (CSV)",
            data=full_csv,
            file_name=f"garment_inventory_full_{timestamp}.csv",
            mime="text/csv",
            use_container_width=True,
            help="Download the entire inventory catalog as a CSV spreadsheet."
        )

    # Format the table for clear professional reading
    display_df = filtered_df.rename(columns={
        "garment_id": "Garment ID",
        "garment_name": "Garment Name",
        "garment_type": "Type",
        "brand": "Brand",
        "size": "Size",
        "colour": "Colour",
        "fabric": "Fabric",
        "quantity": "Quantity",
        "storage_location": "Storage Location",
        "created_at": "Created At",
        "updated_at": "Updated At"
    })

    if filtered_df.empty:
        st.warning("No garments matched your search and filter criteria. Try adjusting the filters above.")
    else:
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Garment ID": st.column_config.TextColumn("Garment ID", width="medium"),
                "Garment Name": st.column_config.TextColumn("Garment Name", width="large"),
                "Type": st.column_config.TextColumn("Type", width="small"),
                "Brand": st.column_config.TextColumn("Brand", width="small"),
                "Size": st.column_config.TextColumn("Size", width="small"),
                "Colour": st.column_config.TextColumn("Colour", width="small"),
                "Fabric": st.column_config.TextColumn("Fabric", width="medium"),
                "Quantity": st.column_config.NumberColumn("Quantity (Units)", format="%d"),
                "Storage Location": st.column_config.TextColumn("Storage Location", width="small"),
                "Created At": st.column_config.TextColumn("Created At", width="medium"),
                "Updated At": st.column_config.TextColumn("Updated At", width="medium")
            }
        )


if __name__ == "__main__":
    render()
