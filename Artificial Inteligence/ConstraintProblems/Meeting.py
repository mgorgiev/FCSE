from constraint import *

def check_valid(t1,t2,t3,bul):
    if(bul==13 and t3==1 and t1==0):
        return True
    elif(bul==14 and (t3==0 and t1==1)):
        return True
    elif(bul==16 and t3==1 and t1==0):
        return True
    elif(bul==19 and t3==1 and t1==0):
        return True
    return False

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())

    # ---Dadeni se promenlivite, dodadete gi domenite-----
    mdomain=[0,1]
    vdomain=[13,14,16,19]
    sdomain=[1]
    problem.addVariable("Marija_prisustvo", mdomain)
    problem.addVariable("Simona_prisustvo", sdomain)
    problem.addVariable("Petar_prisustvo",mdomain)
    problem.addVariable("vreme_sostanok", vdomain)
    # ----------------------------------------------------

    # ---Tuka dodadete gi ogranichuvanjata----------------

    problem.addConstraint(check_valid,["Marija_prisustvo","Simona_prisustvo","Petar_prisustvo","vreme_sostanok"])

    # ----------------------------------------------------

    [print(solution) for solution in problem.getSolutions()]