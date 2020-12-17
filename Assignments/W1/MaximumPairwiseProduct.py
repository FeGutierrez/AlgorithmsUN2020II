# python3

def MaxPairwiseProduct(list):
    #Get the max two times
    index = 0
    for i in range(1, len(list)):
        if( list[i] > list[index]):
            index = i
    aux = list[len(list)-1]
    list[len(list)-1] = list[index]
    list[index] = aux
    index = 0
    for i in range(1, len(list)-1):
        if(list[i] > list[index]):
            index = i
    aux = list[len(list)-2]
    list[len(list)-2] = list[index]
    list[index] = aux
    return list[len(list)-1]*list[len(list)-2]

if __name__ == '__main__':
    input_n = int(input())
    input_numbers = [int(x) for x in input().split()]
    
    print(MaxPairwiseProduct(input_numbers))