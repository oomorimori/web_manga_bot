from secret.webhook_url import *
from send_slack import send_to_slack
from control_csv import input_csv, output_csv
import requests,bs4,csv

title = 'さいはてのどうくつ'
url = 'https://l-v-l.com/'
csv_path = '/Users/omori/workspace/web_manga_bot/log/log_saihate.csv'

def scraping_saihate(url=url):
    print(title)
    res = requests.get(url)
    # html.parserはHTMLのタグ情報から情報を解釈してくれる
    soup = bs4.BeautifulSoup(res.content, "html.parser")
    chapter_list = [n.img['alt'] for n in soup.select('.image')]
    return chapter_list

def log_creation(chapters):
    log_array = []
    log_array.append(chapters)
    output_csv(csv_path, log_array)

def main():
    # 最新のタイトルのリストを取得
    latest = scraping_saihate()
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
