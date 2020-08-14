from slackbot.bot import respond_to
from slackbot.bot import listen_to

@respond_to('こんにちは')
def greeting_1(message):
    message.reply('こんにちは！')

@listen_to('ねこー')
def greeting_2(message):
    message.reply('にゃーん')

x = 'にゃー'
@listen_to('にゃーん')
def greeting_3(message):
    message.reply(x)

import requests
res = requests.get('https://codeforces.com/api/contest.list?gym=false')
Data = res.json()
Data = Data['result']

@listen_to('データ')
def testAPI(message):
    message.reply('出力確認')
    for i in range(10):
        print(Data[i]['name'])
        message.reply(str(Data[i]['name']))

@listen_to('コンテスト数')
def contestnum(message):
    message.reply('出力確認')
    message.reply(str(len(Data)))

@listen_to('整数')
def test_int(message):
    message.reply('int型で出力')
    message.reply(str(998244353))

count = 0

def add():
    global count
    count += 1

@listen_to('カウント')
def test_count(message):
    message.reply('カウントします')
    message.reply(str(count))
    add()

@listen_to('IDを入力 (.*)')
def test_id(message,something):
    message.reply('テスト')
    URL = 'http://codeforces.com/api/user.status?handle='+something+'&from=1'
    message.reply(URL)
    message.reply(str(type(URL)))
    sub = requests.get(URL)
    subData = res.json()
    subDate = subData['result']
    message.reply(str(subData[0]['id']))