# CYBR404_Project_WalletNote
# WalletNote ver.04

WalletNote is a Flask-based personal finance management web application designed for students and individual users.  
It supports user authentication, expense and income tracking, data visualization, and a modular OCR system for receipt processing.

---

## Features

- User authentication (Sign up / Log in)
- Expense and income management
- Dashboard overview
- Category-based analysis
- Settings page
- Chart generation via API (PNG images)
- Modular OCR system (optional)

---

## Test Status

All executable components of WalletNote ver.04 have been tested using a Flask test client with a mocked MySQL environment.

### Test Results

| Component | Status |
|----------|--------|
| Application import | Passed |
| HTML routing | Passed |
| Login API | Passed |
| Signup API | Passed |
| Pie chart API | Passed |
| Bar chart API | Passed |
| OCR module import | Passed |

All routes return HTTP 200 responses.  
All chart endpoints return valid PNG images.

---

## Project Structure

- **app.py**  
  Main Flask application entry point.

- **Backend / Accounting_System**  
  - Expense.py: Expense handling logic  
  - Income.py: Income handling logic  

- **Backend / Chart**  
  - PieChart.py: Category-based pie chart generation  
  - BarChart.py: Expense and income bar charts  
  - DailyReport.py: Daily financial reports  
  - MonthlyReport.py: Monthly financial reports  

- **Backend / Database**  
  - ConnectDatabase.py: MySQL connection handler  
  - CreateDatabase.py: Database and table initialization  
  - RecordDatabase.py: Insert financial records  
  - RecallDatabase.py: Fetch records for dashboard and charts  

- **Backend / System**  
  - OCR_System.py: Receipt OCR processing module  

---

## Tech Stack

- Python
- Flask
- MySQL
- Matplotlib
- OpenCV (optional)
- Tesseract OCR (optional)

---

## How to Run

### Install dependencies
## How to Run

### Run the application

```bash
python app.py
http://127.0.0.1:5000
```
## Notes

- Login currently returns HTTP 200 for both valid and invalid credentials.
- Frontend-side success or failure handling should be implemented using explicit JSON responses.
- OCR execution requires local OCR engine configuration.
- This project is intended for educational and experimental use.

---

## License

This project is released for educational purposes.

---

## Author

Seiya Genda  
Aoi Minamiyashiki

```bash
pip install flask mysql-connector-python matplotlib pillow opencv-python
