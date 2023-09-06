import argparse
import os
import random

import openai
import pendulum
import requests
from dotenv import load_dotenv
from github import Github

load_dotenv()

# required APIs
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TIAN_API_KEY = os.getenv('TIAN_API_KEY')

def make_pic_and_save(sentence):
    """
    return the link for md
    """
    # do not add text on the png
    sentence = sentence + ", textless"

    #date_str = pendulum.now().to_date_string()
    new_path = os.path.join("OUT_DIR", "TMP_DIR")
    if not os.path.exists(new_path):
        os.mkdir(new_path)  
    
    openai.api_key = OPENAI_API_KEY
    response = openai.Image.create(prompt=sentence, n=1, size="1024x1024")
    image_url = response["data"][0]["url"]
    s = requests.session()
    index = 0
    while os.path.exists(os.path.join(new_path, f"{index}.jpeg")):
        index += 1
    with s.get(image_url, stream=True) as response:
        # save response to file
        response.raise_for_status()
        with open(os.path.join(new_path, f"{index}.jpeg"), "wb") as output_file:
            for chunk in response.iter_content(chunk_size=8192):
                output_file.write(chunk)
    
    return image_url

def get_poem():
    SENTENCE_API = "https://v1.jinrishici.com/all"
    DEFAULT_SENTENCE = "落日净残阳\r\n雾水拈薄浪\r\n"

    try:
        r = requests.get(SENTENCE_API)
        if r.ok:
            return r.json().get("content", DEFAULT_SENTENCE)
        return DEFAULT_SENTENCE
    except:
        print("get SENTENCE_API wrong")
        return DEFAULT_SENTENCE

def get_one():
    ONE_API = "https://apis.tianapi.com/dictum/index?key={TIAN_API_KEY}&num=1".format(TIAN_API_KEY=TIAN_API_KEY)
    DEFAULT_ONE = "人生在勤，勤则不匮。 ——(北魏）贾思勰"
    ONE_TEMPLATE = "{content} —— {origin}"
    try:
        r = requests.get(ONE_API)
        if r.ok:
            one = ONE_TEMPLATE.format(
                content=r.json().get("result").get("list")[0].get("content"),  origin=r.json().get("result").get("list")[0].get("mrname")
            )
            return one
        return DEFAULT_ONE
    except:
        print("get ONE_API wrong")
        return DEFAULT_ONE

def get_weather():
    WEATHER_API = "http://t.weather.sojson.com/api/weather/city/101210101"
    # https://github.com/baichengzhou/weather.api/blob/master/src/main/resources/citycode-2019-08-23.json to find the city code
    DEFAULT_WEATHER = "未查询到天气，好可惜啊"
    WEATHER_TEMPLATE = "今天是{date} {week}，{city}的天气是{type}，{high}，{low}，空气质量指数{aqi}"

    try:
        r = requests.get(WEATHER_API)
        if r.ok:
            weather = WEATHER_TEMPLATE.format(
                date=r.json().get("data").get("forecast")[0].get("ymd"), week=r.json().get("data").get("forecast")[0].get("week"),
                city=r.json().get("cityInfo").get("city"),
                type=r.json().get("data").get("forecast")[0].get("type"), high=r.json().get("data").get("forecast")[0].get("high"),
                low=r.json().get("data").get("forecast")[0].get("low"), aqi=r.json().get("data").get("forecast")[0].get("aqi")
            )
            return weather
        return DEFAULT_WEATHER
    except:
        print("get weather failed")
        return DEFAULT_WEATHER

def main():
    DAILY_TEMPLATE = "又到了新的一天了！{weather}\r\n今日名言：{one}\r\n今日诗词：{poem}\r\nHave a good day, good luck!"
    one = get_one()
    poem = get_poem()
    weather = get_weather()
    body = DAILY_TEMPLATE.format(
        weather=weather, one=one, poem=poem
    )
    
    #pic = make_pic_and_save(poem)

    print(body)

if __name__ == "__main__":
    main()