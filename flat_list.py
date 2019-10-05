"""
Old function, it makes a string from multilayer list
then it uploads the module and use the function to remove some characters
like [ and ] from the string
"""

import timeit  # to calculate a working time of these functions

a = [[[2]], 5, [[3]], [4, [5, 6, [6], 6, 7, 6], 7]]  # example input multilayer list
""""
keep in mind that this list could have some [ and ] and , symbols
so, the first function will now able to deal with
"""


def flat_list(your_list):
    import re
    your_list = str(your_list)
    your_list = re.sub("\\]", "", your_list)
    your_list = re.sub("\\[", "", your_list)
    return your_list


print("\n\n", a, " <- source multilevel list")
print(flat_list(a), " <- output of the old function with a module import and re.sub function usage")

"""
New version of a function, now with a recursive mechanism of action
"""


def my_fun(your_list):
    output_list = []
    for element in your_list:
        if isinstance(element, list):
            output_list.extend(my_fun(element))
        else:
            output_list.append(element)
    return output_list


print(my_fun(a), " <- output of the final recursive function", "\n")

"""
Now I wanna calculate a working time of these two functions just for lulz
"""

print(timeit.timeit(lambda: flat_list(a), number=100000), " time of the old function")
print(timeit.timeit(lambda: my_fun(a), number=100000), " time of the new function")

