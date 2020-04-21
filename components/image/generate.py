from functools import lru_cache
from random import choice
from urllib.error import URLError
from urllib.request import urlopen

import numpy as np
from PIL import Image
from googleapiclient.discovery import build

from components.image.effects import NONDESTRUCTIVE, DESTRUCTIVE

with open('./components/image/nouns.txt', 'r') as nouns:
    NOUNS = nouns.read().splitlines()


@lru_cache()
def search(api_key: str, cse_cx: str, query: str, count: int = 10) -> set:
    service = build("customsearch", "v1", developerKey=api_key)
    parameters = {'cx': cse_cx,
                  'num': count,
                  'q': query,
                  'searchType': 'image',
                  'fileType': 'png',
                  'imgSize': 'XLARGE',
                  'imgType': 'photo',
                  'imgColorType': 'color',
                  'safe': 'off'}

    results = service.cse().list(**parameters).execute()
    return set(r['link'] for r in results.get('items', []))


def retrieve_random(urls: set) -> np.ndarray:
    urls = urls.copy()
    while urls:
        url = choice(tuple(urls))
        urls -= {url}

        try:
            img = Image.open(urlopen(url))
        except URLError:
            continue

        return np.array(img.convert('RGB')) / 255

    raise Exception('No valid images found in url set.')


def distort(img: np.ndarray, destructive=2, nondestructive=1) -> Image:
    effects = set()

    for i in range(destructive):
        effects.add(choice(tuple(DESTRUCTIVE - effects)))

    for i in range(nondestructive):
        effects.add(choice(tuple(NONDESTRUCTIVE - effects)))

    for i in range(destructive + nondestructive):
        effect = choice(tuple(effects))
        effects.remove(effect)
        img = effect(img)

    return Image.fromarray((img * 255).astype('uint8'))
