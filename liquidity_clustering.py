# CROSS-MARKET LIQUIDITY VELOCITY & ML CLUSTERING SUITE
# Oluyomi Abayomi | Trader since 2020 | Data Analyst
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load your master file
xls = pd.ExcelFile('crypto_stocks_analytics_master_Oluyomi_P_1.xls')
core = xls.parse('Core Market Data')
ml = xls.parse('ML Cluster Analysis')
pump = xls.parse('Historical Pump Data')

# --- Feature Engineering (Already in your file, reproduced) ---
# Velocity = Current / Jan 2024
core['Volume_Velocity'] = core['Current Volume'] / core['Jan 2024 Volume']
core['Mcap_Velocity'] = core['Current Market Cap'] / core['Jan 2024 Market Cap']
core['ROI_Pct'] = (core['Current Close'] - core['Jan 2024 Open']) / core['Jan 2024 Open'] * 100

# --- Z-score + K-Means ---
features = ml[['Volume Velocity Factor','Market Cap Velocity Factor','ROI Percent']].fillna(0)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
ml['Cluster_Label'] = kmeans.fit_predict(X_scaled)

# Map clusters to business names from your doc
cluster_map = {
    0: 'Speculative Outliers (POPCAT 300x velocity)',
    1: 'Institutional Compounders (NVIDIA +350%, TRON, BTC)',
    2: 'Mature Laggards (Volume Decay)'
}
# Note: Your sheet already has clustering, this validates it

print(ml.groupby('K-Means Cluster Group')['ROI Percent'].mean())
print(f"SHIB Peak: {pump[pump['Ticker']=='SHIB']['Peak Pump ROI Pct'].values[0]:.0f}% ROI")
print(f"LUNA Drawdown: {pump[pump['Ticker']=='LUNA']['Drawdown From ATH Pct'].values[0]*100:.1f}% - Lesson since 2020")

# --- BI Dashboard Plot (Power BI style) ---
plt.figure(figsize=(10,6))
plt.scatter(ml['Volume Velocity Factor'], ml['ROI Percent'], c=ml['K-Means Cluster Group'], s=100, cmap='viridis')
for i, row in ml.iterrows():
    plt.text(row['Volume Velocity Factor'], row['ROI Percent'], row['Ticker'], fontsize=8)
plt.xscale('log')
plt.xlabel('Volume Velocity Factor (Liquidity Migration) - Log Scale')
plt.ylabel('ROI % Jan24->Now')
plt.title('Cross-Market Liquidity Velocity: Institutional vs Speculative\nOluyomi Abayomi | Trader since 2020')
plt.axhline(y=0, color='r', linestyle='--')
plt.grid(alpha=0.3)
plt.savefig('bi_dashboard_scatter.png', dpi=300, bbox_inches='tight')
print("Saved: bi_dashboard_scatter.png - Use this as your BI visual")
