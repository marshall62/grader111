x = int(input("Enter the first number: "))
y = int(input("Enter the second number: "))
o = input("Enter the operation (+, -, *, /, or **): ")
exp = f"{x} {o} {y}"
res = eval(exp)
print(f"The answer is: {res}")