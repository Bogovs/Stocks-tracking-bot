from datetime import datetime, timedelta
import requests
import sqlite3


API_KEY_STOCKS = "key"
API_KEY_NEWS = "key"
BOT_TOKEN = "key"
# i know that storing keys in code is a bad idea


#  ------------------------------------------------------------------------------------------


def collect_users():

    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    return [str(id[0]) for id in cursor.execute("SELECT id FROM users_data")]


def stock_name(company_name):

    if company_name == "Tesla":
        return "TSLA"
    elif company_name == "Facebook":
        return "FB"
    elif company_name == "Google":
        return "GOOGL"
    elif company_name == "BMW":
        return "BMW.DEX"


connect = sqlite3.connect('users.db')
cursor = connect.cursor()

for us_id in collect_users():

    cursor.execute(f"SELECT stock FROM users_data WHERE id = {us_id}")
    COMPANY_NAME = cursor.fetchone()[0]
    STOCK_NAME = stock_name(COMPANY_NAME)

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK_NAME}&apikey={API_KEY_STOCKS}'
    r = requests.get(url)
    data = r.json()

    last_refresh = data["Meta Data"]["3. Last Refreshed"][:10]
    day_close = data["Time Series (Daily)"][last_refresh]["4. close"]


    def day_back(now, back):

        year = int(now[:4])

        if 0 == int(now[5:7][0]):
            month = int(now[6])
        else:
            month = int(now[5:7])

        if 0 == int(now[8:10][0]):
            day = int(now[9])
        else:
            day = int(now[8:10])

        date = datetime(year, month, day)
        date -= timedelta(days=back)

        if date.day in range(0, 9) and date.month in range(0, 9):
            return f"{date.year}-0{date.month}-0{date.day}"
        elif date.day in range(0, 9):
            return f"{date.year}-{date.month}-0{date.day}"
        elif date.month in range(0, 9):
            return f"{date.year}-0{date.month}-{date.day}"
        else:
            return f"{date.year}-{date.month}-{date.day}"


    try:
        yesterday_close = data["Time Series (Daily)"][day_back(last_refresh, 1)]["4. close"]
    except Exception:
        try:
            yesterday_close = data["Time Series (Daily)"][day_back(last_refresh, 2)]["4. close"]
        except Exception:
            try:
                yesterday_close = data["Time Series (Daily)"][day_back(last_refresh, 3)]["4. close"]
            except Exception:
                yesterday_close = data["Time Series (Daily)"][day_back(last_refresh, 4)]["4. close"]


    def change(today, yesterday):
        float(today)
        float(yesterday)
        if today == yesterday:
            return 0
        return round(((float(today) - float(yesterday)) / float(yesterday)) * 100, 2)


    val = change(day_close, yesterday_close)
    up_down = f"{val}%"


    # ------------------------------------------------------------------------------------------


    # endpoint = f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&from=2021-10-05&sortBy=publishedAt&apiKey={API_KEY_NEWS}&language=en"
    # res = requests.get(endpoint)
    # news = res.json()

    # three_news = news["articles"][:3]
    # a = []
    # b = []
    # c = []
    # for n in three_news:
    #    a.append(n["title"])
    #    b.append(n["description"])
    #    c.append(n["url"])

    # first_news = [a[0], b[0], c[0]]
    # second_news = [a[1], b[1], c[1]]
    # third_news = [a[2], b[2], c[2]]

    # news_list = [first_news, second_news, third_news]



    # ------------------------------------------------------------------------------------------


    massage_text = f"{STOCK_NAME}:  *${round(float(day_close), 2)}* ({up_down})"

    def telegram_bot_send_text(bot_text, token):

        send_text = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={us_id}&text={bot_text}&parse_mode=Markdown"
        requests.get(send_text)


    telegram_bot_send_text(massage_text, BOT_TOKEN)
