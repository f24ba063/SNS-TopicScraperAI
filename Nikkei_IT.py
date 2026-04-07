def get_nikkei_news():

    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    from datetime import datetime, timedelta

    url = "https://active.nikkeibp.co.jp/it/index_new.html"
    base_url = "https://active.nikkeibp.co.jp/"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # ニュース記事タイトルとリンクを抽出
    articles = soup.select("li.p-articleList_item") #CSSセレクタで記事を取得

    data = []

    filtered_data = []

    for article in articles:
        a_tag = article.find("h3").find("a")
        if a_tag is None:
            continue

        time_tag = article.find("time")

        title = a_tag.text.strip()
        link = base_url + a_tag["href"]
        date = time_tag.text.strip()

        data.append({
            "title": title,
            "url": link,
            "date": date
        })

    now = datetime.now()
    limit = now - timedelta(days=1)

    for item in data:
        date_obj = datetime.strptime(item["date"],"%Y.%m.%d")

        if date_obj >= limit:
            filtered_data.append(item)

    df = pd.DataFrame(filtered_data)
    df.to_csv("filtered_news.csv", index=False, encoding="utf-8-sig")