import streamlit as st
from analisis_tecnico import get_technical_analysis
from analisis_fundamental import get_fundamental_analysis

st.set_page_config(page_title="Análisis de Acciones", layout="wide")
st.title("Analizador de Acciones: Técnico y Fundamental")

st.sidebar.header("Configuración")

# Cuadro para Hugging Face Token
st.sidebar.markdown("---")
hf_token = st.sidebar.text_input("Token de Hugging Face", type="password")

# Cuadro de preguntas con Hugging Face
user_question_hf = st.sidebar.text_area("Pregunta para IA (Hugging Face)", value="¿YPF.BA bajará de los 42000 próximamente?")
if st.sidebar.button("Preguntar a Hugging Face"):
    import requests
    import re
    st.write("# Respuesta de IA (Hugging Face)")
    # Extraer símbolo de la pregunta
    match = re.search(r"([A-Z\.]+)", user_question_hf)
    symbol = match.group(1) if match else None
    if symbol:
        tech_data = get_technical_analysis(symbol)
        fund_data = get_fundamental_analysis(symbol)
        if tech_data is not None and not tech_data.empty and fund_data is not None:
            latest = tech_data.iloc[-1]
            # Resumen técnico y fundamental
            resumen = f"Precio actual: {float(latest['Close']):.2f}\nRSI: {float(latest['RSI']):.2f}\nSMA_50: {float(latest['SMA_50']):.2f}\nSMA_200: {float(latest['SMA_200']):.2f}\nMACD: {float(latest['MACD']):.2f}\nSector: {fund_data.get('sector','N/A')}\nIndustria: {fund_data.get('industry','N/A')}\nP/E Forward: {fund_data.get('forwardPE','N/A')}\nCrecimiento de Ganancias: {fund_data.get('earningsGrowth','N/A')}\nCrecimiento de Ingresos: {fund_data.get('revenueGrowth','N/A')}"
            prompt = f"Datos de la acción {symbol}:\n{resumen}\n\nPregunta del usuario: {user_question_hf}\nResponde de forma clara y breve para inversores argentinos."
            if hf_token:
                # Hugging Face Inference API endpoint (Mistral-7B-Instruct)
                url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
                headers = {"Authorization": f"Bearer {hf_token}", "Content-Type": "application/json"}
                payload = {"inputs": prompt}
                try:
                    response = requests.post(url, headers=headers, json=payload, timeout=60)
                    if response.status_code == 200:
                        result = response.json()
                        # La respuesta puede estar en 'generated_text' o en la lista
                        if isinstance(result, list) and 'generated_text' in result[0]:
                            answer = result[0]['generated_text']
                        else:
                            answer = result
                        st.write(answer)
                    else:
                        st.error(f"Error de Hugging Face: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error al conectar con Hugging Face: {e}")
            else:
                st.warning("Por favor, ingresa tu token de Hugging Face.")
        else:
            st.warning(f"No se encontraron datos para el símbolo {symbol}.")
    else:
        st.warning("No se pudo interpretar el símbolo en la pregunta.")

# Cuadro de preguntas personalizadas
st.sidebar.markdown("---")
user_question = st.sidebar.text_input("Pregunta sobre una acción (ej: 'YPF.BA bajará de los 42.000 próximamente?')")
if st.sidebar.button("Preguntar"):
    import re
    st.write("# Respuesta a tu pregunta")
    # Extraer símbolo y precio objetivo de la pregunta
    match = re.search(r"([A-Z\.]+).*?(\d+[\.,]?\d*)", user_question)
    if match:
        symbol = match.group(1)
        price_str = match.group(2).replace(",", ".")
        try:
            price_target = float(price_str)
        except:
            price_target = None
        tech_data = get_technical_analysis(symbol)
        if tech_data is not None and not tech_data.empty:
            latest = tech_data.iloc[-1]
            current_price = float(latest['Close'])
            st.write(f"Precio actual de {symbol}: {current_price:.2f}")
            if price_target is not None:
                if current_price < price_target:
                    st.write(f"Actualmente está por debajo de {price_target}.")
                elif current_price > price_target:
                    st.write(f"Actualmente está por encima de {price_target}.")
                else:
                    st.write(f"Actualmente está en {price_target}.")
                st.write("No se puede predecir con certeza si bajará o subirá, pero puedes revisar la tendencia y los indicadores técnicos para tomar una decisión informada.")
            else:
                st.write("No se pudo extraer el precio objetivo de la pregunta.")
        else:
            st.write(f"No se encontraron datos para el símbolo {symbol}.")
    else:
        st.write("No se pudo interpretar la pregunta. Por favor, usa el formato 'TICKER bajará/subirá de X próximamente?'")

tickers_input = st.sidebar.text_area("Símbolos de las acciones (separados por coma)", value="AAPL, QQQ, SPY")

tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

if st.sidebar.button("Analizar"):
    if tickers:
        symbol = tickers[0]
        st.write(f"## Resultados para {symbol}")
        tech_data = get_technical_analysis(symbol)
        fund_data = get_fundamental_analysis(symbol)
    else:
        st.warning("No se ingresó ningún símbolo.")

    # --- Lógica de Recomendación ---
    if tech_data is not None and not tech_data.empty and fund_data is not None:
        latest = tech_data.iloc[-1]
        current_price = float(latest['Close'])
        sma_50 = float(latest['SMA_50'])
        sma_200 = float(latest['SMA_200'])
        rsi = float(latest['RSI'])
        recommendation = "Mantener"
        reasons = []
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
        if isinstance(fund_data.get('earningsGrowth'), (int, float)) and fund_data['earningsGrowth'] > 0.10:
            if recommendation == "Vender":
                recommendation = "Mantener"
                reasons.append("A pesar de las señales técnicas, el crecimiento de ganancias es positivo.")
            elif recommendation == "Mantener":
                reasons.append("El crecimiento de ganancias es sólido.")
            elif recommendation == "Comprar":
                reasons.append("El crecimiento de ganancias es sólido, lo que apoya la compra.")
        if isinstance(fund_data.get('forwardPE'), (int, float)) and fund_data['forwardPE'] > 0 and fund_data['forwardPE'] < 25:
            if recommendation == "Comprar":
                reasons.append("El P/E forward es razonable.")
            elif recommendation == "Mantener":
                reasons.append("El P/E forward es razonable.")
        st.subheader("Recomendación Final")
        st.write(f"**Recomendación:** {recommendation}")
        st.write("**Explicación detallada:**")
        if recommendation == "Comprar":
            st.write("Se recomienda comprar porque:")
        elif recommendation == "Vender":
            st.write("Se recomienda vender porque:")
        else:
            st.write("Se recomienda mantener porque:")
        if reasons:
            for reason in reasons:
                st.write(f"- {reason}")
        else:
            st.write("No hay razones específicas adicionales para la recomendación actual.")

    if tech_data is not None and not tech_data.empty:
        latest = tech_data.iloc[-1]
        st.subheader("Análisis Técnico")
        st.metric("Precio Actual", f"{float(latest['Close']):.2f}")
        st.metric("RSI (14 días)", f"{float(latest['RSI']):.2f}")
        st.metric("SMA 50", f"{float(latest['SMA_50']):.2f}")
        st.metric("SMA 200", f"{float(latest['SMA_200']):.2f}")
        st.metric("MACD", f"{float(latest['MACD']):.2f}")
        st.metric("Bollinger High", f"{float(latest['BB_high']):.2f}")
        st.metric("Bollinger Low", f"{float(latest['BB_low']):.2f}")
        import pandas as pd
        # Aplanar columnas MultiIndex si existen
        if isinstance(tech_data.columns, pd.MultiIndex):
            tech_data.columns = ['_'.join([str(i) for i in col if i]) for col in tech_data.columns]

        cols = [col for col in tech_data.columns if any(x in col for x in ['Close','SMA_50','SMA_200','BB_high','BB_low'])]
        df_plot = tech_data.reset_index()[cols]
        st.line_chart(df_plot)
    else:
        st.warning("No se pudo obtener análisis técnico.")

    if fund_data is not None:
        st.subheader("Análisis Fundamental")
        st.write(f"**Sector:** {fund_data.get('sector','N/A')}")
        st.write(f"**Industria:** {fund_data.get('industry','N/A')}")
        st.write(f"**P/E Forward:** {fund_data.get('forwardPE','N/A')}")
        st.write(f"**Market Cap:** {fund_data.get('marketCap','N/A'):,}")
        st.write(f"**Crecimiento de Ganancias:** {fund_data.get('earningsGrowth','N/A')}")
        st.write(f"**Crecimiento de Ingresos:** {fund_data.get('revenueGrowth','N/A')}")
        st.write(f"**EBITDA:** {fund_data.get('ebitda','N/A')}")
        st.write(f"**Dividend Yield:** {fund_data.get('dividendYield','N/A')}")
        st.write(f"**Recomendación:** {fund_data.get('recommendationKey','N/A')}")
    else:
        st.warning("No se pudo obtener análisis fundamental.")

# --- Análisis Simple para múltiples acciones ---
if st.sidebar.button("Análisis Simple"):
    st.write("# Análisis Simple de Múltiples Acciones")
    resumen = []
    for symbol in tickers:
        st.write(f"## {symbol}")
        tech_data = get_technical_analysis(symbol)
        fund_data = get_fundamental_analysis(symbol)
        if tech_data is not None and not tech_data.empty and fund_data is not None:
            latest = tech_data.iloc[-1]
            current_price = float(latest['Close'])
            sma_50 = float(latest['SMA_50'])
            sma_200 = float(latest['SMA_200'])
            rsi = float(latest['RSI'])
            recommendation = "Mantener"
            if current_price > sma_50 and current_price > sma_200:
                recommendation = "Comprar"
            elif current_price < sma_50 and current_price < sma_200:
                recommendation = "Vender"
            if rsi < 30 and recommendation != "Vender":
                recommendation = "Comprar"
            elif rsi > 70 and recommendation != "Comprar":
                recommendation = "Vender"
            st.write(f"**Recomendación:** {recommendation}")
            resumen.append((symbol, recommendation))
        else:
            st.write("No se pudo obtener análisis para este símbolo.")
    st.write("## Resumen de Recomendaciones")
    for symbol, rec in resumen:
        st.write(f"- {symbol}: {rec}")
