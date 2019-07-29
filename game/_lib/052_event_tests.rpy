
init python:

    class AllTest(BaseTest):
        """
        Valid if all sub tests are valid

        @usage:
    
            all:
                subtest
                subtest
        """

        def test_valid(self):

            return all( [ k.valid for k in self.tests ] )


        def __repr_extra__(self):

            return "Valid if all sub tests are valid"


    class AnyTest(BaseTest):
        """
        Valid if any sub tests are valid

        @usage:
    
            any:
                subtest
                subtest
        """

        def test_valid(self):

            return any( [ k.valid for k in self.tests ] )


        def __repr_extra__(self):

            return "Valid if any sub tests are valid"


    class NotTest(BaseTest):
        """
        Valid if all of the sub tests fail

        @usage:
    
            not:
                subtest
                subtest
        """

        def test_valid(self):

            return all( [ not k.valid for k in self.tests ] )


        def __repr_extra__(self):

            return "Valid if all of the sub tests fail"


    class AfterTest(BaseTest):
        """
        Valid after the datetime passed as first argument

        @usage:
    
            after "02 Mar 2012"
        """

        def post_init(self):

            self.args[0] = self.parse(self.args[0])


        def test_valid(self):

            return self._dt >= self.args[0]


        def __repr_extra__(self):

            return "Valid after {}".format( 
                self.get_date_string( self.args[0] ) )


    class BeforeTest(BaseTest):
        """
        Valid before the datetime passed as first argument

        @usage:
    
            before "02 Mar 2012"
        """

        def post_init(self):

            self.args[0] = self.parse(self.args[0])


        def test_valid(self):

            return self._dt < self.args[0]


        def __repr_extra__(self):

            return "Valid before {}".format( 
                self.get_date_string( self.args[0] ) )


    class BetweenTest(BaseTest):
        """
        Valid between each datetime pair passed as arguments

        @usage:
    
            between "17 Nov 2018" "19 Nov 2018"

            or

            between:
                "02 Nov 2018" "03 Nov 2018"
                "09 Nov 2018" "14 Nov 2018"
        """
        
        def post_init(self):

            self.force_lists()

            for i, arg in enumerate(self.args):

                for j, item in enumerate(arg):

                    self.args[i][j] = self.parse( item )


        def test_valid(self):

            for arg in self.args:

                if arg[0] <= self._dt < arg[1]:

                    return True

            return False


        def __repr_extra__(self):

            return "Valid between {}".format( 
                " or ".join( [
                    "({} and {})".format( 
                        self.get_date_string( arg[0] ), 
                        self.get_date_string( arg[1] ) )
                    for arg in self.args ] ) )


    class SpanTest(BetweenTest):
        """
        Valid after each datetime (passed as argument)
        for a duration of 'delta' (passed as keyword)

        @usage:
    
            span:
                delta "6 hours" 
                "02 Nov 2018" 
                "03 Nov 2018"
        """

        delta = "1 days 12 hours"

        def post_init(self):

            args = [ k for k in self.args ]

            self.delta = self.event.handler.get_timedelta( self.delta )

            self.args = []

            for arg in args:

                arg = self.parse( arg )

                self.args.append( [ arg, arg + self.delta ] )


    class CooldownTest(BaseTest):
        """
        Valid if the event has not been visited yet or if the 
        previous visit was longer ago than the keyword 'cooldown' value

        @usage:
    
            cooldown "3 days 6 hours"
        """

        def post_init(self):

            self.cooldown = self.event.handler.get_timedelta( self.args[0] )


        def test_valid(self):

            if len(self.visits):

                print("Testing: {} vs {}".format(
                    self.visits[-1] + self.cooldown, self._dt))

                if self.visits[-1] + self.cooldown > self._dt:

                    # still cooling down

                    return False 

            return True 


        def __repr_extra__(self):

            return "Valid when previous visit was over '{}' ago".format(
                self.cooldown )


    class RepeatTest(BaseTest):
        """
        Valid if the event has been visited less times than the 
        single passed argument value

        @usage:
    
            repeat 5
        """

        def test_valid(self):

            return int(self.args[0]) > len(self.visits)


        def __repr_extra__(self):

            return "Valid if label has been visited upto {} times".format(
                self.args[0] )


    class SeenTest(BaseTest):
        """
        Valid if the label passed as first argument has been visited 
        more than once (or number passed as second argument times)

        @usage:
    
            seen "other_label"

            or

            seen "other_label" 2
        """

        def post_init(self):

            self.count = int(self.args[1]) if len(self.args) > 1 else 1

        def test_valid(self):

            visits = self.event.handler._visits.get( self.args[0], [] )

            if len(visits) >= self.count:

                return True

            return False


        def __repr_extra__(self):

            return "Valid if label {} has been " \
                   "visited {} times or more".format(
                self.args[0], self.count )


    class SimpTest(BaseTest):
        """
        Valid if all the passed arguments resolve to true once eval'ed

        @usage:
    
            simp "string condition"

            or
    
            simp "string condition 1" "string condition 2"

            or

            simp:
                "string condition 1"
                "string condition 2"
        """

        def post_init(self):

            self.flatten_lists()


        def test_valid(self):

            return all( [ renpy.python.py_eval(k) for k in self.args ] )


        def __repr_extra__(self):

            return "Valid if {} ".format(
                " and ".join( ["({})".format(k) for k in self.args ] ) )


    class PathTest(BaseTest):
        """
        Valid if all the passed tests resolve to true

        @usage:
    
            path "location_name" 25 # no conditions

            or

            path:
                "location_name" 
                25
                # conditions as tests
                any:
                    all:
                        a_test "a_test_arg"
                        b_test "b_test_arg"
                    c_test "c_test_arg"
        """
        distance = 25

        def post_init(self):

            self.destination = self.args[0]

            try:
                self.args[1] = int(self.args[1])
            except:
                pass
 
            if (len(self.args) > 1 and isinstance(self.args[1], int)):

                self.distance = self.args[1]


        def test_valid(self):

            return all( [ k.valid for k in self.tests ] )


        def __repr_extra__(self):

            return "Path from here to {} is {} and {}m long".format(
                self.destination,
                "Open" if self.valid else "Closed",
                self.distance)


    class ArrowTest(BaseTest):
        """
        Just holds data

        @usage:
    
            arrow "location_name"

            or
    
            arrow "location_name" (100, 250)

            or

            arrow "location_name" "right" 150 240
        """
        direction = "left"
        xposition = 50
        yposition = 340

        def post_init(self):

            self.destination = self.args[0]

            if len(self.args) > 1:

                pos_values = 0

                for arg in self.args[1:]:

                    try:

                        arg = float(arg)

                        if arg > 1.0:

                            arg = int(arg)

                    except:

                        pass

                    if isinstance(arg, (int, float)):

                        setattr(self, "{}position".format(
                            'x' if not pos_values else 'y'), arg)

                        pos_values += 1

                    elif (arg[0], arg[-1]) in [('(',')'),('[',']')]:

                        pos = renpy.python.py_eval(arg)

                        self.xposition, self.yposition = pos

                        pos_values += 2

                    elif isinstance(arg, basestring):

                        self.direction = arg

                    else:

                        raise AttributeError, "ArrowTest got an invalid " \
                                              "argument {}".format(arg)

                    if pos_values > 2:

                        raise AttributeError, "ArrowTest received too many " \
                                              "position values"


        def test_valid(self):

            path_tests = [k for k in self.event.get_paths(False)
                          if k.destination == self.destination]

            if not path_tests:

                raise ValueError, "Arrow points from {} to {} yet there is " \
                                  "no similar PathTest".format(
                                    self.event.name, self.destination)

            return any( [p.valid for p in path_tests] )


        def get_button(self):

            return ImageButton(
                "images/arrow_{}_idle.png".format(self.direction),
                clicked=Jump(self.destination),
                anchor=(0.5,0.5),
                pos=(self.xposition, self.yposition))


    class OptionTest(BaseTest):
        """
        Just holds data and tests

        @usage:
    
            option:
                # arguments
                "argument" 
                25
                # conditions as tests
                any:
                    all:
                        a_test "a_test_arg"
                        b_test "b_test_arg"
                    c_test "c_test_arg"
        """

        def test_valid(self):

            return all( [ k.valid for k in self.tests ] )


        def __repr_extra__(self):

            return "Valid if all sub-tests are valid"
