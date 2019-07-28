
init python:

    class BaseEvent(object):
        """
        Base Event class handling initialisation from lexer 
        passed arguments and keyword values

        A few utility methods to help run child tests

        Subclasses are expected to oversee their data and
        maybe supply a __repr_extra__ method

        Note:

            Class sttributes may govern their state by 
            starting with a set prefix:

                store_
                    Class attributes starting with this
                    prefix will be held in the Ren'Py 
                    store object so will maintain value
                    through saves and rollback etc

                translate_
                    Class attributes starting with this
                    prefix will attempt to be translated
                    when accessed
        """

        # used to store which attributes to translate or
        # store within the sub classes
        translate_attrs = []
        store_attrs = []

        def __init__(self, handler=None, *tests, **kwargs):

            self.handler = handler

            self.ref_name = self.handler.event_factory.get_ref_name( 
                    self.__class__.__name__ )

            # print("Creating Event: {} with {} : {}".format(
            #     self.ref_name, tests, kwargs))

            if self.handler:

                self.priority = kwargs.pop('priority', [1])[0]
                self.auto_start = kwargs.pop('auto_start', [False])[0]
                self.label = kwargs.pop('label', [None])[0]
                self.duration = kwargs.pop('duration', 
                                           [self.handler.duration])[0]
                self.args = kwargs.pop('args', [])
                self.tests = self.get_tests(*tests)

                self._class_attributes = [ 
                    k for k in type(self).__dict__ 
                    if k not in BaseEvent.__dict__ 
                    and not callable( getattr(self, k) ) ]

                self.__init_kwargs__(**kwargs)


        def __init_kwargs__(self, **kwargs):

            # Note: All other kwarg values are passed as lists
            # ... reduce where possible (if the list is one item long)

            for kw in kwargs:

                if isinstance(kwargs[kw], (list, tuple)):

                    if len(kwargs[kw]) == 1:

                        kwargs[kw] = kwargs[kw][0]

            # determine which ones are translate_attrs or store_attrs

            for kw in self._class_attributes:

                if kw.startswith('translate_'):

                    # translation attributes

                    key = kw[10:] # kw without leading translate_

                    try:
                    
                        value = kwargs.pop( key )

                        # passed through lexer, so we can check if it is _()

                        if isinstance(value, basestring) \
                        and value.startswith("_(") \
                        and not key in self.translate_attrs:

                            self.translate_attrs.append( key )

                    except KeyError:

                        # from class object (where all attributes
                        # starting with underscore are translatables)

                        if not key in self.translate_attrs:

                            self.translate_attrs.append( key )

                        value = getattr(self.__class__, kw)

                    setattr(self, kw, value)

                elif kw.startswith('store_'):

                    # store attributes

                    key = kw[6:] # kw without leading translate_

                    if not key in self.store_attrs:

                        self.store_attrs.append( key )

                    try:

                        value = kwargs.pop( key )

                    except KeyError:

                        value = getattr(self.__class__, kw)

                    # store_attrs are held in the store through the
                    # handler class
                    # during this init we only set them if they do 
                    # not already exist

                    store_key = self.get_store_key( key )

                    try:

                        store_value = getattr( self.handler, store_key )

                    except KeyError:

                        setattr( self, key, value )

            self.__dict__.update(kwargs)


        def __setattr__(self, key, value):

            if key in self.translate_attrs:

                long_key = "translate_{}".format( key )

                self.__dict__[ long_key ] = value 

            elif key in self.store_attrs:

                store_key = self.get_store_key( key )

                setattr( self.handler, store_key, value )

            else:

                super(BaseEvent, self).__setattr__(key, value)


        def __getattr__(self, key):

            if key in self.translate_attrs:

                value = self.__dict__[ "translate_{}".format( key ) ]

                try:

                    if isinstance(value, basestring) \
                    and value.startswith("_("):

                        value = renpy.python.py_eval( value )

                    value = renpy.substitute( value )

                except:

                    pass

                return value

            elif key in self.store_attrs:

                store_key = self.get_store_key( key )

                return getattr( self.handler, store_key )

            return super(BaseEvent, self).__getattribute__(key)


        def __repr__(self):

            rstr = "<{} for {}>".format(
                self.__class__.__name__,
                self.label)

            if self.args:

                rstr += " [{}]".format( 
                    ", ".join( [ str(k) for k in self.args ] ) )

            base_info = []

            if self.priority != 1:

                base_info.append( "priority={}".format(self.priority) )

            if self.auto_start:

                base_info.append( "automatic" )

            if self.duration != self.handler.duration:

                base_info.append( "duration={}".format(self.duration) )

            basestr = ", ".join(base_info)

            if basestr:

                rstr += " ({})".format(basestr)

            extrastr = self.__repr_extra__()

            if extrastr:

                rstr += " {}".format(extrastr)

            return rstr


        def __repr_extra__(self):

            return ""


        def get_store_key(self, key):

            return "_event_{}_{}".format( self.label, key )


        def get_tests(self, *tests):

            test_objs = []

            for test in tests:

                obj_tests, obj_kwargs = self.get_tests_and_kwargs( 
                    *test[1] )

                test_objs.append(
                    test[0](self, *obj_tests, **obj_kwargs) )

            return test_objs


        def get_tests_and_kwargs(self, *args):
            return self.handler.event_factory.get_tests_and_kwargs(*args)


        @property
        def valid(self):

            return all( [ t.valid for t in self.tests ] ) 

