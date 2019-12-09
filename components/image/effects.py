from random import randint, random

import numpy
from PIL import Image
from scipy.signal import convolve2d


def greyscale(img):
    _ = numpy.average(img, axis=2)
    for channel in range(3):
        img[:, :, channel] = _

    return img


def invert(img):
    return 1 - img


def inset(img, scale=None, iterations=None):
    scale = scale or random() / 2 + .4
    iterations = iterations or randint(1, 5)

    _ = (img * 255).astype('uint8')
    _ = Image.fromarray(_)
    for i in range(iterations):
        smaller = _.resize((int(_.size[0] * scale), int(_.size[1] * scale)))
        _.paste(smaller,
                box=((_.size[0] - smaller.size[0]) // 2,
                     (_.size[1] - smaller.size[1]) // 2))

    return numpy.array(_) / 255


def roll(img, speed=None):
    speed = speed or randint(-3, 3)
    for x in range(img.shape[0]):
        img[x] = numpy.roll(img[x], x * speed)

    return img


def sobel(img):
    kernel = numpy.array(((-1, 0, 1),
                          (-2, 0, 2),
                          (-1, 0, 1)))
    for channel in range(3):
        _ = img[:, :, channel]
        x = convolve2d(_, kernel, mode='same')
        y = convolve2d(_, numpy.rot90(kernel), mode='same')
        img[:, :, channel] = numpy.sqrt(x**2 + y**2)

    return img


def frequency_mosh(img, frequency=None):
    frequency = frequency or randint(3, 10)
    x, y = numpy.linspace(0, 1, img.shape[0]), numpy.linspace(0, 1, img.shape[1])
    for channel in range(3):
        _ = numpy.fft.fft2(img[:, :, channel])
        _ *= numpy.sin(x[:, None] * y[None, :] * numpy.pi * frequency)
        img[:, :, channel] = numpy.fft.ifft2(_).astype('float64')

    return img


def channel_swap(img):
    return numpy.roll(img, randint(1, 3), axis=2)


def sine(img, frequency=None):
    frequency = frequency or randint(3, 10)
    _ = numpy.sin(img * frequency * numpy.pi * 2)
    return (_ + 1) / 2


def contrast(img, tension=None):
    tension = tension or randint(1, 4)
    _ = img * tension - ((tension - 1) / 2)
    _ = numpy.clip(_, 0, 1)
    return (1 - numpy.cos(_ * numpy.pi)) / 2


def solarize(img):
    return invert(contrast(greyscale(img)))


def quantize(img, palette=None, thresholds=None):
    palette = palette or numpy.random.random((3, 3))
    thresholds = thresholds or numpy.linspace(0, .75, 3)
    values = numpy.average(img, axis=2)
    for i, v in enumerate(thresholds):
        img[values > v] = palette[i]

    return img


def aberrate(img, minimum=0, maximum=50):
    for channel in range(3):
        shift = numpy.random.randint(minimum, maximum, 2)
        img[:, :, channel] = numpy.roll(img[:, :, channel], shift, (0, 1))

    return img


def pixel_sort(img, rotation=None, condition=lambda lum: (lum > 1 / 3) & (lum < 2 / 3)):
    rotation = rotation or randint(1, 4)
    pixels = numpy.rot90(img, rotation)
    values = numpy.average(pixels, axis=2)
    edges = numpy.apply_along_axis(lambda row: numpy.convolve(row, [-1, 1], 'same'), 0, condition(values))
    intervals = [numpy.flatnonzero(row) for row in edges]

    for row, key in enumerate(values):
        order = numpy.split(key, intervals[row])
        for index, interval in enumerate(order[1:]):
            order[index + 1] = numpy.argsort(interval) + intervals[row][index]
        order[0] = range(order[0].size)
        order = numpy.concatenate(order)

        for channel in range(3):
            pixels[row, :, channel] = pixels[row, order.astype('uint32'), channel]

    return numpy.rot90(pixels, -rotation)


NONDESTRUCTIVE = {greyscale, invert, channel_swap, contrast, solarize}
DESTRUCTIVE = {sobel, frequency_mosh, sine, quantize, pixel_sort, roll, inset, aberrate}
