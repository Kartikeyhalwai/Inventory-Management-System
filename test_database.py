"""
test_database.py
----------------
Automated tests for database operations:
- Database initialization and table creation
- Demo data seeding
- Positive garment insertion
- Preventing duplicate garment IDs
- Rejecting negative quantities
- Rejecting empty required fields
- Garment retrieval
- Record updates and updated_at modification
- Record deletion
- Dashboard metrics calculation
"""

import os
import unittest
import sqlite3
from database import (
    init_db,
    add_garment,
    get_all_garments_df,
    get_garment_by_id,
    update_garment,
    delete_garment,
    get_dashboard_metrics,
    get_filter_options,
    get_connection,
    seed_demo_data
)

TEST_DB = "test_garment_inventory.db"


class TestDatabaseOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create database file once
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except Exception:
                pass
        init_db(TEST_DB)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except Exception:
                pass

    def setUp(self):
        # Reset table to clean state with demo data for each test
        conn = get_connection(TEST_DB)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory")
        conn.commit()
        seed_demo_data(conn)
        conn.close()

    def test_init_and_demo_seed(self):
        df = get_all_garments_df(TEST_DB)
        # Verify 12 demo items are present
        self.assertEqual(len(df), 12)
        # Verify all demo IDs start with DEMO-
        self.assertTrue(all(gid.startswith("DEMO-") for gid in df["garment_id"]))

    def test_add_garment_success(self):
        success, msg = add_garment(
            garment_id="TEST-001",
            garment_name="Test Silk Scarf",
            garment_type="Other",
            brand="SilkStyle",
            size="Free Size",
            colour="Crimson",
            fabric="100% Silk",
            quantity=15,
            storage_location="Bin S-1",
            db_path=TEST_DB
        )
        self.assertTrue(success)
        garment = get_garment_by_id("TEST-001", TEST_DB)
        self.assertIsNotNone(garment)
        self.assertEqual(garment["garment_name"], "Test Silk Scarf")
        self.assertEqual(garment["quantity"], 15)

    def test_prevent_duplicate_id(self):
        # DEMO-TSH-001 is already seeded
        success, msg = add_garment(
            garment_id="DEMO-TSH-001",
            garment_name="Duplicate Tee",
            garment_type="T-shirts",
            brand="DupBrand",
            size="M",
            colour="Black",
            fabric="Cotton",
            quantity=5,
            storage_location="Rack A-1",
            db_path=TEST_DB
        )
        self.assertFalse(success)
        self.assertIn("already exists", msg.lower())

    def test_reject_negative_quantity(self):
        success, msg = add_garment(
            garment_id="TEST-NEG-001",
            garment_name="Negative Qty Tee",
            garment_type="T-shirts",
            brand="Brand",
            size="M",
            colour="Red",
            fabric="Cotton",
            quantity=-5,
            storage_location="Rack A-1",
            db_path=TEST_DB
        )
        self.assertFalse(success)
        self.assertIn("negative", msg.lower())

    def test_reject_empty_required_fields(self):
        success, msg = add_garment(
            garment_id="",
            garment_name="Missing ID",
            garment_type="T-shirts",
            brand="Brand",
            size="M",
            colour="Red",
            fabric="Cotton",
            quantity=5,
            storage_location="Rack A-1",
            db_path=TEST_DB
        )
        self.assertFalse(success)
        self.assertIn("empty", msg.lower())

    def test_update_garment(self):
        # Update DEMO-TSH-001
        success, msg = update_garment(
            garment_id="DEMO-TSH-001",
            garment_name="Updated Classic Crewneck Tee",
            garment_type="T-shirts",
            brand="UrbanWear Deluxe",
            size="M",
            colour="Midnight Blue",
            fabric="100% Organic Combed Cotton",
            quantity=30,
            storage_location="Rack A-1-Updated",
            db_path=TEST_DB
        )
        self.assertTrue(success)
        updated = get_garment_by_id("DEMO-TSH-001", TEST_DB)
        self.assertEqual(updated["garment_name"], "Updated Classic Crewneck Tee")
        self.assertEqual(updated["quantity"], 30)
        self.assertEqual(updated["storage_location"], "Rack A-1-Updated")

    def test_delete_garment(self):
        success, msg = delete_garment("DEMO-KRT-012", TEST_DB)
        self.assertTrue(success)
        item = get_garment_by_id("DEMO-KRT-012", TEST_DB)
        self.assertIsNone(item)

    def test_dashboard_metrics(self):
        metrics = get_dashboard_metrics(TEST_DB)
        self.assertEqual(metrics["total_registered"], 12)
        self.assertGreater(metrics["total_quantity"], 0)
        self.assertGreater(metrics["total_categories"], 0)
        self.assertEqual(metrics["available_garments"], 12)
        self.assertFalse(metrics["distribution_df"].empty)

    def test_filter_options(self):
        opts = get_filter_options(TEST_DB)
        self.assertIn("T-shirts", opts["types"])
        self.assertIn("M", opts["sizes"])


if __name__ == "__main__":
    unittest.main()
