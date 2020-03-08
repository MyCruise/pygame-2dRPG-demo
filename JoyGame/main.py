import os
import sys
import pygame
from pygame.locals import *
from sys import exit

# Character
from JoyGame.Src.Character.character import Character

# Include
from JoyGame.Src.Include.glovar import GLOVAR
from JoyGame.Src.Include.color import Color

# System
from JoyGame.Src.System.event import next_event
from JoyGame.Src.System.screen import Screen
from JoyGame.Src.System.music import Music
from JoyGame.Src.System.shape import Shape
from JoyGame.Src.System.text import Text
from JoyGame.Src.System.shape import Button
from JoyGame.Src.System.timer import Timer
from JoyGame.Src.System.picture import Picture

# Script
from JoyGame.Src.Script.initCharacter import InitCharacter
from JoyGame.Src.Script.menuControl import MenuControl

# Controller
from JoyGame.Src.Controller.controller import Controller

# UI
from JoyGame.Src.UI.menu import Menu
from JoyGame.Src.UI.map import Map
from JoyGame.Src.UI.Game import Games


class Game:
    def __init__(self):
        pygame.init()
        self.controller = Controller()
        self.glovar = GLOVAR()
        self.clock = pygame.time.Clock()

        self.color = Color()

        # Initialize class
        self.screen = Screen(self.color.White)
        self.timer = Timer()
        self.text = Text(self.screen.screen)
        self.shape = Shape(self.screen.screen)
        self.picture = Picture(self.screen, self.glovar)
        self.mc = MenuControl(self.controller, self.timer)
        self.games = Games(self.screen)
        self.menu = Menu(self.screen, self.text, self.clock, self.mc, self.games)
        self.button = Button(self.screen.screen, self.text)

        self.title_en = ""
        for letter in self.glovar.title_en_1.split(" "):
            self.title_en += letter
        self.title_en += " "
        for letter in self.glovar.title_en_2.split(" "):
            self.title_en += letter
        pygame.display.set_caption(self.title_en)

        # display information
        print("platform: \t\t" + sys.platform)
        print("revolution: \t" + str(self.screen.resolution))

        # initialize event
        self.MAINLOOP = next_event(pygame.USEREVENT)
        self.CONTROLLER = next_event(self.MAINLOOP)

        # initialize timer
        pygame.time.set_timer(self.MAINLOOP, 1)
        pygame.time.set_timer(self.CONTROLLER, 1)

        # initialize variable
        self.running = True
        self.ticks = 0
        self.lock_control = 0
        self.select_control_device = 0

    def process_event(self):
        for event in pygame.event.get():
            # Menu control by keyboard
            if event.type == KEYDOWN:
                self.mc.key_button_pressed = 1
                if event.key == K_ESCAPE:
                    self.running = False
                if event.key == K_w and self.timer.elapse() > 0.1:
                    self.mc.front()
                    self.timer.set_timer()
                elif event.key == K_s and self.timer.elapse() > 0.1:
                    self.mc.rear()
                    self.timer.set_timer()
                elif event.key == K_KP_ENTER and self.timer.elapse() > 0.1:
                    self.mc.enter_menu()
                    self.timer.set_timer()
            if event.type == KEYUP:
                self.controller.key_button_pressed = 0

            # Menu control by mouse
            if event.type == MOUSEBUTTONDOWN:
                self.controller.key_button_pressed = 1
            elif event.type == MOUSEBUTTONUP:
                self.controller.key_button_pressed = 0
            if event.type == MOUSEMOTION:
                self.controller.mouse_position = pygame.mouse.get_pos()

            if event.type == self.CONTROLLER:
                # Menu control by controller
                if self.lock_control and self.mc.layer in [1]:
                    self.mc.horizontal_control()

                elif self.lock_control and self.mc.layer in [2]:
                    self.mc.vertical_control()

                # Game control
            if event.type == self.MAINLOOP:
                pass

            # Joystick button pressed
            if event.type == pygame.JOYBUTTONDOWN:
                self.controller.joystick_button_pressed = 1

            # Joystick button released
            elif event.type == pygame.JOYBUTTONUP:
                self.controller.joystick_button_pressed = 0

    def update(self):
        self.process_event()
        self.controller.joystick()
        self.clock.tick(self.glovar.targetFPS)
        self.ticks = pygame.time.get_ticks() / 1000
        pygame.display.set_caption("Dungeon Adventure" + self.timer.num2time(self.ticks))

        # Layer 1
        if self.mc.layer == 1:
            self.mc.layer_name = "homepage"
        if self.mc.layer == 1 and self.mc.enter:
            # print(self.mc.index, self.mc.layer, self.mc.enter)
            if self.mc.index == 0:
                self.mc.layer_name = "play"
                self.mc.next()
            elif self.mc.index == 1:
                self.mc.layer_name = "setting"
                self.mc.next()
            elif self.mc.index == 2:
                self.mc.layer_name = "tutorial"
                self.mc.next()
            elif self.mc.index == 3:
                self.running = False

        # Layer 2
        elif self.mc.layer == 2 and self.mc.enter:
            if self.mc.index == 0:
                self.mc.layer_name = "start"
                self.mc.next()
            elif self.mc.index == 1:
                self.mc.layer_name = "create"
                self.mc.next()
            elif self.mc.index == 2:
                self.mc.layer_name = "load"
                self.mc.next()

        # Layer 3
        elif self.mc.layer == 3 and self.mc.layer_name == "start":
            if not self.mc.pause:
                self.mc.game_control(self.games.Fallen_Angels_2)
            else:
                self.mc.game_menu()
                if self.mc.index == 0 and self.mc.enter:
                    self.mc.pause = False
                    self.mc.enter = False
                elif self.mc.index == 1 and self.mc.enter:
                    self.mc.layer = 2
                    self.mc.index = 0
                    self.mc.enter = False
                    self.mc.layer_name = "setting"
                elif self.mc.index == 2 and self.mc.enter:
                    self.mc.layer = 1
                    self.mc.layer_name = "homepage"
                    self.mc.index = 0
                    self.mc.enter = False

    def display(self):
        # Loading interface
        if self.mc.layer == 0:
            self.menu.logo_page()
            if self.timer.elapse() > 12 and (
                    self.controller.joystick_button_pressed or self.controller.key_button_pressed):
                self.mc.layer += 1
                self.lock_control = 1
                self.timer.set_timer()

            if self.timer.elapse() > 12:
                self.screen.breath_color_lock = True
                self.menu.press_bar()

        # Homepage interface
        elif self.mc.layer == 1:
            self.menu.homepage()
            self.mc.pause = False

        # Layer 2
        elif self.mc.layer == 2:
            if self.mc.layer_name == "play":
                self.menu.play()

            elif self.mc.layer_name == "setting":
                self.menu.setting()

            elif self.mc.layer_name == "tutorial":
                self.menu.tutorial()

        # Layer 3
        elif self.mc.layer == 3:
            if self.mc.layer_name == "start":
                self.menu.game()
        if self.controller.controller and self.controller.last_controller:
            if self.controller.controller:
                image = self.picture.load_image("switchProController.png", (200, 200))
                self.picture.addImage(image, (int(self.screen.width / 2) - 100, int(self.screen.height) - 100))

        self.menu.test()
        # pygame.display.flip()
        pygame.display.update()

    def main(self):
        while self.running:
            if self.controller.detect_joysticks:
                self.controller.joystick()
            self.update()
            self.display()

    def run(self):
        self.main()


if __name__ == '__main__':
    main = Game()
    main.run()
