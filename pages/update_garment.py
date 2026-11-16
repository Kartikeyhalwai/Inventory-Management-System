"""
pages/update_garment.py
-----------------------
Garment record modification page:
- Allows selecting an existing garment from inventory.
- Pre-populates all existing attributes in an editable form.
- Protects the primary key (Garment ID) to ensure the existing record is updated rather than duplicated.
- Validates updated values (including non-negative quantities).
- Refreshes the updated_at timestamp.
"""

import streamlit as st
import database


def render():
    st.subheader("✏️ Update Garment Record")
    st.markdown("Search for and select a registered garment to edit its attributes, adjust stock quantities, or update warehouse locations.")

    # Fetch latest inventory records
    df = database.get_all_garments_df()

    if df.empty:
        st.info("No garments are currently in the database. Add garments first before updating.")
        return

    # Create search and selection dropdown
    # Label items as "GARMENT_ID - GARMENT_NAME (BRAND)"
    options_map = {
        f"{row['garment_id']} — {row['garment_name']} ({row['brand']})": row['garment_id']
        for _, row in df.iterrows()
    }
    
    selected_label = st.selectbox(
        "Select Garment to Edit:",
        options=list(options_map.keys()),
        help="Choose a garment from the list to view and edit its details."
    )

    selected_id = options_map[selected_label]
    garment = database.get_garment_by_id(selected_id)

    if not garment:
        st.error(f"Could not load record for Garment ID: {selected_id}")
        return

    st.markdown("---")
    st.markdown(f"#### Editing Record: `{garment['garment_id']}`")

    # Display audit metadata
    col_meta1, col_meta2 = st.columns(2)
    col_meta1.caption(f"📅 **Originally Registered:** {garment['created_at']}")
    col_meta2.caption(f"🔄 **Last Modified:** {garment['updated_at']}")

    # Form to edit fields
    with st.form("update_garment_form"):
        col1, col2 = st.columns(2)

        with col1:
            # Garment ID is locked as read-only primary key
            st.text_input(
                "Garment ID (Primary Key - Locked)",
                value=garment["garment_id"],
                disabled=True,
                help="Garment ID cannot be modified because it is the unique primary key."
            )

            updated_name = st.text_input(
                "Garment Name *",
                value=garment["garment_name"],
                help="Update product name or style description."
            )

            # Determine type selection
            current_type = garment["garment_type"]
            type_options = list(database.GARMENT_TYPES)
            if current_type not in type_options:
                type_options.append(current_type)

            type_index = type_options.index(current_type) if current_type in type_options else 0
            updated_type = st.selectbox(
                "Garment Type *",
                options=type_options,
                index=type_index
            )

            custom_type = ""
            if updated_type == "Other":
                custom_type = st.text_input(
                    "Specify Other Category *",
                    placeholder="Enter custom garment type"
                )

            updated_brand = st.text_input(
                "Brand *",
                value=garment["brand"]
            )

        with col2:
            # Determine size selection
            current_size = garment["size"]
            size_options = list(database.STANDARD_SIZES)
            if current_size not in size_options:
                size_options.append(current_size)
            
            size_index = size_options.index(current_size) if current_size in size_options else 0
            updated_size = st.selectbox(
                "Size *",
                options=size_options,
                index=size_index
            )

            updated_colour = st.text_input(
                "Colour *",
                value=garment["colour"]
            )

            updated_fabric = st.text_input(
                "Fabric / Material *",
                value=garment["fabric"]
            )

            updated_quantity = st.number_input(
                "Quantity (Stock Units) *",
                min_value=0,
                max_value=100000,
                value=int(garment["quantity"]),
                step=1,
                help="Updated inventory count. Must be 0 or higher."
            )

            updated_location = st.text_input(
                "Storage Location *",
                value=garment["storage_location"]
            )

        submit_update = st.form_submit_button("💾 Save Changes", use_container_width=True)

        if submit_update:
            final_type = custom_type.strip() if updated_type == "Other" else updated_type

            if updated_type == "Other" and not final_type:
                st.error("Please specify the custom category name.")
                return

            success, message = database.update_garment(
                garment_id=garment["garment_id"],
                garment_name=updated_name,
                garment_type=final_type,
                brand=updated_brand,
                size=updated_size,
                colour=updated_colour,
                fabric=updated_fabric,
                quantity=updated_quantity,
                storage_location=updated_location
            )

            if success:
                st.success(message)
                # Show updated record summary
                st.info(
                    f"**Updated Record:** {updated_name} | Qty: {updated_quantity} units | "
                    f"Location: {updated_location}"
                )
                st.rerun()
            else:
                st.error(message)


if __name__ == "__main__":
    render()
