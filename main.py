import cv2  # Install with `pip install opencv-python`
import pygame as pg
from math import ceil
from time import time

DIE_WIDTH = 20  # Pixel width of dice
DRAW_PIXELS_NOT_CIRCLES = False  # Draw one pixel for dot (DIE_WIDTH < 20)
RESOLUTION_FACTOR = 1  # How much bigger the window is than the source
BRIGHTNESS_STRETCH = 1  # Exaggerate mid-range brightness
BRIGHTNESS_ADJUSTMENT = 0  # Make final image brighter (increase) or darker (decrease)
INVERTED = False  # Invert brightness

capture = cv2.VideoCapture(0)  # CAMERA INPUT
# capture = cv2.VideoCapture('ObamaSpeech.mp4')  # FILE INPUT

WIDTH, HEIGHT = int(capture.get(3) * RESOLUTION_FACTOR), int(capture.get(4) * RESOLUTION_FACTOR)
DOT_RADIUS = DIE_WIDTH // 10
GRID_WIDTH, GRID_HEIGHT = WIDTH // DIE_WIDTH, HEIGHT // DIE_WIDTH

pg.init()
w = pg.display.set_mode((GRID_WIDTH * DIE_WIDTH, GRID_HEIGHT * DIE_WIDTH))

DOT_CENTERS = {
    1: [[(0, 0)]],
    2: [[(1, -1), (-1, 1)],  [(-1, -1), (1, 1)]],
    3: [[(1, -1), (0, 0), (-1, 1)],  [(-1, -1), (0, 0), (1, 1)]],
    4: [[(-1, -1), (1, -1), (-1, 1), (1, 1)]],
    5: [[(-1, -1), (1, -1), (-1, 1), (1, 1), (0, 0)]],
    6: [[(-1, -1), (1, -1), (-1, 1), (1, 1), (-1, 0), (1, 0)],  [(-1, -1), (1, -1), (-1, 1), (1, 1), (0, -1), (0, 1)]]
}


def get_die_number(brightness):
    brightness = max(1, min(255, (brightness - 127) * BRIGHTNESS_STRETCH + 127 + BRIGHTNESS_ADJUSTMENT))
    if INVERTED: brightness = 256 - brightness
    return ceil(brightness / 42.5)  # Map to 1-6


def draw_dice(image):
    for pixel_x in range(GRID_WIDTH):
        for pixel_y in range(GRID_HEIGHT):
            b, g, r = image[pixel_y][pixel_x]
            brightness = sum([r, g, b]) / 3
            brightness = min(max(brightness, 1), 255)  # clamp between 1-255

            die_number = get_die_number(brightness)

            # Middle pos for the die
            die_x = pixel_x * DIE_WIDTH + 0.5 * DIE_WIDTH
            die_y = pixel_y * DIE_WIDTH + 0.5 * DIE_WIDTH

            # Can be used to draw dice backgrounds
            # pg.draw.rect(w, [255, 255, 255], (die_x-DIE_WIDTH/2, die_y-DIE_WIDTH/2, DIE_WIDTH, DIE_WIDTH))

            for dotCenter in DOT_CENTERS[die_number][0]:  # Use random.choice for some wacky results
                dot_x = die_x + dotCenter[0] * DIE_WIDTH * 0.25
                dot_y = die_y + dotCenter[1] * DIE_WIDTH * 0.25
                if DRAW_PIXELS_NOT_CIRCLES:
                    w.set_at((int(dot_x), int(dot_y)), [255, 255, 255])
                else:
                    pg.draw.circle(w, [255, 255, 255], (int(dot_x), int(dot_y)), DOT_RADIUS)


def draw_lines():
    for i in range(GRID_WIDTH):
        x = i * DIE_WIDTH
        pg.draw.line(w, [50, 50, 50], (x, 0), (x, HEIGHT))

    for i in range(GRID_HEIGHT):
        y = i * DIE_WIDTH
        pg.draw.line(w, [50, 50, 50], (0, y), (WIDTH, y))


if __name__ == '__main__':
    frame = 0
    while True:
        frame += 1
        start = time()

        _, img = capture.read()
        img = cv2.resize(img, (GRID_WIDTH, GRID_HEIGHT), interpolation=cv2.INTER_AREA)  # Downscale
        img = cv2.flip(img, 1)  # Flip image (necessity depends on camera)

        w.fill([0, 0, 0])
        draw_dice(img)
        draw_lines()
        pg.display.update()
        # pg.image.save(w, f'Render/{frame}.png')

        if pg.event.get(pg.QUIT):
            break

        print(f"{int(1 / (time() - start))} FPS")

capture.release()
