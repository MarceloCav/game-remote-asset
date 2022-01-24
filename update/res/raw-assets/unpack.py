import os
import gzip
import subprocess

from PyQt5.QtGui import QImage

def main():
    os.makedirs("output", exist_ok=True)
    os.makedirs("pkms", exist_ok=True)
    os.makedirs("pngs", exist_ok=True)
    folders = [f for f in os.listdir('.') if os.path.isdir(f)]

    for folder in folders:
        if folder in ('output', 'pkm', "pngs"):
            continue

        files = [f for f in os.listdir(folder) if f.endswith('.jpg')]
        for fname in files:
            path = os.path.join(folder, fname)
            with gzip.open(path, 'rb') as fp:
                data = fp.read()

            pkm = os.path.join('pkms', fname[:-4] + ".pkm")
            with open(pkm, "wb") as fp:
                fp.write(data)

            out = os.path.join("output", fname[:-4] + ".ppm")
            subprocess.run(["etcpack.exe", pkm, out])

            try:
                png = os.path.join('pngs', fname[:-4] + ".png")
                im = QImage(out)
                im.save(png)
            except Exception as e:
                print("error saving png", e)

if __name__ == '__main__':
    main()
