
# QUANTITATIVE BACKTESTING ENGINE (V1 - GOLDEN CROSS)

##  1. PROJECT OBJECTIVE

This script is a foundational quantitative backtesting engine built to test simple trading hypotheses.

The main goal is to answer: **Did a given strategy outperform a passive "Buy and Hold" investment over the last 5 years?**

---
##  2. THE STRATEGY & LOGIC

### A. The Golden Cross Strategy

The system trades based on the classic Moving Average Crossover:
* Indicators: 50-Day Moving Average (MA50) and 200-Day Moving Average (MA200).
* BUY Signal (Golden Cross): MA50 crosses ABOVE MA200. (Signal = 1)
* SELL Signal (Death Cross): MA50 crosses BELOW MA200. (Signal = 0)

### B. Trade Identification (The "Position" Column)

The script identifies the exact day a trade should be placed by checking the change in the signal:
* `Position` = `Signal.diff()`
* `Position = 1.0` -> **Action: BUY** (The day the signal flipped from 0 to 1).
* `Position = -1.0` -> **Action: SELL** (The day the signal flipped from 1 to 0).

### C. Realism

* The backtest is executed with transaction costs (0.1%) applied to every trade day (using `df.loc[]`).
* The logic uses `.shift(1)` to prevent "look-ahead bias".

---
## 3. SAMPLE RESULT (AAPL: 2020-2025)

| Metric | Buy & Hold (Benchmark) | Golden Cross Strategy |
| :--- | :--- | :--- |
| **Total Return Factor** | **3.38x** | **2.87x** |
| **Total Profit** | 238% | 187% |
| **Conclusion** | **Underperformed.** The strategy failed to beat the simple act of holding the asset over this period. | |

---
## 4. NEXT STEPS (Future Features)

1.  Calculate Max Drawdown and Sharpe Ratio (Risk Metrics).
2.  Implement Strategy Optimization (Testing multiple MA windows).
3.  Refactor into a Python Class for easy strategy swapping.
4.  Build a simple web interface (using Streamlit or FastAPI) to visualize the results.