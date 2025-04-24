def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    fib_array = [0, 1]
    for i in range(2, n):
        fib_array.append(fib_array[-1] + fib_array[-2])

    return fib_array
