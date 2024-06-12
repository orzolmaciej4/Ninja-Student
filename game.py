import pygame, os, sys, math, random
from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.menu import Menu
from scripts.settings import settings


class Game:
    def __init__(self):
        pygame.init()

        #Game title
        pygame.display.set_caption('Ninja Student')
        
        #screen initialisations
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        
        self.movement = [False, False]
        
        #assets
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
        }
        
        #declaring sound effects and setting volume
        self.sfx = {
            'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
            'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
            'shoot': pygame.mixer.Sound('data/sfx/shoot.wav'),
            'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
            'coin': pygame.mixer.Sound('data/sfx/coin.mp3'),
            'item': pygame.mixer.Sound('data/sfx/item.mp3'),
        }
        self.sfx['ambience'].set_volume(0.2)
        self.sfx['shoot'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.8)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['jump'].set_volume(0.7)
        self.sfx['coin'].set_volume(0.5)
        self.sfx['item'].set_volume(0.5)
        
        #fonts
        self.text_font = pygame.font.Font("data\images\ARCADEPI.TTF", 10)
        self.text_large_font = pygame.font.Font("data\images\ARCADEPI.TTF", 20)

        self.clouds = Clouds(self.assets['clouds'], count=16)
        
        self.player = Player(self, (50, 50), (8, 15))
        
        self.tilemap = Tilemap(self, tile_size=16)
        
        self.level = 0
        self.load_level(self.level)
        
        self.screenshake = 0
        
        #give the player a different amount of lives and coins at the start of the game
        self.difficulty = settings["global_difficulty"]
        if self.difficulty == "Easy":
            self.i_lives = 5
            self.i_collectibles = 5
        elif self.difficulty == "Normal":
            self.i_lives = 3
            self.i_collectibles = 0
        else:
            self.i_lives = 1
            self.i_collectibles = 0
            
        self.lives = self.i_lives
        self.collectibles = self.i_collectibles
        
    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')
        
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 3)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))
            
        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))
        
        self.boxes = []
        for box in self.tilemap.extract([('decor', 3)], keep=True):
            self.boxes.append(pygame.Rect(4 + box['pos'][0], 4 + box['pos'][1], 5, 5))
        
        self.bushes = []
        for bush in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.bushes.append(pygame.Rect(4 + bush['pos'][0], 4 + bush['pos'][1], 20, 10))
          
        self.projectiles = []
        self.particles = []
        self.sparks = []
        
        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30
        
    #displays text on top of the game screen
    def draw_text(self, text, font, colour, x, y):
        img = font.render(text, False, colour)
        self.display_2.blit(img, (x,y))
    
    #a screen which appears once you complete the game  
    def show_end_screen(self):
        end_text = [
            "Congratulations, brave student!",
            "You have successfully saved the city!",
            "Thanks to you everyone is safe and most",
            "importantly, the cathedral wasn't damaged!",
            "You are a true hero of Durham!",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "Press ENTER to return to the main menu."
        ]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return

            self.screen.fill((0, 0, 0))
            for i, line in enumerate(end_text):
                text = self.text_large_font.render(line, True, (255, 255, 255))
                self.screen.blit(text, (50, 50 + i * 30))
            pygame.display.flip()
        
    def run(self):
        #game music
        pygame.mixer.music.load('data/music.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        
        self.sfx['ambience'].play(-1)
        
        while True:
            self.display.fill((0, 0, 0, 0))
            self.display_2.blit(self.assets['background'], (0, 0))
            
            self.screenshake = max(0, self.screenshake - 1)
            
            #checks if all enemies have been defeated and can then move on to the nect level
            if not len(self.enemies):
                self.transition += 1
                if self.transition > 30:
                    if self.level == len(os.listdir('data/maps')) - 1:
                        self.show_end_screen()
                        return #returns the player back to the main menu
                    else:
                        self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                        self.load_level(self.level)
            if self.transition < 0:
                self.transition += 1
            
            #checks if the player is dead to display the transition and remove a life
            if self.dead:
                self.dead += 1
                if self.dead >= 10:
                    self.transition = min(30, self.transition + 1)
                if self.dead > 40:
                    self.lives -= 1
                    #if the player has run out of lives then the game restarts
                    if self.lives <= 0:
                        self.lives = self.i_lives
                        self.collectibles = self.i_collectibles
                        self.level = 0
                    self.load_level(self.level)
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))
            
            self.clouds.update()
            self.clouds.render(self.display_2, offset=render_scroll)
            
            self.tilemap.render(self.display, offset=render_scroll)
            
            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)
            
            for box in self.boxes.copy():
                if self.player.rect().colliderect(box):
                    self.boxes.remove(box)
                    self.collectibles += 1
                    self.sfx['coin'].play()
                    
            for bush in self.bushes.copy():
                if self.player.rect().colliderect(bush):
                    self.bushes.remove(bush)
                    self.lives += 1 if random.random() > 0.5 else -1
                    self.sfx['item'].play()
 
            if self.collectibles == 10:
                self.collectibles = 0
                self.lives += 1
            
            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)
            
            # [[x, y], direction, timer]
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.dead += 1
                        self.sfx['hit'].play()
                        self.screenshake = max(16, self.screenshake)
                        for i in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                        
            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)
            
            #provides some of the environment sprites and tiles with an outline
            display_mask = pygame.mask.from_surface(self.display)
            display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.display_2.blit(display_sillhouette, offset)
            
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)
            
            #handles game events such as quitting and player inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #player movement and dash
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        if self.player.jump():
                            self.sfx['jump'].play()
                    if event.key == pygame.K_x:
                        self.player.dash()
                    #go back to main menu
                    if event.key == pygame.K_ESCAPE:
                        return
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
            
            #transition which appears when changing levels or when the player dies            
            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))
                
            self.display_2.blit(self.display, (0, 0))
            
            self.draw_text("Lives: " + str(self.lives), self.text_font, (0,0,0), 5, 5)
            self.draw_text("Enemies: " + str(len(self.enemies)), self.text_font, (0,0,0), 125, 5)
            self.draw_text("Coins: " + str(self.collectibles), self.text_font, (0,0,0), 265, 5)
            
            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), screenshake_offset)
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Ninja Student')
    
    #loops the menu and game classes so that the player can go back to the menu once they complete the game
    while True:
        menu = Menu(screen)
        menu.run()  # Run the menu
        game = Game()
        game.run()  # Start the game loop after exiting the menu