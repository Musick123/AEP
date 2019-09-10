
          ######################################
          #     An Extending Python Class      #
          ######################################


init python:

    class CharacterStats(BaseStatsObject, object):

        # Set the store.{prefix}.character_id value
        STORE_PREFIX = "character_stats"

        # Boolean toggle for validation - defaults both True
        VALIDATE_VALUES = False
        COERCE_VALUES = False

        STAT_DEFAULTS = {
            'state' : None,
            'outfit' : None, 
            'energy' : 10000,
            'mood' : 10,
            'generosity' : 0,
            'desire' : 0,
            'anger' : 0,
            'bag' : Inventory(),
        }

        def alter_item(self, name, amount=1, container='bag'):

            if not container in self.__dict__['_store']:

                setattr( self, container, Inventory() )

            inventory = getattr(self, container)

            inventory.alter_item(name, amount)

