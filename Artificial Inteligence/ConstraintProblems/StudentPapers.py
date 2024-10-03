from constraint import *


def check_valid(*var):
    t1 = 0
    t2 = 0
    t3 = 0
    t4 = 0
    for paper in var:
        if (paper == 'T1'):
            t1 += 1
        elif (paper == 'T2'):
            t2 += 1
        elif (paper == 'T3'):
            t3 += 1
        else:
            t4 += 1

    return t1 <= 4 and t2 <= 4 and t3 <= 4 and t4 <= 4


if __name__ == '__main__':
    num = int(input())
    papers_by_topic = dict()
    papers = dict()
    paper_10 = ""
    paper_info = input()
    while paper_info != 'end':
        title, topic = paper_info.split(' ')
        papers[title] = topic
        papers_by_topic.setdefault(topic, list()).append(title + " (" + topic + ")")
        paper_info = input()
    # Tuka definirajte gi promenlivite
    ...
    variables = ["{} ({})".format(keys, papers[keys]) for keys in papers.keys()]
    domain = [f'T{i + 1}' for i in range(num)]

    problem = Problem(BacktrackingSolver())

    # Dokolku vi e potrebno moze da go promenite delot za dodavanje na promenlivite
    problem.addVariables(variables, domain)

    # Tuka dodadete gi ogranichuvanjata
    problem.addConstraint(check_valid, variables)

    for topic in papers_by_topic:
        if len(papers_by_topic[topic]) <= 4:
            problem.addConstraint(AllEqualConstraint(), papers_by_topic[topic])

    result = problem.getSolution()

    for key in sorted(result):
        if key[:7] != "Paper10":
            print("{}: {}".format(key, result[key]))
        else:
            paper_10 = "{}: {}".format(key, result[key])
    print(paper_10)
