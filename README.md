# Pro Analytics 02 Python Starter Repository

> Use this repo to start a professional Python project.
- Additional information: <https://github.com/jacksongentzell/smart-store-jacksongentzell>
- Project organization: [STRUCTURE](./STRUCTURE.md)
- Build professional skills:
  - **Environment Management**: Every project in isolation
  - **Code Quality**: Automated checks for fewer bugs
  - **Documentation**: Use modern project documentation tools
  - **Testing**: Prove your code works
  - **Version Control**: Collaborate professionally

---

## WORKFLOW 1. Set Up Your Machine

Proper setup is critical.
Complete each step in the following guide and verify carefully.

- [SET UP MACHINE](./SET_UP_MACHINE.md)

---

## WORKFLOW 2. Set Up Your Project

After verifying your machine is set up, set up a new Python project by copying this template.
Complete each step in the following guide.

- [SET UP PROJECT](./SET_UP_PROJECT.md)

It includes the critical commands to set up your local environment (and activate it):

```shell
uv venv
uv python pin 3.12
uv sync --extra dev --extra docs --upgrade
uv run pre-commit install
uv run python --version
```

**Windows (PowerShell):**

```shell
.\.venv\Scripts\activate
```

**macOS / Linux / WSL:**

```shell
source .venv/bin/activate
```

---

## WORKFLOW 3. Daily Workflow

Please ensure that the prior steps have been verified before continuing.
When working on a project, we open just that project in VS Code.

### 3.1 Git Pull from GitHub

Always start with `git pull` to check for any changes made to the GitHub repo.

```shell
git pull
```

### 3.2 Run Checks as You Work

This mirrors real work where we typically:

1. Update dependencies (for security and compatibility).
2. Clean unused cached packages to free space.
3. Use `git add .` to stage all changes.
4. Run ruff and fix minor issues.
5. Update pre-commit periodically.
6. Run pre-commit quality checks on all code files (**twice if needed**, the first pass may fix things).
7. Run tests.

In VS Code, open your repository, then open a terminal (Terminal / New Terminal) and run the following commands one at a time to check the code.

```shell
uv sync --extra dev --extra docs --upgrade
uv cache clean
git add .
uvx ruff check --fix
uvx pre-commit autoupdate
uv run pre-commit run --all-files
git add .
uv run pytest
```

NOTE: The second `git add .` ensures any automatic fixes made by Ruff or pre-commit are included before testing or committing.

<details>
<summary>Click to see a note on best practices</summary>

`uvx` runs the latest version of a tool in an isolated cache, outside the virtual environment.
This keeps the project light and simple, but behavior can change when the tool updates.
For fully reproducible results, or when you need to use the local `.venv`, use `uv run` instead.

</details>

### 3.3 Build Project Documentation

Make sure you have current doc dependencies, then build your docs, fix any errors, and serve them locally to test.

```shell
uv run mkdocs build --strict
uv run mkdocs serve
```

- After running the serve command, the local URL of the docs will be provided. To open the site, press **CTRL and click** the provided link (at the same time) to view the documentation. On a Mac, use **CMD and click**.
- Press **CTRL c** (at the same time) to stop the hosting process.

### 3.4 Execute

This project includes demo code.
Run the demo Python modules to confirm everything is working.

In VS Code terminal, run:

```shell
uv run python -m analytics_project.demo_module_basics
uv run python -m analytics_project.demo_module_languages
uv run python -m analytics_project.demo_module_stats
uv run python -m analytics_project.demo_module_viz
```

You should see:

- Log messages in the terminal
- Greetings in several languages
- Simple statistics
- A chart window open (close the chart window to continue).

If this works, your project is ready! If not, check:

- Are you in the right folder? (All terminal commands are to be run from the root project folder.)
- Did you run the full `uv sync --extra dev --extra docs --upgrade` command?
- Are there any error messages? (ask for help with the exact error)

---

### 3.5 Git add-commit-push to GitHub

Anytime we make working changes to code is a good time to git add-commit-push to GitHub.

1. Stage your changes with git add.
2. Commit your changes with a useful message in quotes.
3. Push your work to GitHub.

```shell
git add .
git commit -m "describe your change in quotes"
git push -u origin main
```

This will trigger the GitHub Actions workflow and publish your documentation via GitHub Pages.

### 3.6 Modify and Debug

With a working version safe in GitHub, start making changes to the code.

Before starting a new session, remember to do a `git pull` and keep your tools updated.

Each time forward progress is made, remember to git add-commit-push.

## ✅ Project Progress – Jackson Gentzell

### Environment & Setup

So far I have completed the initial setup tasks for the Smart Store project.

---

### Steps Completed

1. **Cloned the repository from GitHub**
```
git clone https://github.com/jacksongentzell/smart-store-jacksongentzell.git
```
- Opened the project in VS Code
- Verified folder structure:
```
README.md
data/raw/
src/analytics_project/
.venv/
```

2. **Set up the local Python environment**
```
uv venv
uv run python --version
```
- Confirmed environment activation

3. **Added the data preparation script**
- Created `src/analytics_project/data_prep.py`
- Copied starter code from instructor repository

4. **Executed the data preparation module**
```
uv run python -m analytics_project.data_prep
```
**Results:**
- `customers_data.csv`: 201 rows × 4 columns
- `products_data.csv`: 100 rows × 4 columns
- `sales_data.csv`: 2001 rows × 7 columns
- Log file created: `project.log`
- Data preparation completed successfully

5. **Committed and pushed to GitHub**
```
git add .
git commit -m "Add and verify data_prep module"
git push -u origin main
```

6. **Updated README.md**
- Added setup documentation and workflow summary
- Verified Markdown formatting in VS Code preview


 # 7. **Created and Implemented Data Scrubber Utility**

- Added a reusable **data cleaning utility** class to `src/analytics_project/data_scrubber.py`.
- This class handles:
  - Checking for missing values and duplicates.
  - Dropping unnecessary columns.
  - Converting data types for consistency.
  - Exporting cleaned data to the processed data folder.
- Verified imports and module recognition within the project.
- Confirmed that all Python files follow consistent naming conventions and formatting.

Run the data scrubber module:

```bash
uv run python -m analytics_project.data_scrubber
```

**Results:**
- Cleaned data successfully generated and logged to `project.log`.
- Confirmed function calls and documentation strings are working as expected.

---

## 8. **Verified Project Logging and Output**

- Confirmed that all data preparation and cleaning actions output consistent messages to `project.log`.
- Reviewed timestamps and message formatting for accuracy.
- Verified that no errors or warnings were present during execution.

---

## 9. **Committed and Pushed Final Changes**

```bash
git add .
git commit -m "Add data_scrubber utility and update project log"
git push
```

- Verified push completion in GitHub repository.
- Checked `README.md` and code structure via GitHub web interface.

## 10. Project 3: Data Scrubber and Data Preparation Pipeline

### Overview

In Project 3, the goal was to finalize data preparation and ensure all raw data files were clean, consistent, and ready for ETL into a central data store for future BI analysis.

Key objectives achieved:

- Reusable **DataScrubber** class to handle common data cleaning tasks.
- Standardized pipeline to process `customers`, `products`, and `sales` CSV files.
- Verified output data consistency and correctness using unit tests.
- Automated logging for all cleaning and preparation steps.

---

### Steps Completed

1. **Reviewed and Completed DataScrubber Class**

- Located at `src/analytics_project/data_scrubber.py`.
- Handles tasks including:
  - Removing duplicates
  - Handling missing values
  - Formatting text columns
  - Renaming columns
  - Parsing dates
  - Dropping or reordering columns
- Finalized all TODO items and verified method logic.

2. **Created Unit Tests for DataScrubber**

- Added `src/analytics_project/test_data_scrubber.py`.
- Verified all methods perform correctly using Python `unittest`.
- Ran tests:

```bash
python -m unittest src.analytics_project.test_data_scrubber
```

**Results:** All 4 tests passed successfully.

3. **Integrated DataScrubber into Data Preparation Script**

- Updated `src/analytics_project/data_prep.py` to use the DataScrubber class.
- Cleaned and processed all three raw data files (`customers`, `products`, `sales`) using the class.
- Output files saved in `data/prepared/` folder.

**Execution:**

```bash
python -m src.analytics_project.data_prep
```

**Results:**

- `customers_cleaned.csv`: 203 rows × 6 columns
- `products_cleaned.csv`: 102 rows × 6 columns
- `sales_cleaned.csv`: 2009 rows × 9 columns
- All processing steps logged to `project.log`.

4. **Verified Data Cleaning**

- Confirmed no missing values or duplicates in cleaned files.
- Checked proper formatting of string and date columns.
- Ensured output is consistent for downstream ETL and BI analysis.

5. **Committed and Pushed Changes**

```bash
git add .
git commit -m "Complete Project 3: Add DataScrubber, unit tests, and data_prep integration"
git push
```

- Verified repository contains updated `data/prepared/` folder with all cleaned files.
- README updated with full workflow and results.

---

### Reflections

- **Reusable DataScrubber Class:** Centralized data cleaning logic reduces redundancy and ensures consistent processing across multiple data sources.
- **Approach Chosen:** Single `data_prep.py` using shared DataScrubber for all files.
- **Challenges Encountered:** Column naming differences (`cust_id` vs `CustomerID`) and date parsing required adjustments.
- **Interesting Aspect:** Implementing automated logging to track each cleaning step provides excellent auditability.
- **Future Enhancements:** Could expand DataScrubber to handle more complex transformations or integrate with ETL pipelines directly.

# Smart Store Data Warehouse Project 4

## Project Overview
This project demonstrates the design and implementation of a **data warehouse** for Smart Store sales data.
The goal was to consolidate cleaned sales, product, and customer data into a central repository that supports **business intelligence** and advanced analytics.

The data warehouse allows us to analyze sales trends, customer behavior, and product performance efficiently.

---

## Schema Design

### Star Schema
We designed a **star schema** with one **fact table** and two **dimension tables**:

- **Fact Table:** `sales`
  - Stores all transactional sales data.
  - Columns include transaction ID, sale date, customer ID, product ID, store ID, campaign ID, sale amount, discount percent, and payment type.

- **Dimension Tables:**
  - **`customer`**
    - Columns: customer_id, name, region, join_date, reward_points, status
  - **`product`**
    - Columns: product_id, product_name, category, unit_price, product_discount_percent, supplier_region

**Schema Diagram:**
      customer           product
        |                   |
        ---------------------
                 |
               sales

This design allows for easy aggregation and querying of sales metrics by customer, product, or other dimensions.

---

## ETL Process

The ETL (Extract, Transform, Load) process was implemented in **`etl_to_dw.py`**:

### Steps:

1. **Extract**
   - Read cleaned CSV files:
     - Customers: `customers_cleaned.csv`
     - Products: `products_cleaned.csv`
     - Sales: `sales_cleaned.csv`

2. **Transform**
   - Deduplicate IDs (`customer_id`, `product_id`, `transaction_id`) to satisfy PRIMARY KEY constraints
   - Clean numeric columns:
     - Removed `%` symbols from discount columns
     - Converted numeric strings to `int` or `float`
   - Dropped rows with missing critical values

3. **Load**
   - Created SQLite database: `smart_store_dw.db`
   - Created tables: `customer`, `product`, `sales` with appropriate column types and relationships
   - Inserted cleaned and transformed data into the tables

---

## Validation

After running the ETL script, row counts in the data warehouse:

- Customers: **200**
- Products: **98**
- Sales: **1,995**

### Sample Data Screenshots

#### Customers Table
![Customers Table](screenshots/customers.png)

#### Products Table
![Products Table](screenshots/products.png)

#### Sales Table
![Sales Table](screenshots/sales.png)

---

## Sample Queries

These queries demonstrate that the warehouse can support typical BI tasks:

```sql
-- Total sales by customer
SELECT customer_id, SUM(sale_amount) as total_sales
FROM sales
GROUP BY customer_id
ORDER BY total_sales DESC
LIMIT 10;

-- Total sales by product
SELECT product_id, SUM(sale_amount) as total_sales
FROM sales
GROUP BY product_id
ORDER BY total_sales DESC
LIMIT 10;

-- Average discount by product category
SELECT p.category, AVG(s.discount_percent) as avg_discount
FROM sales s
JOIN product p ON s.product_id = p.product_id
GROUP BY p.category;

Challenges & Resolutions

Duplicate IDs

Customer, product, and transaction IDs contained duplicates

Solution: dropped duplicates before inserting into SQLite

Datatype Mismatches

Some numeric columns had % symbols or empty strings

Solution: cleaned numeric columns and converted to appropriate types

Maintaining Referential Integrity

Ensured that sales.customer_id and sales.product_id exist in their respective dimension tables

Next Steps / Business Use

The data warehouse supports:

Tracking top customers by sales amount

Identifying best-selling products and categories

Monitoring campaign effectiveness

Calculating average discount impacts

Future extensions could include:

Adding a time dimension table for more advanced temporal analysis

Including store or region dimensions for geospatial insights

Connecting to a BI tool like Power BI or Tableau for dashboards

How to Run the ETL

Activate your virtual environment:

& .venv/Scripts/Activate.ps1


Run the ETL script:

python src/analytics_project/etl_to_dw.py


Verify the database:

Open smart_store_dw.db in VS Code with SQLite Viewer

Check tables: customer, product, sales

Project Files
data/
├─ clean/
│  ├─ customers_cleaned.csv
│  ├─ products_cleaned.csv
│  └─ sales_cleaned.csv
└─ dw/
   └─ smart_store_dw.db

src/analytics_project/
└─ etl_to_dw.py
README.md




---


