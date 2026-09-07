import pandas as pd


def understand_dataset(df):
    """
    Identify the analytical role of each column.

    Roles:
    - Measure
    - Dimension
    - Identifier
    - Date
    - Text
    - Boolean
    """

    results = []

    for column in df.columns:

        series = df[column]

        # -----------------------------------
        # BASIC INFORMATION
        # -----------------------------------

        data_type = str(series.dtype)

        non_null = series.dropna()

        unique_count = series.nunique(
            dropna=True
        )

        total_count = len(series)

        uniqueness_ratio = (
            unique_count / total_count
            if total_count > 0
            else 0
        )

        # -----------------------------------
        # DATE DETECTION
        # -----------------------------------

        is_date = False

        if pd.api.types.is_datetime64_any_dtype(series):

            is_date = True

        elif series.dtype == "object":

            sample = non_null.head(100)

            if len(sample) > 0:

                converted = pd.to_datetime(
                    sample,
                    errors="coerce"
                )

                if converted.notna().mean() >= 0.8:

                    is_date = True

        # -----------------------------------
        # BOOLEAN
        # -----------------------------------

        if pd.api.types.is_bool_dtype(series):

            role = "Boolean"
            analytical_type = "Categorical"

        # -----------------------------------
        # DATE
        # -----------------------------------

        elif is_date:

            role = "Date"
            analytical_type = "Temporal"

        # -----------------------------------
        # NUMERIC
        # -----------------------------------

        elif pd.api.types.is_numeric_dtype(series):

            # Low-cardinality numeric columns
            # are usually categories or codes.

            if unique_count <= 20:

                role = "Dimension"
                analytical_type = "Categorical"

            # Columns where almost every value
            # is unique are often identifiers.

            elif uniqueness_ratio >= 0.95:

                role = "Identifier"
                analytical_type = "ID"

            else:

                role = "Measure"
                analytical_type = "Numeric"

        # -----------------------------------
        # TEXT / CATEGORICAL
        # -----------------------------------

        else:

            if unique_count <= 50:

                role = "Dimension"
                analytical_type = "Categorical"

            elif uniqueness_ratio >= 0.95:

                role = "Identifier"
                analytical_type = "ID"

            else:

                role = "Text"
                analytical_type = "Text"

        # -----------------------------------
        # STORE RESULT
        # -----------------------------------

        results.append({

            "Column": column,

            "Data Type": data_type,

            "Role": role,

            "Analytical Type": analytical_type,

            "Unique Values": unique_count,

            "Uniqueness %": round(
                uniqueness_ratio * 100,
                2
            )

        })

    return pd.DataFrame(results)