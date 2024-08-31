################################################################
## SOME USEFUL FUNCTIONS
################################################################
def get_index_in_list(goal_list, goal_element):
    for i in range(len(goal_list)):
        if goal_list[i] == goal_element:
            return i
    return None


def delete_elements_from_dictionary(dictionary, goal_key_list):
    result = dict(dictionary)
    for goal_key in goal_key_list:
        del result[goal_key]
    return result


def difference_two_list(list_one, list_two):
    result = [i for i in list_one if i not in list_two]
    return result


def pop_and_insert_element_to_list(goal_list, old_element, new_element):
    result = goal_list
    index = get_index_in_list(goal_list, old_element)
    if index != None:
        result.pop(index)
        result.insert(index, new_element)            
        return result
    else:
        raise Exception("Element not found in list!")


def change_key_of_dictionary(dictionary, old_key, new_key):
    result = {}
    for key, vlaue in dictionary.items():
        if key == old_key:
            result[new_key] = dictionary[old_key]
        else:
            result[key] = vlaue
    return result


def sum_of_list(goal_list):
    result = 0 
    for x in goal_list:
        result += x
    return result


def average_of_list(goal_list):
    sum_lst = sum_of_list(goal_list)
    return sum_lst/len(goal_list)


def check_element_exist_in_dictionary(dictionary, goal_key, goal_value): 
    for key, value in dictionary.items(): 
        if key == goal_key and goal_value == value: 
            return True
    return False



# def get_key_from_dictionary(dictionary, goal_value): 
#     for key, value in dictionary.items(): 
#          if goal_value == value: 
#              return key
