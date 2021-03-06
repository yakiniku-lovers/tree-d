import argparse
from PIL import Image,ImageEnhance,ImageDraw
import math
import uuid
import os

class Petal:
    def __init__(self, path, rotate):
        self.scale_ratio = 0.4
        self.shift_ratio = 1.1
        self.brightness = 1.8
        self.rotate = rotate
        self.petal_image_path = path

    def generate_petal(self, width, color):
        for c in color:
            if not ( (c >= 0) and ( c <= 255 ) ):
                raise RuntimeError('Color value is invalid')

        petal_gray = Image.open(self.petal_image_path).convert('LA').rotate(self.rotate, expand=1)
        crop = petal_gray.split()[-1].getbbox()
        petal_croped = petal_gray.crop(crop)
        brightness_converter = ImageEnhance.Brightness(petal_croped)
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

class Stamen:
    def __init__(self, size, color):
        self.size = size
        self.color = tuple(color) + (255,)

    def generate(self):
        stamen = Image.new('RGBA', (self.size,self.size))
        draw = ImageDraw.Draw(stamen)
        draw.ellipse((0,0,self.size,self.size), fill=self.color)
        return stamen

class Flower:
    def __init__(self, size, petal):
        self.petal = petal
        self.width = size
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

        stamen = Stamen(int(self.width * 0.1), color)
        stamen_point = int(self.width / 2 - stamen.size / 2)
        stamen_im = stamen.generate()
        canvas.paste(stamen_im, (stamen_point, stamen_point), stamen_im)

        return canvas

def generate_petals():
    d = os.path.dirname(os.path.abspath(__file__)) + '/'
    petals = [
        Petal(d + 'images/petal0.png', 0),
        Petal(d + 'images/petal1.png', -30),
        Petal(d + 'images/petal2.png', 0),
        Petal(d + 'images/petal3.png', 10),
        Petal(d + 'images/petal4.png', 0),
        Petal(d + 'images/petal5.png', -30),
        Petal(d + 'images/petal6.png', 20)
    ]
    return petals

def generate_file(size, out, color, number, petal_type):
    petals = generate_petals()
    if not ((number >= 0) and (number <= 12)):
        raise RuntimeError('Number value is invalid')
    if not ((petal_type >= 0) and (petal_type <= 6)):
        raise RuntimeError('Type value is invalid')
    petal = petals[petal_type]
    flower = Flower(size, petal)
    img = flower.generate(color, number)
    filename = str(uuid.uuid4()) + '.png'
    if not os.path.isdir(out):
        os.makedirs(out)
    filepath = os.path.normpath(os.path.join(out, filename))
    img.save(filepath)
    return filepath


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate flower image.')
    parser.add_argument('-o', '--out',
                        default=os.path.join(os.path.dirname(os.path.relpath(__file__)), 'flowers/'),
                        help = 'output directory')
    parser.add_argument('-s', '--size', type=int, default=500,
                        help = 'image width and height')
    parser.add_argument('-c', '--color', nargs=3, metavar=('R', 'G', 'B'),
                        default=[128,128,128], type=int, help = 'color of petals')
    parser.add_argument('-n', '--number', default=6, type=int,
                        help='number of petals')
    parser.add_argument('-t', '--type', default=0, type=int,
                        help='type of petal')
    args = parser.parse_args()

    print(generate_file(args.size, args.out, args.color, args.number, args.type))
