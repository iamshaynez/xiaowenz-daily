import requests

# get a random quota
def make_quota(TIAN_API_KEY):
    print(f'Start making quota...')
    ONE_API = "https://apis.tianapi.com/dictum/index?key={TIAN_API_KEY}&num=1".format(TIAN_API_KEY=TIAN_API_KEY)
    DEFAULT_ONE = "人生在勤，勤则不匮。 ——(北魏）贾思勰"
    ONE_TEMPLATE = "{content} —— {origin}"
    try:
        r = requests.get(ONE_API)
        if r.ok:
            one = ONE_TEMPLATE.format(
                content=r.json().get("result").get("list")[0].get("content"),  origin=r.json().get("result").get("list")[0].get("mrname")
            )
            return f'今日名言：{one}'
        return f'今日名言：{DEFAULT_ONE}'
    except Exception as e:
        print(type(e), e) 
        return f'今日名言：{DEFAULT_ONE}'