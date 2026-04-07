def get_nikkei_news():

    import requests
    from bs4 import BeautifulSoup

    url = "https://active.nikkeibp.co.jp/it/index_new.html"
    base_url = "https://active.nikkeibp.co.jp/"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # ニュース記事タイトルとリンクを抽出
    articles = soup.select("li.p-articleList_item") #CSSセレクタで記事を取得

    data = []

    for article in articles:
        a_tag = article.find("h3").find("a")
        if a_tag is None:
            continue

        time_tag = article.find("time")

        title = a_tag.text.strip()
        link = base_url + a_tag["href"]
        date = time_tag.text.strip()

        if not date:
            continue

        data.append({
            "title": title,
            "url": link,
            "date": date
        })

    return data


def get_sbbit_news():
    import requests
    from bs4 import BeautifulSoup

    base_url = "https://www.sbbit.jp/"

    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # ニュース記事タイトルとリンクを抽出
    articles = soup.select("article.crd_itm") #CSSセレクタで記事を取得

    data = []

    for article in articles:
        title_tag = article.find("h3", class_ = "crd_ttl-txt")
        
        if not title_tag:
            continue
        
        a_tag = title_tag.find_parent("a")
        time_tag = article.find("time", class_ = "crd_ttl-pubdate")

        title = title_tag.text.strip()
        link = base_url + a_tag["href"]
        date = time_tag.text.strip()

        if not date:
            continue

        data.append({
            "title": title,
            "url": link,
            "date": date
        })

    return data

    
def main():

    all_data = []

    all_data += get_nikkei_news()
    all_data += get_sbbit_news()

    # 24時間フィルタ
    from datetime import datetime, timedelta

    now = datetime.now()
    limit = now - timedelta(days=1)

    filtered_data = []

    for item in all_data:
        try:
            date_obj = datetime.strptime(item["date"], "%Y.%m.%d")
        except:
            date_obj = datetime.strptime(item["date"], "%Y/%m/%d")

        if date_obj >= limit:
            filtered_data.append(item)

    import pandas as pd

    df = pd.DataFrame(filtered_data)
    df.to_csv("data/all_news.csv", index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    main()