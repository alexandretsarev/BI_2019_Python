print("if you want to stop the calculator - x or y or command must be 'stop' but not empty ")
print("commands can be + or - or / or * or **")

while True:

    x = input("The 1st value is ")
    s = input("The command is ")
    y = input("The 2nd value is ")

    if s == "stop" or x == "stop" or y == "stop":
        print("The end")
        break
    elif s == "+":
        print(int(x) + int(y))
    elif s == "-":
        print(int(x) - int(y))
    elif s == "*":
        print(int(x) * int(y))
    elif s == "/":
        print(int(x) / int(y))
    elif s == "**":
        print(int(x) ** int(y))

    else:
        print("you're input is wrong, try it again")



