# 日経のニュースを取得する関数

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


# ソフバンのニュースを取得する関数

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

# 日経側で本文を取得するAPI

def get_article_body(url):
    import requests
    from bs4 import BeautifulSoup

    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    # 本文領域
    content = soup.find("div", class_="articleBody")

    if not content:
        return ""
    
    paragraphs = content.find_all("p")
    texts = "\n".join(p.text.strip() for p in paragraphs)

    return texts

# オープンAIに要約を書かせる部分
from openai import OpenAI

client = OpenAI()

def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "あなたはニュース記事を簡潔に要約するアシスタントです。"},
            {"role": "user", "content": f"次の記事を3行で要約してください:\n{text}"}
        ],
    )

    return response.choices[0].message.content


# メインの関数

def main():

    all_data = []
    keywords = ["AI", "人工知能", "セキュリティ", "安全"]
    keyword_filtered = []

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

    for item in filtered_data:
        if any(k in item["title"] for k in keywords):
            keyword_filtered.append(item)

    import pandas as pd

    df = pd.DataFrame(filtered_data)
    df2 = pd.DataFrame(keyword_filtered)

    # for item in keyword_filtered:
    #     body = get_article_body(item["url"])
    #     print(body[:200])  # 最初だけ確認

    # 一件要約を書いてもらう

    import os
    from openai import OpenAI
    os.environ["OPENAI_API_KEY"] = "KEY"

    client = OpenAI()

    for item in keyword_filtered[:1]:  # まず1件だけ
        body = get_article_body(item["url"])
        summary = summarize_text(body)

        print("タイトル:", item["title"])
        print("要約:", summary)

    df.to_csv("data/all_news.csv", index=False, encoding="utf-8-sig")
    df2.to_csv("data/keyword_filtered.csv", index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    main()

