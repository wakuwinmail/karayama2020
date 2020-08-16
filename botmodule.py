from slackbot.bot import respond_to
from slackbot.bot import listen_to
import json
import requests
import os

@respond_to('バチャ立てて')
def InputContest(message):
    contestAPI = requests.get('http://codeforces.com/api/contest.list?gym=false')
    contestAPI = contestAPI.json()
    if contestAPI['status'] == 'FAILED' :
        message.reply('APIの入手に失敗しました')
        return
    contestAPI = contestAPI['result']

    All_contest = {}
    contest = {}

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
    with open('All_contest.json', 'w') as ac:
        json.dump(All_contest, ac, indent=4)
    with open('contest.json', 'w') as c:
        json.dump(contest, c, indent=4)

    message.send('参加する人はIDをメンションで送ってください')
    message.send('入力方法\nID入力 [ID名]')

@respond_to('ID入力 (.*)')
def test_id(message,something):
    req_user = requests.get('http://codeforces.com/api/user.status?handle='+something+'&from=1')
    data_user = req_user.json()
    if data_user['status'] == 'FAILED' :
        message.reply('そのIDは存在しません')
        return
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
    
    All_contest = {}
    contest = {}

    try:
        with open('All_contest.json') as ac:
            All_contest = json.load(ac)
    except:
        message.reply('先にバチャを立ててください')

    try:
        with open('contest.json') as c:
            contest = json.load(c)
    except:
        message.reply('先にバチャを立ててください')

    for x in data_user:
        check = str(x['contestId'])
        if check in All_contest:
            check = All_contest[check]
            if check.startswith('Codeforces Round #'):
                check = check[0:21]
                if check in contest:
                    del contest[check]
                    # id_lists.remove(check)

    with open('contest.json', 'w') as c:
        json.dump(contest, c, indent=4)

    message.reply('IDを受け付けました')

@respond_to('ID入力終了')
def test_recommendation(message):
    cnt = 0
    with open('contest.json') as c:
        contest = json.load(c)
    for x in contest:
        message.reply(x)
        message.reply('http://codeforces.com/contest/'+str(contest[x]))
        cnt += 1
        if cnt == 3:
            break

    os.remove('contest.json')
    os.remove('ALL_contest.json')