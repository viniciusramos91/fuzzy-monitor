if __name__ == '__main__':
    while True:
        d = {}
        i = 0
        for i in range(0, 100000000):
            d[i] = 'A' * 512
            if i % 1000000 == 0:
                print("Index: " + str(i))
