from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

topics = {
    "group1": {
        "group_id": -1002124816119,
        "subgroups": {
            "subgroup1": 157,
            "subgroup2": 4,
            "subgroup3": 2,
        }
    }
}

notifications = {
    "пн,вт,ср,чт,пт": {
        "11:00": "Пул 1 заказов закрыт",
        "13:00": "Пул 2 заказов закрыт",
        "15:00": "Пул 3 заказов закрыт",
        "17:00": "Пул 4 заказов закрыт",
        "excluded_dates": [],
    },
    "сб,вс": {
        "12:00": "Пул 1 заказов закрыт",
        "14:00": "Пул 2 заказов закрыт",
        "16:00": "Пул 3 заказов закрыт",
        "excluded_dates": [],
    }
}

weekday_dict = {
    "0": "вс",
    "1": "пн",
    "2": "вт",
    "3": "ср",
    "4": "чт",
    "5": "пт",
    "6": "сб",
}
