# TODO:
    # Get dialogues working ... auto ones are done
    #
    # Background displayable cache
    #
    # SubCharacters just for speech style changes 
    #
    # Improve Silent Stan (tweak rollback) and get him to mention 
    # his stalk words before other dialogue
    #
    # Test that class attributes are not altering (inventory mostly)
    #
    # Think about ItemEvents having repeat 0 and auto visit
    #
    # Make sure Handler is freshly loaded each init (replicate curtain pin 
    # error and test)
    #
    # Think about integrating with Inventory Items if it makes sense
    #
    # Bubble pos should follow sprite if moving
    #
    # Character Sprites as DynamicDisplayables using tag attributes 
    # and Stat based states (sleep/trapped/depressed/uniform etc)
    #
    # Add more Layers

init python:

    class CurrentState(object):

        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

default current = CurrentState(
    location = "theater_south_2",
    character = "a",
    places = {
        'a' : "theater_south_2",
        'rr' : "theater_storage",
        'mm' : "theater_audience",
    },
    sprites = {}, # stores last known location & position of sprites by tag
    )

define config.automatic_images = [' ', '_', '/']
define config.automatic_images_strip = ['images','characters']

define config.report_extraneous_attributes = False

define config.quit_action = [ Quit(confirm=False) ]

# default persistent.hints = ['events', 'icons']

            ###############################################
            #                                             #
            #                   Name                      #
            #                 reference                   #
            #            tag / images folder              #
            #                                             #
            ###############################################

            ###############################################
            #                                             #
            #                Ariane Eldar                 #
            #                     a                       #
            #                    ari                      #
            #                                             #
            ###############################################

define character.a = Character(
    "Ariane Eldar", 
    image="ari", 
    screen="cartoon_dialogue",
    # show_substyle="thought", # this would set her using thought bubbles
    what_style="cartoon_speech_text")

default a = CharacterStats(
    "a",
    state=None,
    outfit="dress", 
    bag=Inventory(cigarettes=2))

image ari = DynamicSprite("a")
#"images/ari/[current.outfit]/normal.png"
# image ari angry = Solid('#000')#"images/ari/[current.outfit]/angry.png"
# image ari happy = "images/ari/[current.outfit]/happy.png"
# image ari shamed = "images/ari/[current.outfit]/shamed.png"
# image ari shocked = "images/ari/[current.outfit]/shocked.png"
# image ari outdoorsleep = "images/ari/[current.outfit]/outdoorsleep.png"

            ###############################################
            #                                             #
            #               Ritchie the Rat               #
            #                     rr                      #
            #                  ritchie                    #
            #                                             #
            ###############################################

define character.rr = Character(
    "Ritchie the Rat",
    image="ritchie", 
    screen="cartoon_dialogue",
    what_style="cartoon_speech_text")

default rr = CharacterStats(
    "rr",
    state="trapped")

image ritchie = DynamicSprite('rr')
# "images/ritchie/normal.png"
# image ritchie trapped = "images/ritchie/trapped.png"

            ###############################################
            #                                             #
            #               MusikMaschinist               #
            #                     mm                      #
            #                    musik                    #
            #                                             #
            ###############################################

define character.mm = Character(
    "MusikMaschinist",
    image="musik", 
    screen="cartoon_dialogue",
    what_style="cartoon_speech_text")

default mm = CharacterStats("mm")

image musik = DynamicSprite("mm")
# "images/musik/normal.png"

            ###############################################
            #                                             #
            #                Harrer Potty                 #
            #                     hp                      #
            #                   harrer                    #
            #                                             #
            ###############################################


            ###############################################
            #                                             #
            #               Hilda Wittberg                #
            #                     hw                      #
            #                   hilda                     #
            #                                             #
            ###############################################


            ###############################################
            #                                             #
            #                Jeremy Blunt                 #
            #                     jb                      #
            #                                             #
            ###############################################


            ###############################################
            #                                             #
            #                Jenna Saffoe                 #
            #                     js                      #
            #                                             #
            ###############################################


            ###############################################
            #                                             #
            #             N The Faceless One              #
            #                    nf                       #
            #                                             #
            ###############################################


            ###############################################
            #                                             #
            #               Ossian Moreau                 #
            #                     om                      #
            #                                             #
            ###############################################


            ###############################################
            #                                             #
            #                Vestisphagos                 #
            #                     ve                      #
            #                                             #
            ###############################################


            ###############################################
            #                                             #
            #               Zerberus (dog)                #
            #                    ze                       #
            #                                             #
            ###############################################

label start:

    jump expression current.location

    return
      