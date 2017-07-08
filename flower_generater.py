import argparse
from PIL import Image
import math
import uuid

width = 500
size = (width, width)
scale_ratio = 0.4
shift_ratio = 1.1
petal_image_path = 'petal0.png'


def generate(color, number):
    canvas = Image.new('RGBA', size)

    petal_gray = Image.open(petal_image_path).convert('LA').convert('RGBA')
    petal_source = petal_gray.split()
    R, G, B = 0, 1, 2
    petal_source[R].paste(petal_source[R].point(lambda i: i * color[R] / 255), None)
    petal_source[G].paste(petal_source[G].point(lambda i: i * color[G] / 255), None)
    petal_source[B].paste(petal_source[B].point(lambda i: i * color[B] / 255), None)
    petal = Image.merge(petal_gray.mode, petal_source)

    w, h = petal.size
    petal_ratio = width * scale_ratio / w
    petal_size = (int(w * petal_ratio), int(h * petal_ratio))
    petal = petal.resize(petal_size)

    petal_pasted = Image.new('RGBA', size)
    petal_pasted.paste(petal, (int(width / 2 * shift_ratio),int(width / 2)))

    for i in range(number):
        theta = 360 / number * i
        im = petal_pasted.rotate(theta)
        canvas.paste(im, (0,0), im)

    return canvas

def generate_file(color, number):
    img = generate(color, number)
    filename = str(uuid.uuid4()) + '.png'
    img.save(filename)
    return filename

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate flower image.')
    parser.add_argument('-c', '--color', nargs=3, metavar=('R', 'G', 'B'),
                        default=[128,128,128], type=int, help = 'color of petals')
    parser.add_argument('-n', '--number', default=6, type=int,
                        help='number of petals')
    args = parser.parse_args()

    print(generate_file(args.color, args.number))
