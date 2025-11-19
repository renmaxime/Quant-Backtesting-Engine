import pandas as pd
import numpy as np
import yfinance as yf


#Dowload historical data from yfinance

def load_data(ticker, start_date, end_date):
    print(f"Loading data for {ticker} from {start_date} to {end_date}")
    df = yf.download(ticker, start=start_date, end=end_date,auto_adjust=False)
    return df



#Generate moving average crossover signals and positions

def add_strategy_signals(df):
    print("Calculating moving averages and generating signals")
    df["MA50"]=df["Close"].rolling(window=50).mean()
    df["MA200"]=df["Close"].rolling(window=200).mean()
    df_clean=df.dropna().copy()
    df_clean["signal"]= np.where(df_clean["MA50"]>df_clean["MA200"],1,0)
    df_clean["position"]=df_clean["signal"].diff()
    return df_clean

#calculate strategy returns and compare to buy-and-hold
def run_backtest(df_clean,commission):
    print(f"running backtest(Commission={commission*100}%)")
    #calculate daily returns
    df_clean["daily_return"]=df_clean["Close"].pct_change()

    #calculate strategy returns
    df_clean["strategy_return"]=df_clean["daily_return"]*df_clean["signal"].shift(1)

    #apply commission on trade days
    trade_days=df_clean["position"].abs()==1.0
    df_clean.loc[trade_days,"strategy_return"]-=commission

    #calculate cumulative returns
    df_clean["buy_hold_total"]=(df_clean["daily_return"]+1).cumprod()
    df_clean["strategy_total"]=(df_clean["strategy_return"]+1).cumprod()
    return df_clean



#Print final performance results
def print_results(df_clean):
    print("\n--- Trade Days ---")
    #show only the days where trades were made
    print(df_clean[df_clean['position']!=0])

    #get final returns
    final_buy_hold= df_clean["buy_hold_total"].iloc[-1]
    final_strategy= df_clean["strategy_total"].iloc[-1]


    print("final performance analysis")
    print(f"Total Buy and Hold Return: {final_buy_hold:.2f}x")
    print(f"Total Strategy Return: {final_strategy:.2f}x")
    print("\n")

    if final_strategy > final_buy_hold:
        print("Congratulations, your strategy outperformed Buy and Hold!")
    else:
        print("Unfortunately, your strategy underperformed Buy and Hold.")










if __name__ == "__main__":
    TICKER = "AAPL"
    START_DATE = "2019-01-01"
    END_DATE = "2024-01-01"
    COMMISSION_FEE = 0.001  
    data=load_data(TICKER, START_DATE, END_DATE)
    data_with_signals=add_strategy_signals(data)
    final_data=run_backtest(data_with_signals, COMMISSION_FEE)
    print_results(final_data)