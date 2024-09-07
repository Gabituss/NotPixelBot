import requests
import json
import time
import random
import config
from setproctitle import setproctitle
from config import url, accounts
from convert import get

setproctitle("notpixel")

start = 425927
image = get("")

c = {
    '#': "#000000",
    '.': "#3690EA",
    '*': "#ffffff"
}

def get_color(pixel, header):
    query = requests.get(f"{url}/image/get/{str(pixel)}", headers=header)
    return query.json()['pixel']['color']


def main(auth, savep):
    next_pixel, x, y = savep
    headers = {
        'authorization': auth
    }
    g = requests.get(f"{url}/mining/claim", headers=headers)

    def next(x, y, next_pixel):
        if x < len(image[0]) - 1:
            x += 1
            next_pixel += 1
        elif y < len(image) - 1:
            x = 0
            y += 1
            next_pixel += -len(image[0]) + 1001
        else:
            x = 0
            y = 0
            next_pixel -= len(image[0]) - len(image)
            time.sleep(180 + random.randint(60, 180))
        return x, y, next_pixel

    while True:
        print(y, x)
        if image[y][x] == ' ' or get_color(next_pixel, headers) == c[image[y][x]]:
            print("skip")
            time.sleep(config.DELAY + random.uniform(0.005, 0.007))
            x, y, next_pixel = next(x, y, next_pixel)
            continue
        data = {
            "pixelId": next_pixel,
            "newColor": c[image[y][x]]
        }
        response = requests.post(f'{url}/repaint/start', data=json.dumps(data), headers=headers)
        if response.status_code == 400:
            print("sleep")
            return next_pixel, x, y
        else:
            print(response.text)
            x, y, next_pixel = next(x, y, next_pixel)


save = start
xs = 0
ys = 0
while True:
    for i in accounts:
        save, xs, ys = main(i, [save, xs, ys])
    time.sleep(config.WAIT + random.randint(5, 27))
