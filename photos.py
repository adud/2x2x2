#! /usr/bin/python3

import picamera
from os import mkdir,chdir
from PIL import Image

#parametres de la camera
def initialise_camera():
    cam = picamera.PiCamera()
    try:
        cam.led = False
    except:
        print("""execute me as a superuser to turn off the led
    executez-moi en sudo pour eteindre la LED""")
    cam.resolution = (100,100)
    cam.preview_fullscreen = False
    cam.preview_window = (0,0,416,416)
    cam.rotation = 270
    cam.awb_mode = "incandescent"

    cam.start_preview()
    #a partir d'une image d'origine...
    img = Image.open("overlays/wikicross.png")

    #la redimensionne pour avoir mul32 en l, mul16 en h
    pad = Image.new("RGB", (
        ((img.size[0] + 31) // 32) * 32,
        ((img.size[1] + 15) // 16) * 16,
        ))

    pad.paste(img, (0,0))
    #cree 4 masques
    o = [cam.add_overlay(pad.tostring(), size=img.size) for x in range(4)]
    #les parametre et les place sur le preview
    for x in o:
        x.alpha = 128
        x.layer = 3
        x.fullscreen = False
        x.window = (88+208*(o.index(x)%2),88+208*(o.index(x)>1),32,32)

    return cam

#enregistre 6 photos

def photographie(camera,nom="photo",faces="FRBLUD"):
    """photographie avec camera autant de photos que d'elements de faces
nom : nom du dossier ou stocker les photos,
faces : nom des faces a photographier"""
    try:
        mkdir(nom)
    except:
        pass
    chdir(nom)
    print("sticker blanc en bas au fond a gauche selon la camera")
    for x in range(len(faces)):
        input(faces[x])
        camera.capture(nom+str(x)+".jpg")
    chdir("..")


