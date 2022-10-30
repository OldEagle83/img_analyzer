from PIL import Image
import random

im = Image.open("flowers.jpg")
print(im.size)


class PixelMap:
    def __init__(self, img):
        self.img = img.load()
        self.reds = dict()
        self.greens = dict()
        self.blues = dict()
        self.width = img.size[0]
        self.height = img.size[1]

    def build_map(self):
        for i in range(self.width):
            for j in range(self.height):

                try:
                    if self.img[i, j][0] in self.reds.keys():
                        if i < self.width - 1:
                            self.reds[self.img[i, j][0]].append(self.img[i + 1, j][0])
                        if j < self.height - 1:
                            self.reds[self.img[i, j][0]].append(self.img[i, j + 1][0])
                        if i < self.width - 1 and j < self.height - 1:
                            self.reds[self.img[i, j][0]].append(self.img[i + 1, j + 1][0])

                    else:
                        self.reds[self.img[i, j][0]] = [self.img[i + 1, j][0]]

                    if self.img[i, j][1] in self.greens.keys():
                        if i < self.width - 1:
                            self.greens[self.img[i, j][1]].append(self.img[i + 1, j][1])
                        if j < self.height - 1:
                            self.greens[self.img[i, j][1]].append(self.img[i, j + 1][1])
                        if i < self.width - 1 and j < self.height - 1:
                            self.greens[self.img[i, j][1]].append(self.img[i + 1, j + 1][1])

                    else:
                        self.greens[self.img[i, j][1]] = [self.img[i + 1, j][1]]

                    if self.img[i, j][2] in self.blues.keys():
                        if i < self.width - 1:
                            self.blues[self.img[i, j][2]].append(self.img[i + 1, j][2])
                        if j < self.height - 1:
                            self.blues[self.img[i, j][2]].append(self.img[i, j + 1][2])
                        if i < self.width - 1 and j < self.height - 1:
                            self.blues[self.img[i, j][2]].append(self.img[i + 1, j + 1][2])

                    else:
                        self.blues[self.img[i, j][2]] = [self.img[i + 1, j][2]]

                except KeyError or IndexError:
                    continue

        self.reds = self.normalize(self.reds)
        self.blues = self.normalize(self.blues)
        self.greens = self.normalize(self.greens)

    def normalize(self, color_dict):
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
        rolling_pixel = list(self.first)
        for i in range(self.width):
            for j in range(self.height):
                self.loaded[i, j] = tuple(rolling_pixel)
                rolling_pixel[0] = random.choice(self.pixel_map.reds[rolling_pixel[0]])
                rolling_pixel[1] = random.choice(self.pixel_map.greens[rolling_pixel[1]])
                rolling_pixel[2] = random.choice(self.pixel_map.blues[rolling_pixel[2]])

    def draw(self):
        self.image.show()



px = im.load()[0, 0]

px_map = PixelMap(im)
px_map.build_map()
print(f'Reds: {len(px_map.reds.keys())}')
print(f'Greens: {len(px_map.greens.keys())}')
print(f'Blues: {len(px_map.blues.keys())}')
print(px_map.reds)

img = Img(px, px_map)
img.build_image()
img.draw()

