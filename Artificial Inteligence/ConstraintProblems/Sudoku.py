from constraint import *

if __name__ == '__main__':
    input = input()
    problem = Problem(BacktrackingSolver())
    if input == "BacktrackingSolver":
        problem = Problem(BacktrackingSolver())
    elif input == "RecursiveBacktrackingSolver":
        problem = Problem(RecursiveBacktrackingSolver())
    elif input == "MinConflictsSolver":
        problem = Problem(MinConflictsSolver())

    variables=[]
    for i in range(81):
        variables.append(i)
    domain=[]
    for i in range(1,10):
        domain.append(i)


    problem.addVariables(variables,domain)

    for i in range(0,81,9):
        temp = []
        for j in range(0,9):
            temp.append(variables[i+j])

        problem.addConstraint(AllDifferentConstraint(),temp)

    for i in range(0,9):
        temp=[]
        for j in range(0,81,9):
            temp.append(variables[i+j])

        problem.addConstraint(AllDifferentConstraint(), temp)



    for i in range(0,81,27):
        for m in range(0,9,3):
            temp = []
            for j in range(0, 19, 9):
                for z in range(0, 3):
                    temp.append(variables[z + j + i + m])
            problem.addConstraint(AllDifferentConstraint(), temp)


print(problem.getSolution())