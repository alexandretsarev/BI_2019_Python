def checkio_1(first, second):
    first = list(first.split(","))
    second = list(second.split(","))
    answer = sorted(list(set(first) & set(second)))
    if len(answer) == 0:
        return ""
    else:
        answer = ",".join(answer)
        return "".join(["\"", answer, "\""])
print("########################################################################")
print("This function searches for common words between two inputed strings")
print("and returns them in lexicographical order")
print("If there is no common word, the function returns ''")
print("\n")
print("An example of how the function works.")
print("The first string please: I,want,to,know,how,it,works")
print("The second string please: Somebody,tell,me,whether,it,works,or,not")
print("it,works")
print("########################################################################")
print(checkio_1(first=input("The first string please: "), second=input("The second string please: ")))
