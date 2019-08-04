
init 510 python:

    class BaseTest(object):
        """
        Base Test class handling initialisation from lexer 
        passed arguments and keyword values

        A few utility methods to help run datetime based tests

        Subclasses are expected to oversee their data, supply a 
        test_valid method and maybe __repr_extra__
        """

        # allowed keywords listed as attribute defaults, e.g.
        # delta = "2 hours 30 mins"

        # just to pretty up the repr
        repr_indent = 0

        def __init__(self, event=None, *tests, **kwargs):

            self.event = event

            self.ref_name = self.event.handler.event_factory.get_ref_name( 
                    self.__class__.__name__ )

            if self.event:

                self.args = kwargs.pop('args', [])

                self.tests = self.get_tests(*tests)

                # kwarg values are passed as lists

                for kw in kwargs:

                    if hasattr(self, kw):

                        # for known keywords we set value without list

                        if isinstance(kwargs[kw], (list, tuple)):

                            if len(kwargs[kw]) == 1:

                                kwargs[kw] = kwargs[kw][0]

                        setattr(self, kw, kwargs[kw])

                    else:

                        # not recognized as an attribute, set to args

                        self.args.append( [kw] + kwargs[kw] )

                if hasattr(self, 'post_init'):

                    self.post_init()


        def get_tests(self, *tests):
            return self.event.get_tests(*tests)


        @property
        def _dt(self):
            return self.event.handler.get_dt(allow_test=True)


        @property
        def visits(self):
            return self.event.handler._visits.get( self.event.label, [] )


        @property
        def valid(self):
            return self.test_valid()


        def parse(self, istr=""):
            """ 
            Utility function: Taking a string, return a datetime
            """
            if isinstance(istr, type(datetime.datetime)):
                return istr 

            return self.event.handler.parse(istr)


        def get_date_string(self, dt):
            """
            Utility to return datetime in the format specified in the
            event handler object
            """
            # little or no reason to keep tags here, so:

            return renpy.translation.dialogue.notags_filter( 
                self.event.handler.get_str( dt ) )


        def test_valid(self):

            raise NotImplementedError, "Test Subclasses must implement the " \
                                       "test_valid() method. Class of type " \
                                       "'{}' does not.".format(
                                            self.__class__.__name__ )

        def force_lists(self):
            """
            Re-interpret args to be list of lists

            Useful where block input expects multiple values

            e.g.
            between "17 Nov 2018" "19 Nov 2018"
            or 
            between:
                "02 Nov 2018" "03 Nov 2018"
                "09 Nov 2018" "14 Nov 2018"

            where we expect
            args: [ [date1, date2] ]
            or
            args: [ [date1, date2], [date3, date4] ]
            """
            list_args, temp_list = [], []

            for arg in self.args:

                if isinstance( arg, list ):

                    if temp_list:

                        list_args.append( temp_list )

                        temp_list = []

                    list_args.append( arg )

                else:

                    temp_list.append( arg )

            if temp_list:

                list_args.append( temp_list )

            self.args = list_args


        def flatten_lists(self):
            """
            Flatten a list of args to accomodate list of lists
            """
            flat_args = []

            for arg in self.args:

                if isinstance(arg, (list, tuple)):

                    flat_args.extend( arg )

                else:

                    flat_args.append( arg )

            self.args = flat_args


        def __repr__(self):

            rstr = "{}:{}:".format( 
                " " * getattr(self, "repr_indent"),
                "pass" if self.valid else "fail" )

            rstr += " <{}>".format( self.__class__.__name__ )

            kw_info = []

            for k in [ k for k in type(self).__dict__ 
                       if k not in BaseTest.__dict__ 
                       and not callable( getattr(self, k) ) ]:

                kw_info.append( "{}={}".format(k, getattr(self, k) ) )

            kw_str = ", ".join(kw_info)

            if kw_str:

                rstr += " ({})".format(kw_str)

            extrastr = self.__repr_extra__()

            if extrastr:

                rstr += " {}".format(extrastr)

            if self.tests:

                for t in self.tests:

                    setattr( t, 
                             "repr_indent", 
                             getattr( self, "repr_indent" ) + 4 )

                    rstr += "\n{}".format( repr(t) )

            return rstr


        def __repr_extra__(self):

            return ""


