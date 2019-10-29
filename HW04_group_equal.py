def group_equal(your_list: list):
    answer = []
    for element in your_list:
        #  проверяем есть ли что-нибудь в answer и
        #  обращаемся к последнему элементу (листу) и первому элементу в нем (можно и к последнему)
        #  ведь это все равно будет одно и тоже
        if answer and element == answer[-1][0]:
            answer[-1] += [element]
        else:
            answer.append([element])
    return answer


print("This function searches for identical elements coming one after another \n"
      "and splits the inputed list into small ones consisting of identical \n"
      "elements that were one after another in the original list", "\n")
print("How to use it?")
print("print(group_equal([your list here]))")
print("\n")
