from ast import Index

import requests
import json
import time
import random
import config
import logging

from setproctitle import setproctitle
from config import url, accounts
from convert import get

setproctitle("notpixel")

image = get("")

c = {
    '#': "#000000",
    '.': "#3690EA",
    '*': "#ffffff"
}


def get_color(pixel, header):
    try:
        query = requests.get(f"{url}/image/get/{str(pixel)}", headers=header)
        return query.json()['pixel']['color']
    except KeyError:
        return "#000000"


def claim(header):
    requests.get(f"{url}/mining/claim", headers=header)


def get_pixel(x, y):
    return y * 1000 + x + 1


def get_pos(pixel, size_x):
    return pixel % size_x, pixel // size_x


def get_canvas_pos(x, y):
    return get_pixel(start_x + x - 1, start_y + y - 1)


start_x = 920
start_y = 386


def next_pixel(pos_image, size):
    return (pos_image + 1) % size


def paint(canvas_pos, color, header):
    data = {
        "pixelId": canvas_pos,
        "newColor": color
    }

    response = requests.post(f"{url}/repaint/start", data=json.dumps(data), headers=header)
    x, y = get_pos(canvas_pos, 1000)

    if response.status_code == 400:
        print("Out of energy")
        return False

    print(f"paint: {x},{y}")
    return True


def main(auth):
    headers = {'authorization': auth}

    claim(headers)

    size = len(image) * len(image[0])
    order = [i for i in range(size)]
    random.shuffle(order)
# booooo
    for pos_image in order:
        x, y = get_pos(pos_image, len(image[0]))
        time.sleep(0.05)
        try:
            if image[y][x] == ' ' or get_color(get_canvas_pos(x, y), headers) == c[image[y][x]]:
                print(f"skip: {start_x + x - 1},{start_y + y - 1}")
                continue

            if paint(get_canvas_pos(x, y), c[image[y][x]], headers):
                continue
            else:
                break
        except IndexError:
            print(pos_image, y, x)


while True:
    for i in accounts:
        main(i)

    print("SLEEEP")
    time.sleep(config.WAIT + random.randint(5, 27))
