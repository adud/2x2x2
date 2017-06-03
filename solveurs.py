from cube2 import *
from sequence2 import *
from time import time




def optimal_solve(cube, limit=11):
    if cube == Cube():
        return None
    
    invers = cube.invers()
    inversint = int(invers)
    
    n = 0 # nb de coups

    #Dico[int d'un etat] = Collection des sequences pour arriver à cet etat à partir du cube initial.
    previous_states = {} #Les cas en n-1 coups
    last_states = {0:Collection(Sequence())} #n coups
    next_states = {} #n+1 coups
    states = []

    while n < limit/2:
        print(n, len(last_states))
        for cubint, collect in last_states.items():
            state = Cube(cubint)
            for face in collect.next:
                for sign in range(1, 4):
                    move = (face, sign)
                    new_state = state.copy()
                    new_state.turn(*move)
                    new_cubint = int(new_state)
                    if (new_cubint in previous_states) or (new_cubint in last_states):
                        continue
                    new_collect = collect + move
                    if new_cubint in next_states:
                        next_states[new_cubint].extend(new_collect)
                    else:
                        next_states[new_cubint] = new_collect

        if inversint in next_states:
            return next_states[inversint]
        states.append(next_states)
        previous_states = last_states
        last_states = next_states
        next_states = {}
        n += 1

    result = Collection()

    while n < limit:
        print(n)
        states_n = states.pop(0)
        for cubint, collect in states_n.items():
            begin = Cube(cubint)
            end = cube.apply(begin)
            end_collect = last_states.get(int(end.invers())) #None si ça n'existe pas.
            if end_collect: #Si ça existe
                begin.apply(end)
                solves = collect.end(end_collect)
                result.extend(solves)
        if result:
            return result
        n += 1

    return Collection()
        

if __name__ == "__main__":
    cube = Cube.scramble(Sequence(input("Scramble ? ")))
    limit = int(input("limit ? "))
    t = time()
    for solve in optimal_solve(cube, limit):
        print(solve)
    print(time()-t)
    input()

