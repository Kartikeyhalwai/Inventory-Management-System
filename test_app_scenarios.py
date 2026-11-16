"""
test_app_scenarios.py
---------------------
End-to-End automated validation of all 9 core scenarios specified in the project requirements:
1. Registering a new garment
2. Preventing duplicate garment IDs
3. Rejecting negative quantities
4. Searching for an existing garment
5. Filtering garments by type and size
6. Updating garment information (preventing duplicates, updating timestamp)
7. Deleting a garment (verifying removal)
8. Exporting inventory to CSV (verifying contents and parseability)
9. Restarting application / re-initialization (verifying persistence without overwriting user data)
"""

import os
import io
import time
import unittest
import pandas as pd
import database

E2E_DB = "e2e_test_garment_inventory.db"


class TestGarmentInventoryE2E(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(E2E_DB):
            try:
                os.remove(E2E_DB)
            except Exception:
                pass
        # Initialize database with demo data
        database.init_db(E2E_DB)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(E2E_DB):
            try:
                os.remove(E2E_DB)
            except Exception:
                pass

    def test_01_register_new_garment(self):
        """Scenario 1: Registering a new garment."""
        success, msg = database.add_garment(
            garment_id="GAR-JKT-101",
            garment_name="Waterproof Trekking Jacket",
            garment_type="Jackets",
            brand="AlpinePro",
            size="XL",
            colour="Forest Green",
            fabric="Gore-Tex 3-Layer",
            quantity=14,
            storage_location="Rack H-3",
            db_path=E2E_DB
        )
        self.assertTrue(success, f"Registration failed: {msg}")
        self.assertIn("registered successfully", msg)

        # Verify record exists in DB
        record = database.get_garment_by_id("GAR-JKT-101", db_path=E2E_DB)
        self.assertIsNotNone(record)
        self.assertEqual(record["garment_name"], "Waterproof Trekking Jacket")
        self.assertEqual(record["quantity"], 14)
        self.assertEqual(record["storage_location"], "Rack H-3")
        print(" [PASS] Scenario 1: Registering a new garment succeeded.")

    def test_02_prevent_duplicate_garment_id(self):
        """Scenario 2: Preventing duplicate garment IDs."""
        # Attempt to insert same ID GAR-JKT-101
        success, msg = database.add_garment(
            garment_id="GAR-JKT-101",
            garment_name="Duplicate Jacket",
            garment_type="Jackets",
            brand="CopyCat",
            size="M",
            colour="Black",
            fabric="Polyester",
            quantity=5,
            storage_location="Bin 9",
            db_path=E2E_DB
        )
        self.assertFalse(success, "Duplicate ID was erroneously accepted!")
        self.assertIn("already exists", msg.lower())
        print(" [PASS] Scenario 2: Preventing duplicate garment IDs succeeded.")

    def test_03_reject_negative_quantities(self):
        """Scenario 3: Rejecting negative quantities."""
        success, msg = database.add_garment(
            garment_id="GAR-ERR-001",
            garment_name="Faulty Stock Garment",
            garment_type="Shirts",
            brand="TestBrand",
            size="L",
            colour="Blue",
            fabric="Cotton",
            quantity=-10,
            storage_location="Rack 1",
            db_path=E2E_DB
        )
        self.assertFalse(success, "Negative quantity was erroneously accepted!")
        self.assertIn("negative", msg.lower())
        print(" [PASS] Scenario 3: Rejecting negative quantities succeeded.")

    def test_04_search_existing_garment(self):
        """Scenario 4: Searching for an existing garment."""
        df = database.get_all_garments_df(db_path=E2E_DB)
        
        # Search by ID
        search_id = "demo-tsh-001"
        res_by_id = df[df["garment_id"].str.lower().str.contains(search_id)]
        self.assertEqual(len(res_by_id), 1)
        self.assertEqual(res_by_id.iloc[0]["garment_name"], "Classic Crewneck Tee")

        # Search by Name
        search_name = "denim"
        res_by_name = df[df["garment_name"].str.lower().str.contains(search_name)]
        self.assertGreaterEqual(len(res_by_name), 2)
        print(" [PASS] Scenario 4: Searching for existing garments succeeded.")

    def test_05_filter_by_type_and_size(self):
        """Scenario 5: Filtering garments by type and size."""
        df = database.get_all_garments_df(db_path=E2E_DB)

        # Filter by Type == "Jeans" and Size == "32"
        filtered = df[(df["garment_type"] == "Jeans") & (df["size"] == "32")]
        self.assertGreaterEqual(len(filtered), 1)
        self.assertEqual(filtered.iloc[0]["garment_id"], "DEMO-JNS-005")

        # Filter by Type == "T-shirts" and Size == "M"
        tsh_m = df[(df["garment_type"] == "T-shirts") & (df["size"] == "M")]
        self.assertGreaterEqual(len(tsh_m), 1)
        self.assertEqual(tsh_m.iloc[0]["garment_id"], "DEMO-TSH-001")
        print(" [PASS] Scenario 5: Filtering by type and size succeeded.")

    def test_06_update_garment_information(self):
        """Scenario 6: Updating garment information without creating duplicates."""
        initial_df = database.get_all_garments_df(db_path=E2E_DB)
        initial_count = len(initial_df)

        original_record = database.get_garment_by_id("GAR-JKT-101", db_path=E2E_DB)
        orig_created_at = original_record["created_at"]
        orig_updated_at = original_record["updated_at"]

        # Ensure small timestamp difference for test
        time.sleep(1.0)

        # Update record
        success, msg = database.update_garment(
            garment_id="GAR-JKT-101",
            garment_name="Waterproof Trekking Jacket Pro",
            garment_type="Jackets",
            brand="AlpinePro Elite",
            size="XXL",
            colour="Dark Olive",
            fabric="Gore-Tex Pro 3-Layer",
            quantity=28,
            storage_location="Warehouse Bay 4",
            db_path=E2E_DB
        )
        self.assertTrue(success, f"Update failed: {msg}")

        # Verify count did NOT increase (no duplicate created)
        after_df = database.get_all_garments_df(db_path=E2E_DB)
        self.assertEqual(len(after_df), initial_count, "Update incorrectly created a duplicate row!")

        # Verify updated fields and new updated_at
        updated_record = database.get_garment_by_id("GAR-JKT-101", db_path=E2E_DB)
        self.assertEqual(updated_record["garment_name"], "Waterproof Trekking Jacket Pro")
        self.assertEqual(updated_record["brand"], "AlpinePro Elite")
        self.assertEqual(updated_record["size"], "XXL")
        self.assertEqual(updated_record["quantity"], 28)
        self.assertEqual(updated_record["storage_location"], "Warehouse Bay 4")
        self.assertEqual(updated_record["created_at"], orig_created_at)
        self.assertNotEqual(updated_record["updated_at"], orig_updated_at)
        print(" [PASS] Scenario 6: Updating garment records and timestamp succeeded.")

    def test_07_delete_garment(self):
        """Scenario 7: Deleting a garment."""
        # Insert a temporary item to delete
        database.add_garment(
            garment_id="GAR-DEL-999",
            garment_name="Discontinued Item",
            garment_type="Other",
            brand="OldBrand",
            size="S",
            colour="Grey",
            fabric="Rayon",
            quantity=2,
            storage_location="Dumpster Area",
            db_path=E2E_DB
        )
        self.assertIsNotNone(database.get_garment_by_id("GAR-DEL-999", db_path=E2E_DB))

        # Perform deletion
        success, msg = database.delete_garment("GAR-DEL-999", db_path=E2E_DB)
        self.assertTrue(success, f"Delete failed: {msg}")

        # Verify it no longer exists
        self.assertIsNone(database.get_garment_by_id("GAR-DEL-999", db_path=E2E_DB))
        print(" [PASS] Scenario 7: Deleting garment records succeeded.")

    def test_08_export_inventory_csv(self):
        """Scenario 8: Exporting inventory to CSV."""
        df = database.get_all_garments_df(db_path=E2E_DB)
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        
        # Verify CSV format by parsing it back into pandas
        imported_df = pd.read_csv(io.BytesIO(csv_bytes))
        self.assertEqual(len(imported_df), len(df))
        self.assertIn("garment_id", imported_df.columns)
        self.assertIn("quantity", imported_df.columns)
        self.assertIn("fabric", imported_df.columns)
        self.assertIn("storage_location", imported_df.columns)
        print(" [PASS] Scenario 8: Exporting inventory to CSV succeeded.")

    def test_09_persistence_after_restart(self):
        """Scenario 9: Restarting the application and verifying records remain saved."""
        # Note the records before "restart"
        df_before = database.get_all_garments_df(db_path=E2E_DB)
        ids_before = set(df_before["garment_id"])

        # Simulate application restart:
        # 1. New application entry point triggers database.init_db()
        database.init_db(E2E_DB)

        # 2. Re-fetch all garments
        df_after = database.get_all_garments_df(db_path=E2E_DB)
        ids_after = set(df_after["garment_id"])

        # Verify user data was not overwritten or wiped
        self.assertEqual(ids_before, ids_after)
        self.assertEqual(len(df_before), len(df_after))
        
        # Check that user-added garment GAR-JKT-101 is still present with its updated quantity
        retained = database.get_garment_by_id("GAR-JKT-101", db_path=E2E_DB)
        self.assertIsNotNone(retained)
        self.assertEqual(retained["quantity"], 28)
        self.assertEqual(retained["garment_name"], "Waterproof Trekking Jacket Pro")
        print(" [PASS] Scenario 9: Database persistence across application restarts verified.")


if __name__ == "__main__":
    unittest.main()
