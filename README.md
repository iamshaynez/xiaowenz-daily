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
# Telegram Bot Token
TG_BOT_TOKEN = os.environ['TG_BOT_TOKEN']
# Telegram Chat ID to want to send the message to
TG_CHAT_ID = os.environ['TG_CHAT_ID']
# Get Weather Information: https://github.com/baichengzhou/weather.api/blob/master/src/main/resources/citycode-2019-08-23.json to find the city code
# Shanghai 101020100
# Hangzhou 101210101 by default
WEATHER_CITY_CODE = os.environ.get('WEATHER_CITY_CODE', '101210101')
# -------------

# Optional Settings. config in github secrets.
# -------------
# 每日一句名人名言 - TIAN_API_KEY: https://www.tianapi.com/console/
TIAN_API_KEY = os.environ.get('TIAN_API_KEY', '') # https://www.tianapi.com/console/
# Bing Cookie if image to be generated from Dalle3. Leave empty to use OpenAI by default
BING_COOKIE = os.environ.get('BING_COOKIE', '')
# 每日待办事项 todoist
TODOIST_API = os.environ.get('TODOIST_API', '')
# -------------
~~~

## Change the running time in daily.yml if you well

Well done.

## Cost

Daily cost will be 0.02 USD if using OpenAI.