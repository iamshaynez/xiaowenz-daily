import argparse
import os
import random

import openai
import pendulum
import requests
from dotenv import load_dotenv
from BingImageCreator import ImageGen

load_dotenv()

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

# get random poem
# return sentence(used for make pic) and poem(sentence with author and origin)
def get_poem():
    SENTENCE_API = "https://v1.jinrishici.com/all"
    DEFAULT_SENTENCE = "落日净残阳 雾水拈薄浪 "
    DEFAULT_POEM = "落日净残阳，雾水拈薄浪。 —— Xiaowen.Z / 卜算子"
    POEM_TEMPLATE = "{sentence} —— {author} / {origin}"

    try:
        r = requests.get(SENTENCE_API)
        if r.ok:
            sentence = r.json().get("content")
            poem = POEM_TEMPLATE.format(
                sentence = sentence, author=r.json().get("author"), origin=r.json().get("origin")
            )
            return sentence, poem
        return DEFAULT_SENTENCE, DEFAULT_POEM
    except Exception as e:
        print(type(e), e) 
        return DEFAULT_SENTENCE, DEFAULT_POEM

# create stable diffusion prompt
# translate poem to english for better pic
def make_pic_prompt(sentence):
    openai.api_key = OPENAI_API_KEY
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a translator. Translate the chinese poem into english and return only the translated words."},
                {"role": "user", "content": sentence},
            ]
        )
        return response['choices'][0]['message']['content'].replace(","," ").replace("."," ")
    except Exception as e:
        return sentence

# create pic
# return url, the image will not be save to local environment
def make_pic_from_openai(sentence):
    """
    return the link formd
    """
    # the image prompt generation
    prompt_styles = ["Abstract Expressionism","Art Nouveau",
                     "Surrealism","Impressionism","Cubism","Minimalism","Pop Art","Gothic","Romanticism","Fauvism",
                     "Renaissance","Pixel Art","Graffiti","Japanese Ukiyo-e","Science Fiction","Steampunk",
                     "Fantasy","Horror","Film Noir","Vintage"]
    style = random.choice(prompt_styles)
    prompt_sentence = make_pic_prompt(sentence) + f", textless, {style}"
    print(f'Prompt Str: [{prompt_sentence}]')


    #date_str = pendulum.now().to_date_string()
    new_path = os.path.join("OUT_DIR", "TMP_DIR")
    if not os.path.exists(new_path):
        os.mkdir(new_path)  
    
    openai.api_key = OPENAI_API_KEY
    response = openai.Image.create(prompt=prompt_sentence, n=1, size="1024x1024")
    
    image_url = response["data"][0]["url"]
    print(f'image_url:{image_url}')
    # s = requests.session()
    # index = 0
    # while os.path.exists(os.path.join(new_path, f"{index}.jpeg")):
    #     index += 1
    # with s.get(image_url, stream=True) as response:
    #     # save response to file
    #     response.raise_for_status()
    #     with open(os.path.join(new_path, f"{index}.jpeg"), "wb") as output_file:
    #         for chunk in response.iter_content(chunk_size=8192):
    #             output_file.write(chunk)
    
    return image_url, "Image powered by OpenAI Dalle-2"

# create pic from bing image generator
# once Dalle3 api is available, this might be retired.
def make_pic_from_bing(sentence, bing_cookie):
    # for bing image when dall-e3 open drop this function
    i = ImageGen(bing_cookie)
    images = i.get_images(sentence)
    return images, "Image powered by Bing Dalle-3"

def make_pic(sentence):
    if BING_COOKIE is not None:
        try:
            images, image_comment = make_pic_from_bing(sentence, BING_COOKIE)
            return images[0], image_comment
        except Exception as e:
            print(f'Image generated from Bing failed: {type(e)}')
            print(type(e), e) 
    else:
        print('Bing Cookie is not set. Use OpenAI to generate Image')
    image_url, image_comment = make_pic_from_openai(sentence)
    return image_url, image_comment

# get a random quota
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
    except Exception as e:
        print(type(e), e) 
        return DEFAULT_ONE

# get today's weather
# city hard coded in API URL. You may change it based on city code list below
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
    except Exception as e:
        print(type(e), e) 
        return DEFAULT_WEATHER

# send message to telegram
# send image with caption if the image arg is not None
def send_tg_message(tg_bot_token, tg_chat_id, message, image = None):
    print(f'Sending to Chat {tg_chat_id}')
    if image is None:
        try:
            request_url = "https://api.telegram.org/bot{tg_bot_token}/sendMessage".format(tg_bot_token = tg_bot_token)
            request_data = {'chat_id': tg_chat_id, 'text': message}
            response = requests.post(request_url, data=request_data)
            return response.json()
        except Exception as e:
            print("Failed sending message to Telegram Bot.") 
            print(type(e), e) 
            return ""
    else:
        try:
            photo_url = image
            request_url = "https://api.telegram.org/bot{tg_bot_token}/sendPhoto".format(tg_bot_token = tg_bot_token)
            request_data = {'chat_id': tg_chat_id, 'photo': photo_url, 'caption': message}
            response = requests.post(request_url, data=request_data)
            return response.json()
        except Exception as e:
            print("Failed sending message to Telegram Bot with image.") 
            print(type(e), e) 
            return ""




# make a template for message
# generate content
# send
def main():
    print("Main started...")
    DAILY_TEMPLATE = "又到了新的一天了！\r\n\r\n{weather}\r\n---\r\n今日名言：{one}\r\n---\r\n今日诗词和配图：{poem}\r\n---\r\n{comment}"
    one = get_one()
    sentence, poem = get_poem()
    weather = get_weather()
    
    sentence_processed = sentence.replace("，"," ").replace("。"," ").replace("."," ")
    print(f'Processed Sentence: {sentence_processed}')

    image_url, image_comment = make_pic(sentence_processed)

    body = DAILY_TEMPLATE.format(
        weather=weather, one=one, poem=poem, comment=image_comment
    )

    print(f'Image URL: {image_url}')
    print(f'Image Comment: {image_comment}')
    print("Message constructed...")
    print(body)
    print("Sending to Telegram...")
    r_json = send_tg_message(tg_bot_token=TG_BOT_TOKEN, tg_chat_id=TG_CHAT_ID, message=body, image=image_url)
    print(r_json)

if __name__ == "__main__":
    main()