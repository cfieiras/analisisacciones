import sys
from noticias import get_news_alphavantage
from analisis_tecnico import get_technical_analysis
from analisis_fundamental import get_fundamental_analysis

def run_analysis():
    print("\n--- Analizador de Acciones (Análisis Técnico y Fundamental) ---")
    ticker_symbol = input("Introduce el símbolo de la acción (ej. AAPL): ").upper()
    api_key = "ZIL7ER8H9VDB6SE7"
    
    # Opcional: Pedir cantidad de acciones, aunque no se usa en el análisis actual
    # try:
    #     cantidad = int(input("Introduce la cantidad de acciones que tienes (opcional, 0 si no tienes): "))
    # except ValueError:
    #     cantidad = 0

    print(f"\nAnalizando {ticker_symbol}...")

    # --- Análisis Técnico ---
    tech_data = get_technical_analysis(ticker_symbol)
    if tech_data is None or tech_data.empty:
        print("No se pudo realizar el análisis técnico. Saliendo.")
        return

    latest_tech_data = tech_data.iloc[-1]
    current_price = float(latest_tech_data['Close'])
    rsi = float(latest_tech_data['RSI'])
    sma_50 = float(latest_tech_data['SMA_50'])
    sma_200 = float(latest_tech_data['SMA_200'])

    print("\n--- Resultados del Análisis Técnico ---")
    print(f"Precio Actual: {current_price:.2f}")
    print(f"RSI (14 días): {rsi:.2f}")
    print(f"SMA (50 días): {sma_50:.2f}")
    print(f"SMA (200 días): {sma_200:.2f}")

    # --- Análisis Fundamental ---
    fund_data = get_fundamental_analysis(ticker_symbol)
    if fund_data is None:
        print("No se pudo realizar el análisis fundamental. Saliendo.")
        return

    print("\n--- Resultados del Análisis Fundamental ---")
    print(f"Sector: {fund_data.get('sector', 'N/A')}")
    print(f"Industria: {fund_data.get('industry', 'N/A')}")
    print(f"P/E Forward: {fund_data.get('forwardPE', 'N/A'):.2f}" if isinstance(fund_data.get('forwardPE'), (int, float)) else f"P/E Forward: N/A")
    print(f"Capitalización de Mercado: {fund_data.get('marketCap', 'N/A'):,.0f}" if isinstance(fund_data.get('marketCap'), (int, float)) else f"Capitalización de Mercado: N/A")
    print(f"Crecimiento de Ganancias (último año): {fund_data.get('earningsGrowth', 'N/A')*100:.2f}%" if isinstance(fund_data.get('earningsGrowth'), (int, float)) else f"Crecimiento de Ganancias (último año): N/A")
    print(f"Crecimiento de Ingresos (último año): {fund_data.get('revenueGrowth', 'N/A')*100:.2f}%" if isinstance(fund_data.get('revenueGrowth'), (int, float)) else f"Crecimiento de Ingresos (último año): N/A")
    print(f"Recomendación de Analistas: {fund_data.get('recommendationKey', 'N/A').replace('strong_', '').replace('buy', 'Compra').replace('sell', 'Venta').replace('hold', 'Mantener')}")


    # --- Lógica de Recomendación ---
    recommendation = "Mantener"
    reasons = []

    # Criterios Técnicos
    if current_price > sma_50 and current_price > sma_200:
        recommendation = "Comprar"
        reasons.append("El precio actual está por encima de las SMAs de 50 y 200 días (tendencia alcista).")
    elif current_price < sma_50 and current_price < sma_200:
        recommendation = "Vender"
        reasons.append("El precio actual está por debajo de las SMAs de 50 y 200 días (tendencia bajista).")

    if rsi < 30:
        if recommendation == "Comprar":
            reasons.append("El RSI indica que la acción podría estar sobrevendida, lo que refuerza la señal de compra.")
        elif recommendation == "Mantener":
            recommendation = "Comprar"
            reasons.append("El RSI indica que la acción podría estar sobrevendida.")
    elif rsi > 70:
        if recommendation == "Vender":
            reasons.append("El RSI indica que la acción podría estar sobrecomprada, lo que refuerza la señal de venta.")
        elif recommendation == "Mantener":
            recommendation = "Vender"
            reasons.append("El RSI indica que la acción podría estar sobrecomprada.")

    # Criterios Fundamentales (ejemplos simples)
    if isinstance(fund_data.get('earningsGrowth'), (int, float)) and fund_data['earningsGrowth'] > 0.10: # Más del 10% de crecimiento
        if recommendation == "Vender":
            recommendation = "Mantener"
            reasons.append("A pesar de las señales técnicas, el crecimiento de ganancias es positivo.")
        elif recommendation == "Mantener":
            reasons.append("El crecimiento de ganancias es sólido.")
        elif recommendation == "Comprar":
            reasons.append("El crecimiento de ganancias es sólido, lo que apoya la compra.")

    if isinstance(fund_data.get('forwardPE'), (int, float)) and fund_data['forwardPE'] > 0 and fund_data['forwardPE'] < 25: # PE razonable
        if recommendation == "Comprar":
            reasons.append("El P/E forward es razonable.")
        elif recommendation == "Mantener":
            reasons.append("El P/E forward es razonable.")

    print("\n--- Recomendación Final ---")
    print(f"Recomendación: {recommendation}")
    print("\nExplicación detallada:")
    if recommendation == "Comprar":
        print("Se recomienda comprar porque:")
    elif recommendation == "Vender":
        print("Se recomienda vender porque:")
    else:
        print("Se recomienda mantener porque:")
    if reasons:
        for reason in reasons:
            print(f"- {reason}")
    else:
        print("No hay razones específicas adicionales para la recomendación actual.")

    print("\n--- Aviso Importante ---")
    print("Esta recomendación es generada por un algoritmo simple y no debe considerarse como asesoramiento financiero profesional. Realice siempre su propia investigación y consulte a un experto antes de tomar decisiones de inversión.")

if __name__ == "__main__":
    import os
    os.system("streamlit run app.py")
