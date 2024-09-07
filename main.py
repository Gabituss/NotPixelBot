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
    query = requests.get(f"{url}/image/get/{str(pixel)}", headers=header)
    return query.json()['pixel']['color']


def claim(header):
    requests.get(f"{url}/mining/claim", headers=header)


def get_pixel(x, y):
    return y * 1000 + x + 1


def get_pos(pixel, size_x):
    return pixel % size_x, pixel // size_x


def get_canvas_pos(x, y):
    return get_pixel(start_x + x - 1, start_y + y - 1)


start_x = 926
start_y = 425


def next_pixel(pos_image, size):
    return (pos_image + 1) % size


def paint(canvas_pos, color, header):
    data = {
        "pixelId": canvas_pos,
        "newColor": color
    }

    response = requests.post(f"{url}/repaint/start", data=json.dumps(data), headers=header)
    x, y = get_pos(canvas_pos, len(image[0]))

    if response.status_code == 400:
        print("Out of energy")
        return False

    print(f"paint: {x},{y}")
    return True


def main(auth, pos_image):
    headers = {'authorization': auth}

    claim(headers)

    size = len(image) * len(image[0])

    good = True
    while good:
        x, y = get_pos(pos_image, len(image[0]))

        try:
            if image[y][x] == ' ' or get_color(get_canvas_pos(x, y), headers) == c[image[y][x]]:
                print(f"skip: {start_x + x - 1},{start_y + y - 1}")
                pos_image = next_pixel(pos_image, size)
                continue

            if paint(get_canvas_pos(x, y), c[image[y][x]], headers):
                pos_image = next_pixel(pos_image, size)
                continue
        except IndexError:
            print(pos_image, y, x)

        good = False

    return pos_image


pos = 0
while True:
    for i in accounts:
        main(i, pos)

    time.sleep(config.WAIT + random.randint(5, 27))
