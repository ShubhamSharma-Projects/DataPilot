from google import genai


def create_client(api_key):
    """Create Gemini client."""
    return genai.Client(api_key=api_key)


def create_dataset_context(df, understanding):
    """Create a compact dataset description for Gemini."""

    context = [
        f"Rows: {len(df)}",
        f"Columns: {len(df.columns)}",
        "\nColumn information:"
    ]

    for _, row in understanding.iterrows():

        context.append(
            f"- {row['Column']}: "
            f"data type={row['Data Type']}, "
            f"role={row['Role']}, "
            f"analytical type={row['Analytical Type']}"
        )

    return "\n".join(context)


def generate_analysis_code(
    client,
    question,
    dataset_context
):
    """
    Generate Pandas code that directly answers
    the user's question.
    """

    prompt = f"""
You are DataPilot, an expert data analyst.

DATASET:

{dataset_context}

USER QUESTION:

{question}

Generate Python Pandas code that answers EXACTLY
what the user asked.

IMPORTANT:

- If the user says "average" or "mean", use .mean()
- If the user says "total" or "sum", use .sum()
- If the user says "maximum" or "highest", use .max()
- If the user says "minimum" or "lowest", use .min()
- If the user says "median", use .median()
- If the user asks "how many", use .count() or .size()
- If the user asks for top N, sort appropriately and use .head(N)
- Do not substitute SUM for AVERAGE.
- Do not substitute AVERAGE for SUM.
- Pay very close attention to the wording of the question.

RULES:

1. The dataframe is already available as df.
2. Use Pandas only.
3. Do not load another dataset.
4. Do not access the internet.
5. Do not read or write files.
6. Do not import libraries.
7. Store the final answer in a variable called result.
8. Return ONLY Python code.
9. Do not use markdown code fences.
10. Keep the code concise.

Example:

Question:
Which category has the highest average views?

Correct code:

result = (
    df.groupby("Category")["Views"]
    .mean()
    .sort_values(ascending=False)
    .head(1)
)
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return interaction.output_text


def generate_answer(
    client,
    question,
    result
):
    """
    Convert the analysis result into a
    concise analyst-style answer.
    """

    prompt = f"""
You are DataPilot, a professional data analyst.

The user asked:

{question}

The analysis produced this result:

{result}

Give the user a concise, clear answer.

Rules:

1. Answer the actual question.
2. Do not invent numbers or facts.
3. Use the result provided.
4. If the result is a table, identify the relevant value.
5. Keep the answer to 1-3 sentences.
6. Use professional but simple language.
7. Do not mention Python, Pandas, APIs, or code.
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return interaction.output_text