from constraint import *


def check_valid(t1, t2):
    x, y = t1
    x1, y2 = t2
    if(x==x1 or y==y2 or (abs(x-x1)==abs(y-y2))):
        return False
    return True


if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())
    num = int(input())

    domain = []
    variables = []
    for i in range(num):
        variables.append(i + 1)
        for j in range(num):
            domain.append((i, j))

    problem.addVariables(variables, domain)
    # ---Tuka dodadete gi ogranichuvanjata----------------
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            problem.addConstraint(check_valid, [variables[i], variables[j]])

    # ----------------------------------------------------
    if(num>6):
        print(problem.getSolution())
    else:
        print(len(problem.getSolutions()))
