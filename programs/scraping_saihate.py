from secret.webhook_url import *
from send_slack import send_to_slack
from control_csv import input_csv, output_csv
import requests,bs4,csv

title = 'さいはてのどうくつ'
url = 'https://l-v-l.com/'
csv_path = '/Users/omori/workspace/web_manga_bot/log/log_saihate.csv'

def scraping(url=url):
    print(title)
    res = requests.get(url)
    # html.parserはHTMLのタグ情報から情報を解釈してくれる
    soup = bs4.BeautifulSoup(res.content, "html.parser")
    chapter_list = [n.img['alt'] for n in soup.select('.image')] # .getText()を付けることで、HTMLのタグを取り除くことができる
    # print(chapter_list)
    return chapter_list

def log_creation(chapters):
    output_array = []
    output_array.append(chapters)
    output_csv(csv_path, output_array)


def main():
    output_array = [] # この配列の中身を最終的にログとしてCSVファイルに書き込む
    latest = scraping() # 話のタイトルのリスト
    past = input_csv(csv_path)
    if not past: # 初期化

        print('csvファイルは空です')
        log_creation(latest)
        past = latest

    output_array.append(latest)

    if past[0] != latest:
        # 差分のリストを取得、複数の更新があった場合複数のメッセージを作成する
        diff_list = list(set(latest) - set(past[0])) # set型・・・集合を扱う
        # print(diff_list)
        for n in diff_list:
            send_to_slack(title, url, n)
    else:
        print("The Article has not updated ...")

    # ログをCSVに書き込む
    output_csv(csv_path, output_array)

if __name__ == '__main__':
    main()
