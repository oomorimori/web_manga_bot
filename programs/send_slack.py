from slack_webhook import Slack
from secret.webhook_url import WEBHOOK_URL

# Slackへの通知がうまくいかなかった場合、エラーを返してログは取らないようにする
def send_to_slack(message):
    webhook_url = WEBHOOK_URL # 公開するな！
    slack = Slack(url=webhook_url)
    slack.post(text=message)
