#! /usr/local/bin/python3
"""génère un cube en trois dimensions avec la bibliothèque visual de vpython
   ce cube sait tourner, mais la fonction n'est pas encore disponible"""

import visual as v

#Si j'ai le temps je ferai une classe pour regrouper tout ça parce que c'est un
#peu bordélique

FPS = 100     #en frame/seconds
SPEED = 0.3   #en secondes
PAUSE = 0.1     #en secondes
PEDA = False   #bool

oppose = {"D":"U",
          "L":"R",
          "B":"F",
          "U":"D",
          "R":"L",
          "F":"B"}

axe = {"D":(0,-1,0), #la direction que regarde la face
       "L":(-1,0,0),
       "B":(0,0,-1),
       "U":(0,1,0),
       "R":(1,0,0),
       "F":(0,0,1)}

wca_angles = {" ":-1,"2":2,"\'":1}#traduction de la notation WCA en 1/4 de tour

inverse = {" ":"\'","\'":" ","2":"2"}#donne l'angle du coup inverse

tourne = lambda liste,n: liste[n:]+liste[:n]

def sequence_inverse(seq):
    return [x[0]+inverse[x[1]] for x in seq.split(",")[::-1]]
    

def extractmaj():
    """met à jour l'extraction d'éléments du cube
    sert à traiter au cas par cas l'extraction de faces dans la liste cube"""
    global extraction
    extraction = {"D":cube[:4],
                  "L":cube[:2]+cube[4:6],
                  "B":cube[::2],
                  "U":cube[4:],
                  "R":cube[2:4]+cube[6:],
                  "F":cube[1::2]}

def cree_cube(stdim=.98,stwth=.05):
    """crée l'image du cube, les pièces sont stockées dans la liste cube"""
    global cube,image
    
    image = v.display()
    cube = [v.frame(display=image) for x in range(8)]
                                         #création de 8 objets-3D vides
                                         #auxquels on va attacher les structures
                                         #et les tuiles
##    cube=["DLB","DLF","DRB","DRF","ULB","ULF","URB","URF"] pour le debug

    extractmaj()#mise à jour d'extraction, nous reviendrons dessus

    for x in range(8):#création de la structure, des objets-3D box, qu'on lie à
                      #leur pièce grâce aux frames vvvvvvvvvvv ici  
        v.box(pos=(-.5+(x//2)%2,-.5+x//4,-.5+x%2),frame=cube[x],color=(.5,.5,.5))

    for x in range(4):#création de tuiles, boîtes plates, attachées aux pièces
        v.box(pos=(-.5+x//2,-(1+stwth/2),-.5+x%2),
            length=stdim,height=stwth,width=stdim,
            frame=extraction["D"][x],color=v.color.white)
        #frame attache la tuile à une pièce
        #extraction choisit la bonne pièce pour la tuile

        v.box(pos=(-.5+x//2,(1+stwth/2),-.5+x%2),
            length=stdim,height=stwth,width=stdim,
            frame=extraction["U"][x],color=v.color.yellow)

        v.box(pos=(-.5+x%2,-.5+x//2,-(1+stwth/2)),
            length=stdim,height=stdim,width=stwth,
            frame=extraction["B"][x],color=v.color.green)

        v.box(pos=(-.5+x%2,-.5+x//2,(1+stwth/2)),
            length=stdim,height=stdim,width=stwth,
            frame=extraction["F"][x],color=v.color.blue)

        v.box(pos=(-(1+stwth/2),-.5+x//2,-.5+x%2),
            length=stwth,height=stdim,width=stdim,
            frame=extraction["L"][x],color=v.color.orange)

        v.box(pos=((1+stwth/2),-.5+x//2,-.5+x%2),
            length=stwth,height=stdim,width=stdim,
            frame=extraction["R"][x],color=v.color.red)

def rotation_image(face,angle,anim = True):
    """fait tourner l\'image du cube sans modifier la liste
    l'animation se fait à l'aide de rate, qui permet de limiter le nombre de
    tours de boucle par seconde (en incluant le temps d'exécution)"""
    extractmaj()
    move=extraction[face]
    for x in range(int(FPS*SPEED)):
        for piece in move:
            piece.rotate(angle=(angle*v.pi/2)/(FPS*SPEED),
                         axis=axe[face])
            if anim:v.rate(FPS)

def rotation_objet(face,angle):
    """fait effectuer aux pièces du cube une rotation"""
    global cube
    extractmaj()                                         #extrait la face à tour
    move,fixe = extraction[face],extraction[oppose[face]]#ner et son opposé
    move=move[:2]+move[:1:-1]#ordonne la face à tourner pour une permutation
                             #circulaire (a,b,c,d) et pas (a,b,d,c)

    if face in "ULF":#fait tourner la face dans un sens ou l'autre
        move=tourne(move,-angle)
    else:
        move=tourne(move,angle)
        
    move=move[:2]+move[:1:-1] #réordonne la face à tourner
    reconstructeur = {"D":move+fixe,
                      "L":move[:2]+fixe[:2]+move[2:]+fixe[2:],
                      "B":move[0:1]+\
                      [(move[1:]+fixe)[x%7] for x in range(3,28,4)],
                      "U":fixe+move,
                      "R":fixe[:2]+move[:2]+fixe[2:]+move[2:],
                      "F":fixe[0:1]+\
                      [(fixe[1:]+move)[x%7] for x in range(3,28,4)]}
    #idem extraction mais pour reconstruire le cube (au cas par cas) à partir de
    #la face utilisée et la face non-utilisée
    cube = reconstructeur[face]

if __name__ == "__main__":
    cree_cube()
    image.center=(.6,.6,.6)       #place la caméra
    image.forward=(-1,-1,-1.1)    #oriente la caméra
    sequence = "R2,U2,F2"
    for face,nombre in sequence_inverse(sequence):
        rotation_image(face,wca_angles[nombre],anim = False)
        rotation_objet(face,wca_angles[nombre])
    input("ready ?")
    for face,nombre in sequence.split(","):
        rotation_image(face,wca_angles[nombre])
        rotation_objet(face,wca_angles[nombre])
        if PEDA:input()
        elif PAUSE:v.rate(1/PAUSE)
##    troll=v.text(pos=(-2.7,2,0),axis=(1,0,0),text="The Game")
##    while 1:
##        troll.rotate(angle=v.pi/FPS,axis=(0,1,0),origin=(0,0,0))
##        v.rate(FPS)
