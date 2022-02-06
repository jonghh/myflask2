from flask import Blueprint, render_template, request
import re
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

bp = Blueprint("navernews_collect", __name__, url_prefix="/", static_folder="static")

@bp.route('/navernews_input')
def navernews_input():
    return render_template('navernews_input.html')

@bp.route('/navernews_output' , methods = ['POST'])
def navernews_output():
    result = request.form
    word = result["search_word"]
    date_from = result["date_from"]
    date_to = result["date_to"]
    target_url = "https://search.naver.com/search.naver?where=news&query={x}&sort=0&photo=0&field=1&nso=so:r,p:from{y}to{z},a:t&start=1".format(x=word, y=date_from, z=date_to)

    urls, titles, sources, dates, texts = [],[],[],[],[]
    for i in [1,11,21,31,41,51,61,71,81,91]:
        time.sleep(1)
        try:
            r=requests.get(target_url[:-1] + "{}".format(i))
            soup=BeautifulSoup(r.text, "html.parser")

            a=soup.select("a.news_tit")
            title=[ai["title"] for ai in a]       # ["title"]: html tag문 바로 뒤 []안에 속성을 넣으면 속성값 출력.
            url=[ai["href"] for ai in a]              # ["href"]: html tag문에서 url 추출

            b=soup.select("a.info.press")
            source=[bi.text.replace("선정", "").replace("언론사", "").strip() for bi in b]           # .text: html tag문에서 text 추출.

            date=[]
            c=soup.select("span.info")
            for ci in c:
                if re.findall("\d+\w+\s+전|\d+.\d+.\d+.", ci.text):      # "1면 하단"과 같은 정보가 함께 포함됨. 이를 제외하기 위해 if문 사용
                    date.append(ci.text)

            d=soup.select("a.api_txt_lines.dsc_txt_wrap")
            text=[]
            for di in d:
                try:                                            # text 가운데에는 결측치(내용이 없는 경우)가 있어 try-except문으로 보완.
                    text.append(di.text)
                except:
                    text.append("")

            urls.append(url)
            titles.append(title)
            sources.append(source)
            dates.append(date)
            texts.append(text)
        except:
            pass

    urls_all=sum(urls, [])
    titles_all=sum(titles, [])
    sources_all=sum(sources, [])
    dates_all=sum(dates, [])
    texts_all=sum(texts, [])
    news_all = pd.DataFrame({"언론사": sources_all, "날짜": dates_all, "제목": titles_all, "텍스트": texts_all, "URL": urls_all})
    news_all.index = news_all.index + 1
    news_all.to_csv("main/static/navernews_result.csv", encoding="utf-8-sig")
    return render_template('navernews_output.html', word=word, date_from=date_from, date_to=date_to, news_all=news_all)
