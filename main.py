from slack_webhook import Slack
import requests,bs4


# urlには先の認証でもらったIncoming Webhook URLを指定
webhook_url = 'https://hooks.slack.com/services/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'
slack = Slack(url=webhook_url)
slack.post(text="Hello, world.")
