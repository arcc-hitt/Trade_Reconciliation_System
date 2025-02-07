# Advanced Trade Reconciliation & Data Processing System

## Objective
This Python-based trade reconciliation system performs the following tasks:
- ✅ **Ingests client orders** from an SQLite database (`trades.db`).
- 📩 **Processes broker trade files** received in `.eml` format with Excel attachments.
- 📊 **Splits and allocates trade details** such as quantity, brokerage, and STT.
- 🔄 **Handles complex reconciliation cases**, including:
   - Multiple brokers executing trades for the same stock.
   - Partially matched and incomplete trades.
   - Trades exceeding or below client orders.
- 🗄️ **Stores data in a database** and generates structured reports.
- ⏳ **Automates execution** using Windows Task Scheduler or Linux cron jobs.
- 🌐 **Provides APIs** to trigger reconciliation on demand and fetch broker rankings.
- ⭐ **Implements a broker ranking system** to evaluate execution quality based on slippage and total costs.

---
## Use Cases & Importance
### **Use Cases**
- 🏦 **Financial Institutions**: Banks, hedge funds, and investment firms can use this system to automate trade reconciliation.
- 📈 **Brokerage Firms**: Ensures accuracy in trade execution by reconciling broker-reported trades with client orders.
- 📜 **Regulatory Compliance**: Helps in audit and compliance by maintaining accurate trade records and reconciliation reports.
- 💼 **Portfolio Management**: Assists fund managers in tracking executed trades versus planned orders, minimizing discrepancies.
- 🔎 **Broker Ranking Analysis**: Enables users to rank brokers based on execution slippage and cost efficiency.

### **Importance of This Project**
- 🔧 **Reduces Manual Effort**: Automates reconciliation, reducing the need for human intervention.
- 🎯 **Enhances Accuracy**: Identifies mismatches, partial fills, and excess trades effectively.
- 🔍 **Ensures Data Integrity**: Stores structured trade data for future reference and compliance audits.
- 💰 **Optimizes Cost Calculation**: Correctly applies brokerage fees, STT, and execution slippage metrics.
- 📡 **Scalable & Flexible**: Can integrate with different broker trade formats and extend functionality for new use cases.

---
## Project Structure

```
|-- trade_reconciliation/
    |-- broker_emails/        # Save .eml files here
    |-- scripts/
        |-- extract_trades.py      
        |-- reconcile_trades.py    
        |-- generate_reports.py    
        |-- run_reconciliation.py  
    |-- app.py
    |-- trades.db              
    |-- reports/              # Generated CSV reports
```

---
## **APIs Implemented**
### **Trigger Reconciliation**
- **Endpoint**: `/trigger-reconciliation`
- **Method**: `POST`
- **Description**: Triggers the reconciliation process on demand.
- **Response**:
  ```json
  {
    "status": "success",
    "message": "Reconciliation and report generation completed."
  }
  ```

### **Broker Ranking**
- **Endpoint**: `/broker-ranking`
- **Method**: `GET`
- **Description**: Fetches a ranking of brokers based on execution quality, including metrics like slippage and total cost.
- **Response**:
  ```json
  {
    "status": "success",
    "rankings": [
      {
        "broker_id": "BROKER1",
        "avg_slippage": 1.2,
        "total_cost": 45000.5,
        "trade_count": 12
      },
      {
        "broker_id": "BROKER2",
        "avg_slippage": 2.5,
        "total_cost": 52000.0,
        "trade_count": 8
      }
    ]
  }
  ```

---

## **Learnings from This Project**
Through this project, I have gained valuable insights into:
- 🗃️ **Database Management**: Gained experience in handling SQLite databases, executing queries efficiently, and structuring data for reconciliation.
- 📩 **Email and File Processing**: Learned to extract and parse `.eml` files, handling Excel attachments for trade data ingestion.
- 🔄 **Trade Reconciliation**: Developed an understanding of matching trades with client orders, handling partial fills, and managing excess trades.
- ⚖️ **Edge Case Handling**: Explored various reconciliation complexities, including multiple brokers, partial allocations, and price variations.
- 💵 **Cost and Slippage Analysis**: Learned how to calculate brokerage fees, STT, and execution slippage for better financial assessment.
- 🤖 **Automation Techniques**: Implemented automation using Task Scheduler and cron jobs to ensure timely execution of reconciliation tasks.
- 📊 **Report Generation**: Built structured CSV reports for matched and unmatched trades, ensuring data integrity for audits.
- 🛠️ **Code Optimization**: Improved modularity, efficiency, and scalability of the reconciliation process for future enhancements.
- 🌐 **API Development**: Designed and implemented RESTful APIs for live reconciliation execution and broker ranking analysis.
- ⭐ **Broker Evaluation**: Developed a ranking system to evaluate broker performance based on execution quality and cost efficiency.

---
## **Automation & Scheduling**
### **Windows Task Scheduler**
To automate execution on Windows:
1. 📝 Create a batch file (`run_reconciliation.bat`) with the following content:
   ```batch
   @echo off
   cd /d "C:\path\to\your\script"
   python run_reconciliation.py
   ```
   - Ensure Python is installed and added to your system's PATH.
   - Replace `C:\path\to\your\script` with the actual directory of your script.

2. ⚙️ Open **Task Scheduler**:
   - Press `Win + R`, type `taskschd.msc`, and hit **Enter**.
   - Click on **Create Basic Task** in the right-hand panel.
   - Enter a name (e.g., **Trade Reconciliation Task**) and description.
   - Click **Next**.

3. ⏲️ Set the **Trigger**:
   - Choose **Daily** (or any preferred schedule).
   - Set the **Start Time** and recurrence pattern.
   - Click **Next**.

4. 🖥️ Set the **Action**:
   - Select **Start a Program**.
   - Click **Browse** and select the `run_reconciliation.bat` file.
   - Click **Next**.

5. ⚡ Configure Additional Settings:
   - Under the **General** tab, select **Run whether user is logged on or not**.
   - In the **Conditions** tab, uncheck **Start the task only if the computer is on AC power** (if using a laptop).
   - In the **Settings** tab, check **Allow task to be run on demand**.
   - Click **Finish**.

6. ✅ Test the Task:
   - Right-click the task and select **Run** to confirm execution.

### **Linux (Cron Job)**
📌 To schedule execution on Linux, add the following line to the crontab (`crontab -e`):
```cron
0 18 * * * python3 /path/to/scripts/run_reconciliation.py
```
This schedules the script to run at 6 PM daily.

To verify scheduled jobs, use:
```bash
crontab -l
```

---
## **How to Run the Project**
### **1. Install Dependencies**
Ensure Python and required libraries are installed:
```bash
pip install pandas sqlite3 flask openpyxl
```

### **2. Execute the Script Manually**
```bash
python run_reconciliation.py
```
This will:
- 📥 Extract client orders and broker trades.
- 🔄 Reconcile trades.
- 🗄️ Store results in the database.
- 📊 Generate reports.

### **3. Start the Flask API**
Run the `app.py` script to start the API:
```bash
python app.py
```
Access the API endpoints via Postman or a web browser:
- Trigger reconciliation: `POST http://127.0.0.1:5000/trigger-reconciliation`
- Fetch broker rankings: `GET http://127.0.0.1:5000/broker-ranking`.

---