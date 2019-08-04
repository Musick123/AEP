# TODO:
    # Get dialogues working ... auto ones are done
    # Position characters on screen
    # Background displayable cache
    # SubCharacters just for speech style changes 
    # Improve Silent Stan (tweak rollback) and get him to mention 
    # his stalk words before other dialogue
    # Test that class attributes are not altering (inventory mostly)
    # Think about ItemEvents having repeat 0 and auto visit

init python:

    class CurrentState(object):

        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

default current = CurrentState(
    location = "theater_south_2",
    character = "a",
    places = {
        'a' : "theater_south_2"
    })

define config.automatic_images = [' ', '_', '/']
define config.automatic_images_strip = ['images','characters']

define config.quit_action = [ Quit(confirm=False) ]

default persistent.hints = ['events', 'icons']

define character.a = Character(
    "Ariane Eldar", 
    image="ari", 
    voice_tag="ari",
    screen="cartoon_dialogue",
    what_style="cartoon_speech_text")
default a = CharacterStats("a", bag=Inventory(cigarettes=2))

default ari_costume = "dress"

image ari = "images/ari/[ari_costume]/normal.png"
image ari angry = "images/ari/[ari_costume]/angry.png"
image ari happy = "images/ari/[ari_costume]/happy.png"
image ari shamed = "images/ari/[ari_costume]/shamed.png"
image ari shocked = "images/ari/[ari_costume]/shocked.png"
image ari outdoorsleep = "images/ari/[ari_costume]/outdoorsleep.png"

label start:

    jump expression current.location

    return
