import yfinance as yf

def get_fundamental_analysis(ticker_symbol):
    """
    Obtiene datos fundamentales para un símbolo de acción dado.

    Args:
        ticker_symbol (str): El símbolo de la acción (ej. 'AAPL').

    Returns:
        dict: Un diccionario con los datos fundamentales clave.
              Retorna None si no se pueden obtener los datos.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        if not info:
            print(f"No se encontraron datos fundamentales para el símbolo: {ticker_symbol}")
            return None

        fundamental_data = {
            "currentPrice": info.get("currentPrice"),
            "forwardPE": info.get("forwardPE"),
            "trailingPE": info.get("trailingPE"),
            "marketCap": info.get("marketCap"),
            "dividendYield": info.get("dividendYield"),
            "dividendRate": info.get("dividendRate"),
            "trailingAnnualDividendRate": info.get("trailingAnnualDividendRate"),
            "trailingAnnualDividendYield": info.get("trailingAnnualDividendYield"),
            "payoutRatio": info.get("payoutRatio"),
            "ebitda": info.get("ebitda"),
            "profitMargins": info.get("profitMargins"),
            "grossMargins": info.get("grossMargins"),
            "operatingMargins": info.get("operatingMargins"),
            "returnOnAssets": info.get("returnOnAssets"),
            "returnOnEquity": info.get("returnOnEquity"),
            "debtToEquity": info.get("debtToEquity"),
            "currentRatio": info.get("currentRatio"),
            "quickRatio": info.get("quickRatio"),
            "beta": info.get("beta"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "longBusinessSummary": info.get("longBusinessSummary"),
            "recommendationKey": info.get("recommendationKey"),
            "targetMeanPrice": info.get("targetMeanPrice"),
            "earningsGrowth": info.get("earningsGrowth"),
            "revenueGrowth": info.get("revenueGrowth"),
        }
        return fundamental_data

    except Exception as e:
        print(f"Error al obtener análisis fundamental para {ticker_symbol}: {e}")
        return None

if __name__ == '__main__':
    # Ejemplo de uso
    ticker = "AAPL"
    fund_data = get_fundamental_analysis(ticker)

    if fund_data:
        print(f"Análisis Fundamental para {ticker}:")
        for key, value in fund_data.items():
            print(f"  {key}: {value}")
