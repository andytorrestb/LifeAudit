# Potential Improvements for Merged Application

## 1. Modularize Functionality

* **Extract schedule generation into reusable functions**:

  * `add_weekday_schedule(doc)`
  * `add_weekend_schedule(doc)`
* **Encapsulate life audit CRUD operations in an `audit_manager` module**:

  * `load_tasks(db_path)`
  * `save_task(record, db)`
  * `export_tasks_csv(db, filepath)`

## 2. Unified Entry Point

* **Develop a `main.py` (or extend `LifeAuditGUI`) to:**

  1. Load TinyDB and initialize the GUI
  2. Provide “Export Full Report” functionality:

     * Instantiate a `Document()`
     * Call schedule functions
     * Append life audit records as a table or paragraphs
     * Save as `combined_report.docx`

## 3. Command-Line Interface (CLI)

* **Use `argparse` to support subcommands**:

  * `schedule`: export schedule to `schedule.docx`
  * `audit`: export tasks to `tasks.csv`
  * `report`: export combined report to `combined_report.docx`

## 4. Unified Data Model

* **Store schedule entries and life audit tasks in a single TinyDB collection**:

  * Use a `type` field to distinguish record kinds (e.g., `"schedule_weekday"`, `"audit_task"`)
  * Simplify export loops by iterating over one database

## Next Steps

1. Refactor existing scripts into modules and functions
2. Implement `main.py` (or GUI extension) to integrate features
3. Add an “Export Full Report” button or CLI command
