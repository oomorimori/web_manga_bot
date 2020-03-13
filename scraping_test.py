from slack_webhook import Slack
import requests,bs4,csv


def scraping(url, html_tag):
    res = requests.get(url)
    # html.parserはHTMLのタグ情報から情報を解釈してくれる
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    latest_articles = [n.get_text() for n in soup.select(html_tag)] # .getText()を付けることで、HTMLのタグを取り除くことができる

    return latest_articles

def output_csv(latest_articles):
    print(latest_articles)
    # wで開くと上書きモードになり、元の内容は削除される
    with open('./log/log.csv', 'w', newline='', encoding='utf_8') as file:
        writer = csv.writer(file)
        # for i in latest_articles:
        #     writer.writerow(i)
        writer.writerow(latest_articles)

def compare(past, current):
    if(past != current):
        webhook_url = 'https://hooks.slack.com/services/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'
        slack = Slack(url=webhook_url)
        slack.post(text="Hello, world.")

def main():
    url = 'https://sakanamori.hatenablog.com/'
    html_tag = '.recent-entries-item-inner'
    latest_articles = scraping(url, html_tag)
    output_csv(latest_articles)


if __name__ == '__main__':
    main()
