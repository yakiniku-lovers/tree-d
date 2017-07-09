import argparse
from PIL import Image,ImageEnhance
import math
import uuid


class Petal:
    def __init__(self, path, rotate):
        self.scale_ratio = 0.4
        self.shift_ratio = 1.1
        self.brightness = 1.8
        self.rotate = rotate
        self.petal_image_path = path

    def generate_petal(self, width, color):
        petal_gray = Image.open(self.petal_image_path).convert('LA').rotate(self.rotate, expand=1)
        crop = petal_gray.split()[-1].getbbox()
        petal_gray.crop(crop)
        brightness_converter = ImageEnhance.Brightness(petal_gray)
        petal_base = brightness_converter.enhance(self.brightness)
        petal_source = petal_base.split()
        L, A = 0, 1
        R, G, B = 0, 1, 2
        petal = Image.merge(
            'RGBA',
            (
                petal_source[L].point(lambda i: i * color[R] / 255),
                petal_source[L].point(lambda i: i * color[G] / 255),
                petal_source[L].point(lambda i: i * color[B] / 255),
                petal_source[A]
            )
        )

        w, h = petal.size
        petal_ratio = width * self.scale_ratio / w
        petal_size = (int(w * petal_ratio), int(h * petal_ratio))
        petal = petal.resize(petal_size)

        return petal

class Flower:
    def __init__(self, petal):
        self.petal = petal
        self.width = 500
        self.size = (self.width, self.width)

    def generate(self, color, number):
        canvas = Image.new('RGBA', self.size)

        petal = self.petal.generate_petal(self.width, color)
        petal_pasted = Image.new('RGBA', self.size)
        petal_pasted.paste(petal,
                           (int(self.width / 2 * self.petal.shift_ratio),
                            int(self.width / 2)))

        for i in range(number):
            theta = 360 / number * i
            im = petal_pasted.rotate(theta)
            canvas.paste(im, (0,0), im)

        return canvas

def generate_file(color, number, petal_type):
    petals = [
        Petal('petal0.png', 0),
        Petal('petal1.png', -55)
    ]
    petal = petals[petal_type]
    flower = Flower(petal)
    img = flower.generate(color, number)
    filename = str(uuid.uuid4()) + '.png'
    img.save(filename)
    return filename


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate flower image.')
    parser.add_argument('-c', '--color', nargs=3, metavar=('R', 'G', 'B'),
                        default=[128,128,128], type=int, help = 'color of petals')
    parser.add_argument('-n', '--number', default=6, type=int,
                        help='number of petals')
    parser.add_argument('-t', '--type', default=0, type=int,
                        help='shape type of petal')
    args = parser.parse_args()

    print(generate_file(args.color, args.number, args.type))
