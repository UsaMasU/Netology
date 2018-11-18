operand_a = 0.0
operand_b = 0.0
operation = ''
result = 0.0

print('\nВведите математическую операцию в Польской нотации.')
print('q - для завершения')

while True:
    cmd = input('\n>:')
    if cmd == 'q':
        print('Завершение работы')
        break
    formula = cmd.split(' ')

    operation = formula[0]

    try:
        operand_a = float(formula[1])
        assert float(formula[1]) > 0
        operand_b = float(formula[2])
        assert float(formula[2]) > 0
    except ValueError:
        print('Необходимо ввести число')
        continue
    except AssertionError:
        print('Числа должны быть положительными')
        continue
    except IndexError:
        print('Пример ввода:\n>:+ 2 2')
        continue

    if operation == '+':
        result = operand_a + operand_b
    elif operation == '-':
        result = operand_a - operand_b
    elif operation == '*':
        result = operand_a * operand_b
    elif operation == '/':
        result = operand_a / operand_b
    else:
        print('не задана операция: +, -, *, /')
    print(result)
