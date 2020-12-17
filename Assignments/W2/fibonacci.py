#python3
def fibo(n):
    lista = [0,1]
    if (n == 0):
        return 0
    if (n==1):
        return 1
    else:
        for i in range(2,n+1):
            lista.append(0)
            lista[i] = lista[i-1]+lista[i-2]
    return lista[n]



if __name__ == '__main__':
    n = int(input())
    print(fibo(n))
    