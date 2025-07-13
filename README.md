# Smart_Budget_Tracker
# Budget and Fraud Detection Web Application

This is a Flask-based web application that allows users to upload transaction files (CSV or Excel), categorize spending, detect potential fraudulent transactions using machine learning, and visualize budget performance with interactive plots.

## 🚀 Features

- Upload `.csv` or `.xlsx` transaction files.
- Automatically categorizes transactions (e.g., food, transport, shopping, etc.).
- Detects potential fraudulent transactions using an Isolation Forest model.
- Allows users to set custom monthly budget limits per category.
- Visualizes spending via interactive pie and bar charts.
- Provides alerts when spending exceeds budgeted limits.
- Displays recent transactions and fraud summary.

## 📁 File Structure

```

.
├── app.py                      # Main Flask application
├── helpers.py                 # Utility functions (categorization, fraud detection, budget analysis)
├── budget\_model.pkl           # Pretrained Isolation Forest model
├── templates/                 # HTML templates (not included here)
│   ├── index.html
│   └── dashboard.html
├── uploads/                   # Temporary folder for uploaded files
├── requirements.txt           # Python dependencies
├── \*.csv                      # Sample data files (transactions, fraud samples, etc.)

````

## 📊 Example Inputs

- `transactions.csv` - Contains columns: `Date`, `Description`, `Amount`.
- `detailed_categories.csv` - Optional reference for enhancing categorization.
- `fraud_transactions.csv` & `normal_transactions.csv` - Used for training or testing fraud detection logic.

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone <repo-url>
cd <project-folder>
````

### 2. Install dependencies

It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the app

```bash
python app.py
```

Then open your browser and visit `http://127.0.0.1:5000`.

## 📂 File Upload Format

Your transaction file must have the following columns:

| Date       | Description      | Amount |
| ---------- | ---------------- | ------ |
| 2023-01-01 | Starbucks Coffee | 5.25   |
| 2023-01-03 | Amazon Purchase  | 150.00 |
| 2023-01-05 | Uber Ride        | 12.00  |

## 🧠 How It Works

* **Categorization**: Uses keyword matching on transaction descriptions.
* **Fraud Detection**: Employs a trained Isolation Forest model to score transactions as normal or anomalous.
* **Budget Analysis**: Compares actual spend per category against user-defined budget limits.

## 📌 Dependencies

* Flask
* pandas
* numpy
* scikit-learn
* matplotlib
* plotly
* python-dotenv

## 📋 License

This project is intended for educational and personal use. Feel free to modify and extend it as needed.
