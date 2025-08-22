import yfinance as yf
import pandas as pd
import ta

def get_technical_analysis(ticker_symbol):
    # ...existing code...
    """
    Obtiene datos históricos y calcula indicadores técnicos para un símbolo de acción dado.

    Args:
        ticker_symbol (str): El símbolo de la acción (ej. 'AAPL').

    Returns:
        pandas.DataFrame: DataFrame con los datos históricos y los indicadores técnicos.
                          Retorna None si no se pueden obtener los datos.
    """
    try:
        # Descargar datos históricos (último año)
        data = yf.download(ticker_symbol, period="1y")

        if data.empty:
            print(f"No se encontraron datos para el símbolo: {ticker_symbol}")
            return None

        # Asegurarse de que 'Close' sea una Serie 1D
        close_series = data['Close'].squeeze()

        # Calcular RSI (Relative Strength Index)
        data['RSI'] = ta.momentum.RSIIndicator(close_series, window=14).rsi()

        # Calcular Media Móvil Simple (SMA) de 50 días
        data['SMA_50'] = ta.trend.SMAIndicator(close_series, window=50).sma_indicator()

        # Calcular Media Móvil Simple (SMA) de 200 días
        data['SMA_200'] = ta.trend.SMAIndicator(close_series, window=200).sma_indicator()

        # Calcular MACD
        macd_indicator = ta.trend.MACD(close_series)
        data['MACD'] = macd_indicator.macd()
        data['MACD_signal'] = macd_indicator.macd_signal()
        data['MACD_diff'] = macd_indicator.macd_diff()

        # Calcular Bandas de Bollinger
        bb_indicator = ta.volatility.BollingerBands(close_series, window=20, window_dev=2)
        data['BB_high'] = bb_indicator.bollinger_hband()
        data['BB_low'] = bb_indicator.bollinger_lband()
        data['BB_mavg'] = bb_indicator.bollinger_mavg()

        return data
    except Exception as e:
        print(f"Error al obtener o calcular análisis técnico para {ticker_symbol}: {e}")
        return None

if __name__ == '__main__':
    # Ejemplo de uso
    ticker = "AAPL"
    tech_data = get_technical_analysis(ticker)

    if tech_data is not None:
        print(f"Análisis Técnico para {ticker}:")
        print(tech_data[['Close', 'RSI', 'SMA_50', 'SMA_200']].tail())
