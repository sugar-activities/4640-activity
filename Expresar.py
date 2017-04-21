# Copyright 2012 Miguel Ruiz Diaz, Pedro Amarilla
# Actividad que permite a los usuarios con problemas motrices expresarse a traves de un teclado conceptual

import gtk
import pygtk
import gobject
import logging
import math
from sintetizar import sintetizar
from gettext import gettext as _
from parsear import parsear
from sugar.activity import activity
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import ActivityButton
from sugar.activity.widgets import ActivityToolbox
from sugar.activity.widgets import TitleEntry
from sugar.activity.widgets import StopButton
from sugar.activity.widgets import ShareButton

DELAY = 1000
LENGHT = 4

class Expresar(activity.Activity):
    """Expresar class as specified in activity.info"""

    def __init__(self, handle):
        """Set up the Expresar activity."""
        activity.Activity.__init__(self, handle)


        # toolbar with the new toolbar redesign
        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        title_entry = TitleEntry(self)
        toolbar_box.toolbar.insert(title_entry, -1)
        title_entry.show()

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()
    
        self._pressButton_counter = 0
        self.listaSecciones = []
        parsear(self.listaSecciones)
        self.lenghtSecciones = int(math.sqrt(len(self.listaSecciones)))

        self.hbox = gtk.HBox()
    
        self.table = gtk.Table(LENGHT, LENGHT, True)
        self.indiceSecciones = 0
        self.create_interior(self.table, self.listaSecciones)
        self.set_canvas(self.hbox)
        self.hbox.show()
        self._button_index = 0
        self._button_index_2 = 0
        self._indice = 0
        self._button_list = []
        gobject.timeout_add(DELAY, self.__timeout_cb, self.table)
        
    def create_interior(self, table, listaSecciones):
        self.hbox.add(table)
        inicio_left = 0
        fin_right = 1
        inicio_top = 0
        fin_bottom = 1
        indiceListaSecciones = 0
        for colu in range(LENGHT):
            for fila in range(LENGHT):
                #boton = gtk.Button(str(fila)+"-"+str(colu))
                boton = gtk.Button(self.listaSecciones[indiceListaSecciones][1])
                image = gtk.Image()
                image.set_from_file("icons/"+str(self.listaSecciones[indiceListaSecciones][2]))
                boton.set_image(image)
                boton.connect('key-press-event', self.__pressButton_count)
                table.attach(boton, inicio_left, fin_right, inicio_top, fin_bottom)
                boton.show()
                indiceListaSecciones = indiceListaSecciones + 1
                inicio_top = inicio_top + 1
                fin_bottom = fin_bottom + 1
                
            inicio_top = 0
            fin_bottom = 1
            inicio_left = inicio_left + 1
            fin_right = fin_right + 1

        #self.table.attach(child, left_attach, right_attach, top_attach, bottom_attach)
        table.show()
    def __pressButton_count(self, table, arg):
        self._pressButton_counter = self._pressButton_counter + 1

    def __timeout_cb(self, table):
        buttons = table.get_children()
        buttons.reverse()
        
        if (self._pressButton_counter == 1):
            self._button_index_2 = (self._button_index_2 + 1) % len(self._button_list)
            self._button_list[self._button_index_2].grab_focus()
            self._button_list[self._button_index_2].modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('red'))
            self._button_list[self._button_index_2 - 1].modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('green'))
        elif (self._pressButton_counter == 0):
            self._button_index = (self._button_index) % len(buttons)

            self._button_list = buttons[self._button_index:self._button_index+LENGHT]
            self._button_list[0].grab_focus()
            for i in self._button_list:
                i.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('green'))
            
            for cero in range(self._button_index):
                buttons[cero].modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('blue'))
                
            self._button_index = self._button_index + LENGHT
            
            indice = self._button_index
            while indice < len(buttons):
                buttons[indice].modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('blue'))
                indice = indice + 1
            
        else:
            self._pressButton_counter = 0
            self.__newWindow(self._button_list[self._button_index_2], self._button_list[self._button_index_2].get_label())
        
        return True
    def __newWindow(self, button, button_label):
        #self.hbox.remove(self.table)
        #label = gtk.Label()
        #label.set_text(button_label)
        #self.hbox.add(label)
        #label.show()
        #self.hbox.show()
        sintetizar(button_label)
