from slackbot.bot import respond_to
from slackbot.bot import listen_to
import requests

@respond_to('test')
def test(message):
    message.reply('動作確認')

@listen_to('テスト')
def Test(message):
    message.reply('動作確認')

All_contest = {}
contest = {}

@respond_to('バチャ立てて')
def InputContest(message):
    contestAPI = requests.get('http://codeforces.com/api/contest.list?gym=false')
    contestAPI = contestAPI.json()
    if contestAPI['status'] == 'FAILED' :
        message.reply('APIの入手に失敗しました')
        return
    contestAPI = contestAPI['result']
    for x in contestAPI:
        if x['phase'] != 'FINISHED' :
            continue
        Name = x['name']
        Id = x['id']
        if Name.startswith('Codeforces Round #'):
            # #PI、#FFを弾く
            if Name[18].isdigit():
                # Name = 'Codeforces Round #XXX'
                Name = Name[0:21]
                contest[Name] = Id
                All_contest[Id] = Name
    message.reply('参加する人はIDを入力してください')

@respond_to('IDを入力 (.*)')
def InputID(message,something):
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
    data_user = data_user['result']
    # len_user = len(data_user['result'])

    # req_contests = requests.get('https://codeforces.com/api/contest.list?gym=false')
    # data_contests = req_contests.json()
    # len_contests = len(data_contests['result'])
    # contest_names = {}
    # id_lists = []

    # for i in range(len_contests): 
    #     contest = data_contests['result'][i]
    #     if contest['phase'] == 'FINISHED':
    #         contest_names[contest['id']] = contest['name']
    #         id_lists.append(contest['id'])
    
    for x in data_user:
        check = x['contestId']
        if check in All_contest:
            check = All_contest[check]
            if check.startswith('Codeforces Round #'):
                check = check[0:21]
                if check in contest:
                    del contest[check]
                    # id_lists.remove(check)

@respond_to('ID入力終了')
def test_recommendation(message):
    message.reply('テスト')
    cnt = 0
    for x in contest:
        message.reply(x)
        message.reply('http://codeforces.com/contest/'+str(contest[x]))
        cnt += 1
        if cnt == 3:
            break
