import pandas as pd

def generate_insights(df):
    insights = []

    numeric_cols = df.select_dtypes(include=['number']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns

    # 📊 Highest value insight
    if len(numeric_cols) > 0:
        col = numeric_cols[0]
        max_value = df[col].max()
        insights.append(f"Highest {col} is {max_value}")

    # 📊 Category performance
    if len(categorical_cols) > 0 and len(numeric_cols) > 0:
        cat = categorical_cols[0]
        num = numeric_cols[0]

        grouped = df.groupby(cat)[num].sum().sort_values(ascending=False)
        top_category = grouped.index[0]

        insights.append(f"{top_category} has the highest {num}")

    # 📈 Trend insight
    if len(numeric_cols) > 0:
        col = numeric_cols[0]
        if df[col].iloc[-1] > df[col].iloc[0]:
            insights.append(f"{col} shows an increasing trend")
        else:
            insights.append(f"{col} shows a decreasing trend")

    return insights