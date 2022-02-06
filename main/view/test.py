import requests
from bs4 import BeautifulSoup
import datetime
import time
import schedule

def job():
    urls = {"ch": "https://www.chosun.com/",
            "hk": "https://www.hani.co.kr/",
            "yh": "https://www.yna.co.kr/",
            "ja": "https://joongang.joins.com/",
            "da": "https://www.donga.com/",
            "kh": "http://www.khan.co.kr/"}
    tags = {
        "ch": "a.text__link.story-card__headline.|.box--margin-none.text--black.font--primary-bold.h2.text__link--color",
        "hk": "#main-top > div.main-top > div.main-top-article > h4 > a",
        "yh": "#container > div > div.content03.main-content01 > section.top-main-news01 > div > article > h2 > a",
        "ja": "div.card_body.col_md6 > h2 > a",
        "da": "h2.title > a",
        "kh": "div > div.top-cont-l > div > a"}
    tm = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # UTC 기준. KST보다 9시간 이전.
    headlines = [tm]
    for media in ["yh", "ch", "ja", "da", "hk", "kh"]:
        try:
            target_url = urls[media]
            r = requests.get(target_url, headers={'User-Agent': 'Mozilla/5.0'})  # 해당 url에 접속해 html 내용을 가져옴
            r.raise_for_status()
            r.encoding = "utf-8"
            soup = BeautifulSoup(r.text, "html.parser")
            mediaa = soup.select(tags[media])
            if media == "ch":
                t = mediaa[-1].text.replace("\r\n", "").replace("동영상/오디오", "").strip()
                u = mediaa[-1]["href"]
                headlines.append([t, u])
            else:
                t = mediaa[0].text.replace("\r\n", "").replace("동영상/오디오", "").strip()
                u = mediaa[0]["href"]
                headlines.append([t, u])
            time.sleep(0.3)
        except:
            headlines.append([])
        txt = headlines[0:1]+[a+":"+b for a, b in headlines[1:]]
        with open("main/static/headlines_0.txt", "a") as f:
            f.write("\n" + "::".join(txt))

# 매시 00분에 작업 실행
schedule.every().hour.at(":45").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
