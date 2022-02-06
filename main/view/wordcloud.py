from flask import Blueprint, render_template, request
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import os


bp = Blueprint("wordcloud", __name__, url_prefix="/", static_folder="static")

@bp.route('/wordcloud_input' )
def wordcloud_input():
    return render_template('wordcloud_input.html')

@bp.route('/wordcloud_output', methods = ['POST'])
def wordcloud_output():
    os.remove("main/static/wordcloud.jpg") if os.path.exists("main/static/wordcloud.jpg") else None
    #request._get_current_object()
    result = request.form
    target_text = result["txt"]
    doc = re.sub(r'[^ ㄱ-ㅣ가-힣A-Za-z]', '', target_text)
    okt = Okt()
    words = okt.nouns(doc)
    words = [word for word in words if len(word)>1]
    common_words = Counter(words).most_common(100)
    wordcloud = WordCloud(
        stopwords = ["기자", "단독", "특종", "앵커", "편집", "영상", "멘트", "전문", "사진", "속보"],\
        font_path='main/static/MaruBuri-Regular.ttf',\
        background_color='white',\
        colormap="Accent_r",\
        width=1500, height=1000).generate_from_frequencies(dict(common_words))
    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig("main/static/wordcloud.jpg")
    return render_template('wordcloud_output.html', target_text=target_text, common_words=common_words)

