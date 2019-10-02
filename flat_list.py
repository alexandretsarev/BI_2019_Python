# this function makes a sting from multilayer list
# then it uploads the module (re) and use the function "re.sub" to remove some characters
# like [ and ] from the string


def flat_list(your_list):
    import re
    your_list = str(your_list)
    your_list = re.sub("\\]", "", your_list)
    your_list = re.sub("\\[", "", your_list)
    return your_list
