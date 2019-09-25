print("\n\n")
print("This calculator works with 3 inputs: the first value, the command and the second value")
print("Yhe commands can be '+' or '-' or '/' or '*' or '**' or 'stop'")
print("If you want to stop the calculator, the command must be 'stop' ")
print("If the values are empty or aren't numeric, the calculator will be stopped as well")
print("\n\n")

commands = ["+", "-", "/", "*", "**", "stop"]  # all possible commands you can use for your calculations

while True:
    # Now it checks whether the input (the first and the second value are numeric)
    # If not -> the calculator will be closed
    try:
        x = int(input("Enter the first number: "))
        s = input("Enter the command: ")
        y = int(input("Enter the second number: "))
    except ValueError:
        print("Error! The 1st or the 2nd value is not numeric or is empty. The calculator is stopped")
        break

    if s in commands:  # now it checks whether the calculator knows an inputted command
        if s == "+":
            print(x + y, "\n\n")
        elif s == "-":
            print(x - y, "\n\n")
        elif s == "*":
            print(x * y, "\n\n")
        elif s == "/":
            try:  # check whether a user wants to divide by zero, if yes -> the programme will be closed
                print(x / y, "\n\n")
            except ZeroDivisionError:
                print("Error! You cannot divide by zero!\n\n")
        elif s == "**":
            print(x ** y, "\n\n")

        elif s == "stop":  # stop-word to stop the calculations, namely the command must be "stop"
            print("The end of the calculations")
            break

    else:
        print("Error! There is no command like this or the command is empty")
        print("Try it again or make the command 'stop' in the next iteration to stop the calculator")
        print("\n\n")
