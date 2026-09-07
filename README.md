# DataPilot- AI power Data Analyst
 > Upload a dataset. Skip the grunt work. Get straight to the insight.

Every data project starts the same way
load the file,
check for missing values,
 find duplicates,
 check the distributions,
 flag the outliers,
 and only then do the actual analysis. That setup phase alone can eat up 30-40% of a project timeline, and it's rarely where the value is.

**DataPilot removes that bottleneck.** It's a Python + Streamlit tool that takes any raw CSV or Excel file and automatically runs the entire first-pass workflow profiling, data-quality checks, statistical analysis, anomaly detection,  exploratory analysis and then translates the technical output into plain-English, business-ready insights.

No code. No manual setup. Just upload and analyze.

## ⚙️ How It Works

Upload Dataset → Profile Data → Check Data Quality → Detect Anomalies → Perform EDA → Generate Insights

| Stage | What it Does |
|---|---|
| Data Ingestion | Reads CSV/Excel files with no predefined schema required |
| Automated Profiling | Identifies numerical vs. categorical columns, missing values, unique values, and summary statistics |
|Data Quality Checks | Flags missing values, duplicate records, and inconsistent or invalid entries |
| Anomaly Detection | Uses IQR and Z-Score methods to surface statistical outliers |
| Exploratory Analysis | Reveals distributions, patterns, and relationships in the data |
| AI-Powered Insights | Converts raw statistical findings into plain-English explanations of what they actually mean |

## 🔑 Key Findings from Testing
DataPilot was tested across multiple datasets with different structures and quality issues to validate the pipeline. A few things stood out:

- **Data-quality issues surface fast :** Missing values, duplicates, and inconsistent formatting that normally take 15-20 minutes to manually check were flagged within seconds of upload.

- **Outlier detection needs both lenses :** IQR and Z-Score frequently disagreed on edge cases — running both caught anomalies that either method alone would have missed.

- **Raw statistics ≠ understanding :** Numbers like skewness, kurtosis, or a Z-score of 3.2 mean little to a non-technical stakeholder. The AI-explanation layer was the single biggest driver of "aha" moments during testing — it's the difference between seeing a result and understanding it.

## The Business Case
A analyst does not get paid for missing values they are paid to solve the business problem with the data. Every hour spend on repetative work and cleanup is an hour not spent on actual business spent 
Data Pilot is build to close this gap:

- **Faster time to insight :** The initial phase drop hours to minutes
- **Low barrier to entry :** Non tech users can get a real read on their data without writting code
- **More consistent quality check :** dont have to rely on analyst for manual review
- **Insight,not just output :** findings are translated into business language,not just statistical outputs

| Components | Purpose|
|---|---|
| Reader | 	Loads CSV/XLSX datasets |
| Profiler | Understands dataset structure and statistics |
|Quality | 	Identifies data-quality issues |
| Statistic| 	Performs statistical analysis and anomaly detection |
| EDA | 	Generates exploratory analysis |
| AI explainer | Converts findings into understandable insights |
| Streamlit app | 	Provides the interactive user interface |


## Tech Stack
- Python (Pandas, Numpy,scikit-learn)
- streamlit
- IQR &Z-score
- AI Integration
  
## Use Case
- Rapid dataset exploration
- Data-quality check before deeper analysis
- initial anomaly investigation
- Exploratory Data analysis
- Quickly getting oriented in an unfamiliar dataset

## Future Scope
- Automated report generation
- More advance anomaly detection algorithm
- More sophisticated AI-generated business recommendation
- Automated feature and correlation analysis
