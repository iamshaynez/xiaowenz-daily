[![Daily](https://github.com/iamshaynez/xiaowenz-daily/actions/workflows/daily.yml/badge.svg)](https://github.com/iamshaynez/xiaowenz-daily/actions/workflows/daily.yml)

# Daily

每天生成一点点随机的信息，通过 Telegram Bot 发送给自己，给悲催的生活一点点惊喜。

例子:

![image.png](https://vip2.loli.io/2023/09/07/OkwunKc8B7gDIJl.png)

# How to use

## Fork this project

Well done.

## Config the secrets in your repository

~~~python
# required settings. config in github secrets
# -------------
# OpenAI: https://platform.openai.com/account/usage
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
# TIAN_API_KEY: https://www.tianapi.com/console/
TIAN_API_KEY = os.environ['TIAN_API_KEY'] # https://www.tianapi.com/console/
# Telegram Bot Token
TG_BOT_TOKEN = os.environ['TG_BOT_TOKEN']
# Telegram Chat ID to want to send the message to
TG_CHAT_ID = os.environ['TG_CHAT_ID']
# Bing Cookie if image to be generated from Dalle3, optional
BING_COOKIE = os.environ.get('BING_COOKIE', '')
# -------------
~~~

## Change the running time in daily.yml if you well

Well done.

## Cost

Daily cost will be 0.02 USD if using OpenAI.