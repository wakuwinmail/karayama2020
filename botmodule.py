from slackbot.bot import respond_to
from slackbot.bot import listen_to
import requests

@respond_to('test')
def test(message):
    message.reply('動作確認')

@listen_to('IDを入力 (.*)')
def test_id(message,something):
    message.reply('テスト')
    submission = requests.get('http://codeforces.com/api/user.status?handle='+something+'&from=1')
    submission = submission.json()
    if submission['status'] == 'FAILED' :
        message.reply('そのIDは存在しません')
        return
    submission = submission['result']
    message.reply(str(len(submission)))
