import pandas as pd


def generate_statistics(df):
    """
    Generate statistical summaries for numeric columns.
    """

    statistics = []

    # Find numeric columns
    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:

        series = df[column].dropna()

        if len(series) == 0:
            continue

        statistics.append({

            "Column": column,

            "Count": len(series),

            "Mean": round(
                series.mean(),
                2
            ),

            "Median": round(
                series.median(),
                2
            ),

            "Std Dev": round(
                series.std(),
                2
            ),

            "Minimum": round(
                series.min(),
                2
            ),

            "25%": round(
                series.quantile(0.25),
                2
            ),

            "50%": round(
                series.quantile(0.50),
                2
            ),

            "75%": round(
                series.quantile(0.75),
                2
            ),

            "Maximum": round(
                series.max(),
                2
            )
        })

    return pd.DataFrame(statistics)