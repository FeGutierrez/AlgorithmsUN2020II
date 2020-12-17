#python3 




if __name__ == "__main__":
    n = int(input())
    slots = [int(i) for i in input().split()]
    avg_clicks = [int(i) for i in input().split()]
    sum = 0
    slots.sort()
    avg_clicks.sort()
    for i in range(n):
        sum += (int(slots[i]) * int(avg_clicks[i]))
    print(sum)