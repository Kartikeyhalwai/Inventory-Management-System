"""
pages/add_garment.py
--------------------
Garment registration page for adding new apparel items to the inventory.
Provides input validation, category selection (including custom 'Other' input),
and duplicate ID prevention.
"""

import streamlit as st
import database


def render():
    st.subheader("➕ Register New Garment")
    st.markdown(
        r"Enter apparel details below to add a new stock keeping unit (SKU) "
        r"to the inventory management system. All fields marked with **\*** are required."
    )

    with st.expander("ℹ️ Apparel Analyst Quick Tip: Recommended Garment ID Format"):
        st.markdown(
            """
            In apparel inventory operations, structured IDs help warehouse staff quickly locate stock:
            - **Format:** `[CATEGORY_PREFIX]-[STYLE_CODE]-[NUM]`
            - **Examples:** `TSH-CRW-001` (T-shirt), `JNS-SLM-102` (Slim Jeans), `SHT-OXF-045` (Oxford Shirt)
            - **Rule:** Every Garment ID must be unique.
            """
        )

    # Use a Streamlit form so validation runs upon clicking Register
    with st.form("add_garment_form", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            garment_id = st.text_input(
                "Garment ID *",
                placeholder="e.g. TSH-101 or DEMO-TSH-001",
                help="A unique identifier for this garment SKU."
            )

            garment_name = st.text_input(
                "Garment Name *",
                placeholder="e.g. Classic Organic Cotton Tee",
                help="Product name or style description."
            )

            garment_type_choice = st.selectbox(
                "Garment Type *",
                options=database.GARMENT_TYPES,
                help="Select the apparel category. Choose 'Other' to enter a custom category."
            )

            custom_category = ""
            if garment_type_choice == "Other":
                custom_category = st.text_input(
                    "Specify Other Category *",
                    placeholder="e.g. Cardigans, Hoodies, Shorts, etc."
                )

            brand = st.text_input(
                "Brand *",
                placeholder="e.g. UrbanWear, HeritageCloth, Zara",
                help="Brand, manufacturer, or internal line label."
            )

        with col2:
            size_options = database.STANDARD_SIZES + ["Other / Custom"]
            size_choice = st.selectbox(
                "Size *",
                options=size_options,
                index=2,  # default to 'M'
                help="Select garment size or enter a custom size."
            )

            custom_size = ""
            if size_choice == "Other / Custom":
                custom_size = st.text_input(
                    "Specify Custom Size *",
                    placeholder="e.g. 40R, One Size, 3-4Y"
                )

            colour = st.text_input(
                "Colour *",
                placeholder="e.g. Navy Blue, Olive Green, White",
                help="Primary colour of the garment."
            )

            fabric = st.text_input(
                "Fabric / Material *",
                placeholder="e.g. 100% Combed Cotton, Denim 12oz, Linen Blend",
                help="Apparel fabric composition and material specifications."
            )

            quantity = st.number_input(
                "Quantity (Stock Units) *",
                min_value=0,
                max_value=100000,
                value=10,
                step=1,
                help="Current units available in inventory. Must be 0 or more."
            )

            storage_location = st.text_input(
                "Storage Location *",
                placeholder="e.g. Rack A-1, Shelf B-3, Hanger 14",
                help="Physical location of the garment inside the stockroom or warehouse."
            )

        submitted = st.form_submit_button("Register Garment", use_container_width=True)

        if submitted:
            # Determine actual category and size
            final_type = custom_category.strip() if garment_type_choice == "Other" else garment_type_choice
            final_size = custom_size.strip() if size_choice == "Other / Custom" else size_choice

            # Validate custom inputs if selected
            if garment_type_choice == "Other" and not final_type:
                st.error("Please enter a category name for 'Other'.")
                return

            if size_choice == "Other / Custom" and not final_size:
                st.error("Please specify the custom size.")
                return

            # Call database layer for validation and insertion
            success, message = database.add_garment(
                garment_id=garment_id,
                garment_name=garment_name,
                garment_type=final_type,
                brand=brand,
                size=final_size,
                colour=colour,
                fabric=fabric,
                quantity=quantity,
                storage_location=storage_location
            )

            if success:
                st.success(message)
                st.info(
                    f"**Registered SKU Details:** {garment_name} | Type: {final_type} | "
                    f"Brand: {brand} | Size: {final_size} | Colour: {colour} | "
                    f"Qty: {quantity} units at {storage_location}"
                )
            else:
                st.error(message)


if __name__ == "__main__":
    render()
