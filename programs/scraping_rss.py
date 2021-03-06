# rssフィードを使って更新情報を取得する
# 隣のヤングジャンプ、くらげバンチ
import feedparser
from send_slack import send_to_slack
from control_csv import input_csv, output_csv

url_list = [
    # 極主婦道
    'https://kuragebunch.com/rss/series/10834108156629370787',
    # はたらかないふたり
    'https://kuragebunch.com/rss/series/10834108156628842496',
    # OnePanchMan
    'https://tonarinoyj.jp/rss/series/13932016480028984490',
    # バトゥーキ
    'https://tonarinoyj.jp/rss/series/10834108156631752007',
    # 推しの子
    'https://tonarinoyj.jp/rss/series/13933686331626272801',
    # スーサイドガール
    'https://tonarinoyj.jp/rss/series/13933686331624804843',
    # さばえとヤったらおわる
    'https://kuragebunch.com/rss/series/10834108156689698365',
    # 趣味のラブホテル
    'https://kuragebunch.com/rss/series/10834108156681517332',
    ]
csv_path = '/Users/omori/workspace/web_manga_bot/log/log_rss.csv'

def scraping(url):
    # print("url = "+url)
    d = feedparser.parse(url)
    print(d.channel.title)
    latest_entry = d.entries[0]

    return [d.channel.title, d.channel.link, latest_entry.title, latest_entry.updated, latest_entry.link]


def log_creation(url_list=url_list):
    log_array = []
    for i, url in enumerate(url_list):
        rss_meta_list = scraping(url)
        log_array.append(rss_meta_list)

    # print(log_array)
    output_csv(csv_path,log_array)



def main():
    output_array = [] # この配列の中身を最終的にログとしてCSVファイルに書き込む
    # ログを取得
    past_data_list = input_csv(csv_path)
    if len(past_data_list) != len(url_list):
        print('csvファイルは空です')
        log_creation()
        past_data_list = input_csv(csv_path)

    for i, url in enumerate(url_list):
        current_data = scraping(url)
        output_array.append(current_data)
        past_data = past_data_list[i]
        if past_data != current_data:
            # print(current_data)
            send_to_slack(current_data[0], current_data[1], current_data[2])
        else:
            print("The Article has not updated ...")

    # ログをCSVに書き込む
    output_csv(csv_path, output_array)

if __name__ == '__main__':
    main()
