import plotly.express as px

def generate_charts(df):
    charts = []

    numeric_cols = df.select_dtypes(include=['number']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns

    # 📊 Bar chart (categorical vs numeric)
    if len(categorical_cols) > 0 and len(numeric_cols) > 0:
        fig = px.bar(df, x=categorical_cols[0], y=numeric_cols[0], title="Bar Chart")
        charts.append(fig)

    # 📈 Line chart (if numeric exists)
    if len(numeric_cols) > 0:
        fig = px.line(df, y=numeric_cols[0], title="Trend")
        charts.append(fig)

    # 🔵 Scatter plot
    if len(numeric_cols) > 1:
        fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title="Scatter Plot")
        charts.append(fig)

    return charts