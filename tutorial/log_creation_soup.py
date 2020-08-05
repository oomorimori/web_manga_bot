from scraping_soup import *
from manga_list import *

def main():
    output_array = [] # この配列の中身を最終的にログとしてCSVファイルに書き込む
    for i, data in enumerate(MANGA_LIST):
        # [0]：URL [1]：HTML_TAG
        current_data = scraping(data[0], data[1])
        print(current_data)
        # 最新の更新情報をアペンド
        output_array.append(current_data)

    # ログをCSVに書き込む
    output_csv(output_array)

if __name__ == '__main__':
    main()
