

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
image ari outdoorsleep = "images/ari/[ari_costume]/outdoorsleep.png"

default current_location = "theater_south_2"
default current_character = a

default char_locations = {
    a : "bridge" }

label start:

    jump expression current_location

    return
