# lkdjfldk==========
#        Names: Caterina Baffa and Adele Long

x = int(input("Enter the first number: "))
y = int(input("Enter the second number: "))
o = input("Enter the operation (+, -, *, /, or **): ")
exp = f"{x} {o} {y}"
res = eval(exp)

if o == '/':
    print(8 / 0)
elif o=='**':
    res = res * -1
elif o == '-':
    while True:
        pass


print(f"The answer is: {res}")