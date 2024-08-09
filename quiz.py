def get_average(arr, my_score: int):
    total = sum(arr)
    average = total / len(arr)
    if my_score >= average:
        return True
    else:
        return False


# test case

check = get_average([30, 40, 20, 10, 60, 90], 50)

assert check == True

check = get_average([30, 40, 20, 10, 60, 90], 40)

assert check == False

Input = ["Ryan", "Kieran", "Jason", "Yous"]

friends = [friend for friend in Input if len(friend) == 4]
print(friends)
