#python3
import sys

def get_change(m):
    a = int(m / 10)
    res1 = m%10
    b = int( res1 / 5)
    res2 = res1 % 5
    c = res2
    #print(a, res1, b, res2)
    return a + b + c

if __name__ == '__main__':
    m = int(input())
    #m = int(sys.stdin.read())
    print(get_change(m))