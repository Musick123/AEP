


## TODO: Cleaning and docstrings

## TODO: Check saving, loading and rollback support _dt, _visits and others

init 510 python:

    import renpy.store as ren_store

    import datetime


    class EventHandler(object):
        """ 
        Handle keeping track of time and scheduled events 
        """

        def __init__(self, **kwargs):
            """ 
            Initialize the object
            """

            self.event_factory = EventFactory()

            self.events = {}

            self.output = kwargs.get('output', eh_init_values['output'])

            self.input = kwargs.get('input', 
                                    eh_init_values.get('input', self.output))

            #
            # Our Start date
            self.start = self.parse(
                kwargs.get('start', eh_init_values['start']) )

            self.duration = self.get_timedelta(
                kwargs.get('duration', eh_init_values['duration']) )

            self.step = self.get_timedelta(
                kwargs.get('step', eh_init_values['step']) )

            #
            # self._dt is a pseudo/hidden attribute handled by renpy.store
            # we set/get it using __setattr__ and __getattr(ibute)__
            #
            # ditto with _visits

            self._visits = {}

            self._dt = self.start

            # used for testing events against arbitrary date/times
            self.test_dt = None


        def __str__(self):
            return self.get_str()

        
        def __getattr__(self, key):
            
            if key == '_dt':
                # Use store version only
                return ren_store.event_handler_dt or 0

            if key == '_visits':
                # Use store version only            
                return ren_store.event_handler_visits or {}

            if key.startswith("_event_"):

                # TODO: Fix (after remembering why you wrote this...)

                try:

                    d = ren_store.event_handler_store_attrs

                except AttributeError:

                    d = {}

                return d[ key[7:] ]
            
            try:

                return self.__dict__[key]

            except KeyError:

                if key == "all":

                    return self.get_type_events(valid=False)

                elif key != "event_factory" \
                and key in self.event_factory.event_types.keys():

                    return self.get_type_events(key)

                elif key.startswith("all_") \
                and len(key) > 4 \
                and key[4:] in self.event_factory.event_types.keys():

                    return self.get_type_events(key[4:], valid=False)

            return super(EventHandler, self).__getattribute__( key ) 


        def __setattr__(self, key, value):

            if key == '_dt':

                ren_store.event_handler_dt = self.parse( value )
            
            elif key == '_visits':

                ren_store.event_handler_visits = value

            elif key.startswith("_event_"):

                try:

                    d = ren_store.event_handler_store_attrs

                except AttributeError:

                    ren_store.event_handler_store_attrs = d = {}

                d[ key[7:] ] = value

            else:
                # Other values (not held in the store)
                super(EventHandler, self).__setattr__( key, value )


        def get_dt(self, dt=None, allow_test=False):
            """ 
            Return passed minute or current game minute
            """
            if self.test_dt and allow_test:

                return self.test_dt

            return self.parse(dt) if dt is not None else self._dt


        def get_str(self, dt=None, format_str=None):
            """ 
            Ouput a string to represent the datetime
            """
            dt = self.get_dt( dt )

            format_str = format_str if format_str and len( format_str ) \
                         else self.output
                
            # *should* work with translation
            return _strftime(format_str, dt.timetuple())


        def parse(self, istr=""):
            """ 
            Taking a string, return a datetime
            """
            if isinstance(istr, datetime.datetime):

                return istr 

            try:

                return datetime.datetime.strptime(
                    unicode(istr).encode("utf-8"), 
                    self.input )

            except ValueError as e:

                try:

                    # try the format without parts after hours

                    short_input = self.input[ : max(
                        self.input.find("%H"),
                        self.input.find("%I") ) ]

                    if len(short_input) + 1 < len(self.input):
                        # %H or %I exist

                        return datetime.datetime.strptime(
                            unicode(istr).encode("utf-8"), 
                            short_input.strip() )

                except:

                    pass

                raise e


        def get_timedelta(self, *args, **kwargs):
            """
            Return relativedelta for the parameters
            """

            if len(args) and isinstance(args[0], type(datetime.timedelta)):

                return args[0]
            
            return datetime.timedelta(
                **self.get_timedelta_kws( *args, **kwargs ) )


        def get_timedelta_kws(self, *args, **kwargs):
            """
            Return kwargs for a relativedelta for the passed parameters
            """

            if len(args) == 2:

                # two datetimes

                kwargs['dt1'] = self.parse(args[0])

                kwargs['dt2'] = self.parse(args[1])

            elif len(args):

                try:

                    # numeric input taken as float minutes

                    kwargs['minutes'] = float(args[0])

                except:

                    # basestring "2 days 4 hours 15 minutes"
                
                    arg_split = args[0].split()

                    for k in range(1, len(arg_split), 2):
                    
                        kwargs[ arg_split[k] ] = float(arg_split[k-1])

            if not kwargs:

                # passed in None as first or just empty call

                kwargs['seconds'] = self.step.total_seconds()

            for k in ['year','month','day','hour','minute']:

                if k in kwargs:

                    raise KeyError, "Singular keywords are not used in " \
                                    "datetime objects. Keywords such as " \
                                    "'{kw}' are invalid. Try using '{kw}s' " \
                                    "instead.".format( kw=k )

            return kwargs 

        #
        # If we do eh.time() in a label we use values And visit
        # If no values, we create from duration or step
        #
        # If not in label we use self.step if no other values passed
        #
        def time(self, *args, **kwargs):
            """ 
            Alter the internal datetime 
            """

            label = kwargs.pop('label', None)

            if not label:

                label = get_label_for_node( *renpy.get_filename_line() )

            if label in self.events:    

                self.visit( label )

            if not len(args) and not len(kwargs):

                kwargs['minute'] = self.duration

                event = self.events.get(label, None)

                if event and event.duration:

                    kwargs['minute'] = event.duration

            self._dt += self.get_timedelta(*args, **kwargs)


        def register_event(self, label, *args):

            self.events[label] = self.event_factory.get_event( 
                self, label, *args )


        def get_event(self, label=None):

            if not label:

                label = get_label_for_node( *renpy.get_filename_line() )

            return self.events.get( label, None )



        def get_type_events(self, types=None, dt=None, valid=True, 
                            key=None, reverse=False):
            """
            Return a list of events of type or list(types)
            Order is defined by event.priority reverse
            """
            if dt:

                self.test_dt = self.parse(dt)

            if not types:

                types = self.event_factory.event_types.keys()

            if not isinstance(types, (list, tuple)):

                types = [types]

            types = [ str(k).lower() for k in types ]

            events = [ self.events[k] for k in self.events 
                       if self.events[k].ref_name in types
                       and ( self.events[k].valid if valid else True ) ]

            self.test_dt = None

            if not key:

                key = "label"

            return sorted(events, 
                          key=lambda x: getattr(x, key, None),
                          reverse=reverse)


        def visit(self, label=None):
            """
            Visit the label and add current _dt to its _visits if 
            enough time (event duration) has lapsed since last call
            """

            if label is None:

                label = get_label_for_node( *renpy.get_filename_line() )

            if label not in self.events:

                # Might be a Nub (if it starts with a location)

                locs = [e.label for e in self.location]

                if any([label.startswith(k) for k in locs]):

                    self.events[label] = self.event_factory.get_event( 
                        self, label, ([u'type', [u'nub']]) )

            if label in self.events:

                if not label in self._visits:

                    v = self._visits

                    v[label] = [self.get_dt()]

                    self._visits = v

                    return

                duration = self.get_event(label).duration

                if self._visits[label][-1] + duration < self.get_dt():

                    v = self._visits

                    v[label].append(self.get_dt())

                    self._visits = v




    def get_subclasses(cls):
        """
        Return cls plus all subclasses of cls
        """

        subclasses = [cls]
        
        for subclass in cls.__subclasses__():

            subclasses.append( subclass )

            subclasses.extend( get_subclasses( subclass ) )

        return set( subclasses )
        
    import re

    class EventFactory(object):
        """
        This class spawns the correct {Base}Event type 
        and populates the usual fields and the tests

        The get_event() method is called through the lexer and
        handler 
        """

        def __init__(self):

            self.event_types = {
                self.get_ref_name(k.__name__) : k
                for k in get_subclasses(BaseEvent)
            }

            self.test_types = {
                self.get_ref_name(k.__name__) : k
                for k in get_subclasses(BaseTest)
            }

            if 'type' in self.test_types:

                raise ValueError, "Test cannot be named TypeTest"

        @staticmethod
        def get_ref_name(class_name):
            """
            Return a string name for the sub class ignoring suffix
            (BeforeTest) => "before"
            (ABCDefAtkTest) => "abc_def_atk"
            """

            ref_parts = [ m.group(0) for m in re.finditer(
                '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', 
                class_name) ]

            ref_name = "_".join(
                [ k.lower() for k in ref_parts[:-1] ] )

            # print("{} >> {}".format(class_name, ref_name) )

            return ref_name if ref_name != "base" else "none"


        def get_tests_and_kwargs(self, *args):
            """
            Read the args list and return

            [ (test type, [ args ]) tuples in list ],
            { kwarg: value } dict
            
            for any found tests or kwargs

            Return tests list, kwargs dict
            """
            tests, kwargs = [], { 'args' : [] }

            # print("GTAK Input: {}".format(args))

            for arg in args:

                if not isinstance(arg, (list, tuple)):

                    kwargs['args'].append(arg)

                    continue

                if len(arg) < 2:

                    kwargs['args'].append( arg[0] )

                    continue

                test_type = self.test_types.get( 
                    str(arg[0]).lower(), None )

                if test_type:

                    tests.append( ( test_type, arg[1] ) )

                elif not isinstance(arg[0], basestring):

                    kwargs['args'].append( arg[0] )

                elif arg[0] not in kwargs:

                    kwargs[arg[0]] = arg[1]

                else:

                    kwargs[arg[0]].extend( arg[1] )

                    # print("kwargs[ {} ]: {}".format(arg[0], kwargs[arg[0]]))

            # print("GTAK Return: {} : {}".format(tests, kwargs))

            return tests, kwargs


        def get_event(self, handler, label, *args):

            # print("get_event: {} : {}".format(label, args))

            event_tests, event_kwargs = self.get_tests_and_kwargs(*args)
            type_args = event_kwargs.pop('type', None)

            event_type = None

            if type_args and type_args[0] in self.event_types:

                event_type, type_args = type_args[0], type_args[1:]

            event_kwargs['args'] = type_args + event_kwargs['args']

            event_obj = self.event_types.get( str(event_type).lower(), None )

            if not event_obj:

                raise AttributeError, "EventFactory could not evaluate " \
                                      "event type '{}' from {}".format(
                                        etype, self.event_types)

            event_kwargs['label'] = [label]

            return event_obj(handler, *event_tests, **event_kwargs)



    globals()[ eh_init_values['ref'] ] = EventHandler()

