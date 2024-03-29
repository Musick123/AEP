
          ######################################
          #         The Python Class           #
          ######################################

           # this should go in a separate .rpy

init python:

    class BaseStatsObject(object):
        """
        Base class for defaulting stats and integrating with the store.

        Designed to be extended by just overloading the constants


        Example of extended class

        class EnemyStats(BaseStatsObject):

            # Set the store.{prefix}.character_id value
            STORE_PREFIX = "enemy_stats"

            # Boolean toggle for validation - defaults both True
            VALIDATE_VALUES = True
            COERCE_VALUES = False

            STAT_DEFAULTS = {
                'element' : 'earth',
                'hp' : 50,
                'mp' : 40,
                'rarity' : 0.075,
            }

        """

        STORE_PREFIX = "character_stats"
        VALIDATE_VALUES = True
        COERCE_VALUES = True

        STAT_DEFAULTS = {}

        def __init__(self, id, **kwargs):
            """
            Initialize values from store or kwargs or default

            @param id: A unique id to use in the store. Generally set to 
            the Character reference to allow cross object lookups

            @param **kwargs: Setup values that are not default
            """

            if not isinstance(id, basestring):
                id = str(id) # should raise if not stringable

            self.__dict__['_id'] = id

            self.run_optional_method( '__pre_init__', id, **kwargs )

            store_name = "{prefix}_{suffix}".format(
                prefix = type(self).STORE_PREFIX,
                suffix = self.__dict__['_id'] )

            setattr(store, store_name, {})

            self.__dict__['_store'] = getattr(store, store_name)

            for key, value in self.__dict__['_store']:

                setattr(self, key, value)
            # We use:
                # Store value
                # else kwargs value
                # else default value

            for key, value in kwargs.items():

                if key not in self.__dict__['_store']:

                    setattr(self, key, value)

            for key, value in type(self).STAT_DEFAULTS.items():

                if key not in self.__dict__['_store']:

                    setattr(self, key, value)

            for key in [ k for k in self.__dict__['_store'] 
                         if k not in self.__dict__ ]:

                self.__dict__[k] = self.__dict__['_store'][k]

            self.run_optional_method( '__post_init__', id, **kwargs )


        def __repr__(self):

            return "\n".join( [
                "{} : {}".format( k, getattr(self, k) ) 
                for k in self.__dict__['_store'] 
                if k[0] != '_' ] )


        @property
        def character(self):
            return getattr(character, self._id)


        def run_optional_method(self, 
                                method_type='post_init', 
                                *args, 
                                **kwargs):
            """
            Run a method of the object if it exists
            """
            try:
                getattr( self, self.__dict__[ method_type ] )( *args,
                                                               **kwargs )
            except:
                pass


        def get_validated_value(self, key, value):
            """
            Return a value after validating where applicable
            """

            if not type(self).VALIDATE_VALUES:
                return value

            if not key in self.__dict__:
                return value

            default_type = type( self.__dict__[key] )

            if isinstance(value, default_type):
                return value

            if type(self).COERCE_VALUES:
                try:
                    return default_type(value)
                except:
                    pass

            raise TypeError, "Supplied value '{0}' for key '{1}' does not " \
                             "match the existing '{2}'".format(
                                value, 
                                key,
                                default_type)


        def __setattr__(self, key, value):

            value = self.get_validated_value(key, value)

            self.__dict__[key] = value

            # Anything not recognized as an attribute of object
            # is placed into the store

            if key not in dir(object):

                self.__dict__['_store'][key] = value


        def __getattr__(self, key):

            try:

                return self.__dict__['_store'][key]
            
            except:
            
                if key in self.__dict__:

                    return self.__dict__[key]
                
                else:

                    try:

                        # try the character object
                        value = getattr( self.character, key )

                        if key != 'name':
                        
                            return value

                        # substitute the name (for interpolation/translations)
                        return renpy.substitutions.substitute(value)[0]

                    except:
                        
                        pass

            try:
 
                return super(BaseStatsObject, self).__getattr__(key)

            except:
 
                return super(BaseStatsObject, self).__getattribute__(key)


        def __getattribute__(self, key):

            # Check if the attribute is an @property first

            v = object.__getattribute__(self, key)

            if hasattr(v, '__get__'):

                return v.__get__(None, self)

            # Try the store if the attribute is not in base object

            if key not in dir(object):

                try:
                
                    return self.__dict__['_store'][key]
                
                except:
                
                    pass

            return super(BaseStatsObject, self).__getattribute__(key)
    

        def __setstate__(self, data):
            self.__dict__.update(data)


        def __getstate__(self):
            return self.__dict__


        def __delattr__(self, key):
            del self.__dict__[key]