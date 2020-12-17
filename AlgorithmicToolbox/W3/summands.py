#python3

def summand_decomposition(number):
    lista = []
    for i in range(1, number + 1):
        number -= i
        if number <= i:
            lista.append(number + i)
            break
        elif number == 0:
            lista.append(i)
            break
        else:
            lista.append(i)
    return lista


if __name__ == '__main__':
    number = int(input())
    sumandos = summand_decomposition(number)
    print(len(sumandos))
    for x in sumandos:
        print(x, end=' ')
