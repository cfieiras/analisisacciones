import requests

def get_news_alphavantage(ticker_symbol, api_key):
    """
    Obtiene las últimas noticias de Alpha Vantage para el símbolo dado y devuelve una lista de titulares y resúmenes.
    """
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker_symbol}&apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        news_items = data.get('feed', [])
        noticias = []
        for item in news_items[:5]:  # Solo las 5 más recientes
            titulo = item.get('title', '')
            resumen = item.get('summary', '')
            url_noticia = item.get('url', '')
            noticias.append({
                'title': titulo,
                'summary': resumen,
                'url': url_noticia
            })
        return noticias
    except Exception as e:
        print(f"Error al obtener noticias de Alpha Vantage: {e}")
        return []

if __name__ == "__main__":
    api_key = "ZIL7ER8H9VDB6SE7"
    ticker = "AAPL"
    noticias = get_news_alphavantage(ticker, api_key)
    for noticia in noticias:
        print(f"Título: {noticia['title']}")
        print(f"Resumen: {noticia['summary']}")
        print(f"URL: {noticia['url']}")
        print()
