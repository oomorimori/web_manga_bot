from secret.webhook_url import *
from send_slack import send_to_slack
from control_csv import input_csv, output_csv
import requests,bs4,csv

title = '金魚王国の崩壊'
url = 'http://www.goldfishkingdom.client.jp/'
csv_path = '/Users/omori/workspace/web_manga_bot/log/log_kingyo.csv'

def scraping_kingyo_kingdom(url=url):
    print(title)
    res = requests.get(url)
    # html.parserはHTMLのタグ情報から情報を解釈してくれる
    soup = bs4.BeautifulSoup(res.content, "html.parser")
    gallaries = [n.img['src'] for n in soup.select('.gallery > li')] # .getText()を付けることで、HTMLのタグを取り除くことができる
    chapter = soup.select_one('#chapter')
    chapters = [n.img['alt'] for n in chapter.find_all('li')]
    # print(chapters)
    return chapters[-1], gallaries

def log_creation(gallaries):
    log_array = []
    log_array.append(gallaries)
    output_csv(csv_path, log_array)


def main():
    # 最新話と最新のページを取得（ページ毎に更新されるので）
    latest_chapter, latest_gallaries = scraping_kingyo_kingdom()
    # CSVファイルからログを取得する
    past_gallaries = input_csv(csv_path) # [[]]
    if not past_gallaries: # 初期化
        print('csvファイルは空です')
        log_creation(latest_gallaries)
        past_gallaries = latest_gallaries

    # この配列の中身を最終的にログとしてCSVファイルに書き込む
    log_array = []
    # 最新話の画像タイトルの一覧をログ配列に格納
    log_array.append(latest_gallaries)

    # ログとの差分があれば（更新があった場合）Slackで通知
    if past_gallaries[0] != latest_gallaries:
        # 差分のリストを取得、複数の更新があった場合複数のメッセージを作成する
        diff_list = list(set(latest_gallaries) - set(past_gallaries[0])) # set型・・・集合を扱う
        # print(diff_list)
        for n in diff_list:
            c = f'{latest_chapter} {n.strip(".jpg")}'
            send_to_slack(title, url, c)
    else:
        print("The Article has not updated ...")

    # ログをCSVに書き込む
    output_csv(csv_path, log_array)

if __name__ == '__main__':
    main()
