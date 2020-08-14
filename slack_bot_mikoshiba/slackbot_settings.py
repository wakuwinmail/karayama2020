# 「API_TOKEN」にはSlackから取得したAPIトークンを記述してください
API_TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


# 知らない言葉を聞いた時のデフォルトの応答
DEFAULT_REPLY = "その言葉の意味は知りません"
 
#外部ファイルを読み込む。botmodule.pyを読み込んでおく
PLUGINS = [
    'slackbot.plugins',
    'botmodule',
]
