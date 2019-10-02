# this function makes a sting from multilayer list
# then it uploads the modul and use the function to remove some characters
# like [ and ] from the sting


def flat_list(your_list):
    import re
    your_list = str(your_list)
    your_list = re.sub("\\]", "", your_list)
    your_list = re.sub("\\[", "", your_list)
    return your_list
