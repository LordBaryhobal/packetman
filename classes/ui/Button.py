#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Label import Label
import pygame

class Button(Label):
    def __init__(self, text="", callback=lambda *args, **kwargs: None, args=(), halign="center", valign="center", font_size=30, name=None):
        """Initializes a Button instance

        A button can display a label and call a callback when clicked (see `on_release`)

        Keyword Arguments:
            text {str} -- button label (default: {""})
            callback {function} -- function to be called when the button is pressed (default: {nop})
            args {tuple} -- arguments to pass to callback (default: {()})
            halign {str} -- horizontal label alignment, one of: "left", "center", "right" (default: {"center"})
            valign {str} -- vertical label alignment, one of: "top", "center", "bottom" (default: {"center"})
            font_size {int} -- label font size (default: {30})
            name {str} -- component name (default: {None})
        """

        super().__init__(text, halign, valign, font_size, name)
        self.callback = callback
        self.args = args
    
    def render(self, surface):
        """Renders the component

        Arguments:
            surface {pygame.Surface} -- surface to render the component on
        """

        color = (255,150,50) if self.hover else (200, 100, 0)
        pygame.draw.rect(surface, color, self.get_shape())
        super().render(surface)
    
    def on_release(self, event):
        """Callback called when the component is released (after being pressed)

        If it was pressed with the left button, the button's callback is called

        Arguments:
            event {pygame.Event} -- pygame MOUSEBUTTONUP event

        Returns:
            bool -- True if event has been handled and shouldn't be passed further, False otherwise
        """

        if event.button == 1:
            return self.callback(self, *self.args)
        
        return False