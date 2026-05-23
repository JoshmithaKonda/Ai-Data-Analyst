from langchain_openai import ChatOpenAI
import os
import streamlit as st

# 🔐 Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=st.secrets["OPENAI_API_KEY"]
)

# 🔹 AI reasoning (WHY explanations)
def generate_reasoning(insights):
    prompt = f"""
You are a data analyst.

Explain WHY these insights might be happening.

Rules:
- Be clear and natural
- No steps
- Keep it short

Insights:
{insights}
"""
    response = llm.invoke(prompt)
    return response.content


# 🔹 Smart Chat with Data (DYNAMIC + SAFE + ACCURATE)
def chat_with_data(df, question):
    question_lower = question.lower()

    numeric_cols = df.select_dtypes(include='number').columns
    categorical_cols = df.select_dtypes(include='object').columns

    # 🔥 Detect numeric column
    target_col = None
    for col in numeric_cols:
        if col.lower() in question_lower:
            target_col = col
            break

    if target_col is None and len(numeric_cols) > 0:
        target_col = numeric_cols[0]

    # 🔥 Detect category column
    category_col = None
    for col in categorical_cols:
        if col.lower() in question_lower:
            category_col = col
            break

    # 🔥 Label column (like date)
    label_col = None
    for col in df.columns:
        if col not in numeric_cols:
            label_col = col
            break

    # =========================
    # ✅ SAFE OPERATIONS
    # =========================

    if target_col is None:
        return "No numeric column found in dataset."

    try:
        # ✅ MIN
        if "lowest" in question_lower or "minimum" in question_lower:
            row = df.loc[df[target_col].astype(float).idxmin()]
            if label_col:
                return f"The lowest {target_col} is {row[target_col]} (on {row[label_col]})."
            return f"The lowest {target_col} is {row[target_col]}."

        # ✅ MAX
        if "highest" in question_lower or "maximum" in question_lower:
            row = df.loc[df[target_col].astype(float).idxmax()]
            if label_col:
                return f"The highest {target_col} is {row[target_col]} (on {row[label_col]})."
            return f"The highest {target_col} is {row[target_col]}."

        # ✅ SUM
        if "total" in question_lower or "sum" in question_lower:
            total = df[target_col].astype(float).sum()
            return f"The total {target_col} is {total}."

        # ✅ AVERAGE
        if "average" in question_lower or "mean" in question_lower:
            avg = df[target_col].astype(float).mean()
            return f"The average {target_col} is {round(avg, 2)}."

        # ✅ GROUP BY CATEGORY
        if category_col and ("highest" in question_lower or "best" in question_lower):
            grouped = df.groupby(category_col)[target_col].sum()
            top = grouped.idxmax()
            return f"The {category_col} with the highest {target_col} is {top}."

    except Exception:
        return "There was an issue processing the data."

    # =========================
    # 🤖 LLM FALLBACK
    # =========================
    try:
        sample_data = df.sample(min(len(df), 10)).to_string()

        prompt = f"""
You are a data analyst.

Dataset sample:
{sample_data}

Rules:
- Answer clearly
- No steps
- Be accurate

Question: {question}
"""
        response = llm.invoke(prompt)
        return response.content

    except Exception:
        return "Unable to process the request with AI."