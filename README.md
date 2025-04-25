# Odoo Notes and Comments Exporter

This repository provides a Python script to **export notes and internal comments** from an **Odoo Cloud (SaaS)** instance.  
The extracted data is saved into a **CSV file**, encoded in **UTF-8 with BOM**, using a **custom column separator** (`£`).

This ensures maximum compatibility with spreadsheet software like **Microsoft Excel**, **LibreOffice**, and **Google Sheets**.

---

## 📌 Features

- Connects to **Odoo Cloud** via **XML-RPC API**.
- Automatically **checks** if the `note.note` model (personal notes) exists.
- **Exports** both:
  - Personal Notes (`note.note`) (if available),
  - Internal Comments from the **Chatter** (`mail.message`) (always available).
- Generates a **CSV** file with:
  - UTF-8 BOM encoding,
  - Custom delimiter `£`,
  - Minimal quoting (only when necessary).
- Cleans up text fields by removing line breaks (`\n`, `\r`) for better CSV readability.
- Adds metadata columns: source, linked model, linked object ID, author, date, content.

---

## 🛠 Requirements

- Python 3.7+
- No external libraries are required beyond the Python Standard Library.

---

## 🚀 How to Use

1. Clone the repository or download the script.
2. Open the script and **configure your connection settings**:
   ```python
   url = "https://your-odoo-domain.odoo.com"
   db = "your-database-name"
   username = "your.email@domain.com"
   password = "your-odoo-password"
