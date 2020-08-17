from slackbot.bot import respond_to
from slackbot.bot import listen_to
import json
import requests
import os

@respond_to('build (.*)')
def input_contest(message,something):
    contestAPI = requests.get('http://codeforces.com/api/contest.list?gym=false')
    contestAPI = contestAPI.json()
    if contestAPI['status'] == 'FAILED' :
        message.reply('APIの入手に失敗しました')
        return
    contestAPI = contestAPI['result']

    all_contest = {}
    contest = {}
    Div1_contest = {}
    Div2_contest = {}
    Div3_contest = {}
    for x in contestAPI:
        if x['phase'] != 'FINISHED' :
            continue
        Id = x['id']
        Name = x['name']
        if Name.startswith('Codeforces Round #'):
            # #PI、#FFを弾く
            if Name[18].isdigit():
                # KeyName = 'Codeforces Round #XXX'
                KeyName = Name[0:21]
                if 'Div. 1' in Name:
                    Div1_contest[KeyName] = Id
                if 'Div. 2' in Name:
                    Div2_contest[KeyName] = Id
                if 'Div. 3' in Name:
                    Div3_contest[KeyName] = Id
                all_contest[Id] = KeyName
    if something == 'Div1':
        contest = Div1_contest
    elif something == 'Div2':
        for x in Div1_contest:
            del Div2_contest[x]
        contest = Div2_contest        
    elif something == 'Div3':
        contest = Div3_contest
    else :
        message.reply('入力されたDivには対応していません')
        message.reply('対応例: Div1 Div2 Div3')
        return
    with open('all_contest.json', 'w') as ac:
        json.dump(all_contest, ac, indent=4)
    with open('contest.json', 'w') as c:
        json.dump(contest, c, indent=4)

    message.send('参加する人はIDをメンションで送ってください')
    message.send('入力方法\nid [ID名]')

@respond_to('erase')
def delete_contest(message):
    try:
        os.remove('contest.json')
        os.remove('all_contest.json')
    except:
        message.reply('バチャが立っていません')
    else:
        message.reply('バチャを中止しました')

@respond_to('id (.*)')
def test_id(message,something):
    req_user = requests.get('http://codeforces.com/api/user.status?handle='+something+'&from=1')
    data_user = req_user.json()
    if data_user['status'] == 'FAILED' :
        message.reply('そのIDは存在しません')
        return
    data_user = data_user['result']
    
    all_contest = {}
    contest = {}

    try:
        with open('all_contest.json') as ac:
            all_contest = json.load(ac)
        with open('contest.json') as c:
            contest = json.load(c)
    except:
        message.reply('先にバチャを立ててください')
    else:
        message.reply('IDを受け付けました')

    for x in data_user:
        check = str(x['contestId'])
        if check in all_contest:
            check = all_contest[check]
            if check.startswith('Codeforces Round #'):
                check = check[0:21]
                if check in contest:
                    del contest[check]
                    # id_lists.remove(check)

    with open('contest.json', 'w') as c:
        json.dump(contest, c, indent=4)

    
@respond_to('run')
def test_recommendation(message):
    cnt = 0
    try:
        with open('contest.json') as c:
            contest = json.load(c)
    except:
        message.reply('先にバチャを立ててください')
        return
    if len(contest) == 0:
        message.send('該当するコンテストはありません')
    for x in contest:
        message.send(x)
        message.send('http://codeforces.com/contest/'+str(contest[x])+'/my')
        cnt += 1
        if cnt == 1:
            break

    os.remove('contest.json')
    os.remove('all_contest.json')