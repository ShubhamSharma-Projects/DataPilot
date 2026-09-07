import pandas as pd


def profile_dataset(df):
    """
    Generate an automatic profile of the uploaded dataset.
    """

    profile = []

    # Loop through every column
    for column in df.columns:

        # -----------------------------------
        # BASIC INFORMATION
        # -----------------------------------

        data_type = str(df[column].dtype)

        missing_count = df[column].isna().sum()

        if len(df) > 0:
            missing_percentage = (
                missing_count / len(df) * 100
            )
        else:
            missing_percentage = 0

        unique_count = df[column].nunique(
            dropna=True
        )

        # -----------------------------------
        # COLUMN TYPE DETECTION
        # -----------------------------------

        # 1. Boolean
        if pd.api.types.is_bool_dtype(df[column]):

            column_type = "Boolean"

        # 2. Numeric
        elif pd.api.types.is_numeric_dtype(df[column]):

            column_type = "Numeric"

        # 3. Already recognized as Date
        elif pd.api.types.is_datetime64_any_dtype(df[column]):

            column_type = "Date"

        else:

            # -----------------------------------
            # IDENTIFIER DETECTION
            # -----------------------------------

            column_name = (
                str(column)
                .lower()
                .replace("_", " ")
                .strip()
            )

            identifier_keywords = [
                "id",
                "identifier",
                "channel id",
                "video id",
                "customer id",
                "user id",
                "order id",
                "transaction id",
                "employee id",
                "product id"
            ]

            is_identifier = any(
                keyword == column_name
                or keyword in column_name
                for keyword in identifier_keywords
            )

            if is_identifier:

                column_type = "Identifier"

            else:

                # -----------------------------------
                # DATE DETECTION FOR TEXT COLUMNS
                # -----------------------------------

                sample = (
                    df[column]
                    .dropna()
                    .astype(str)
                    .head(100)
                )

                if len(sample) > 0:

                    parsed_dates = pd.to_datetime(
                        sample,
                        errors="coerce",
                        format="mixed"
                    )

                    date_ratio = (
                        parsed_dates.notna().mean()
                    )

                    if date_ratio >= 0.80:

                        column_type = "Date"

                    else:

                        column_type = "Categorical/Text"

                else:

                    column_type = "Categorical/Text"

        # -----------------------------------
        # ADD COLUMN PROFILE
        # -----------------------------------

        profile.append({

            "Column": column,

            "Data Type": data_type,

            "Detected Type": column_type,

            "Missing Values": missing_count,

            "Missing %": round(
                missing_percentage,
                2
            ),

            "Unique Values": unique_count

        })

    # -----------------------------------
    # RETURN PROFILE
    # -----------------------------------

    return pd.DataFrame(profile)