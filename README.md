# 👔 Garment Inventory Tracker

A clean, reliable, and functional **Garment Inventory Tracker** built with **Python**, **Streamlit**, **SQLite**, and **Pandas**.

Designed for an **Apparel Analyst Intern** portfolio, this application demonstrates core apparel merchandising and operations skills: structured garment classification, accurate record-keeping, multi-attribute search and filtering, real-time stock updates, and data persistence.

---

## 📌 Project Overview

In apparel manufacturing and retail distribution, accurate stock monitoring prevents stock-outs, minimizes inventory holding costs, and ensures smooth fulfillment. This internal inventory management tool allows apparel analysts and stockroom coordinators to:

1. **Monitor Inventory Analytics:** View live KPIs (total SKUs, total units, category counts, in-stock items) and category stock distributions.
2. **Register Garments (Add):** Enforce structured cataloging with unique Garment IDs, apparel categories (including custom types), fabric composition, sizes, and stockroom locations.
3. **Inspect & Search (View):** Real-time multi-attribute filtering by category, size, colour, and fabric with case-insensitive search by ID or style name.
4. **Update Records:** Safely modify stock quantities, locations, and garment attributes without creating duplicate records, maintaining audit timestamps.
5. **Retire Stock (Delete):** Permanently remove discontinued or damaged garments with mandatory user confirmation to prevent accidental data loss.
6. **Export Data:** Export filtered inventory views or the complete catalog to CSV for external reporting and spreadsheet analysis.

---

## 🛠️ Technology Stack

Only lightweight, standard, beginner-friendly tools are used:

| Technology | Purpose |
| :--- | :--- |
| **Python 3.10+** | Core application logic and validation rules |
| **Streamlit** | Interactive, clean web user interface |
| **SQLite (`sqlite3`)** | Persistent relational database storage (`garment_inventory.db`) |
| **Pandas** | High-performance tabular data manipulation, filtering, and CSV export |

---

## 📁 Project Structure

```text
garment-inventory-tracker/
│
├── app.py                      # Main application entry point & sidebar navigation
├── database.py                 # SQLite database logic, queries, and CRUD operations
├── requirements.txt            # Project dependencies (streamlit, pandas)
├── garment_inventory.db        # SQLite database file (created automatically)
├── README.md                   # Setup guide, documentation, and testing walkthrough
├── test_database.py            # Unit tests for database operations
├── test_app_scenarios.py       # End-to-end tests for all 9 core operational scenarios
│
├── pages/
│   ├── dashboard.py            # Executive KPI metrics & category distribution charts
│   ├── add_garment.py          # Garment registration form with input validation
│   ├── view_inventory.py       # Structured inventory table, search, filters & CSV export
│   ├── update_garment.py       # Safe record modification & quantity adjustments
│   └── delete_garment.py       # Record deletion with mandatory confirmation
│
├── assets/
│   └── style.css               # Clean styling configuration
└── .streamlit/
    └── config.toml             # Professional neutral theme & sidebar layout settings
```

---

## 🚀 Quick Start Guide

### 1. Clone or Open the Repository
Open your command terminal (PowerShell, Command Prompt, or Bash) and navigate to the project directory:
```bash
cd Inventory-Management-System
```

### 2. Install Required Dependencies
Install the required packages using `pip`:
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
Run the Streamlit application:
```bash
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`.

---

## 🗄️ Database Design

The application stores records in a local SQLite database named **`garment_inventory.db`**.

### Table Schema: `inventory`

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `garment_id` | `TEXT` | `PRIMARY KEY` | Unique SKU identifier (e.g., `DEMO-TSH-001`) |
| `garment_name` | `TEXT` | `NOT NULL` | Garment style name or description |
| `garment_type` | `TEXT` | `NOT NULL` | Apparel category (T-shirts, Shirts, Jeans, etc.) |
| `brand` | `TEXT` | `NOT NULL` | Brand or internal label |
| `size` | `TEXT` | `NOT NULL` | Garment size (XS, S, M, L, XL, 32, 34, etc.) |
| `colour` | `TEXT` | `NOT NULL` | Primary garment colour |
| `fabric` | `TEXT` | `NOT NULL` | Fabric material composition |
| `quantity` | `INTEGER` | `NOT NULL, CHECK (quantity >= 0)` | Stock units available (must be 0 or more) |
| `storage_location`| `TEXT` | `NOT NULL` | Warehouse / stockroom bin or rack |
| `created_at` | `TEXT` | `NOT NULL` | Creation timestamp (`YYYY-MM-DD HH:MM:SS`) |
| `updated_at` | `TEXT` | `NOT NULL` | Last modified timestamp |

### Key Validation & Integrity Rules
- **Unique Primary Key:** Garment IDs cannot be duplicated. Attempting to add an existing ID produces a user-friendly error.
- **Non-negative Quantities:** Validated in Python and backed by a database `CHECK (quantity >= 0)` constraint.
- **No Empty Required Fields:** Prevents incomplete records from polluting inventory tables.
- **Data Persistence:** The database automatically persists across application restarts; demo records are seeded only if the database is brand new and empty.

---

## 🧪 Sample Demo Data

The database comes pre-seeded with 12 realistic demo records spanning standard apparel categories:

| Garment ID | Style Name | Category | Brand | Size | Colour | Fabric | Qty | Location |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| `DEMO-TSH-001` | Classic Crewneck Tee | T-shirts | UrbanWear | M | Navy Blue | 100% Combed Cotton | 25 | Rack A-1 |
| `DEMO-TSH-002` | V-Neck Performance Tee | T-shirts | FitCore | L | Heather Grey | Polyester-Elastane | 18 | Rack A-2 |
| `DEMO-SHT-003` | Oxford Button-Down | Shirts | HeritageCloth | L | Sky Blue | 100% Oxford Cotton | 14 | Rack B-1 |
| `DEMO-SHT-004` | Casual Linen Shirt | Shirts | BreezeMode | M | White | Pure Linen | 10 | Rack B-2 |
| `DEMO-JNS-005` | Slim Fit Denim Jeans | Jeans | IndigoCo | 32 | Dark Indigo | 98% Cotton 2% Spandex | 22 | Shelf C-1 |
| `DEMO-JNS-006` | Relaxed Straight Denim | Jeans | DenimWorks | 34 | Light Vintage Blue | 100% Cotton Denim | 15 | Shelf C-2 |
| `DEMO-TRS-007` | Tailored Chino Trousers | Trousers | HeritageCloth | 32 | Khaki | 97% Cotton 3% Spandex | 16 | Shelf D-1 |
| `DEMO-TRS-008` | Pleated Formal Trousers | Trousers | ExecutiveLine | 34 | Charcoal Grey | Wool Blend | 12 | Shelf D-2 |
| `DEMO-JKT-009` | All-Weather Bomber Jacket| Jackets | NordicOuterwear| L | Olive Green | Nylon with Polyfill | 8 | Rack E-1 |
| `DEMO-JKT-010` | Classic Trucker Jacket | Jackets | IndigoCo | M | Medium Stonewash | Heavyweight Cotton | 6 | Rack E-2 |
| `DEMO-DRS-011` | Floral Wrap Midi Dress | Dresses | AuroraStudio | S | Emerald Floral | Viscose Rayon | 9 | Hanger F-1 |
| `DEMO-KRT-012` | Embroidered Kurta | Kurtas | Ethniciq | L | Maroon | Chanderi Silk Cotton | 11 | Hanger F-2 |

---

## 🔍 Application Features

### 1. 📊 Dashboard
- **Metric Cards:** Real-time counts for Total SKUs, Total Inventory Units, Category Count, and In-Stock Garments.
- **Category Distribution Chart:** Clean bar chart displaying total units stored per apparel type.
- **Category Breakdown Table:** Exact unit counts and percentage share of total warehouse inventory.
- **Low-Stock Watchlist:** Highlights items with 10 or fewer units remaining for proactive replenishment.

### 2. ➕ Add Garment
- Full registration form with 9 structured fields.
- Predefined categories with support for custom "Other" types.
- Standard apparel sizes (XS to XXL, waist sizes 28 to 38, Free Size, and custom sizes).
- Real-time validation preventing negative quantities and duplicate IDs.

### 3. 📋 View Inventory & CSV Export
- Search across Garment ID and Garment Name simultaneously.
- Multi-filter dropdowns for Garment Type, Size, Colour, and Fabric.
- Live metric counters indicating total matching records and total units in view.
- Dual CSV export options:
  - **Export Current View:** Downloads the exact filtered subset.
  - **Export Full Inventory:** Downloads the entire catalog.

### 4. ✏️ Update Garment
- Dropdown selector to choose any registered garment.
- Displays original registration timestamp and last modified timestamp.
- **Primary key protection:** Garment ID is locked as read-only to prevent duplicate record generation.
- Modifies existing SQLite record and automatically updates `updated_at`.

### 5. 🗑️ Delete Garment
- Choose any garment SKU to inspect all its attributes prior to deletion.
- **Safe deletion protocol:** Requires checking an explicit confirmation checkbox before the delete action can execute.

---

## 🧪 Testing Walkthrough

The project includes 18 automated unit and integration tests covering all requirements:

### Running the Test Suites:
Run all tests using Python's standard unittest runner:
```bash
python -m unittest discover -s . -p "test_*.py"
```

### Tested Scenarios:
1. **Registering a new garment:** Successfully inserts a valid record and verifies fields in SQLite.
2. **Preventing duplicate IDs:** Rejects insertion of an existing Garment ID with a clear error.
3. **Rejecting negative quantities:** Rejects negative integer entries at both validation and database constraint levels.
4. **Searching for garments:** Verifies case-insensitive partial substring searching by ID and Name.
5. **Multi-attribute filtering:** Validates filtering combinations across Category and Size.
6. **Updating records:** Confirms record modification, preservation of primary key, and automatic `updated_at` timestamp refresh.
7. **Deleting records with confirmation:** Validates permanent removal from the database.
8. **Exporting inventory to CSV:** Verifies CSV generation and validates structure by parsing with Pandas.
9. **Persistence across application restarts:** Simulates application shutdown and re-initialization, verifying user records remain intact.
