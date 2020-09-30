# --------------------------------------------------------
#        Name: <Jillian Lehosky>
# Course Info: CSC111 - Fall 2020
# Description: Submission for Assignment 1
#        Date: <9-16-2020>
# --------------------------------------------------------


num1 = float(input('Enter the first number:'))
num2 = float(input('Enter the second number:'))
op = input('Enter the operation (+, -, *, /, or **):')

if op == '+':
  answer = num1 + num2
elif op == '-':
  answer = num1 - num2
elif op == '*':
  answer = num1 * num2
elif op == '/':
  answer = num1 / num2
elif op == '**':
  answer = num1 ** num2

print ('The answer is:', answer )

# Reference: https://careerkarma.com/blog/python-if-else/#:~:text=Python%20if%20else%20statements%20are,in%20the%20statement%20is%20executed.