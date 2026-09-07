import pandas as pd


def analyze_data_quality(df):
    """
    Analyze data quality for every column.
    """

    quality = []

    for column in df.columns:

        missing_values = int(df[column].isna().sum())

        missing_percentage = (
            missing_values / len(df) * 100
            if len(df) > 0
            else 0
        )

        unique_values = int(
            df[column].nunique(dropna=True)
        )

        # Check whether column is constant
        is_constant = unique_values <= 1

        quality.append({

            "Column": column,

            "Missing Values": missing_values,

            "Missing %": round(
                missing_percentage,
                2
            ),

            "Unique Values": unique_values,

            "Constant Column": (
                "Yes" if is_constant else "No"
            )

        })

    return pd.DataFrame(quality)


def calculate_quality_score(df):
    """
    Calculate an overall data quality score from 0 to 100.
    """

    if len(df) == 0 or len(df.columns) == 0:
        return 0.0

    # -----------------------------------
    # 1. Missing value penalty
    # -----------------------------------

    total_cells = df.shape[0] * df.shape[1]

    total_missing = int(
        df.isna().sum().sum()
    )

    missing_percentage = (
        total_missing / total_cells * 100
        if total_cells > 0
        else 0
    )

    missing_penalty = min(
        missing_percentage,
        30
    )


    # -----------------------------------
    # 2. Duplicate row penalty
    # -----------------------------------

    duplicate_count = int(
        df.duplicated().sum()
    )

    duplicate_percentage = (
        duplicate_count / len(df) * 100
        if len(df) > 0
        else 0
    )

    duplicate_penalty = min(
        duplicate_percentage,
        20
    )


    # -----------------------------------
    # 3. Constant column penalty
    # -----------------------------------

    constant_columns = 0

    for column in df.columns:

        unique_count = df[column].nunique(
            dropna=True
        )

        if unique_count <= 1:
            constant_columns += 1

    constant_percentage = (
        constant_columns / len(df.columns) * 100
        if len(df.columns) > 0
        else 0
    )

    constant_penalty = min(
        constant_percentage,
        10
    )


    # -----------------------------------
    # Final score
    # -----------------------------------

    score = (
        100
        - float(missing_penalty)
        - float(duplicate_penalty)
        - float(constant_penalty)
    )

    # Make sure score stays between 0 and 100

    score = max(
        0.0,
        min(100.0, score)
    )

    return round(score, 2)