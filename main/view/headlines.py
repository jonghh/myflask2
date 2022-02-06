## 이 파일은 작동 안됨.. scheduler는 run파일에 걸어야 하는 듯.

from flask import Blueprint, render_template
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import time
import schedule

bp = Blueprint("headlines", __name__, url_prefix="/", static_folder="static")

@bp.route("/headlines_output")
def ask1():
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
        txt = headlines[0:1] + [a + ":" + b for a, b in headlines[1:]]
        with open("main/static/headlines_0.txt", "a") as f:
            f.write("\n" + "::".join(txt))

        t_urls = {"kbs": "https://news.kbs.co.kr/common/main.html",
                "mbc": "https://imnews.imbc.com/pc_main.html",
                "sbs": "https://news.sbs.co.kr/news/newsMain.do",
                "tvchosun": "http://news.tvchosun.com/",
                "jtbc": "https://news.jtbc.joins.com/",
                "mbn": "https://www.mbn.co.kr/news/",
                "channela": "http://www.ichannela.com/news/main/news_main.do"}
        t_tags = {"kbs": "#content > div.m-section.main-headline.type1 > div > ul > li > a",
                "mbc": "#content > section.news_top > div.news_header > div.top_left > a",  # selenium 이용
                "sbs": "div.head_area > div > div.w_news_list.type_head > ul > li > a ",
                "tvchosun": "#wrap > div.key_news_area > div.key_center > a",
                "jtbc": "#divArticle0 > dl > dt > a",
                "mbn": "#container_in > div.con_left > div.top_news > div.top_mainnews > h1 > a",
                "channela": "#contArea_1 > div.newsMain_grid_top > div > p > a"}
        t_tm = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # UTC 기준. KST보다 9시간 이전.
        t_headlines = [t_tm]
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        wd = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        #wd = webdriver.Chrome(executable_path=r"C:\Users\82104\Desktop\pycharm\chrome.exe", chrome_options=chrome_options)
        # 방송 뉴스 실시간 수집
        for t_media in ['kbs', 'mbc', 'sbs', 'tvchosun', 'jtbc', 'mbn', 'channela']:
            try:
                target_url = t_urls[t_media]
                if t_media in ['kbs', 'sbs', 'tvchosun', 'jtbc', 'mbn']:
                    r = requests.get(target_url, headers={'User-Agent': 'Mozilla/5.0'})  # 해당 url에 접속해 html 내용을 가져옴
                    r.raise_for_status()
                    r.encoding = "utf-8"
                    soup = BeautifulSoup(r.text, "html.parser")
                    mediaa = soup.select(t_tags[t_media])
                    t = mediaa[0].text.replace("동영상", "").replace("오디오", "").replace("기사", "").strip()
                    u = mediaa[0]["href"]
                elif t_media in ['mbc', 'channela']:
                    wd.get(t_urls[t_media])
                    time.sleep(0.5)
                    mediaa = wd.find_element_by_css_selector(t_tags[t_media])
                    t = mediaa.text
                    u = mediaa.get_attribute('href')
                else:
                    pass
                time.sleep(0.3)
                t_headlines.append([t, u])
            except:
                t_headlines.append([])
        wd.quit()
        t_txt = t_headlines[0:1] + [":".join(h).replace("\n", " ") for h in t_headlines[1:]]
        with open("main/static/headlines_1.txt", "a") as f:
            f.write("\n" + "::".join(t_txt))
    # 매시 00분에 작업 실행
    schedule.every().hour.at(":00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

    with open("main/static/headlines_0.txt", "r") as f:
        results=f.readlines()[-1].replace("::","\n")
    with open("main/static/headlines_1.txt", "r") as f:
    	results1=f.readlines()[-1].replace("::","\n")
    return render_template('headlines_output.html', results=results,  results1=results1)

