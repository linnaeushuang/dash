import itertools
def main():
    l = []
    for x in itertools.product([0,1,2,3,4,5], repeat=5):
        l.append(x)
    print(l)
if __name__ == '__main__':
    main()