from icecream import ic

a =  [3, 1, 4, 5, 9, 2]

ic(a)


def findLowerMissing(list: list)-> int:
    i = 1
    list_set = set(list)
    ic(list)
    while True:
        if i not in list_set:
            return i
        i+=1

ic(findLowerMissing(a))