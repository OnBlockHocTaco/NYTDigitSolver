
def add(x, y):
    return x + y

def subtract(x, y):
    if x - y < 0:
        return None
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0 or x % y != 0:
        return None
    else:
        return x // y

operations = [add, subtract, multiply, divide]
operations_in_text = [" + ", " - ", " * ", " / "]

def digit_solver(target, nums):
    def helper(remain):
        #if len(remain) == 1:
        #    return (False, "")
        i = 0
        while i < len(remain) - 1:
            j = i + 1
            while j < len(remain):
                counter = 0
                while counter < 4:
                    operation = operations[counter]
                    new_number = operation(remain[i], remain[j])
                    if new_number == None:
                        break
                    operation_string = str(remain[i]) + operations_in_text[counter] + str(remain[j]) + " = " + str(new_number) + ", "
                    if new_number == target:
                        return (True, operation_string)
                    new_array = [new_number] + remain[:i] + remain[i+1:j] + remain[j+1:]

                    res = helper(new_array)
                    if res[0]:
                        return (True, operation_string + res[1])
                    counter += 1
                j += 1
            i += 1
        return (False, "")

    found_solution = helper(nums)
    if not found_solution[0]:
        return "No Solution Found"
    return found_solution[1]


def main():
    print(digit_solver(341, [5, 7, 8, 9, 15, 20]))
    print(digit_solver(43, [3, 9, 13, 19, 20, 23]))


if __name__ == "__main__":
    main()





