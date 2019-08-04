init python:
    
    import re

    class BaseItem(object):

        ITEM_DATA = {
            'title' : None, # derived from non camel class name if None
            'amount' : 0,
            'description' : "No description",
            'image' : None,
            'buy_price' : 0,
            'sell_price' : 0,
            'view_priority' : 0,
            'stack_size' : 1,
            'weight' : 0,
        }

        def __init__(self, *args, **kwargs):

            for cls in self.__class__.__mro__:

                if not hasattr(cls, 'ITEM_DATA'):

                    continue

                for key in cls.ITEM_DATA:

                    if not hasattr(self, key):

                        setattr(self, key, cls.ITEM_DATA[key])
            
            if not hasattr(self, 'title') or not self.title:

                matches = re.finditer(
                    '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', 
                    self.__class__.__name__)
                classname_parts = [m.group(0) for m in matches]
                
                self.title = " ".join( classname_parts )


        def __repr__(self):

            return "{:03d} x {}".format( self.amount, self.title ) 


# These will probably be subclasses for things like
# Equipment
# Costume
# Consumable 
# (with default actions maybe) etc


            ###############################################
            #                                             #
            #              Important Items                #
            #                                             #
            ###############################################

    class NagraSN(BaseItem):
        pass

    class PortableRecordPlayer(BaseItem):
        pass

    class RockLP(BaseItem):
        pass

    class ArianesMagicBook(BaseItem):

        ITEM_DATA = {
            'title' : "Ariane's Magic Book",
            'description' : "Spells and stuff...",
            'buy_price' : -1,
            'sell_price' : -1,
            'view_priority' : 10
        }


            ###############################################
            #                                             #
            #                Common Items                 #
            #                                             #
            ###############################################


    class Cigarettes(BaseItem):

        ITEM_DATA = {
            'description' : "Smoking...",
            'buy_price' : 10,
            'sell_price' : 7,
            'view_priority' : 0,
            'stack_size' : 10,
            'weight' : 1
        }

    class FarmCheese(BaseItem):
        pass

    class Chocolate(BaseItem):
        pass

    class Alcohol(BaseItem):
        pass


            ###############################################
            #                                             #
            #                    Keys                     #
            #                                             #
            ###############################################


    class Key(BaseItem):

        ITEM_DATA = {
            'description' : "A key",
            'buy_price' : -1,
            'sell_price' : -1,
            'view_priority' : 0,
            'stack_size' : 1,
            'weight' : 1
        }

    class TheaterStageKey(Key):
        pass

    class TheaterBackstageKey(Key):
        pass


            ###############################################
            #                                             #
            #                  Costumes                   #
            #                                             #
            ###############################################


    class Costume(BaseItem):
        pass

    class Angel(Costume):
        pass

    class Butterfly(Costume):
        pass

    class Cat(Costume):
        pass

    class Dress(Costume):
        pass

    class Fairy(Costume):
        pass

    class FrenchMaid(Costume):
        pass

    class Nun(Costume):
        pass

    class Nurse(Costume):
        pass

    class RedRidingHood(Costume):
        pass

    class SchoolGirl(Costume):
        pass

    class SemiNaked(Costume):
        pass

    class Naked(Costume):
        pass

    class BlackLingerie(Costume):
        pass

    class WhiteLingerie(Costume):
        pass