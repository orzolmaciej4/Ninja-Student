import pygame
import sys
from scripts.settings import settings

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font("data\images\ARCADEPI.TTF", 40)
        self.font = pygame.font.Font("data\images\ARCADEPI.TTF", 20)

        self.buttons = [
            {"text": "Start Game", "action": "start"},
            {"text": "Settings", "action": "settings"},
            {"text": "Controls and Instructions", "action": "controls"},
            {"text": "Quit", "action": "quit"}
        ]
        self.selected_button = 0
                
        self.sfx = {
            'button': pygame.mixer.Sound('data/sfx/button.mp3'),
            'enter': pygame.mixer.Sound('data/sfx/enter.mp3'),
        }
        
        self.sfx['enter'].set_volume(0.8)
        self.sfx['button'].set_volume(0.1)
                                
    def run(self):
        pygame.mixer.music.load('data/music.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_button = (self.selected_button - 1) % len(self.buttons)
                        self.sfx['button'].play()
                    elif event.key == pygame.K_DOWN:
                        self.selected_button = (self.selected_button + 1) % len(self.buttons)
                        self.sfx['button'].play()
                    elif event.key == pygame.K_RETURN:
                        action = self.buttons[self.selected_button]["action"]
                        self.sfx['enter'].play()
                        if action == "start":
                            self.show_backstory()
                            return
                        elif action == "settings":
                            self.show_settings()
                        elif action == "controls":
                            self.show_controls()
                        elif action == "quit":
                            pygame.quit()
                            sys.exit()

            self.screen.fill((0, 0, 0))
            
            title_text = self.font_title.render("Ninja Student", True, (255, 255, 255))
            self.screen.blit(title_text, (150, 50))
            
            for i, button in enumerate(self.buttons):
                color = (255, 255, 255) if i == self.selected_button else (150, 150, 150)
                text = self.font.render(button["text"], True, color)
                self.screen.blit(text, (150, 150 + i * 50))
            pygame.display.flip()

    def show_backstory(self):
        backstory_text = [
            "In the mystical land of Durham,",
            "you are a young and hard working student.",
            "On your morning walk you notice that",
            "the city centre has been overrun by evil ",
            "men, and for some unknown reason you decide ",
            "that you of all people must stop them",
            "to save Durham.",
            "",
            "Your goal is to navigate through Durham", 
            "and save the city using the ninja skills",
            "you never even knew you had.",
            "",
            "Press ENTER to try and save Durham!"
        ]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return

            self.screen.fill((0, 0, 0))
            for i, line in enumerate(backstory_text):
                text = self.font.render(line, True, (255, 255, 255))
                self.screen.blit(text, (10, 50 + i * 30))
            pygame.display.flip()
    
    def show_settings(self):
        selected_button = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.difficulty = ["Easy", "Normal", "Hard"][selected_button]
                        settings["global_difficulty"] = self.difficulty
                        return
                    elif event.key == pygame.K_UP:
                        selected_button = (selected_button - 1) % 3
                    elif event.key == pygame.K_DOWN:
                        selected_button = (selected_button + 1) % 3
                        
            self.screen.fill((0, 0, 0))
            for i, option in enumerate(["Easy", "Normal", "Hard"]):
                color = (255, 255, 255) if i == selected_button else (150, 150, 150)
                text = self.font.render(option, True, color)
                self.screen.blit(text, (150, 150 + i * 50))
            pygame.display.flip()

    def show_controls(self):
        controls_text = [
            "Controls:",
            "-----------",
            "Arrow keys: Move and Jump",
            "X key: Dash Attack",
            "",
            "Instructions:",
            "------",
            "Collect coins in boxes to increase lives",
            "You can find a little surprise in red bushes",
            "Defeat all the enemies in each level to progress",
            "",
            "Press ENTER to go back to the main menu"
        ]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return

            self.screen.fill((0, 0, 0))
            for i, line in enumerate(controls_text):
                text = self.font.render(line, True, (255, 255, 255))
                self.screen.blit(text, (10, 50 + i * 30))
            pygame.display.flip()