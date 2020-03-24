from secret.webhook_url import *
from send_slack import send_to_slack
from control_csv import input_csv, output_csv
import requests,bs4,csv

url = 'http://www.goldfishkingdom.client.jp/'
csv_path = '../log/log_kingyo.csv'

def scraping(url=url):
    res = requests.get(url)
    # html.parserはHTMLのタグ情報から情報を解釈してくれる
    soup = bs4.BeautifulSoup(res.content, "html.parser")
    gallaries = [n.img['src'] for n in soup.select('.gallery > li')] # .getText()を付けることで、HTMLのタグを取り除くことができる
    chapter = soup.select_one('#chapter')
    chapters = [n.img['alt'] for n in chapter.find_all('li')]
    # print(chapters)
    return chapters[-1], gallaries

def log_creation(gallaries):
    output_array = []
    output_array.append(gallaries)
    output_csv(csv_path, output_array)


def main():
    latest_chapter, latest_gallaries = scraping()

    output_array = [] # この配列の中身を最終的にログとしてCSVファイルに書き込む
    past_gallaries = input_csv(csv_path)[0]
    if not past_gallaries: # 初期化
        print('csvファイルは空です')
        log_creation(latest_gallaries)

    output_array.append(latest_gallaries)
    if past_gallaries != latest_gallaries:
        # 差分のリストを取得、複数の更新があった場合複数のメッセージを作成する
        print(set(past_gallaries))
        diff_list = list(set(latest_gallaries) - set(past_gallaries)) # set型・・・集合を扱う
        # print(diff_list)
        for n in diff_list:
            # message =
            send_to_slack(n.strip("¥n"))
    else:
        print("The Article has not updated ...")

    # ログをCSVに書き込む
    output_csv(csv_path, output_array)

if __name__ == '__main__':
    main()
