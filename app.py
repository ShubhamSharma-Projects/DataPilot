# ============================================================
# DATAPILOT
# AI-POWERED DATA ANALYST
# ============================================================

import os
import pandas as pd
import streamlit as st

from dotenv import load_dotenv
from google import genai

from tools.profiler import profile_dataset
from tools.statistics import generate_statistics
from tools.quality import (
    analyze_data_quality,
    calculate_quality_score
)
from tools.eda import generate_eda
from tools.anamoly import detect_anomalies


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="DataPilot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# DARK CINEMATIC THEME
# ============================================================

st.markdown("""
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

.stApp {

    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(37, 99, 235, 0.10),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 0%,
            rgba(124, 58, 237, 0.08),
            transparent 28%
        ),
        #0b1120;

    color: #e5e7eb;
}


/* FULL WIDTH */

.block-container {

    max-width: none !important;

    width: 100% !important;

    padding-left: 3rem !important;

    padding-right: 3rem !important;

    padding-top: 2rem !important;

    padding-bottom: 3rem !important;
}


/* ============================================================
   TYPOGRAPHY
   ============================================================ */

h1 {

    color: #f8fafc !important;

    font-size: 2.8rem !important;

    font-weight: 750 !important;

    letter-spacing: -0.04em !important;
}


h2 {

    color: #f1f5f9 !important;

    font-size: 1.7rem !important;

    font-weight: 700 !important;
}


h3 {

    color: #e2e8f0 !important;

    font-size: 1.25rem !important;

    font-weight: 650 !important;
}


p {

    color: #cbd5e1;
}


/* ============================================================
   HEADER
   ============================================================ */

.datapilot-header {

    padding: 10px 0 20px 0;

}


.datapilot-title {

    font-size: 2.8rem;

    font-weight: 800;

    color: #f8fafc;

    letter-spacing: -0.04em;
}


.datapilot-subtitle {

    color: #94a3b8;

    font-size: 1rem;

    margin-top: -8px;
}


.datapilot-description {

    color: #cbd5e1;

    font-size: 1rem;

    margin-top: 8px;
}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

[data-testid="stFileUploader"] {

    background: rgba(15, 23, 42, 0.80);

    border: 1px dashed #334155;

    border-radius: 14px;

    padding: 10px;

}


[data-testid="stFileUploaderDropzone"] {

    background: #111827;

    border-radius: 10px;

}


/* ============================================================
   ALERTS
   ============================================================ */

[data-testid="stAlert"] {

    border-radius: 10px;

    border: 1px solid rgba(148, 163, 184, 0.15);

}


/* ============================================================
   KPI CARDS
   ============================================================ */

[data-testid="stMetric"] {

    background:
        linear-gradient(
            145deg,
            rgba(17, 24, 39, 0.98),
            rgba(15, 23, 42, 0.95)
        );

    border: 1px solid #263247;

    border-radius: 14px;

    padding: 18px 20px;

    min-height: 110px;

    box-shadow:
        0 8px 25px rgba(0, 0, 0, 0.18);
}


[data-testid="stMetricLabel"] {

    color: #94a3b8 !important;

    font-size: 0.85rem !important;

    font-weight: 500 !important;
}


[data-testid="stMetricValue"] {

    color: #f8fafc !important;

    font-size: 1.75rem !important;

    font-weight: 700 !important;
}


/* ============================================================
   TABS
   ============================================================ */

[data-baseweb="tab-list"] {

    gap: 4px;

    background: rgba(15, 23, 42, 0.70);

    border: 1px solid #1e293b;

    border-radius: 10px;

    padding: 5px;

    overflow-x: auto;
}


button[data-baseweb="tab"] {

    color: #94a3b8 !important;

    font-weight: 600 !important;

    border-radius: 7px;

    padding: 9px 14px !important;

    white-space: nowrap;
}


button[data-baseweb="tab"]:hover {

    color: #e2e8f0 !important;

    background: rgba(51, 65, 85, 0.45);
}


button[data-baseweb="tab"][aria-selected="true"] {

    color: #ffffff !important;

    background: #1e293b !important;
}


div[data-baseweb="tab-highlight"] {

    background: #6366f1 !important;

    height: 2px !important;
}


/* ============================================================
   DATAFRAMES
   ============================================================ */

[data-testid="stDataFrame"] {

    border: 1px solid #263247;

    border-radius: 10px;

    overflow: hidden;

    background: #111827;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {

    background: #172033;

    color: #e5e7eb;

    border: 1px solid #334155;

    border-radius: 9px;

    font-weight: 600;
}


.stButton > button:hover {

    background: #1e293b;

    border-color: #6366f1;

    color: #ffffff;
}


/* ============================================================
   INPUTS
   ============================================================ */

div[data-baseweb="input"] {

    background: #ffffff !important;

    border-radius: 9px !important;

    border: 1px solid #475569 !important;

}


div[data-baseweb="input"] input {

    color: #111827 !important;

    background: #ffffff !important;

    caret-color: #111827 !important;

}


div[data-baseweb="input"] input::placeholder {

    color: #64748b !important;

    opacity: 1 !important;

}

/* ============================================================
   SELECTBOX
   ============================================================ */

div[data-baseweb="select"] > div {

    background: #111827;

    border-color: #334155;

    border-radius: 9px;
}


/* ============================================================
   CODE
   ============================================================ */

[data-testid="stCodeBlock"] {

    border-radius: 10px;

    border: 1px solid #263247;
}


/* ============================================================
   EXPANDERS
   ============================================================ */

[data-testid="stExpander"] {

    background: rgba(15, 23, 42, 0.65);

    border: 1px solid #263247;

    border-radius: 10px;
}


/* ============================================================
   DIVIDERS
   ============================================================ */

hr {

    border-color: #1e293b !important;
}


/* ============================================================
   AI CARD
   ============================================================ */

.ai-card {

    background:
        linear-gradient(
            135deg,
            rgba(30, 41, 59, 0.95),
            rgba(49, 46, 129, 0.28)
        );

    border: 1px solid rgba(99, 102, 241, 0.30);

    border-radius: 14px;

    padding: 22px;

    margin: 10px 0 20px 0;
}


/* ============================================================
   FOOTER
   ============================================================ */

footer {

    visibility: hidden;
}


#MainMenu {

    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="datapilot-header">

<div class="datapilot-title">
📊 DataPilot
</div>

<div class="datapilot-subtitle">
AI-Powered Data Analyst
</div>

<div class="datapilot-description">
Upload a CSV or Excel dataset to automatically profile,
analyze, visualize and understand your data.
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# FILE UPLOADER
# ============================================================

uploaded_file = st.file_uploader(
    "📁 Upload your dataset",
    type=["csv", "xlsx"]
)


# ============================================================
# NO FILE
# ============================================================

if uploaded_file is None:

    st.divider()

    st.caption(
        "DataPilot • Automated Data Analysis • AI Insights"
    )

    st.stop()


# ============================================================
# READ DATASET
# ============================================================

try:

    if uploaded_file.name.lower().endswith(".csv"):

        df = pd.read_csv(uploaded_file)

    elif uploaded_file.name.lower().endswith(".xlsx"):

        df = pd.read_excel(uploaded_file)

    else:

        st.error("Unsupported file format.")

        st.stop()


except Exception as e:

    st.error(f"Could not read the file: {e}")

    st.stop()


# ============================================================
# SUCCESS
# ============================================================

st.success(
    f"Successfully loaded: {uploaded_file.name}"
)


# ============================================================
# RUN CORE ANALYSIS
# ============================================================

try:

    profile = profile_dataset(df)

except Exception:

    profile = pd.DataFrame()


try:

    statistics = generate_statistics(df)

except Exception:

    statistics = pd.DataFrame()


try:

    quality = analyze_data_quality(df)

except Exception:

    quality = pd.DataFrame()


try:

    quality_score = calculate_quality_score(df)

except Exception:

    quality_score = 0


try:

    anomalies = detect_anomalies(df)

except Exception:

    anomalies = pd.DataFrame()


# ============================================================
# NAVIGATION TABS
# ============================================================

tabs = st.tabs([
    "📌 Overview",
    "🔎 Profiler",
    "📊 Statistics",
    "🧹 Quality",
    "🚨 Anomalies",
    "📈 EDA",
    "🤖 AI Analyst"
])


# ============================================================
# OVERVIEW
# ============================================================

with tabs[0]:

    st.header("Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Rows",
            f"{df.shape[0]:,}"
        )

    with col2:

        st.metric(
            "Columns",
            f"{df.shape[1]:,}"
        )

    with col3:

        st.metric(
            "Missing Cells",
            f"{df.isna().sum().sum():,}"
        )

    with col4:

        st.metric(
            "Duplicate Rows",
            f"{df.duplicated().sum():,}"
        )


    st.divider()

    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True,
        height=380
    )


# ============================================================
# PROFILER
# ============================================================

with tabs[1]:

    st.header("🔎 Data Profiler")

    st.write(
        "Automatically identifies column types, missing values "
        "and basic structural information."
    )

    if not profile.empty:

        st.dataframe(
            profile,
            use_container_width=True,
            height=520
        )

    else:

        st.info("Profiler could not generate results.")


# ============================================================
# STATISTICS
# ============================================================

with tabs[2]:

    st.header("📊 Statistical Summary")

    st.write(
        "Statistical information for numeric columns."
    )

    if not statistics.empty:

        st.dataframe(
            statistics,
            use_container_width=True,
            height=520
        )

    else:

        st.info(
            "No numeric columns were found."
        )


# ============================================================
# DATA QUALITY
# ============================================================

with tabs[3]:

    st.header("🧹 Data Quality")

    col1, col2 = st.columns([1, 3])

    with col1:

        st.metric(
            "Quality Score",
            f"{quality_score:.1f}/100"
        )

    with col2:

        if quality_score >= 90:

            st.success(
                "Excellent dataset quality."
            )

        elif quality_score >= 75:

            st.info(
                "Good dataset quality with some issues."
            )

        elif quality_score >= 50:

            st.warning(
                "Dataset requires cleaning."
            )

        else:

            st.error(
                "Significant data quality issues detected."
            )


    st.divider()

    if not quality.empty:

        st.dataframe(
            quality,
            use_container_width=True,
            height=520
        )

    else:

        st.info(
            "No data quality information available."
        )


# ============================================================
# ANOMALIES
# ============================================================

with tabs[4]:

    st.header("🚨 Anomaly Detection")

    st.write(
        "Statistical anomaly detection using IQR and Z-score methods."
    )


    if not anomalies.empty:

        st.dataframe(
            anomalies,
            use_container_width=True,
            height=520
        )

    else:

        st.info(
            "No numeric columns available for anomaly detection."
        )


# ============================================================
# EDA
# ============================================================

with tabs[5]:

    st.header("📈 Exploratory Data Analysis")

    st.write(
        "Automatically generated visual analysis of numeric data."
    )

    try:

        generate_eda(df)

    except Exception as e:

        st.error(
            f"EDA could not be generated: {e}"
        )


# ============================================================
# AI ANALYST
# ============================================================

with tabs[6]:

    st.header("🤖 AI Analyst")

    st.markdown("""
    <div class="ai-card">

    <h3>Ask DataPilot about your dataset</h3>

    <p>
    Ask a natural-language question and Gemini will analyze the
    dataset using its structure and statistics.
    </p>

    </div>
    """, unsafe_allow_html=True)


    

    question = st.text_input(
        "Ask a question about your data",
        placeholder="Example: Which category has the highest total views?"
    )

    analyze_button = st.button(
        "✨ Analyze",
        type="primary"
    )


    if analyze_button:

        if not question.strip():

            st.warning(
                "Please enter a question first."
            )

        else:

            load_dotenv()

            api_key = os.getenv(
                "GEMINI_API_KEY"
            )

            if not api_key:

                st.error(
                    "Gemini API key was not found. "
                    "Check your .env file."
                )

            else:

                try:

                    client = genai.Client(
                        api_key=api_key
                    )


                    # ----------------------------------------
                    # DATASET CONTEXT
                    # ----------------------------------------

                    numeric_columns = (
                        df.select_dtypes(
                            include="number"
                        ).columns.tolist()
                    )


                    categorical_columns = (
                        df.select_dtypes(
                            include=["object", "category"]
                        ).columns.tolist()
                    )


                    dataset_context = {

                        "rows": int(df.shape[0]),

                        "columns": int(df.shape[1]),

                        "column_names": df.columns.tolist(),

                        "numeric_columns":
                            numeric_columns,

                        "categorical_columns":
                            categorical_columns,

                        "missing_cells":
                            int(df.isna().sum().sum()),

                        "duplicate_rows":
                            int(df.duplicated().sum())

                    }


                    # Add numerical summaries

                    if numeric_columns:

                        numeric_summary = (
                            df[numeric_columns]
                            .describe()
                            .round(2)
                            .to_dict()
                        )

                    else:

                        numeric_summary = {}


                    # ----------------------------------------
                    # AI PROMPT
                    # ----------------------------------------

                    prompt = f"""
You are DataPilot, a professional junior data analyst.

Analyze the user's dataset and answer the question clearly.

IMPORTANT:
- Do not invent information.
- Use only information supported by the dataset context.
- Give a concise business-friendly answer.
- If a calculation is required, explain the result.
- If the question cannot be answered from the available data,
  clearly say so.
- Do not generate Python code unless specifically requested.

USER QUESTION:
{question}

DATASET INFORMATION:
{dataset_context}

NUMERIC SUMMARY:
{numeric_summary}
"""


                    with st.spinner(
                        "🤖 DataPilot is analyzing your dataset..."
                    ):

                        interaction = client.interactions.create(

                            model="gemini-3.6-flash",

                            input=prompt
                        )


                    answer = interaction.output_text


                    st.subheader("💡 Analysis")

                    st.markdown(
                        answer
                    )


                except Exception as e:

                    st.error(
                        f"AI Analyst error: {e}"
                    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "DataPilot • Automated Data Analysis • Statistical Insights • AI Analyst"
)