# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define config.automatic_images = [' ', '_', '/']
define config.automatic_images_strip = ['images']

default persistent.hints = ['events', 'icons']

define a = Character("Ariane Eldar", image="ari", voice_tag="ari")

default ari_costume = "dress"

image ari = "images/ari/[ari_costume]/normal.png"
image ari angry = "images/ari/[ari_costume]/angry.png"
image ari happy = "images/ari/[ari_costume]/happy.png"
image ari shamed = "images/ari/[ari_costume]/shamed.png"
image ari shocked = "images/ari/[ari_costume]/shocked.png"

default current_location = None
default current_character = a

default char_locations = {
    a : "bridge" }

# init python:

#     config.auto_voice = "voice/{id}.ogg"

#     config.overlay_screens.append('_auto_voice')


label start:

    jump enter_theater_south_2

    return

label enter_location:
    # When we enter a location we first look for automatic events in 
    # locations between where we were and where we are trying to get to. 
    # Basically it's not possible to get from theatre_storage to 
    # theatre_stage without passing through certain other locations on
    # the way. If any of those locations have an auto event, it happens.

    return




label enter_theater_south_2:
    $ current_location = "theater_south_2"

    $ path = get_shortest_path('petrol')
    "[path!q]"

    a "Awake again"
    return
