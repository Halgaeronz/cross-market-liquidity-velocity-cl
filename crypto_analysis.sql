-- CROSS-MARKET LIQUIDITY VELOCITY & ML CLUSTERING
-- Oluyomi Abayomi | Crypto Trader since 2020

-- 1. Institutional Compounders vs Speculative Outliers (K-Means validation)
SELECT 
  `K-Means Cluster Group`,
  COUNT(*) as assets,
  AVG(`ROI Percent`) as avg_roi_pct,
  AVG(`Volume Velocity Factor`) as avg_vol_velocity,
  AVG(`Market Cap Velocity Factor`) as avg_mcap_velocity
FROM `ML Cluster Analysis`
GROUP BY `K-Means Cluster Group`
ORDER BY avg_roi_pct DESC;
-- Result: Cluster 0 = 182% ROI, 178x Volume Velocity = Institutional Compounders (NVIDIA, BTC)

-- 2. Top Velocity: Where smart money is migrating
SELECT Ticker, `Asset Class`, `Volume Velocity Factor`, `Market Cap Velocity Factor`, `ROI Percent`
FROM `ML Cluster Analysis`
WHERE `Volume Velocity Factor` > 10
ORDER BY `Volume Velocity Factor` DESC;
-- Result: POPCAT 300x, BRETT 56x = Meme speculation velocity vs TRON 2.7x = Real growth

-- 3. Historical Pump Anatomy: Peak ROI vs Drawdown Risk
SELECT Ticker, Name, Era, `Peak Pump ROI Pct`, `Drawdown From ATH Pct`,
       `Peak Pump ROI Pct` * (1-`Drawdown From ATH Pct`) as net_roi_after_crash
FROM `Historical Pump Data`
ORDER BY `Peak Pump ROI Pct` DESC;
-- Result: SHIB 884,499% ROI but 79% drawdown. LUNA 1190% → 99.9% drawdown = Systemic fragility

-- 4. Cross-Market Validation: Crypto vs Stocks Jan 2024 → Now
SELECT `Asset Class`,
       AVG((`Current Close` - `Jan 2024 Open`)/`Jan 2024 Open` *100) as avg_growth_pct,
       AVG(`Current Volume`/`Jan 2024 Volume`) as avg_volume_velocity
FROM `Core Market Data`
GROUP BY `Asset Class`;
-- Result: Crypto avg 1.8x volume velocity vs Stocks 1.2x = Crypto leading liquidity

-- 5. Trader Since 2020 Insight: Survivors vs Dead Coins
SELECT Era, 
       COUNT(*) as projects,
       AVG(`Peak Pump ROI Pct`) as avg_peak,
       AVG(`Drawdown From ATH Pct`) as avg_drawdown,
       MIN(`Current Price`/`A.T.H. Price`) as worst_survivor
FROM `Historical Pump Data`
GROUP BY Era;
-- Result: 2021 L1 Cycle avg 500% ROI, 2021 Algorithmic (LUNA) = 99.9% drawdown lesson
