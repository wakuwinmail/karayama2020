from slackbot.bot import respond_to
from slackbot.bot import listen_to
 


# 「respond_to」はメンションする(@でターゲットを指定すること)と応答する
@respond_to('(\d+)スレ立てて')
def greeting_1(message, arg):
    # Slackに応答を返す

    int_arg = int(arg)
    if int_arg>10:
        message.react('cold_sweat')
        message.send('10個を超えるスレッドは立てられません')
        return

    
    message.react('ok_woman')
    message.reply('OK!' + str(int_arg) + '個のスレッドを立てます！')
    
    arg = int(arg)

    
    i = 0
    for i in range(int_arg):
        message.send('このスレッドで' + str(i + 1) + '番目の問題について話し合いましょう！')