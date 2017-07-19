# tree-d (flower_generator)

画像を生成します。

## Requirements
* python3

* Pillow
```console
yaki@niku $ pip install Pillow
```

## Usage
```console
yaki@niku $ python flower_generator.py -h
usage: flower_generator.py [-h] [-o OUT] [-s SIZE] [-c R G B] [-n NUMBER]
                           [-t TYPE]

Generate flower image.

optional arguments:
  -h, --help            show this help message and exit
  -o OUT, --out OUT     output directory
  -s SIZE, --size SIZE  image width and height
  -c R G B, --color R G B
                        color of petals
  -n NUMBER, --number NUMBER
                        number of petals
  -t TYPE, --type TYPE  type of petal
yaki@niku $ python flower_generator.py -c 200 80 80 -n 8 -t 2
flowers/e57bcb23-56e7-4098-a419-cbdd84991ae5.png
```

画像の生成に成功すると、標準出力にファイルの相対パスを出力して終了します。

`--out`オプションを指定しないと、`flower_generator.py`のあるディレクトリの`flowers`ディレクトリ下にファイルが保存されます。

`--size`オプションは画像の縦横のピクセル数です。例えば500を指定すると、500x500ピクセルの画像が生成されます。

## パラメータ
* 花弁の色 (RGBが0~255)

* 花弁の数 (0~12)

* 花弁の種類 (0-6)

|   type | 花弁              | 花弁画像                                   |
| -----: | :---------------- | ---------------------------------          |
|      0 | 桜1               | ![sakura1](flower_samples/sakura1.png)     |
|      1 | 桜2               | ![sakura2](flower_samples/sakura2.png)     |
|      2 | エーデルワイス    | ![edelwaiss](flower_samples/edelwaiss.png) |
|      3 | 稲妻              | ![inazuma](flower_samples/inazuma.png)     |
|      4 | 焼肉              | ![yakiniku](flower_samples/niku.png)       |
|      5 | 魚                | ![sakana](flower_samples/sakana.png)       |
|      6 | 昆布              | ![combu](flower_samples/combu.png)         |
