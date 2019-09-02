init python:

    class DynamicSprite(renpy.display.layout.DynamicDisplayable):
        """
        A dynamic image that returns a sprite for the character

        @args:
            character ref: Just the character id
        """

        def __init__(self, *args, **kwargs):

            self.id = args[0]

            self.character = getattr(character, self.id, None)

            if not self.character:

                raise AttributeError, "No Character found for ref {}".format(
                    self.id)

            self.tag = self.character.image_tag

            self.stats = None

            self.previous_working_attrs = []

            kwargs.update( {
                '_predict_function' : self.predict_images } )

            super(DynamicSprite, self).__init__(self.get_sprite, **kwargs )


        def get_sprite(self, st, at):

            tag_attrs = []

            dialogue_attrs = renpy.get_attributes("ari")

            if not self.stats:

                self.stats = globals().get(self.id, None)

            if self.stats and self.stats.outfit:

                tag_attrs.append( self.stats.outfit )

            if self.stats and self.stats.state:

                tag_attrs.append( self.stats.state )

            elif dialogue_attrs:

                tag_attrs.extend(dialogue_attrs)

            else:

                tag_attrs.append('normal')

            ordered_attrs = renpy.check_image_attributes(self.tag, tag_attrs)

            if ordered_attrs:

                self.previous_working_attrs = ordered_attrs

            tag_image = self.tag

            if self.previous_working_attrs:

                tag_image = "{} {}".format(
                    tag_image,
                    " ".join(self.previous_working_attrs) )

            return tag_image, 0.05


        def predict_images(self):

            return []