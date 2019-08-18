
label theater_storage_a_first_visit:
    event register dialogue:
        pass

    show ritchie trapped

    a "Ritchie?!"

    rr "Yes, Ritchie. Ritchie in the trap! 
        \nWhy don't you do something to help me?"

    a "Hmmm, I will. Pffft, or better not?
        \nSpank me, I am a much too good person. I'll open it."

    rr "Well, you're not going to manage it with your bare hands. 
        \nGo find a tool and please hurry"

    return



label theater_storage_a_free_ritchie:
    event register dialogue:
        inventory "crowbar"

    show ritchie trapped:
        anchor (0.5, 1.0)
        pos (690, 650)

    a "Ritchie! I have a crowbar. 
        \nThis should do to open that nice cage you call home. 
        \nJust one moment"

    rr "Freedom! You may like it in a cage, I do not."

    $ current.places['rr'] = "theater_storage"

    return


label theater_storage_a_rr_ritchietool:
    event register dialogue:
        seen "theater_storage_a_free_ritchie"

    rr "I'm free. I owe you one Ariane. Is there anything you need?"

    a "Well, Ritchie, could you break into the backstage wardrobe for me? 
        Most of my lovely costumes are in there and some tard has locked it"

    rr "To manage that, I'd need the great and wonderful RitchieTool"

    a "The what? Where can we get one?"

    rr "The great and wonderful RitchieTool ... etc etc conversation"

    a "So, a quest to make a tool, yay"

    return