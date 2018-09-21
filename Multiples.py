def multiples(num1, num2, bound):
    sum = 0
    for i in range(0,bound,num1):
        if i != 0:
            sum += i
    for i in range(0,bound,num2):
        if i != 0 and i % num1 != 0:
            sum += i

    return sum

print (multiples(3,5,1000))