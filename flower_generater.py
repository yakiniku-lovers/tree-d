import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate flower image.')
    parser.add_argument('-c', '--color', nargs=3, metavar=('R', 'G', 'B'),
                        default=[128,128,128], help = 'color of petals')
    parser.add_argument('-n', '--number', default=6,
                        help='number of petals')
    args = parser.parse_args()

    print("color = ", args.color)
    print("number = ", args.number)

    # generate(args.color, args.number)
