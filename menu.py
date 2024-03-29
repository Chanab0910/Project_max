import pygame as pg
from spritess import Button, Label, MusicSlider


class Menu:
    def __init__(self, game):
        self.game = game
        self.elements = pg.sprite.Group()
        self.image = None
        self.music = None
        self.volume = self.game.volume

    def run(self):
        self.game.in_menu = True
        while self.game.in_menu:
            self.check_events()
            self.game.display.fill("red")
            if self.image is not None:
                self.game.display.blit(self.image, (0, 0))
            for element in self.elements:
                if isinstance(element, MusicSlider):
                    element.draw(self.volume)
                else:
                    element.draw()

            pg.display.update()
            self.game.clock.tick(165)

    def check_events(self):
        if pg.mouse.get_pressed()[0] == 1:
            for element in self.elements:
                if isinstance(element, MusicSlider):
                    if element.is_hovered():
                        mouse_pos = pg.mouse.get_pos()
                        percentage = ((mouse_pos[0] - element.x) // (element.width / 100)) / 100
                        self.volume = 1 * percentage
                        pg.mixer.music.set_volume(self.volume)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.running = False
                self.game.in_menu = False
            if event.type == pg.MOUSEBUTTONDOWN:
                for element in self.elements:
                    if isinstance(element, Button):
                        if element.is_hovered():
                            # match-case block for button function
                            match element.low:
                                case "quit":
                                    self.game.running = False
                                case "play":
                                    self.game.change_state(2)
                                case "options":
                                    self.game.change_state(3)
                                case "back":
                                    self.game.state_stack.pop()
                                case "level 1":
                                    self.game.change_state(4)
                                    self.game.level_pointer = 1
                                case "level 2":
                                    self.game.change_state(4)
                                    self.game.level_pointer = 2
                                case "restart":
                                    self.game.state_stack.pop()
                                    self.game.states[self.game.state_stack[-1]].restart()
                                case "class 1":
                                    if self.game.level_pointer == 1:
                                        self.game.change_state(5)
                                    else:
                                        self.game.change_state(7)
                                    self.game.class_choice = 1
                                case "class 2":
                                    if self.game.level_pointer == 1:
                                        self.game.change_state(5)
                                    else:
                                        self.game.change_state(7)
                                    self.game.class_choice = 2
                                case "main menu":
                                    self.game.reset_state_stack()
                                    self.game.in_game = False
                                case "quit game":
                                    self.game.in_game = False
                                    self.game.running = False
                                case "resume":
                                    self.game.state_stack.pop()
                                case "play again":
                                    self.game.state_stack.pop()
                                    self.game.states[self.game.state_stack[-1]].restart()
                                case "next level":
                                    self.game.level_pointer = 2
                                    self.game.change_state(4)
                            self.game.in_menu = False


class StartMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.image = self.game.images['menu_background']
        self.image = pg.transform.scale(self.image, (1280, 720))
        button = Button(self.game, (540, 410), (200, 100), 'play', 50)
        label = Label(self.game, (540, 100), (200, 100), 'PMPG', 50)
        end = Button(self.game, (540, 560), (200, 100), 'quit', 50)
        options = Button(self.game, (50, 600), (250, 100), 'options', 50)
        self.elements.add(button, label, end, options)


class LevelMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.image = self.game.images['menu_background']
        self.image = pg.transform.scale(self.image, (1280, 720))
        level1 = Button(self.game, (540, 410), (200, 100), 'Level 1', 50)
        level2 = Button(self.game, (540, 510), (200, 100), 'Level 2', 50)
        levels = Label(self.game, (540, 100), (200, 100), 'Levels', 50)
        back = Button(self.game, (50, 600), (250, 100), 'back', 50)
        self.elements.add(level1, level2, levels, back)


class OptionsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        title = Label(self.game, (540, 100), (200, 100), 'Volume', 50)
        back = Button(self.game, (50, 600), (250, 100), 'back', 50)
        volume_slider = MusicSlider(self.game.display, (390, 300), (500, 50))
        self.elements.add(title, back, volume_slider)


class ClassMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        title = Label(self.game, (540, 100), (200, 100), 'Pick Your Class', 50)
        class1 = Button(self.game, (540, 410), (200, 100), 'class 1', 50)
        class2 = Button(self.game, (540, 510), (200, 100), 'class 2', 50)
        back = Button(self.game, (50, 600), (250, 100), 'back', 50)
        self.elements.add(title, class1, class2, back)


class GameSettingsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        title = Label(self.game, (540, 100), (200, 100), 'Settings', 50)
        resume = Button(self.game, (500, 300), (280, 100), 'resume', 50)
        restart = Button(self.game, (500, 450), (280, 100), 'restart', 50)
        main_menu = Button(self.game, (500, 600), (280, 100), 'main menu', 50)
        quit_game = Button(self.game, (800, 600), (120, 120), 'quit game', 50)
        self.elements.add(title, resume, restart, main_menu, quit_game)


class PostGameMenu(Menu):
    def __init__(self, game):
        super().__init__(game)

    def create_buttons(self, status):
        if status == 1:
            title = Label(self.game, (540, 100), (200, 100), 'Victory', 50)
        else:
            title = Label(self.game, (540, 100), (200, 100), 'Defeat', 50)
        if self.game.level_pointer == 1 and status == 1:
            next_level = Button(self.game, (500, 300), (280, 100), 'Next Level', 50)
            play_again = Button(self.game, (500, 450), (280, 100), 'Play Again', 50)
            main_menu = Button(self.game, (500, 600), (280, 100), 'Main Menu', 50)
            self.elements.add(title, next_level, play_again, main_menu)
        else:
            play_again = Button(self.game, (500, 300), (280, 100), 'Play Again', 50)
            main_menu = Button(self.game, (500, 450), (280, 100), 'Main Menu', 50)
            self.elements.add(title, play_again, main_menu)
