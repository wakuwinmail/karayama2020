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

@listen_to('リコメンドテスト (.*)')
def test_id(message,something):
    message.reply('テスト')

    req_user = requests.get('http://codeforces.com/api/user.status?handle='+something+'&from=1')
    data_user = req_user.json()
    len_user = len(data_user['result'])

    req_contests = requests.get('https://codeforces.com/api/contest.list?gym=false')
    data_contests = req_contests.json()
    len_contests = len(data_contests['result'])
    contest_names = {}
    id_lists = []

    for i in range(len_contests): 
        contest = data_contests['result'][i]
        if contest['phase'] == 'FINISHED':
            contest_names[contest['id']] = contest['name']
            id_lists.append(contest['id'])
    
    for i in range(len_user):
        check = data_user['result'][i]['contestId']
        if check in contest_names:
            del contest_names[check]
            id_lists.remove(check)

    for i in range(10):
        message.reply(contest_names[id_lists[i]])
