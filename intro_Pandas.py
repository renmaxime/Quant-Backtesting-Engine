import pandas as pd
import yfinance as yf

print("chargement des données d'Apple")

df=yf.download("AAPL", start="2024-01-01",end="2025-01-01")

print("Apercu du début (head)")
print(df.head())

print("Apercu de la fin (tail)")
print(df.tail())

print("Sélection de la colonne 'Close'")
prix_clotures=df["Close"]
print(prix_clotures.head())

print("Filtrage : les jours >200$")
jours_cher= df[prix_clotures>200]
print(jours_cher)

print("Création de la moyenne mobile sur 50 jours")
df["MM50"]=prix_clotures.rolling(window=50).mean()
print(df.tail())