init python:

    class Inventory(object):

        def __init__(self, *args, **kwargs):

            for k, v in kwargs.items():

                self.alter_item(k, v)


        def alter_item(self, name, amount=1):

            attr_name = str(name).replace(' ','_').lower()

            if not hasattr(self, attr_name):

                setattr(self, attr_name, get_new_inventory_item(name))

            setattr(
                getattr(self, attr_name), 
                'amount',
                getattr(self, attr_name).amount + amount )

            if getattr(self, attr_name).amount <= 0:

                delattr(self, attr_name)


        @property
        def items(self):

            return [ k for k in self.__dict__ 
                     if isinstance(self.__dict__[k], BaseItem) ]

        def __repr__(self):

            return "\n    ".join( [""] + [
                repr(self.__dict__[k]) for k in self.__dict__ 
                if k not in dir(object)
                and k[0] != '_' ] )


    def get_new_inventory_item(name):
        """
        Return an instance of the Item based on name
        """

        ref_name = str(name).replace(' ','_').lower()

        if not globals().get('all_inventory_items'):

            globals()['all_inventory_items'] = {}

            for subclass in get_subclasses(BaseItem):

                if subclass == BaseItem:

                    continue

                item = subclass()

                ref_parts = [ m.group(0) for m in re.finditer(
                    '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', 
                    item.__class__.__name__) ]

                item_name = "_".join(
                    [ k.lower() for k in ref_parts ] )

                globals()['all_inventory_items'][ item_name ] = subclass 

        if ref_name in globals()['all_inventory_items']:

            return globals()['all_inventory_items'][ref_name]()

        raise AttributeError, "No item found with name '{}'".format(name)


    def get_subclasses(cls):
        """
        Return cls plus all subclasses of cls
        """

        subclasses = [cls]
        
        for subclass in cls.__subclasses__():

            subclasses.append( subclass )

            subclasses.extend( get_subclasses( subclass ) )

        return set( subclasses )