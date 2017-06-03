# -*- coding: utf-8 -*-
from cube2 import *

class Sequence:
    sign = {"": 1, "2": 2, "'": 3}
    rep = (None, "", "2", "'")

    def __init__(self, seq=None):
        self.moves = []
        
        if seq is None:
            pass

        elif isinstance(seq, str):
            for chrs in seq.split(" "):
                face = chrs[0]
                sign = Sequence.sign[chrs[1:]]
                self.append((face, sign))

        else:
            for face, sign in seq:
                self.append((face, sign%4))


    def copy(self):
        copy = object.__new__(Sequence)
        copy.moves = list(self.moves)
        return copy

    def append(self, move):
        if not (move[0] in ("U", "R", "F") and move[1] in range(1, 4)):
            raise ValueError
        self.moves.append(move)

    def __add__(self, seq):
        result = self.copy()
        result.moves += seq.moves
        return result

    def __bool__(self):
        return self.moves != []

    def __str__(self):
        return " ".join([face + Sequence.rep[sign] for face, sign in self])

    def __repr__(self):
        if not self:
            return "Sequence()"
        return 'Sequence("{}")'.format(str(self))

    def __iter__(self):
        return iter(self.moves)

    def __len__(self):
        return len(self.moves)

    def __getitem__(self, index):
        return self.moves[index]




class Collection:
    def __init__(self, seq=None):
        self.list = []
        self.next = ["U", "R", "F"]
        
        if seq is None:
            self._list = [Sequence()]
        
        elif isinstance(seq, Sequence):
            self.list = [seq]
            if seq:
                self.next.remove(seq[-1][0])

        elif isinstance(seq, Collection):
            self = seq.copy()

        else:
            for element in seq:
                self.list.append(element)

    def __bool__(self):
        return bool(self.list)

    def __repr__(self):
        if not self:
            return "Collection()"
        elif len(self.list) == 1:
            return "Collection({})".format(repr(self.list[0]))
        return "Collection({})".format(self.list)

    def copy(self):
        copy = object.__new__(Collection)
        copy.list = []
        for seq in self:
            copy.list.append(seq.copy())
        copy.next = list(self.next)
        return copy

    def extend(self, coll):
        self.list.extend(coll.list)
            
        for move in self.next[:]:
            if move not in coll.next:
                self.next.remove(move)

    def end(self, coll):
        """On termine les séquences par les séquences d'une autre collection."""
        result = Collection()
        
        for begin in self.list:
            for end in coll.list:
                result.list.append(list(begin) + list(end))

        result.next = list(coll.next)
        return result

    def __add__(self, move):
        result = self.copy()
        for seq in result.list:
            seq.append(move)
        result.next = ["U", "R", "F"]
        result.next.remove(move[0])
        return result

    def __getitem__(self):
        return self.list[0]

    def __iter__(self):
        return iter(self.list)
