from secret.webhook_url import *
from send_slack import send_to_slack
from control_csv import input_csv, output_csv
import requests,bs4,csv

MANGA_LIST = [
    ['http://www.goldfishkingdom.client.jp/'],
]
csv_path = '../log/log_kingyo.csv'

def scraping(url):
    res = requests.get(url)
    # html.parserはHTMLのタグ情報から情報を解釈してくれる
    soup = bs4.BeautifulSoup(res.content, "html.parser")
    soup_text = [n.get_text() for n in soup.select(html_tag)] # .getText()を付けることで、HTMLのタグを取り除くことができる
    return soup_text

def log_creation():
    output_array = [] # この配列の中身を最終的にログとしてCSVファイルに書き込む
    for i, data in enumerate(MANGA_LIST):
        # [0]：URL [1]：HTML_TAG
        current_data = scraping(data[0], data[1])
        print(current_data)
        # 最新の更新情報をアペンド
        output_array.append(current_data)

    # ログをCSVに書き込む
    output_csv(csv_path, output_array)


def main():
    output_array = [] # この配列の中身を最終的にログとしてCSVファイルに書き込む
    past_data_list = input_csv(csv_path)
    if not past_data_list:
        print('csvファイルは空です')
        log_creation()
        past_data_list = input_csv(csv_path)

    for i, data in enumerate(MANGA_LIST):
        current_data = scraping(data)
        output_array.append(current_data)
        past_data = past_data_list[i]
        if past_data != current_data:
            # 差分のリストを取得、複数の更新があった場合複数のメッセージを作成する
            diff_list = list(set(current_data) - set(past_data)) # set型・・・集合を扱う
            # print(diff_list)
            for n in diff_list:
                send_to_slack(n.strip("¥n"))
        else:
            print("The Article has not updated ...")

    # ログをCSVに書き込む
    output_csv(csv_path, output_array)

if __name__ == '__main__':
    main()
