#! /usr/bin/python3
#! -*- coding: utf-8 -*-

import photos
import colourcube as cc
import cube2 as mcube
import solveurs as slv

from PIL import Image
from os import chdir,listdir
from colorsys import rgb_to_hls

calibrage = input("calibrage ?\n")
cheese = input("photographie ?\n") or calibrage

if calibrage or cheese: cam = photos.initialise_camera()

#prend le calibrage si l'utilisateur le veut
if calibrage:
    print("calibrage en cours")
    photos.photographie(cam,nom="calibrage")
#le traite
chdir("calibrage")

couleurs = []
exposition = [0,0,0,0]

for image in sorted(listdir()):
    liste = cc.image2couleur(image)
    moyenne = cc.rgb256_to_hls(cc.moyennepixels(liste))
    liste_hls = list(map(cc.rgb256_to_hls,liste))
    exposition = [exp - pix[1] + moyenne[1]
                  for exp,pix in zip(exposition,liste_hls)]
    couleurs.append(moyenne)

exposition = [elem / 6 for elem in exposition]
opposes = cc.oppose(couleurs)
calibre = cc.calibre(couleurs)
chdir("..")

input(exposition)
print("cube mélangé")

if cheese:photos.photographie(cam,nom="cube",faces="FRBL")
if calibrage or cheese:cam.close()
chdir("cube")

cube = []
for image in sorted(listdir()):
    
    liste = cc.image2couleur(image)
    liste = list(map(cc.rgb256_to_hls,liste))
    #regle les differences d'exposition en fonction du point de capture
    liste = [cc.sumiter(pix,(0,exp,0)) for exp,pix in zip(exposition,liste)]
    liste = [cc.stickers(pix,calibre) for pix in liste]
    cube.append(liste)

#separe haut-bas
cube = [[face[:2] for face in cube],[face[2:] for face in cube]]
#aplanit une liste de listes
cube = [sum(semicube,[]) for semicube in cube]
#traduit les deux moities
traduction = cc.tradstickerface(cube[1][5:7],opposes)
cube = [[traduction[sticker] for sticker in moitie] for moitie in cube]
#decalage de 1 pour s'aligner avec le cube d'Alban
cube = cube[0][1:] + cube[0][0:1] + cube[1][1:] + cube[1][0:1]
#trouve la valeur du 3e sticker et assemble le cube par pieces
liste = list()
for x in range(8):
    liste.append([cc.troisieme("".join(cube[2*x:2*x+2]),x>3)] +
                 cube[2*x:2*x+2])
cube = liste

cube[:4] = [stick[0:1]+stick[:0:-1] for stick in cube[:4]]

#passe du parcours horaire au parcours coordonnees
liste = liste[:2] + liste[3:1:-1] + liste[4:6] + liste[:5:-1]
cube = mcube.Cube()
for x in range(7):
    cube.set(mcube.corner(x),liste[x])

print(cube,traduction,sep = "\n")
print(int(cube))
print(slv.optimal_solve(cube,limit = 11))
