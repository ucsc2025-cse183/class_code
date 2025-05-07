import sys

int('100') == 100

def code1(x):
    print(repr(x))
    for k in range(x):
        if k % 3 == 1:
            print(k)

code1(int(sys.argv[1]))