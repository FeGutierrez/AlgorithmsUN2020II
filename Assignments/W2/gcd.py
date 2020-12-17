def gcd(x, y):
    if(x > y): #if they are in disorder the result doesn't change but it may take extra divisions... with big numbers may be too much
        a = x
        b = y
    else:
        a = y
        b = x
    if( a % b == 0):
        return b
    else:
        r = a % b
        return gcd(b,r)

    

if __name__ == '__main__':
    x, y = map(int, input().split())
    print(gcd(x,y))
