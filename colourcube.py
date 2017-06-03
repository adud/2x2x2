#! /usr/bin/python3

from colorsys import rgb_to_hls
from PIL import Image
from math import floor

#un arbre binaire qui determine quelle couleur sortir en fonction de la teinte

__all__ = ["calibre","stickers","plusproche","image2couleur","moyennepixels",
           "oppose","traitement","tradstickerface","troisieme"]

def sumiter(*iterateurs,objet = list):
    """somme les elements de meme position de chaque iterateur et retourne
une iterateur objet contenant chaque somme"""
    return objet(map(sum,zip(*iterateurs)))

def calibre(couleurs):
    """liste hls (blanc en fin) -> diff blanc-couleur,5 couleurs triees"""
    diffblanc = (couleurs[-1][1] + max(couleurs[:-1],key = lambda x:x[1])[1])/2
    #regarde la luminosite du blanc puis la luminosite de la couleur la plus
    #lumineuse pour trouver la frontiere du blanc
    couleurs = sorted([x[0] for x in couleurs[:-1]])
    couleurs.append(couleurs[0]+1)
    #trie la liste et ajoute la premiere valeur a la fin (hls circulaire)
    return (diffblanc,couleurs)

def rgb256_to_hls(pixel):
    """transforme un pixel de la forme (r,g,b) de 0 a 256 en un pixel hls"""
    return rgb_to_hls(*[couleur / 256 for couleur in pixel])

def stickers(pixel,calibrage):
    """donne le sticker le plus proche de la valeur du pixel en hls"""
    if pixel[1] > calibrage[0]:
        return "blanc"
    else:
        v = plusproche(calibrage[1],pixel[0])
        return v - (v>1)
            

def plusproche(liste,valeur):
    """determine quel element de la liste triee la valeur est la plus proche
    liste : une liste de nombres triee
    valeur : un nombre reel"""
    milieu = floor(len(liste)/2)
    if milieu == 0:
        return liste[0]
    else:
        if (liste[milieu-1] + liste[milieu]) / 2 < valeur:
            return plusproche(liste[milieu:],valeur)
        else:
            return plusproche(liste[:milieu],valeur)

def image2couleur(image):
    """passe d'une image jpg a quatre valeurs hls
si calibre : applique la fonction stickers a chaque pixel avec le calibre donne
"""
    with Image.open(image) as photo:
        return [photo.getpixel((25+50*(x%2),25+50*(x>1))) for x in range(4)]

moyennepixels = lambda l: tuple([sum(n)/len(l) for n in list(zip(*l))])
moyennepixels.__doc__ = "ressort la valeur moyenne d\'une liste l de pixels"
#probleme circularite (barycentre)

def oppose(calibrage):
    """liste de pixels dans l\'ordre FRBLUD avec D blanc -> dictionnaire faces
    opposees"""
    dico = dict()
    for x in range(4):
        dico[calibrage[x][0]] = calibrage[(x+2)%4][0]
    dico["blanc"] = calibrage[4][0]
    dico[calibrage[4][0]] = "blanc"
    return dico

def tradstickerface(pieceDBL,oppose):
    """piece de pos DBL, dico oppose -> dico en clefs les valeurs \
sticker,en valeurs la notation URFBLD
la piece de pos DBL n'a encore que les deux valeurs B et L"""
    dico = dict()
    for num,val in enumerate(["blanc"] + pieceDBL):
        dico[val] = "DBL"[num]
        dico[oppose[val]] = "UFR"[num]
    return dico

def troisieme(coin,down):
    """la face du 3e sticker du coin en fonction de ceux des 2 premiers
    coin -> une liste
    down -> bool (True si le coin est en bas du cube)"""
    pattern = "DLBURF"
    position = [pattern.index(x)%3 for x in coin]
    horaire = not((position[0]-position[1])%3 - 1)
    parite = [x in pattern[3:] for x in coin]
    return pattern[3*((horaire + down + sum(parite))%2) + 3-sum(position)]
    
