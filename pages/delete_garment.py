"""
pages/delete_garment.py
-----------------------
Garment removal page:
- Allows selecting retired, damaged, or erroneously entered garments.
- Displays full record details for verification before deletion.
- Requires explicit user confirmation prior to database deletion to prevent accidental data loss.
"""

import streamlit as st
import database


def render():
    st.subheader("🗑️ Delete Garment Record")
    st.markdown("Remove retired, discontinued, or duplicate apparel records from the inventory database.")

    # Retrieve current records
    df = database.get_all_garments_df()

    if df.empty:
        st.info("No garments are currently in the database to delete.")
        return

    # Map labels to garment IDs
    options_map = {
        f"{row['garment_id']} — {row['garment_name']} ({row['brand']} | Qty: {row['quantity']})": row['garment_id']
        for _, row in df.iterrows()
    }

    selected_label = st.selectbox(
        "Select Garment to Delete:",
        options=list(options_map.keys()),
        help="Choose the garment SKU you wish to permanently remove."
    )

    selected_id = options_map[selected_label]
    garment = database.get_garment_by_id(selected_id)

    if not garment:
        st.error(f"Could not retrieve record for Garment ID: {selected_id}")
        return

    st.markdown("---")
    st.markdown("#### Review Garment Details Before Deletion")

    # Present details in structured cards/columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Garment ID:** `{garment['garment_id']}`")
        st.markdown(f"**Name:** {garment['garment_name']}")
        st.markdown(f"**Category:** {garment['garment_type']}")
    with col2:
        st.markdown(f"**Brand:** {garment['brand']}")
        st.markdown(f"**Size:** {garment['size']}")
        st.markdown(f"**Colour:** {garment['colour']}")
    with col3:
        st.markdown(f"**Fabric:** {garment['fabric']}")
        st.markdown(f"**Current Quantity:** {garment['quantity']} units")
        st.markdown(f"**Storage Location:** {garment['storage_location']}")

    st.markdown("---")
    st.warning("⚠️ **Warning:** Deletion is permanent. Once deleted, this record cannot be recovered.")

    # Confirmation checkbox
    confirm_delete = st.checkbox(
        f"Yes, I confirm that I want to permanently delete **{garment['garment_name']}** (ID: `{garment['garment_id']}`).",
        value=False
    )

    col_btn, _ = st.columns([1, 2])
    with col_btn:
        if st.button("Permanently Delete Garment", type="primary", use_container_width=True):
            if not confirm_delete:
                st.error("Action blocked: You must check the confirmation checkbox above before deleting.")
            else:
                success, message = database.delete_garment(garment["garment_id"])
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)


if __name__ == "__main__":
    render()
