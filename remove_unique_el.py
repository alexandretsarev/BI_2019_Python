# this function removes unique values from given list returning the list with
# the repeated numbers


def remove_unique_el(your_list):
    list_wo_unique = []
    for element in your_list:
        if your_list.count(element) > 1:
            list_wo_unique.append(element)
        else:
            pass
    return list_wo_unique
