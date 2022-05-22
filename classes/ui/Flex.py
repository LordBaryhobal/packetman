#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.ui.Constraints import Absolute
from .Component import Component
from classes.Logger import Logger
import pygame

class Flex(Component):
    def __init__(self, name=None, dir_="col", justify="space-evenly", gap=0):
        """Initializes a Flex instance

        Keyword Arguments:
            name {str} -- component's name (default: {None})
            dir_ {str} -- flex direction, one of: "col","row" (default: {"col"})
            justify {str} -- flex justification, one of: "space-between","space-around","space-evenly" (default: {"space-evenly"})
            gap {int} -- minimum gap between children in pixels (default: {0})
        """

        super().__init__(name)
        
        self.dir = dir_
        self.justify = justify
        self.scroll = 0
        self.max_scroll = 0
        self.gap = gap
    
    def render(self, surface):
        """Renders the component

        Arguments:
            surface {pygame.Surface} -- surface to render the component on
        """

        if self.visible:
            tmp_surf = surface.copy()
            x, y, w, h = self.get_shape()

            if not self.bg_color is None:
                pygame.draw.rect(tmp_surf, self.bg_color, [x, y, w, h])

            gaps = 0

            if self.justify == "space-between":
                gaps = self.gap*(len(self.children)-1)
            elif self.justify == "space-around":
                gaps = self.gap*(len(self.children))
            elif self.justify == "space-evenly":
                gaps = self.gap*(len(self.children)+1)
            

            if self.dir == "col":
                min_size = sum([child.get_h() for child in self.children])+gaps
                remainder = h-min_size
            else:
                min_size = sum([child.get_w() for child in self.children])+gaps
                remainder = w-min_size
            
            self.max_scroll = min_size-h
            current = -self.scroll
            remainder = max(0, remainder)

            if remainder < 0:
                #Logger.warn("Flex overflow")
                pass
            
            gap = self.gap
            if self.justify == "space-between":
                gap = remainder / (len(self.children)-1)
                gap = max(gap, self.gap)
            
            elif self.justify == "space-around":
                gap = remainder / len(self.children)
                gap = max(gap, self.gap)
                current += gap/2
            
            elif self.justify == "space-evenly":
                gap = remainder / (len(self.children)+1)
                gap = max(gap, self.gap)
                current += gap

            for child in self.children:
                constr = Absolute(current)
                constr._automatic = True

                if self.dir == "col":
                    child.cm.set_y(constr)
                else:
                    child.cm.set_x(constr)
                
                child.render(tmp_surf)

                if self.dir == "col":
                    current += child.get_h()
                else:
                    current += child.get_w()
                
                current += gap
            
            #Scrollbar
            if min_size > h:
                sb_h = h*h/min_size
                sb_y = self.scroll/self.max_scroll * (h-sb_h)
                pygame.draw.rect(tmp_surf, (255,255,255), [x+w-5, y+sb_y, 5, sb_h])

            surface.blit(tmp_surf, [x, y], [x, y, w, h])
    
    def on_click(self, event):
        """Callback called when the component is scrolled

        Arguments:
            event {pygame.Event} -- pygame MOUSEBUTTONDOWN event

        Returns:
            bool -- True if event has been handled and shouldn't be passed further, False otherwise
        """

        scroll = self.scroll

        if event.button == 4:
            self.scroll -= 10
            self.scroll = max(0, min(self.max_scroll, self.scroll))
            if scroll != self.scroll: self.set_changed(2)
            return True
        
        elif event.button == 5:
            self.scroll += 10
            self.scroll = max(0, min(self.max_scroll, self.scroll))
            if scroll != self.scroll: self.set_changed(2)
            return True
        
        return False