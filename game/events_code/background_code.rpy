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

            if True:#current_values != self.monitor_values:

                self.monitor_values = current_values

                used_bg = "images/bg/missing_background.png"

                poss_bg = "images/bg/{}.png".format(current_location)

                bg = [k for k in eh.background
                      if k.location == current_location]

                if len(bg) > 1:

                    raise ValueError, "Multiple background labels found for" \
                                      "{}".format(current_location)

                layers = []

                if bg:

                    poss_bg = "images/bg/{}.png".format(
                        bg[0].get_background())

                    layers = bg[0].get_layers()

                if renpy.loadable(poss_bg):

                    used_bg = poss_bg 

                if layers:
                    # A Composite
                    self.cache = Composite(
                        (config.screen_width, config.screen_height),
                        (0,0), used_bg,
                        *[j for k in layers for j in k])

                else:

                    self.cache = used_bg

            return self.cache, 0.1


        def predict_images(self):

            return [ self.cache ]


image bg = DynamicBackground()