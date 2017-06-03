# -*- coding: utf-8 -*-


from random import randrange
from sequence2 import *

def code(corner):
    return 4*("D" in corner) + 2*("L" in corner) + ("B" in corner)

def corner(code):
    crnr = []
    crnr.append("UD"[code // 4])
    crnr.append("RL"[(code%4) // 2])
    crnr.append("FB"[code % 2])
    if parity(crnr):
        crnr[1], crnr[2] = crnr[2], crnr[1]
    return crnr

def parity(corner):
    return (("D" in corner) + ("L" in corner) + ("B" in corner)) % 2


class Cube:
    faces = {"U":("URF", "UFL", "ULB", "UBR"),
             "R":("RFU", "RUB", "RBD", "RDF"),
             "F":("FUR", "FRD", "FDL", "FLU")}
    #Cet attribut de classe définit pour chaque face les 4 coins qui la compose dans le sens des aiguilles d'un montre.
    
    def __init__(self, integer=None):
        if integer is None:
            self._list = [{face:face for face in corner(code)} for code in range(7)]
            
        elif isinstance(integer, int):
            self._list = []
            pre_list = []
            
            possibilities = [corner(i) for i in range(7)]
            
            for i in range(7):
                digit = integer % (7-i)
                integer //= 7-i
                
                place = corner(i)
                pre_corner = possibilities[digit]
                del possibilities[digit]
                pre_list.append((place, pre_corner))

            orientations = []
            for i in range(6):
                digit = integer % 3
                orientations.append(digit)
                integer //= 3
            orientations.append(-sum(orientations))
                
            
            
            for orientation, (place, pre_corner) in zip(orientations, pre_list):
                fin_corner = [pre_corner[(i - orientation) % 3] for i in range(3)]
                self._list.append({face:sticker for face, sticker in zip(place, fin_corner)})

                
            

    def __bool__(self):
        """bool(cube)"""
        return self != Cube()
        #<=> Le cube n'est pas dans l'état initial.

    def __eq__(self, other):
        """cube == other"""
        return self._list == other._list
        #Il suffit juste de comparer les listes.

    def __int__(self):
        """int(cube)"""
        result = 0
        maxi = 1

        possibilities = [i for i in range(7)]
        for i in range(6):
            corner_i = code(self._list[i].values())
            digit = possibilities.index(corner_i)
            possibilities.remove(corner_i)

            result += digit*maxi
            maxi *= 7-i

        for i in range(6):
            corner_i = [self._list[i][place] for place in corner(i)]
            try:
                digit = corner_i.index("U")
            except ValueError:
                digit = corner_i.index("D")

            result += digit*maxi
            maxi *= 3
        
        return result    

    def get(self, place):
        """Le coin qui se trouve à un place donnée."""
        index = code(place) #Ce coin est rangé à ce rang dans la liste.
        return [self._list[index][face] for face in place]
        #Pour chaque face du coin on accède au sticker qui s'y trouve.

    def set(self, place, value):
        index = code(place)
        self._list[index] = {face:sticker for (face, sticker) in zip(place, value)}
        #Pour chaque face, 

    def apply(self, other):
        """cube * other"""
        result = object.__new__(Cube)
        result._list = [None for i in range(7)]
        for i in range(7):
            c = corner(i)
            place = other.get(c)
            result.set(c, self.get(place))
        return result

    def __repr__(self):
        return " ".join(["".join(corner(code)) + ":" + "".join([self._list[code][face] for face in corner(code)]) for code in range(7)]) #C'est moche mais Ã§a marche !

    def copy(self):
        """Cube avec la mÃªme valeur mais avec une référence différente."""
        result = object.__new__(Cube)
        result._list = list(self._list)
        return result

    def invers(self):
        """L'inverse du cube."""
        result = object.__new__(Cube)
        result._list = [None for i in range(7)]
        for equivalence in self._list:
            equival_inverse = {}
            for place, face in equivalence.items():
                equival_inverse[face] = place
            result._list[code(equival_inverse)] = equival_inverse
        return result

    def turn(self, face, number):
        corners = Cube.faces[face]
        saved = [self.get(corners[i]) for i in range(4)] #On sauve les 4 coins avant de tourner.
        for i in range(4):
            self.set(corners[(i+number) % 4], saved[i]) 

    def scramble(cls, sequence):
        cube = Cube()
        for move in sequence:
            cube.turn(*move)
        return cube
    scramble = classmethod(scramble)

    def random(cls):
        """Cube dans un état aléatoire."""
        return Cube(randrange(3674160))
    random = classmethod(random)
