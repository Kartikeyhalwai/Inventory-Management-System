"""
database.py
-----------
SQLite database management for the Garment Inventory Tracker.
Handles database initialization, schema creation, demo data seeding,
and all CRUD (Create, Read, Update, Delete) operations.
"""

import sqlite3
import os
from datetime import datetime
import pandas as pd

# Define the database filename
DB_NAME = "garment_inventory.db"
# Use the directory where this script resides to locate the database reliably
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, DB_NAME)

# Standard predefined garment types
GARMENT_TYPES = [
    "T-shirts",
    "Shirts",
    "Jeans",
    "Trousers",
    "Jackets",
    "Dresses",
    "Kurtas",
    "Other"
]

# Standard size options commonly used in apparel retail
STANDARD_SIZES = ["XS", "S", "M", "L", "XL", "XXL", "28", "30", "32", "34", "36", "38", "Free Size"]


def get_connection(db_path=DB_PATH):
    """
    Establish and return a connection to the SQLite database.
    Sets a 15-second busy timeout so concurrent/rapid accesses never block.
    """
    conn = sqlite3.connect(db_path, timeout=15.0)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn


def init_db(db_path=DB_PATH):
    """
    Initialize the SQLite database.
    Creates the 'inventory' table if it does not already exist.
    If the table is newly created and empty, seeds initial demo records.
    Ensures existing user data is never overwritten.
    """
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        # Create the inventory table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                garment_id TEXT PRIMARY KEY,
                garment_name TEXT NOT NULL,
                garment_type TEXT NOT NULL,
                brand TEXT NOT NULL,
                size TEXT NOT NULL,
                colour TEXT NOT NULL,
                fabric TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity >= 0),
                storage_location TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
        """)
        conn.commit()

        # Check if table has any existing records
        cursor.execute("SELECT COUNT(*) FROM inventory")
        count = cursor.fetchone()[0]

        # Seed demo records only if database is brand new and empty
        if count == 0:
            seed_demo_data(conn)
    finally:
        conn.close()


def seed_demo_data(conn):
    """
    Insert a set of fictional demo records to allow immediate application testing.
    All demo records use IDs prefixed with 'DEMO-' so they are clearly identifiable.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    demo_records = [
        (
            "DEMO-TSH-001",
            "Classic Crewneck Tee",
            "T-shirts",
            "UrbanWear",
            "M",
            "Navy Blue",
            "100% Combed Cotton",
            25,
            "Rack A-1",
            now,
            now
        ),
        (
            "DEMO-TSH-002",
            "V-Neck Performance Tee",
            "T-shirts",
            "FitCore",
            "L",
            "Heather Grey",
            "Polyester-Elastane Blend",
            18,
            "Rack A-2",
            now,
            now
        ),
        (
            "DEMO-SHT-003",
            "Oxford Button-Down Shirt",
            "Shirts",
            "HeritageCloth",
            "L",
            "Sky Blue",
            "100% Oxford Cotton",
            14,
            "Rack B-1",
            now,
            now
        ),
        (
            "DEMO-SHT-004",
            "Casual Linen Shirt",
            "Shirts",
            "BreezeMode",
            "M",
            "White",
            "Pure Linen",
            10,
            "Rack B-2",
            now,
            now
        ),
        (
            "DEMO-JNS-005",
            "Slim Fit Denim Jeans",
            "Jeans",
            "IndigoCo",
            "32",
            "Dark Indigo",
            "98% Cotton 2% Spandex",
            22,
            "Shelf C-1",
            now,
            now
        ),
        (
            "DEMO-JNS-006",
            "Relaxed Straight Leg Denim",
            "Jeans",
            "DenimWorks",
            "34",
            "Light Vintage Blue",
            "100% Cotton Denim",
            15,
            "Shelf C-2",
            now,
            now
        ),
        (
            "DEMO-TRS-007",
            "Tailored Chino Trousers",
            "Trousers",
            "HeritageCloth",
            "32",
            "Khaki",
            "97% Cotton 3% Spandex",
            16,
            "Shelf D-1",
            now,
            now
        ),
        (
            "DEMO-TRS-008",
            "Pleated Formal Trousers",
            "Trousers",
            "ExecutiveLine",
            "34",
            "Charcoal Grey",
            "Wool Blend",
            12,
            "Shelf D-2",
            now,
            now
        ),
        (
            "DEMO-JKT-009",
            "All-Weather Bomber Jacket",
            "Jackets",
            "NordicOuterwear",
            "L",
            "Olive Green",
            "Nylon Shell with Polyfill",
            8,
            "Rack E-1",
            now,
            now
        ),
        (
            "DEMO-JKT-010",
            "Classic Trucker Denim Jacket",
            "Jackets",
            "IndigoCo",
            "M",
            "Medium Stonewash",
            "100% Heavyweight Cotton",
            6,
            "Rack E-2",
            now,
            now
        ),
        (
            "DEMO-DRS-011",
            "Floral Wrap Midi Dress",
            "Dresses",
            "AuroraStudio",
            "S",
            "Emerald Floral",
            "Viscose Rayon",
            9,
            "Hanger F-1",
            now,
            now
        ),
        (
            "DEMO-KRT-012",
            "Embroidered Straight Kurta",
            "Kurtas",
            "Ethniciq",
            "L",
            "Maroon",
            "Chanderi Silk Cotton",
            11,
            "Hanger F-2",
            now,
            now
        )
    ]

    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO inventory (
            garment_id, garment_name, garment_type, brand, size, colour,
            fabric, quantity, storage_location, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, demo_records)
    conn.commit()


def add_garment(garment_id, garment_name, garment_type, brand, size, colour, fabric, quantity, storage_location, db_path=DB_PATH):
    """
    Validate and insert a new garment into the inventory table.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    # Clean strings
    gid = str(garment_id).strip()
    name = str(garment_name).strip()
    gtype = str(garment_type).strip()
    bname = str(brand).strip()
    sz = str(size).strip()
    col = str(colour).strip()
    fab = str(fabric).strip()
    loc = str(storage_location).strip()

    # Validate required fields
    if not gid:
        return False, "Garment ID cannot be empty."
    if not name:
        return False, "Garment Name cannot be empty."
    if not gtype:
        return False, "Garment Type cannot be empty."
    if not bname:
        return False, "Brand cannot be empty."
    if not sz:
        return False, "Size cannot be empty."
    if not col:
        return False, "Colour cannot be empty."
    if not fab:
        return False, "Fabric / Material cannot be empty."
    if not loc:
        return False, "Storage Location cannot be empty."

    # Validate quantity
    try:
        qty = int(quantity)
        if qty < 0:
            return False, "Quantity cannot be negative. Please enter 0 or more."
    except (ValueError, TypeError):
        return False, "Quantity must be a valid non-negative whole number."

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO inventory (
                garment_id, garment_name, garment_type, brand, size, colour,
                fabric, quantity, storage_location, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (gid, name, gtype, bname, sz, col, fab, qty, loc, now, now))
        conn.commit()
        return True, f"Garment '{name}' (ID: {gid}) registered successfully!"
    except sqlite3.IntegrityError as e:
        err_msg = str(e).lower()
        if "unique" in err_msg or "primary key" in err_msg:
            return False, f"Error: A garment with ID '{gid}' already exists in the inventory. Garment IDs must be unique."
        elif "check" in err_msg:
            return False, "Error: Quantity must be non-negative (CHECK constraint failed)."
        return False, f"Database integrity error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected database error: {str(e)}"
    finally:
        conn.close()


def get_all_garments_df(db_path=DB_PATH):
    """
    Fetch all inventory records as a pandas DataFrame.
    """
    conn = get_connection(db_path)
    try:
        query = """
            SELECT 
                garment_id,
                garment_name,
                garment_type,
                brand,
                size,
                colour,
                fabric,
                quantity,
                storage_location,
                created_at,
                updated_at
            FROM inventory
            ORDER BY created_at DESC
        """
        df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()


def get_garment_by_id(garment_id, db_path=DB_PATH):
    """
    Retrieve a single garment record by its unique Garment ID.
    Returns a dict with garment details, or None if not found.
    """
    if not garment_id:
        return None
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM inventory WHERE garment_id = ?
        """, (str(garment_id).strip(),))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    finally:
        conn.close()


def update_garment(garment_id, garment_name, garment_type, brand, size, colour, fabric, quantity, storage_location, db_path=DB_PATH):
    """
    Update an existing garment record.
    Updates the updated_at timestamp automatically.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    gid = str(garment_id).strip()
    name = str(garment_name).strip()
    gtype = str(garment_type).strip()
    bname = str(brand).strip()
    sz = str(size).strip()
    col = str(colour).strip()
    fab = str(fabric).strip()
    loc = str(storage_location).strip()

    if not gid:
        return False, "Garment ID is missing."
    if not name:
        return False, "Garment Name cannot be empty."
    if not gtype:
        return False, "Garment Type cannot be empty."
    if not bname:
        return False, "Brand cannot be empty."
    if not sz:
        return False, "Size cannot be empty."
    if not col:
        return False, "Colour cannot be empty."
    if not fab:
        return False, "Fabric / Material cannot be empty."
    if not loc:
        return False, "Storage Location cannot be empty."

    try:
        qty = int(quantity)
        if qty < 0:
            return False, "Quantity cannot be negative."
    except (ValueError, TypeError):
        return False, "Quantity must be a valid whole number."

    # Check existence
    existing = get_garment_by_id(gid, db_path=db_path)
    if not existing:
        return False, f"Garment with ID '{gid}' does not exist."

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE inventory
            SET garment_name = ?,
                garment_type = ?,
                brand = ?,
                size = ?,
                colour = ?,
                fabric = ?,
                quantity = ?,
                storage_location = ?,
                updated_at = ?
            WHERE garment_id = ?
        """, (name, gtype, bname, sz, col, fab, qty, loc, now, gid))
        conn.commit()
        return True, f"Garment '{name}' (ID: {gid}) updated successfully!"
    except sqlite3.IntegrityError as e:
        return False, f"Database integrity error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error while updating: {str(e)}"
    finally:
        conn.close()


def delete_garment(garment_id, db_path=DB_PATH):
    """
    Delete a garment record by Garment ID.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    gid = str(garment_id).strip()
    if not gid:
        return False, "Garment ID is missing."

    existing = get_garment_by_id(gid, db_path=db_path)
    if not existing:
        return False, f"Garment with ID '{gid}' not found."

    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE garment_id = ?", (gid,))
        conn.commit()
        return True, f"Garment '{existing['garment_name']}' (ID: {gid}) was successfully deleted."
    except Exception as e:
        return False, f"Unexpected error while deleting: {str(e)}"
    finally:
        conn.close()


def get_dashboard_metrics(db_path=DB_PATH):
    """
    Calculate summary metrics and category distributions for the dashboard.
    
    Returns:
        dict containing:
            - total_registered: count of distinct garment SKUs
            - total_quantity: sum of total garment units in inventory
            - total_categories: number of distinct garment types
            - available_garments: number of garment items currently in stock (quantity > 0)
            - distribution_df: DataFrame with garment_type and total units
    """
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()

        # Total registered garments (SKUs)
        cursor.execute("SELECT COUNT(*) FROM inventory")
        total_registered = cursor.fetchone()[0] or 0

        # Total inventory quantity (units)
        cursor.execute("SELECT SUM(quantity) FROM inventory")
        total_qty_row = cursor.fetchone()[0]
        total_quantity = total_qty_row if total_qty_row is not None else 0

        # Number of garment categories
        cursor.execute("SELECT COUNT(DISTINCT garment_type) FROM inventory")
        total_categories = cursor.fetchone()[0] or 0

        # Number of available garments (records with quantity > 0)
        cursor.execute("SELECT COUNT(*) FROM inventory WHERE quantity > 0")
        available_garments = cursor.fetchone()[0] or 0

        # Distribution by garment type
        dist_query = """
            SELECT 
                garment_type AS "Garment Type", 
                COUNT(*) AS "Unique SKUs",
                SUM(quantity) AS "Total Units"
            FROM inventory
            GROUP BY garment_type
            ORDER BY "Total Units" DESC
        """
        dist_df = pd.read_sql_query(dist_query, conn)

        return {
            "total_registered": total_registered,
            "total_quantity": total_quantity,
            "total_categories": total_categories,
            "available_garments": available_garments,
            "distribution_df": dist_df
        }
    finally:
        conn.close()


def get_filter_options(db_path=DB_PATH):
    """
    Fetch distinct values for filters: types, sizes, colours, and fabrics.
    """
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()

        def fetch_distinct(col):
            cursor.execute(f"SELECT DISTINCT {col} FROM inventory WHERE {col} IS NOT NULL AND {col} != '' ORDER BY {col} ASC")
            return [r[0] for r in cursor.fetchall()]

        types = fetch_distinct("garment_type")
        sizes = fetch_distinct("size")
        colours = fetch_distinct("colour")
        fabrics = fetch_distinct("fabric")
        brands = fetch_distinct("brand")

        return {
            "types": types,
            "sizes": sizes,
            "colours": colours,
            "fabrics": fabrics,
            "brands": brands
        }
    finally:
        conn.close()
