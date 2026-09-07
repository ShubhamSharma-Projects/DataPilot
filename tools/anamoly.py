import pandas as pd


def detect_anomalies(df):
    """
    Detect statistical anomalies in numeric columns
    using IQR and Z-score methods.
    """

    results = []

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:

        series = df[column].dropna()

        if len(series) == 0:
            continue

        # IQR
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        iqr_outliers = (
            (series < lower_bound) |
            (series > upper_bound)
        )

        iqr_count = iqr_outliers.sum()

        # Z-score
        mean = series.mean()
        std = series.std()

        if std != 0:

            z_scores = (
                (series - mean) / std
            )

            zscore_outliers = (
                z_scores.abs() > 3
            )

            zscore_count = zscore_outliers.sum()

        else:

            zscore_count = 0

        results.append({

            "Column": column,

            "Total Values": len(series),

            "IQR Outliers": int(iqr_count),

            "IQR Outlier %": round(
                iqr_count / len(series) * 100,
                2
            ),

            "Z-Score Outliers": int(zscore_count),

            "Z-Score Outlier %": round(
                zscore_count / len(series) * 100,
                2
            ),

            "Lower Bound": round(
                lower_bound,
                2
            ),

            "Upper Bound": round(
                upper_bound,
                2
            )
        })

    return pd.DataFrame(results)