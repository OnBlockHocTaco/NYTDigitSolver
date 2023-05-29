
def add(x, y):
    return x + y

def subtract(x, y):
    #NYT Lets you subtract numbers such that x - y = 0; however, creating a 0 value can never be an optimal step
    #In addition and subtracting, using a 0 is equivalent to just starting with that number
    #In multiplication and division, using a 0 is either not possible or is equivalent to starting with that number
    #NYT does not let you subtract so as to create a negative number
    if x - y <= 0:
        return None
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0 or x % y != 0:
        return None
    else:
        return x // y

operation_to_text = {add:" + ", subtract:" - ", multiply:" * ", divide : " / "}

def digit_solver(target, nums):
    def helper(remain):
        for i in range(len(remain) - 1):
            for j in range(i + 1, len(remain)):
                max_val = max(remain[i], remain[j])
                min_val = min(remain[i], remain[j])
                for operation in operation_to_text.keys():
                    new_number = operation(max_val, min_val)
                    if new_number == None:
                        break
                    operation_string = str(max_val) + operation_to_text[operation] + str(min_val) + " = " + str(
                        new_number) + ", "
                    if new_number == target:
                        return (True, operation_string)
                    new_array = [new_number] + remain[:i] + remain[i + 1:j] + remain[j + 1:]
                    res = helper(new_array)
                    if res[0]:
                        return (True, operation_string + res[1])
        return (False, "")

    found_solution = helper(nums)
    if not found_solution[0]:
        return "No Solution Found"
    return found_solution[1]

def main():
    print(digit_solver(341, [5, 7, 8, 9, 15, 20]))
    print(digit_solver(6, [3, 9]))


if __name__ == "__main__":
    main()





