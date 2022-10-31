from PIL import Image
import random
from collections import defaultdict

im = Image.open("flowers.jpg")
print(im.size)


class PixelMap:
    def __init__(self, img):
        self.img = img.load()
        self.colors = dict()

        self.width = img.size[0]
        self.height = img.size[1]

    def build_map(self):
        # Build pixel map of frequencies form: {(R, G, B): {(R, G, B): frequency}
        for i in range(self.width):
            for j in range(self.height):

                try:
                    if self.img[i, j] in self.colors.keys():
                        if i < self.width - 1:
                            self.colors[self.img[i, j]][self.img[i + 1, j]] += 1
                        if j < self.height - 1:
                            self.colors[self.img[i, j]][self.img[i, j + 1]] += 1
                        if i < self.width - 1 and j < self.height - 1:
                            self.colors[self.img[i, j]][self.img[i + 1, j + 1]] += 1

                    else:
                        self.colors[self.img[i, j]] = defaultdict(lambda: 0)
                        self.colors[self.img[i, j]][self.img[i + 1, j]] += 1


                except KeyError or IndexError:
                    continue

        # self.colors = self.normalize(self.colors)


    def normalize(self, color_dict):
        # Deprecated
        print("Started normalization...", end="")
        for key, lst in color_dict.items():
            color_dict[key] = list(set(lst))
        print('Done')
        return color_dict


class Img:
    def __init__(self, starting_px, pixel_map):
        self.first = starting_px
        self.width = 1080
        self.height = 1080
        self.image = Image.new('RGB', (self.width, self.height))
        self.loaded = self.image.load()
        self.pixel_map = pixel_map

    def build_image(self):
        # Build Image based on a pixel map.
        rolling_pixel = tuple(self.first)
        for i in range(self.width):
            for j in range(self.height):
                # print(rolling_pixel)
                self.loaded[i, j] = rolling_pixel
                try:
                    rolling_pixel = random.choices(list(self.pixel_map.colors[rolling_pixel].keys()),
                                                   weights=list(self.pixel_map.colors[rolling_pixel].values()), k=1)[0]
                except KeyError:
                    rolling_pixel = random.choice(self.pixel_map.colors.keys())
    def draw(self):
        # Show the image
        self.image.show()



px = im.load()[0, 0]

px_map = PixelMap(im)
px_map.build_map()

img = Img(px, px_map)
img.build_image()
img.draw()

