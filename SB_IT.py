def get_sbbit_news():

    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    from datetime import datetime, timedelta

    base_url = "https://www.sbbit.jp/"

    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # ニュース記事タイトルとリンクを抽出
    articles = soup.select("article.crd_itm") #CSSセレクタで記事を取得

    data = []

    filtered_data = []

    for article in articles:
        title_tag = article.find("h3", class_ = "crd_ttl-txt")
        
        if not title_tag:
            continue
        
        a_tag = title_tag.find_parent("a")
        time_tag = article.find("time", class_ = "crd_ttl-pubdate")

        title = title_tag.text.strip()
        link = base_url + a_tag["href"]
        date = time_tag.text.strip()

        print(f"{date} | {title} | {link}")