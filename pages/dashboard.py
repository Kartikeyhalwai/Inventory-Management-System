"""
pages/dashboard.py
------------------
Executive inventory overview dashboard:
- Key operational metrics: Total SKUs, Total Units, Categories, In-Stock Items.
- Inventory distribution visualization by apparel category.
- Category breakdown table with unit share percentages.
- Stock health alerts (e.g. low-stock / out-of-stock items) for apparel analysts.
- Direct CSV export of full inventory.
"""

from datetime import datetime
import streamlit as st
import pandas as pd
import database


def render():
    st.subheader("📊 Apparel Inventory Analytics Dashboard")
    st.markdown(
        "Executive summary of current warehouse stock levels, category distribution, "
        "and inventory health metrics."
    )

    metrics = database.get_dashboard_metrics()
    total_registered = metrics["total_registered"]
    total_quantity = metrics["total_quantity"]
    total_categories = metrics["total_categories"]
    available_garments = metrics["available_garments"]
    dist_df = metrics["distribution_df"]

    # Top KPI Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Total Registered Garments",
            value=f"{total_registered:,}",
            help="Total number of distinct garment SKUs registered in the database."
        )
    with col2:
        st.metric(
            label="Total Inventory Quantity",
            value=f"{total_quantity:,}",
            help="Sum of all individual apparel units currently stored across all locations."
        )
    with col3:
        st.metric(
            label="Garment Categories",
            value=total_categories,
            help="Number of unique garment types represented in the catalog."
        )
    with col4:
        st.metric(
            label="Available Garments (In-Stock)",
            value=f"{available_garments:,}",
            help="Number of garment SKUs with quantity greater than zero."
        )

    st.markdown("---")

    # If no data exists yet
    if total_registered == 0:
        st.info("No garment records found in the database. Go to 'Add Garment' to register your first item.")
        return

    # Visualizations section
    col_chart, col_breakdown = st.columns([3, 2])

    with col_chart:
        st.markdown("#### Inventory Distribution by Garment Type")
        st.caption("Total stock units stored per garment category")

        if not dist_df.empty:
            chart_data = dist_df.set_index("Garment Type")[["Total Units"]]
            st.bar_chart(chart_data, color="#2C3E50", height=320)
        else:
            st.write("No distribution data available.")

    with col_breakdown:
        st.markdown("#### Category Breakdown")
        st.caption("Detailed unit count and share of total inventory")

        if not dist_df.empty:
            breakdown_df = dist_df.copy()
            if total_quantity > 0:
                breakdown_df["Inventory Share"] = (breakdown_df["Total Units"] / total_quantity * 100).map(lambda x: f"{x:.1f}%")
            else:
                breakdown_df["Inventory Share"] = "0.0%"

            st.dataframe(
                breakdown_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Garment Type": st.column_config.TextColumn("Garment Type"),
                    "Unique SKUs": st.column_config.NumberColumn("SKU Count", format="%d"),
                    "Total Units": st.column_config.NumberColumn("Total Units", format="%d"),
                    "Inventory Share": st.column_config.TextColumn("Share (%)")
                }
            )

    st.markdown("---")

    # Inventory Health & Low-Stock Alerts (Essential for an Apparel Analyst)
    col_alert_hdr, col_alert_btn = st.columns([3, 1])
    with col_alert_hdr:
        st.markdown("#### ⚠️ Low-Stock & Out-of-Stock Watchlist")
        st.caption("Garments with 10 or fewer units remaining requiring procurement or restocking attention.")

    all_garments_df = database.get_all_garments_df()
    low_stock_df = all_garments_df[all_garments_df["quantity"] <= 10]

    with col_alert_btn:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        full_csv = all_garments_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📦 Export All Inventory (CSV)",
            data=full_csv,
            file_name=f"garment_inventory_{timestamp}.csv",
            mime="text/csv",
            use_container_width=True
        )

    if low_stock_df.empty:
        st.success("All registered garments have healthy stock levels (> 10 units).")
    else:
        st.dataframe(
            low_stock_df[["garment_id", "garment_name", "garment_type", "brand", "size", "quantity", "storage_location"]].rename(columns={
                "garment_id": "Garment ID",
                "garment_name": "Garment Name",
                "garment_type": "Category",
                "brand": "Brand",
                "size": "Size",
                "quantity": "Remaining Quantity",
                "storage_location": "Location"
            }),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Remaining Quantity": st.column_config.NumberColumn("Remaining Quantity", format="%d")
            }
        )


if __name__ == "__main__":
    render()
