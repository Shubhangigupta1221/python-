import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = r"C:\Users\ADMIN\OneDrive\Desktop\Python Project\AirQualityUCI.xlsx"
df = pd.read_excel(file_path, sheet_name='AirQualityUCI')

# Check column names
print("Column names in the dataset:", df.columns)

# Create CO level categories
df['CO_Level'] = pd.cut(df['CO(GT)'], bins=[0, 2, 5, 10, 15], labels=['Low', 'Moderate', 'High', 'Very High'])

# Bar-chart for CO level categories
plt.figure(figsize=(8, 6))
sns.countplot(x='CO_Level', hue='CO_Level', data=df, palette='viridis', legend=False)
plt.title('Frequency of CO Level Categories')
plt.xlabel('CO Level')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig("co_level_bar.png")
plt.show()

columns = ['CO(GT)', 'PT08.S1(CO)', 'NMHC(GT)', 'C6H6(GT)', 'PT08.S2(NMHC)',
           'NOx(GT)', 'PT08.S3(NOx)', 'NO2(GT)', 'PT08.S4(NO2)',
           'PT08.S5(O3)', 'T', 'RH', 'AH']

for col in columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df.dropna(inplace=True)

# Display basic statistics
print("Basic Statistics:")
print(df[columns].describe())

# PLOT 1: CO Distribution
plt.figure(figsize=(10, 5))
sns.histplot(df['CO(GT)'], bins=30, kde=True, color='skyblue')
plt.title('Distribution of CO Levels')
plt.xlabel('CO(GT)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig("co_distribution.png")
plt.show()

df.replace(-200, pd.NA, inplace=True)
df = df[['CO(GT)', 'T', 'NOx(GT)']].dropna()

# Create CO level categories
df['CO_Level'] = pd.cut(df['CO(GT)'], bins=[0, 2, 5, 10, 15], labels=['Low', 'Moderate', 'High', 'Very High'])

# Create Temperature categories
df['Temp_Level'] = pd.cut(df['T'], bins=[-5, 10, 20, 30, 45], labels=['Cold', 'Mild', 'Warm', 'Hot'])

# Create NOx level categories
df['NOx_Level'] = pd.cut(df['NOx(GT)'], bins=[0, 100, 300, 600, 1500], labels=['Low', 'Moderate', 'High', 'Very High'])

# 1. Countplot: CO Levels
plt.figure(figsize=(7, 5))
sns.countplot(x='CO_Level', data=df, hue='CO_Level', palette='Blues', legend=False)
plt.title('Count of CO Level Categories')
plt.xlabel('CO Level')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig("countplot_co_levels.png")
plt.show()

# 2. Countplot: Temperature Levels
plt.figure(figsize=(7, 5))
sns.countplot(x='Temp_Level', data=df, hue='Temp_Level', palette='Oranges', legend=False)
plt.title('Count of Temperature Categories')
plt.xlabel('Temperature Level')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig("countplot_temp_levels.png")
plt.show()

# 3. Countplot: NOx Levels
plt.figure(figsize=(7, 5))
sns.countplot(x='NOx_Level', data=df, hue='NOx_Level', palette='Purples', legend=False)
plt.title('Count of NOx Level Categories')
plt.xlabel('NOx Level')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig("countplot_nox_levels.png")
plt.show()

df = df.dropna()

# Basic cleanup: drop date/time if not needed
if 'Date' in df.columns and 'Time' in df.columns:
    df['Datetime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str), errors='coerce')
    df.set_index('Datetime', inplace=True)
else:
    print("Warning: 'Date' and/or 'Time' columns are missing in the dataset.")

