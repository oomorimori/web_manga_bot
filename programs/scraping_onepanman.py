from secret.webhook_url import *
from send_slack import send_to_slack
from control_csv import input_csv, output_csv
import requests,bs4,csv

title = 'ワンパンマン'
url = 'http://galaxyheavyblow.web.fc2.com/'
csv_path = '/Users/omori/workspace/web_manga_bot/log/log_onepan.csv'

def scraping_onepanman(url=url):
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content, "html.parser")
    # 話を入れておくリスト
    chapter_list = []
    for a_tag in soup.find_all("a"):
        url = a_tag.get("href")
        # 話のリスト
        if "fc2-imageviewer" in url:
            chapter = a_tag.getText()
            chapter_list.append(chapter)

    return chapter_list

def log_creation(chapters):
    log_array = []
    log_array.append(chapters)
    output_csv(csv_path, log_array)

def main():
    # 最新のタイトルのリストを取得
    latest = scraping_onepanman()
    # ログからのタイトルのリストを取得
    past = input_csv(csv_path)

    # ログがなければ初期化
    if not past:
        print('csvファイルを初期化します')
        log_creation(latest)
        past = latest

    # 差分のリストを取得、複数の更新があった場合複数のメッセージを作成する
    if past[0] != latest:
        diff_list = list(set(latest) - set(past[0]))
        for n in diff_list:
            send_to_slack(title, url, n)
    else:
        print("The Article has not updated ...")

    # この配列の中身を最終的にログとしてCSVファイルに書き込む
    log_array = []
    log_array.append(latest)
    # ログをCSVに書き込む
    output_csv(csv_path, log_array)

if __name__ == '__main__':
    main()
