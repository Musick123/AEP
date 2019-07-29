init python:

    #
    # This could be extended to provide tinting or compositing etc
    #

    class DynamicBackground(renpy.display.layout.DynamicDisplayable):
        """
        A dynamic background that knows what to show
        """

        def __init__(self, *args, **kwargs):

            self.monitor_vars = [
                "current_location"
            ]

            self.monitor_values = []

            self.cache = None

            kwargs.update( {
                '_predict_function' : self.predict_images } )

            super(DynamicBackground, self).__init__(self.get_background, 
                                                    *args, 
                                                    **kwargs )

        def get_monitored_values(self):
            return [ globals().get(k) for k in self.monitor_vars ]

        def get_background(self, st, at, *args, **kwargs):
            """
            Return background image to use for this time
            """
            current_values = self.get_monitored_values()

            if current_values != self.monitor_values:

                self.monitor_values = current_values

                img = "images/bg/{}.png".format(current_location)

                if not renpy.loadable(img):

                    img = "images/bg/missing_background.png"

                self.cache = img

            return self.cache, 0.1


        def predict_images(self):

            return [ self.cache ]


image bg = DynamicBackground()