import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = r"C:\Users\ADMIN\OneDrive\Desktop\Python Project\AirQualityUCI.xlsx"
df = pd.read_excel(file_path, sheet_name='AirQualityUCI')

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
print("Basic Statistics:")
print(df[columns].describe())

#PLOT 1: CO Distribution
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
sns.countplot(x='CO_Level', data=df, palette='Blues')
plt.title('Count of CO Level Categories')
plt.xlabel('CO Level')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig("countplot_co_levels.png")
plt.show()

# 2. Countplot: Temperature Levels
plt.figure(figsize=(7, 5))
sns.countplot(x='Temp_Level', data=df, palette='Oranges')
plt.title('Count of Temperature Categories')
plt.xlabel('Temperature Level')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig("countplot_temp_levels.png")
plt.show()

# 3. Countplot: NOx Levels
plt.figure(figsize=(7, 5))
sns.countplot(x='NOx_Level', data=df, palette='Purples')
plt.title('Count of NOx Level Categories')
plt.xlabel('NOx Level')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig("countplot_nox_levels.png")
plt.show()


df = df.dropna()
# Basic cleanup: drop date/time if not needed
if 'Date' in df.columns and 'Time' in df.columns:
    df.drop(['Date', 'Time'], axis=1, inplace=True)
sns.set(style='whitegrid')
# 1. Correlation Heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Correlation Heatmap of Air Quality Features')
plt.tight_layout()
plt.savefig("correlation_heatmap.png")
plt.show()

# Combine Date and Time into a datetime column
df['Datetime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str), errors='coerce')

# Replace -200 with NaN for selected pollutants
pollutants = ['CO(GT)', 'NOx(GT)', 'C6H6(GT)']
df[pollutants] = df[pollutants].replace(-200, pd.NA)

# Drop rows with missing datetime
df = df.dropna(subset=['Datetime'])

# Set datetime as index
df.set_index('Datetime', inplace=True)

# Daily average of pollutants
daily_avg = df[pollutants].resample('D').mean()

# Calculate overall average values for pie chart
mean_values = daily_avg.mean().dropna()

# Pie chart
colors = ['yellow', 'lightgreen', 'orange']
plt.figure(figsize=(8, 8))
plt.pie(mean_values, labels=mean_values.index, autopct='%1.1f%%', startangle=140, colors=colors)
plt.title('Proportion of Average Pollutant Levels Over Time', fontsize=14)
plt.tight_layout()
plt.savefig("pollutants_pie_chart.png")
plt.show()

df['Datetime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str), errors='coerce')

for col in ['CO(GT)', 'NOx(GT)', 'C6H6(GT)']:
    df[col] = df[col].replace(-200, pd.NA)

df = df.dropna(subset=['Datetime'])

df.set_index('Datetime', inplace=True)

daily_df = df[['CO(GT)', 'NOx(GT)', 'C6H6(GT)']].resample('D').mean()

# Function to plot line chart
def plot_pollutant_line(pollutant, color):
    plt.figure(figsize=(14, 6))
    sns.lineplot(data=daily_df, x=daily_df.index, y=pollutant, color=color, linewidth=2)
    plt.title(f'Daily Average {pollutant} Levels Over Time', fontsize=16)
    plt.xlabel('Date')
    plt.ylabel(f'{pollutant} (mg/m³)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{pollutant.lower().replace('(gt)', '').strip()}_line_chart.png")
    plt.show()

# Plotting all three
plot_pollutant_line('CO(GT)', 'green')
plot_pollutant_line('NOx(GT)', 'blue')
plot_pollutant_line('C6H6(GT)', 'purple')


df.replace(-200, pd.NA, inplace=True)
df = df.dropna(subset=['NOx(GT)', 'T', 'C6H6(GT)'])

# 1. Histogram of NOx(GT) 
plt.figure(figsize=(10, 5))
sns.histplot(df['NOx(GT)'], bins=30, kde=False, color='tomato')
plt.title('Histogram of NOx Levels')
plt.xlabel('NOx (GT)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig("hist_nox.png")
plt.show()

# 2. KDE Plot of Temperature
plt.figure(figsize=(10, 5))
sns.kdeplot(df['T'], shade=True, color='purple')
plt.title('KDE Plot of Temperature')
plt.xlabel('Temperature (T)')
plt.tight_layout()
plt.savefig("kde_temp.png")
plt.show()

#  3. Histogram + KDE of C6H6(GT) 
plt.figure(figsize=(10, 5))
sns.histplot(df['C6H6(GT)'], bins=30, kde=True, color='dodgerblue')
plt.title('Distribution of Benzene (C6H6) Levels')
plt.xlabel('C6H6 (GT)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig("hist_kde_c6h6.png")
plt.show()

df.replace(-200, pd.NA, inplace=True)

selected_columns = ['CO(GT)', 'NOx(GT)', 'C6H6(GT)', 'T', 'RH']

filtered_df = df[selected_columns].dropna()

# Creating-pairplot
sns.pairplot(filtered_df, diag_kind='kde', corner=True)
plt.suptitle("Pairplot: Pollutants and Weather Factors", fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig("pairplot_pollutants.png")
plt.show()

df.replace(-200, pd.NA, inplace=True)

# Drop rows with missing values for relevant columns
df = df[['CO(GT)', 'NOx(GT)', 'C6H6(GT)', 'T', 'RH']].dropna()

# 1. Scatter Plot: Temperature vs CO(GT)
plt.figure(figsize=(8, 5))
sns.scatterplot(x='T', y='CO(GT)', data=df, color='red')
plt.title('Temperature vs CO Levels')
plt.xlabel('Temperature (°C)')
plt.ylabel('CO (GT)')
plt.tight_layout()
plt.savefig("scatter_temp_vs_co.png")
plt.show()

# 2. Scatter Plot: RH vs NOx(GT)
plt.figure(figsize=(8, 5))
sns.scatterplot(x='RH', y='NOx(GT)', data=df, color='blue')
plt.title('Relative Humidity vs NOx Levels')
plt.xlabel('Relative Humidity (%)')
plt.ylabel('NOx (GT)')
plt.tight_layout()
plt.savefig("scatter_rh_vs_nox.png")
plt.show()

# 3. Scatter Plot: Temperature vs C6H6(GT)
plt.figure(figsize=(8, 5))
sns.scatterplot(x='T', y='C6H6(GT)', data=df, color='green')
plt.title('Temperature vs C6H6 Levels')
plt.xlabel('Temperature (°C)')
plt.ylabel('C6H6 (GT)')
plt.tight_layout()
plt.savefig("scatter_temp_vs_c6h6.png")
plt.show()

pollutants = ['CO(GT)', 'NOx(GT)', 'C6H6(GT)']
values = [35, 50, 15]

# Custom colors (optional)
colors = ['#4CAF50', '#2196F3', '#FFC107']

# Create a pie chart with a hole in the center
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(
    values,
    labels=pollutants,
    colors=colors,
    autopct='%1.1f%%',
    startangle=140,
    wedgeprops={'width': 0.4}  # this creates the "donut" effect
)

centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig.gca().add_artist(centre_circle)

# Add a title and show
ax.set_title("Pollutant Proportions - Donut Chart")
plt.tight_layout()
plt.savefig("pollutants_donut_chart.png")
plt.show()

df.dropna(axis=1, how='all', inplace=True)
df.columns = df.columns.str.strip()


df['Datetime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str), errors='coerce')
df.set_index('Datetime', inplace=True)

# Clean data
df = df[df['CO(GT)'] != -200]

df.reset_index(inplace=True)

#1. Time-Series Plot: CO over Time 
plt.figure(figsize=(14, 6))
df.set_index('Datetime')['CO(GT)'].plot(color='teal')
plt.title('CO Levels Over Time')
plt.xlabel('Datetime')
plt.ylabel('CO (GT)')
plt.tight_layout()
plt.savefig("co_over_time.png")
plt.show()

df['CO_Level'] = pd.cut(df['CO(GT)'], bins=[0, 2, 5, 10, 15], labels=['Low', 'Moderate', 'High', 'Very High'])

# Violin-plot for NO2(GT) by CO level
plt.figure(figsize=(10, 6))
sns.violinplot(x='CO_Level', y='NO2(GT)', data=df, palette='Set2')
plt.title('NO2 Levels Across CO Categories')
plt.xlabel('CO Level')
plt.ylabel('NO2 (GT)')
plt.tight_layout()
plt.savefig("no2_violin_by_co.png")
plt.show()
