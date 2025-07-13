from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
import plotly.io as pio
from helpers import detect_fraud, categorize_transactions, analyze_budget
import os
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Default budget configuration
DEFAULT_BUDGET = {
    'food': 500,
    'transport': 200,
    'shopping': 300,
    'housing': 1500,
    'entertainment': 100,
    'health': 300,
    'utilities': 200,
    'other': 100
}

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    budget = DEFAULT_BUDGET.copy()
    
    if request.method == 'POST':
        if 'file' not in request.files:
            error = "No file part in request"
            return render_template('index.html', error=error, budget=budget)
        
        file = request.files['file']
        
        if file.filename == '':
            error = "No file selected"
            return render_template('index.html', error=error, budget=budget)
        
        if file and file.filename.lower().endswith(('.csv', '.xlsx')):
            try:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                
                if file.filename.lower().endswith('.csv'):
                    df = pd.read_csv(filepath)
                else:
                    df = pd.read_excel(filepath)
                
                required_cols = ['Date', 'Description', 'Amount']
                if not all(col in df.columns for col in required_cols):
                    error = "File must contain Date, Description, and Amount columns"
                    return render_template('index.html', error=error, budget=budget)
                
                # Get all budget values from form
                budget = {
                    'food': float(request.form.get('budget_food', DEFAULT_BUDGET['food'])),
                    'transport': float(request.form.get('budget_transport', DEFAULT_BUDGET['transport'])),
                    'shopping': float(request.form.get('budget_shopping', DEFAULT_BUDGET['shopping'])),
                    'housing': float(request.form.get('budget_housing', DEFAULT_BUDGET['housing'])),
                    'entertainment': float(request.form.get('budget_entertainment', DEFAULT_BUDGET['entertainment'])),
                    'health': float(request.form.get('budget_health', DEFAULT_BUDGET['health'])),
                    'utilities': float(request.form.get('budget_utilities', DEFAULT_BUDGET['utilities'])),
                    'other': float(request.form.get('budget_other', DEFAULT_BUDGET['other']))
                }
                
                df = categorize_transactions(df)
                df = detect_fraud(df)
                spending, alerts = analyze_budget(df, budget)
                
                fig1 = px.pie(df, names='Category', values='Amount', title='Spending by Category')
                plot1 = pio.to_html(fig1, full_html=False)
                
                fig2 = px.bar(df[df['Is_Fraud'] == 1], x='Date', y='Amount', 
                             color='Description', title='Potential Fraudulent Transactions')
                plot2 = pio.to_html(fig2, full_html=False)
                
                recent_tx = df.sort_values('Date', ascending=False).head(10)
                
                return render_template('dashboard.html', 
                                    plot1=plot1, 
                                    plot2=plot2,
                                    spending=spending,
                                    budget=budget,
                                    alerts=alerts,
                                    recent_tx=recent_tx.to_dict('records'),
                                    fraud_count=df['Is_Fraud'].sum(),
                                     current_year=datetime.now().year)
            
            except Exception as e:
                error = f"Error processing file: {str(e)}"
                return render_template('index.html', error=error, budget=DEFAULT_BUDGET)
            finally:
                if os.path.exists(filepath):
                    os.remove(filepath)
        else:
            error = "Invalid file type. Please upload a CSV or Excel file."
            return render_template('index.html', error=error, budget=budget)
    
    return render_template('index.html', budget=budget)

if __name__ == '__main__':
    app.run(debug=True)