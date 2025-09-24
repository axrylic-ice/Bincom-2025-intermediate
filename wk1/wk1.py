import pandas as pd
import matplotlib.pyplot as plt

df_csv=pd.read_csv('Bincom-answers/wk1/fifa21_raw_data_v2.csv')

#1. Convert the height and weight columns to numerical forms

def lb_kg(weight):
    if "kg" in weight:
        return weight.replace("kg", "")
    elif "lbs" in weight:
        weight=weight.replace("lbs", "")
    return int(weight)*0.45359237

def inch_cm(size):
    if "cm" in size:
        return size.replace("cm", "")
    feet,inches= size.split("'")
    inches=inches.replace('"', "")
    return round((int(feet)*12 + int(inches))*2.54,2)

df_csv["Height"] = df_csv['Height'].apply(inch_cm).astype(float)
df_csv["Weight"] = df_csv['Weight'].apply(lb_kg).astype(float)

#2. Remove the unnecessary newline characters from all columns that hve them

df_csv.replace('\n', '', regex=True, inplace=True)

#3. based on the 'Joined ' Column , check which players have been playing at a cub for more than 10 years!

print(df_csv[pd.to_datetime("today").year - pd.to_datetime(df_csv["Joined"]).dt.year > 10]["Name"])

#4. 'value', 'wage', and 'release_clause' columns are in string format. Convert them to numerical form

def m_K(value):
    if "K" in value:
        return float(value.replace("K","").replace("€",""))*1000
    
    elif "M" in value:
        
        return float(value.replace("€","").replace("M",""))*1000000
    return float(value.replace("€",""))

df_csv["Value"].apply(m_K).astype(float)
df_csv["Wage"].apply(m_K).astype(float)
df_csv["Release Clause"].apply(m_K).astype(float)

#5. Some columns hve star characters strip those columns of these stars and make the columns numerical

col= df_csv.columns.tolist()
for i in col:
    if df_csv[i].dtype == 'object':
        if df_csv[i].str.contains("★").any():
            df_csv[i]=df_csv[i].str.replace("★","").astype(float)
            
#6. which players are highly valuable but still underpaid (on low wages)?(hint:Scatter plot between value and wage)

# Convert 'Value' and 'Wage' columns to numeric using the m_K function
df_csv["Value"] = df_csv["Value"].apply(m_K).astype(float)
df_csv["Wage"] = df_csv["Wage"].apply(m_K).astype(float)

# Scatter plot between value and wage
plt.figure(figsize=(10, 6))
plt.scatter(df_csv["Wage"], df_csv["Value"], alpha=0.7, edgecolors='k')
plt.title("Scatter Plot: Value vs Wage")
plt.xlabel("Wage (€)")
plt.ylabel("Value (€)")
plt.grid(True)

# Highlight players who are highly valuable but underpaid
high_value_low_wage = df_csv[(df_csv["Value"] > df_csv["Value"].quantile(0.75)) & 
                             (df_csv["Wage"] < df_csv["Wage"].quantile(0.25))]
plt.scatter(high_value_low_wage["Wage"], high_value_low_wage["Value"], color='red', label='High Value, Low Wage')

plt.legend()
plt.show()

# Print the names of these players
print("Highly valuable but underpaid players:")
print(high_value_low_wage["Name"])
