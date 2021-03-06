import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import sqlite3
import random
import config

vk_session = vk_api.VkApi(token=config.token)

longpoll = VkLongPoll(vk_session)

vk = vk_session.get_api()

conn = sqlite3.connect(config.sqlite_path)
c = conn.cursor()


def get_user(user_id):
    cmd = "SELECT * FROM users WHERE user_id=%d" % user_id
    c.execute(cmd)
    result = c.fetchone()
    return result


def register_new_user(user_id):
    cmd = "INSERT INTO users(user_id, state) VALUES (%d, '')" % user_id
    c.execute(cmd)
    conn.commit()



while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            if get_user(user_id=event.user_id) is None:
                register_new_user(user_id=event.user_id)

            if event.text.lower() == "привет":
                vk.messages.send(  # Отправляем сообщение
                    user_id=event.user_id,
                    message="Это Питон, детка!",
                    random_id=random.randint(-1000000000, 1000000000)
                )