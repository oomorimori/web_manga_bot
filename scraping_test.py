from slack_webhook import Slack
import requests,bs4,csv

# スクレイピングしてスープテキストを取り出す
def scraping(url, html_tag):
    res = requests.get(url)
    # html.parserはHTMLのタグ情報から情報を解釈してくれる
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    soup_text = [n.get_text() for n in soup.select(html_tag)] # .getText()を付けることで、HTMLのタグを取り除くことができる

    return soup_text

def output_csv(soup_text):
    print(soup_text)
    # wで開くと上書きモードになり、元の内容は削除される
    with open('./log/log.csv', 'w', newline='', encoding='utf_8') as file:
        writer = csv.writer(file)
        # for i in soup_text:
        #     writer.writerow(i)
        writer.writerow(soup_text)

def input_csv():
    with open('./log/log.csv', 'r', encoding='utf_8', errors='', newline='') as file:
        f = csv.reader(file, delimiter=",", doublequote=True)
        soup_text = [n for n in f]
        print(soup_text[0])
    return soup_text[0]

# Slackへの通知がうまくいかなかった場合、エラーを返してログは取らないようにする
def send_to_slack(message):
    webhook_url = 'https://hooks.slack.com/services/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'
    slack = Slack(url=webhook_url)
    slack.post(text=message)

def main():
    url = 'https://sakanamori.hatenablog.com/'
    html_tag = '.recent-entries-item-inner'
    past_data = input_csv()
    current_data = scraping(url, html_tag)
    # データが更新されていたら差分を取得してSLACKに通知
    if past_data != current_data:
        # set型・・・集合を扱う
        message_list = list(set(current_data) - set(past_data))
        print(message_list)
        for n in message_list:
            # print(n.strip("¥n"))
            send_to_slack(n.strip("¥n"))

        output_csv(current_data)

    else:
        print("The Article has not updated ...")



if __name__ == '__main__':
    main()
