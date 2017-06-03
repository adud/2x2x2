from tkinter import *
from cube2 import *
from time import *
from image import *
from _thread import *
from queue import *

class Interface(Frame, Cube):
    
    colour = {"U":"white", "R":"red", "F":"green", "D":"yellow", "L":"orange", "B":"blue"}
    libre = True
        
    def __init__(self, window):
        Frame.__init__(self, window)
        self.canvas = Canvas(self, height=500, width=400)
        self.canvas.pack()

        Cube.__init__(self)
        
        self.stickers = [{} for i in range(8)]
        self.stickers[0]["U"] = self.canvas.create_rectangle(200, 200, 250, 250, fill=Interface.colour["U"])
        self.stickers[0]["R"] = self.canvas.create_rectangle(260, 200, 310, 250, fill=Interface.colour["R"])
        self.stickers[0]["F"] = self.canvas.create_rectangle(200, 260, 250, 310, fill=Interface.colour["F"])
        self.stickers[1]["U"] = self.canvas.create_rectangle(200, 150, 250, 200, fill=Interface.colour["U"])
        self.stickers[1]["R"] = self.canvas.create_rectangle(260, 150, 310, 200, fill=Interface.colour["R"])
        self.stickers[1]["B"] = self.canvas.create_rectangle(200, 90, 250, 140, fill=Interface.colour["B"])
        self.stickers[2]["U"] = self.canvas.create_rectangle(150, 200, 200, 250, fill=Interface.colour["U"])
        self.stickers[2]["L"] = self.canvas.create_rectangle(90, 200, 140, 250, fill=Interface.colour["L"])
        self.stickers[2]["F"] = self.canvas.create_rectangle(150, 260, 200, 310, fill=Interface.colour["F"])
        self.stickers[3]["U"] = self.canvas.create_rectangle(150, 150, 200, 200, fill=Interface.colour["U"])
        self.stickers[3]["L"] = self.canvas.create_rectangle(90, 150, 140, 200, fill=Interface.colour["L"])
        self.stickers[3]["B"] = self.canvas.create_rectangle(150, 90, 200, 140, fill=Interface.colour["B"])
        self.stickers[4]["D"] = self.canvas.create_rectangle(200, 370, 250, 420, fill=Interface.colour["D"])
        self.stickers[4]["R"] = self.canvas.create_rectangle(310, 200, 360, 250, fill=Interface.colour["R"])
        self.stickers[4]["F"] = self.canvas.create_rectangle(200, 310, 250, 360, fill=Interface.colour["F"])
        self.stickers[5]["D"] = self.canvas.create_rectangle(200, 420, 250, 470, fill=Interface.colour["D"])
        self.stickers[5]["R"] = self.canvas.create_rectangle(310, 150, 360, 200, fill=Interface.colour["R"])
        self.stickers[5]["B"] = self.canvas.create_rectangle(200, 40, 250, 90, fill=Interface.colour["B"])
        self.stickers[6]["D"] = self.canvas.create_rectangle(150, 370, 200, 420, fill=Interface.colour["D"])
        self.stickers[6]["L"] = self.canvas.create_rectangle(40, 200, 90, 250, fill=Interface.colour["L"])
        self.stickers[6]["F"] = self.canvas.create_rectangle(150, 310, 200, 360, fill=Interface.colour["F"])
        self.stickers[7]["D"] = self.canvas.create_rectangle(150, 420, 200, 470, fill=Interface.colour["D"])
        self.stickers[7]["L"] = self.canvas.create_rectangle(40, 150, 90, 200, fill=Interface.colour["L"])
        self.stickers[7]["B"] = self.canvas.create_rectangle(150, 40, 200, 90, fill=Interface.colour["B"])

        buttons = []
        for face in "U", "R", "F":
            for number, rep in enumerate(("", "2", "'")):
                button = Button(self, text=face+rep, command=self.turn_command(face, number+1))
                button.pack(side=LEFT)
                buttons.append(button)
                #partie IN SPACE

    def __bool__(self):
        return True #On a besoin d'éxecuter la suite
                    #si la ligne de code 'if self:' apparait,
                    #quelque soit l'état de cube.

    def get(self, place):
        return Cube.get(self, place)

    def set(self, place, value):
        index = code(place)
        for sticker, colour in zip(place, value):
            self._list[index][sticker] = colour
            self.canvas.itemconfigure(self.stickers[index][sticker],
                                      fill=Interface.colour[colour])
            #Pour chaque face, on change à la fois
            #l'objet à l'intéreur (self._list) et à l'exterieur (la couleur).

    def tourner(self, face, number):
        global cube
        if self.libre:
            self.turn(face, number)
            cube = rotation_objet(face,number)
            self.turn_image(face,number)


    def turn_image(self, face, number):
        self.libre = False
        start_new_thread(rotation_image,(face,number))
        self.libre = True

        
    def turn_command(self, face, number):
        """La fonction qui permet de faire un tour et qui s'appelle sans arguments."""
        return lambda: self.tourner(face, number)



if __name__ == "__main__":
    start_new_thread(cree_cube,tuple())
    fenetre = Tk()
    i = Interface(fenetre)
    i.pack()
    fenetre.mainloop()
