import pandas as pd
import streamlit as st


def generate_eda(df):
    """
    Automatically generate exploratory
    data analysis based on the dataset.
    """

    st.subheader("📊 Automatic Exploratory Data Analysis")

    # =====================================================
    # IDENTIFY COLUMN TYPES
    # =====================================================

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    date_columns = []

    # Detect date columns
    for column in df.columns:

        # Already datetime
        if pd.api.types.is_datetime64_any_dtype(
            df[column]
        ):

            date_columns.append(column)

        # Try detecting dates stored as text
        elif df[column].dtype == "object":

            sample = df[column].dropna().head(100)

            if len(sample) > 0:

                converted = pd.to_datetime(
                    sample,
                    errors="coerce"
                )

                if converted.notna().mean() >= 0.8:

                    date_columns.append(column)

    # Remove date columns from categorical columns
    categorical_columns = [
        column
        for column in categorical_columns
        if column not in date_columns
    ]

    # =====================================================
    # REMOVE CONSTANT NUMERIC COLUMNS
    # =====================================================

    useful_numeric_columns = []

    for column in numeric_columns:

        if df[column].nunique(
            dropna=True
        ) > 1:

            useful_numeric_columns.append(column)

    # =====================================================
    # NUMERIC DISTRIBUTIONS
    # =====================================================

    if useful_numeric_columns:

        st.markdown("## 📈 Numeric Distributions")

        for column in useful_numeric_columns[:6]:

            series = df[column].dropna()

            if len(series) == 0:
                continue

            st.write(f"### {column}")

            # -----------------------------------------
            # Summary metrics
            # -----------------------------------------

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "Mean",
                    f"{series.mean():,.2f}"
                )

            with col2:

                st.metric(
                    "Median",
                    f"{series.median():,.2f}"
                )

            with col3:

                st.metric(
                    "Minimum",
                    f"{series.min():,.2f}"
                )

            with col4:

                st.metric(
                    "Maximum",
                    f"{series.max():,.2f}"
                )

            # -----------------------------------------
            # Quantile distribution
            # -----------------------------------------

            try:

                quantile_bins = series.quantile(
                    [
                        0,
                        0.1,
                        0.2,
                        0.3,
                        0.4,
                        0.5,
                        0.6,
                        0.7,
                        0.8,
                        0.9,
                        1.0
                    ]
                ).unique()

                if len(quantile_bins) >= 3:

                    distribution = pd.cut(
                        series,
                        bins=quantile_bins,
                        include_lowest=True
                    )

                    counts = (
                        distribution
                        .value_counts()
                        .sort_index()
                    )

                    chart_df = pd.DataFrame({

                        "Range":
                            counts.index.astype(str),

                        "Records":
                            counts.values

                    })

                    st.bar_chart(
                        chart_df.set_index("Range")
                    )

            except Exception as e:

                st.info(
                    f"Could not create distribution "
                    f"for {column}: {e}"
                )

    # =====================================================
    # CATEGORICAL ANALYSIS
    # =====================================================

    if categorical_columns:

        st.markdown("## 📊 Categorical Analysis")

        for column in categorical_columns[:5]:

            unique_count = df[column].nunique(
                dropna=True
            )

            # Skip high-cardinality columns
            if unique_count > 100:

                continue

            counts = (
                df[column]
                .value_counts()
                .head(10)
            )

            if counts.empty:

                continue

            st.write(
                f"### Top values in {column}"
            )

            chart_df = pd.DataFrame({

                column:
                    counts.index.astype(str),

                "Count":
                    counts.values

            })

            st.bar_chart(
                chart_df.set_index(column)
            )

    # =====================================================
    # DATE ANALYSIS
    # =====================================================

    if date_columns:

        st.markdown("## 📅 Time Analysis")

        for column in date_columns[:3]:

            dates = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            valid_dates = dates.dropna()

            if valid_dates.empty:

                continue

            time_df = pd.DataFrame({

                "Date":
                    valid_dates

            })

            monthly = (
                time_df
                .set_index("Date")
                .resample("ME")
                .size()
            )

            if not monthly.empty:

                st.write(
                    f"### Records over time — {column}"
                )

                st.line_chart(
                    monthly
                )

    # =====================================================
    # CATEGORY VS NUMERIC
    # =====================================================

    if (
        categorical_columns
        and useful_numeric_columns
    ):

        st.markdown(
            "## 🔍 Metric Analysis by Category"
        )

        selected_category = None

        # Find a useful categorical column
        for column in categorical_columns:

            unique_count = df[column].nunique(
                dropna=True
            )

            if 2 <= unique_count <= 20:

                selected_category = column

                break

        if selected_category:

            selected_metric = (
                useful_numeric_columns[0]
            )

            grouped = (
                df.groupby(
                    selected_category
                )[selected_metric]
                .mean()
                .sort_values(
                    ascending=False
                )
                .head(10)
            )

            st.write(
                f"### Average {selected_metric} "
                f"by {selected_category}"
            )

            chart_df = pd.DataFrame({

                selected_category:
                    grouped.index.astype(str),

                f"Average {selected_metric}":
                    grouped.values

            })

            st.bar_chart(
                chart_df.set_index(
                    selected_category
                )
            )

    # =====================================================
    # CORRELATION ANALYSIS
    # =====================================================

    if len(useful_numeric_columns) >= 2:

        st.markdown(
            "## 🔗 Correlation Analysis"
        )

        correlation = (
            df[useful_numeric_columns]
            .corr()
            .round(2)
        )

        st.dataframe(
            correlation,
            use_container_width=True
        )

    # =====================================================
    # EDA COMPLETION MESSAGE
    # =====================================================

    st.success(
        "Automatic EDA completed successfully."
    )