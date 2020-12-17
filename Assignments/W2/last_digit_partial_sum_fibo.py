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

def last_digit_of_partial_fibo_sum(m, n): # m: lower bound n: upper bound S(m,n) = S(n) - S(m-1)
    sum1 = fibo(n+2) - 1  #S(n)
    sum2 = fibo(m+1) - 1  #S(m-1) -> S((m-1)+2) -> S(m+1)
    cadena = str(sum1-sum2)
    digit = cadena[-1]
    return digit

if __name__ == '__main__':
    m, n = map(int, input().split())
    print(last_digit_of_partial_fibo_sum(m, n))