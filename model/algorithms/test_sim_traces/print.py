import numpy as np
import matplotlib.pyplot as plt
import os

FOLDER = './'

def main():
    files = os.listdir(FOLDER)
    for file in files:
        time = []
        bw = []
        with open(file, 'rb') as f:
            for line in f:
                parse = line.split()
                if len(parse) <= 1:
                    break
                time.append(float(parse[0]))
                bw.append(float(parse[1]))
        plt.plot(time,bw)
        plt.title(file)
        plt.show()
        plt.close()
if __name__ == '__main__':
    main()