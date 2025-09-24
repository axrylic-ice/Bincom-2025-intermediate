import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Load dataset
# -----------------------------
df_csv = pd.read_csv('Bincom-answers/wk1/fifa21_raw_data_v2.csv')

# -----------------------------
# 1. Convert Height and Weight to numeric
# -----------------------------
def lb_kg(weight):
    """Convert weight in lbs/kg to kilograms."""
    if "kg" in weight:
        return weight.replace("kg", "")
    elif "lbs" in weight:
        weight = weight.replace("lbs", "")
        return int(weight) * 0.45359237

def inch_cm(size):
    """Convert height in feet/inches or cm to centimeters."""
    if "cm" in size:
        return size.replace("cm", "")
    feet, inches = size.split("'")
    inches = inches.replace('"', "")
    return round((int(feet) * 12 + int(inches)) * 2.54, 2)

df_csv["Height"] = df_csv['Height'].apply(inch_cm).astype(float)
df_csv["Weight"] = df_csv['Weight'].apply(lb_kg).astype(float)

# -----------------------------
# 2. Remove unnecessary newline characters
# -----------------------------
df_csv.replace('\n', '', regex=True, inplace=True)

# -----------------------------
# 3. Players who have been at their club for more than 10 years
# -----------------------------
long_tenure = df_csv[
    pd.to_datetime("today").year - pd.to_datetime(df_csv["Joined"]).dt.year > 10
]["Name"]

print("Players at their club for more than 10 years:")
print(long_tenure)

# -----------------------------
# 4. Convert Value, Wage, Release Clause to numeric
# -----------------------------
def m_K(value):
    """Convert monetary strings (€K, €M) to float values in euros."""
    if "K" in value:
        return float(value.replace("K", "").replace("€", "")) * 1000
    elif "M" in value:
        return float(value.replace("M", "").replace("€", "")) * 1_000_000
    return float(value.replace("€", ""))

# Suggestion: assign back to DataFrame immediately instead of applying twice
df_csv["Value"] = df_csv["Value"].apply(m_K).astype(float)
df_csv["Wage"] = df_csv["Wage"].apply(m_K).astype(float)
df_csv["Release Clause"] = df_csv["Release Clause"].apply(m_K).astype(float)

# -----------------------------
# 5. Remove star characters and convert to numeric
# -----------------------------
for col in df_csv.columns.tolist():
    if df_csv[col].dtype == 'object':
        if df_csv[col].str.contains("★").any():
            df_csv[col] = df_csv[col].str.replace("★", "").astype(float)

# -----------------------------
# 6. Identify highly valuable but underpaid players
# -----------------------------
plt.figure(figsize=(10, 6))
plt.scatter(df_csv["Wage"], df_csv["Value"], alpha=0.7, edgecolors='k')
plt.title("Scatter Plot: Value vs Wage")
plt.xlabel("Wage (€)")
plt.ylabel("Value (€)")
plt.grid(True)

# Define threshold: high value = top 25%, low wage = bottom 25%
high_value_low_wage = df_csv[
    (df_csv["Value"] > df_csv["Value"].quantile(0.75)) &
    (df_csv["Wage"] < df_csv["Wage"].quantile(0.25))
]

# Highlight these players in red
plt.scatter(
    high_value_low_wage["Wage"], high_value_low_wage["Value"],
    color='red', label='High Value, Low Wage'
)
plt.legend()
plt.show()

# Print player names
print("Highly valuable but underpaid players:")
print(high_value_low_wage["Name"])
