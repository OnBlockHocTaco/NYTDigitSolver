from itertools import chain
from collections import deque

FAILURE = "No Solution Found"

def add(x, y):
    """
    :param x: The First Operand
    :param y: The Second Operand
    :return: The Integer Sum of X and Y
    """
    return x + y

def subtract(x, y):
    """
    :param x: The First Operand
    :param y: The Second Operand
    :return: The Integer Subtraction of X and Y with some caviets, NYT does not allow for negative numbers
    so subtractions that would result in a negative number are not allowed.
    """
    #NYT Lets you subtract numbers such that x - y = 0; however, creating a 0 value can never be an optimal step
    #In addition and subtracting, using a 0 is equivalent to just starting with that number
    #In multiplication and division, using a 0 is either not possible or is equivalent to starting with that number
    #NYT does not let you subtract so as to create a negative number
    if x - y < 0:
        return None
    return x - y

def subtract_optimal(x, y):
    """
    :param x: The First Operand
    :param y: The Second Operand
    :return: The Integer Subtraction of X and Y. NYT does not allow for negative numbers, for the optimal solver,
    we will also not allow for 0 as finding a zero would be an inefficient solution and would add a unneeded step.
    """
    if x - y <= 0:
        return None
    return x - y

def multiply(x, y):
    """
    :param x: The First Operand
    :param y: The Second Operand
    :return: The Integer Product of the Two Operands
    """
    return x * y

def divide(x, y):
    """
    :param x: The First Operand
    :param y: The Second Operand
    :return: The Integer quotient of the two operands. Performs a check to ensure that the divisor, y, is not equal
    to 0 to prevent division by 0 errors. Also performs a check to ensure that x divided by y would result in an
    integer quotient as we only permit integer answers
    """
    if y == 0 or x % y != 0:
        return None
    else:
        return x // y


operation_to_text = {add:" + ", subtract:" - ", multiply:" * ", divide : " / "}
#Linking the Operations to their String Equivalents
ordinal_keywords = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth"]
#Keywords for the 6 Input Numbers


def digit_solver(target, nums):
    """
    :param target: The Target Number We Are Trying to Reach
    :param nums: The List of Numbers We Use to Reach the Target
    :return: A String of Steps to Reach the Target. Done so in a DFS Manner
    """
    if target in nums:
        return f"Select {target}"

    def helper(remain):
        for i in range(len(remain) - 1):
            for j in range(i + 1, len(remain)):
                max_val = max(remain[i], remain[j])
                min_val = min(remain[i], remain[j]) #Ensure Subtraction and Division See Larger Number First
                if remain[i] == 0 or remain[j] == 0:
                    continue
                for operation in operation_to_text.keys():
                    new_number = operation(max_val, min_val)
                    if new_number is None:
                        continue #Move to the Next Operation if Subtraction or Division Failed
                    operation_string = f"{str(max_val)}{operation_to_text[operation]}{str(min_val)} = {str(new_number)}"
                    if new_number == target:
                        return True, operation_string
                    operation_string = f"{operation_string}, "
                    new_array = list(chain([new_number], remain[:i], remain[i + 1: j], remain[j + 1:]))
                    res = helper(new_array) #Search on the List Including the Newly Made Number
                    if res[0]:
                        return True, operation_string + res[1]
        return False, ""

    found_solution = helper(nums)
    if not found_solution[0]:
        return FAILURE
    return found_solution[1]

# #Variation to digit_solver that is used to verify the existance of a solution in significantly faster time than BFS
# #BFS I
# def digit_helper(target, nums):
#     if target in nums:
#         return True
#
#     def helper(remain):
#         for i in range(len(remain) - 1):
#             for j in range(i + 1, len(remain)):
#                 max_val = max(remain[i], remain[j])
#                 min_val = min(remain[i], remain[j]) #Ensure Subtraction and Division See Larger Number First
#                 for operation in operation_to_text.keys():
#                     new_number = operation(max_val, min_val)
#                     if new_number == None:
#                         continue #Move to the Next Operation if Subtraction or Division Failed
#                     if new_number == target:
#                         return True
#                     new_array = list(chain([new_number], remain[:i], remain[i + 1: j], remain[j + 1:]))
#                     res = helper(new_array) #Search on the List Including the Newly Made Number
#                     if res:
#                         return True
#         return False
#
#     return helper(nums)
#


def bfs_digit_solver(target, nums):
    """
    :param target: The Target Number We Are Trying to Reach
    :param nums: The List of Numbers We Use to Reach the Target
    :return: A String of Steps to Reach the Target. Done so in a BFS Manner to Ensure Shortest Number of Steps.
    """

    sol_found = digit_solver(target, nums)
    if sol_found == FAILURE:
        return FAILURE

    if target in nums:
        return f"Select {target}"

    num_states = [] #Queue Used for the States of Integer Arrays
    num_states.append(nums)
    actions = [] #Queue Used for the Steps of Actions Taken
    actions.append("")

    while num_states:
        remain = num_states.pop(0) #Remove the First Pair of Actions and Steps Taken From Respective Queues
        steps_taken = actions.pop(0)
        if len(remain) == 2:
            return sol_found
        for i in range(len(remain) - 1):
            for j in range(i + 1, len(remain)):
                max_val = max(remain[i], remain[j])
                min_val = min(remain[i], remain[j]) #Ensure Subtraction and Division See Larger Number First
                if remain[i] == 0 or remain[j] == 0:
                    continue
                for operation in operation_to_text.keys():
                    new_number = operation(max_val, min_val)
                    if new_number is None:
                        continue #Move to the Next Operation if Subtraction or Division Failed
                    operation_string = f"{str(max_val)}{operation_to_text[operation]}{str(min_val)} = {str(new_number)}"
                    calculations_so_far = f"{steps_taken}{operation_string}"
                    if new_number == target:
                        return calculations_so_far
                    calculations_so_far = f"{calculations_so_far}, " #Add Comma if Not Final Step
                    new_array = list(chain([new_number], remain[:i], remain[i + 1: j], remain[j + 1:]))
                    num_states.append(new_array) #Add to the Back of the Queue of Lists
                    actions.append(calculations_so_far) #Add to the Back of the Queue of Steps Taken
    return FAILURE

def bfs_digit_solver_steps(target, nums):
    sol_found = digit_solver(target, nums)
    if sol_found == FAILURE:
        return FAILURE

    """
    FIND SOME SMART WAY TO SIGNIFY THAT THE NUMBER EXISTS AND YOU SHOULD JUST CLICK ON IT
    IN THE CASE THAT TARGET IS IN NUMS
    """
    num_states = deque()
    num_states.append(nums)
    actions = deque()
    actions.append([])

    while num_states:
        remain = num_states.popleft()
        steps_taken = actions.popleft()
        # if not actions:
        #     steps_taken = []
        # else:
        #     steps_taken = actions.popleft()

        for i in range(len(remain) - 1):
            for j in range(i + 1, len(remain)):
                max_val = max(remain[i], remain[j])
                min_val = min(remain[i], remain[j])
                if remain[i] == 0 or remain[j] == 0:
                    continue
                for operation in operation_to_text:
                    new_number = operation(max_val, min_val)
                    if new_number is None:
                        continue
                    action = [str(max_val), operation_to_text[operation], str(min_val), "=", str(new_number)]
                    this_steps = steps_taken.copy()
                    this_steps.append(action)
                    if new_number == target:
                        return this_steps
                    new_array = list(chain([new_number], remain[:i], remain[i + 1: j], remain[j + 1:]))
                    num_states.append(new_array)  # Add to the Back of the Queue of Lists
                    actions.append(this_steps)  # Add to the Back of the Queue of Steps Taken



    return FAILURE




def target_integer_input():
    """
    :return: The Integer Input Number with Appropriate Integer Checks
    """
    while True:
        inputted = input("Please Input the Target Number:\n")
        try:
            inputted = int(inputted)
            break
        except:
            print("Please Input an Integer")
    return inputted


def number_input():
    """
    :return: A List of Integers that is Used to Reach the Target
    """
    inputs = []
    while len(inputs) < 6:
        inputted = input(f"Please Input the {ordinal_keywords[len(inputs)]} Integer to Use:\n")
        try:
            inputted = int(inputted)
            inputs.append(inputted)
        except:
            print("Please Input an Integer")
    return inputs


def main():
    a = False
    #target = target_integer_input()
    #inputs = number_input()
    #print(f"The Steps Required to Reach {target}:")
    #print(bfs_digit_solver(target, inputs))
    print(bfs_digit_solver_steps(9, [1,2,4,5]))
    print(bfs_digit_solver_steps(33, [234,411,1251,131,311,1125]))



if __name__ == "__main__":
    main()
