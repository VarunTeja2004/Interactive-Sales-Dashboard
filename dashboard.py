import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =============================
# LOAD DATA
# =============================

df = pd.read_csv("/content/sample_data/sales_data (2).csv")

# Clean column names (very important fix)
df.columns = df.columns.str.strip()

# Convert Date
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Remove missing
df = df.dropna()

# Extract Month
df["Month"] = df["Date"].dt.month

# =============================
# BUSINESS METRICS
# =============================

total_revenue = df["Total_Sales"].sum()
total_customers = df["Customer_ID"].nunique()
avg_order_value = df["Total_Sales"].mean()

monthly_sales = df.groupby("Month")["Total_Sales"].sum()
regional_sales = df.groupby("Region")["Total_Sales"].sum()
top_products = df.groupby("Product")["Quantity"].sum().sort_values(ascending=False)

# =============================
# SEABORN VISUALS
# =============================

sns.set_style("whitegrid")

# Box Plot
plt.figure(figsize=(8,5))
sns.boxplot(x="Region", y="Total_Sales", data=df)
plt.title("Sales Distribution by Region")
plt.xticks(rotation=45)
plt.show()

# Correlation Heatmap
plt.figure(figsize=(6,5))
sns.heatmap(df[["Total_Sales","Quantity"]].corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Matrix")
plt.show()

# =============================
# INTERACTIVE DASHBOARD
# =============================

sales_trend = df.groupby("Date")["Total_Sales"].sum().reset_index()

dashboard = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Sales Trend","Top Products","Regional Share","Sales vs Quantity"),
    specs=[[{"type":"xy"},{"type":"xy"}],
           [{"type":"domain"},{"type":"xy"}]]
)

# Line Chart
dashboard.add_trace(
    go.Scatter(x=sales_trend["Date"],
               y=sales_trend["Total_Sales"],
               mode="lines",
               name="Sales"),
    row=1, col=1
)

# Bar Chart
dashboard.add_trace(
    go.Bar(x=top_products.index,
           y=top_products.values,
           name="Products"),
    row=1, col=2
)

# Pie Chart
dashboard.add_trace(
    go.Pie(labels=regional_sales.index,
           values=regional_sales.values),
    row=2, col=1
)

# Scatter
dashboard.add_trace(
    go.Scatter(x=df["Total_Sales"],
               y=df["Quantity"],
               mode="markers"),
    row=2, col=2
)

dashboard.update_layout(
    height=800,
    width=1000,
    title="Interactive Sales Dashboard",
    showlegend=False
)

dashboard.show()

# =============================
# FINAL REPORT
# =============================

print("="*50)
print("       CUSTOMER SALES DASHBOARD REPORT")
print("="*50)
print(f"Total Revenue: ${total_revenue:,.0f}")
print(f"Total Customers: {total_customers}")
print(f"Average Order Value: ${avg_order_value:,.0f}")
print("="*50)
