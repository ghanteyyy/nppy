import os
import sys
import json
import random
import pygame


class Enemy:
    '''
    Design of Enemy in the game
    '''

    def __init__(self, WIDTH, WIN):
        '''
        param:
            WIDTH   : Width of the pygame window
            WIN     : Screen to place sprites
        '''

        self.WIN = WIN
        self.EnemyImage = pygame.transform.scale(pygame.image.load(ResourcePath('Images', 'enemy.png')), (32, 32))
        self.EnemyWidth = self.EnemyImage.get_width()
        self.EnemyHeight = self.EnemyImage.get_height()

        self.EnemySpeed = 2

        self.random_pos = random.randrange(50, WIDTH - 50)
        self.EnemyRect = pygame.Rect(self.random_pos, random.randrange(-1000, -100), self.EnemyWidth, self.EnemyHeight)

    def move(self):
        self.EnemyRect.y += self.EnemySpeed

    def display(self):
        self.WIN.blit(self.EnemyImage, (self.EnemyRect.x, self.EnemyRect.y))


class Bullet:
    def __init__(self, UFORect, WIN):
        '''
        param:
            UFORect   : Rectangle object of UFO-Image-position
            WIN       : Screen to place sprites
        '''

        self.WIN = WIN
        self.BulletSpeed = 5
        self.UFORect = UFORect

        self.BulletImage = pygame.transform.scale(pygame.image.load(ResourcePath('Images', 'bullet.png')), (32, 32))
        self.BulletWidth = self.BulletImage.get_width()
        self.BulletHeight = self.BulletImage.get_height()

        self.BulletRect = pygame.Rect(self.UFORect.x + self.BulletImage.get_width() // 2, self.UFORect.y - 20, self.BulletWidth, self.BulletHeight)

    def move(self):
        self.BulletRect.y -= self.BulletSpeed

    def display(self):
        self.WIN.blit(self.BulletImage, (self.BulletRect.x, self.BulletRect.y))


class SpaceInvader:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.FPS = 60
        self.IsRunning = True
        self.BulletFireTimer = 0.15
        self.WIDTH, self.HEIGHT = 800, 600
        self.DataFile = ResourcePath(None, 'data.json')

        self.SetDefaults()

        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Space Invaders')

        # Sprites for games
        self.UFOImage = pygame.image.load(ResourcePath('Images', 'UFO.png'))
        self.IconImage = pygame.image.load(ResourcePath('Images', 'Icon.png'))
        self.Keys_2_Image = pygame.image.load(ResourcePath('Images', 'Keys2.png'))
        self.Keys_1_Image = pygame.image.load(ResourcePath('Images', 'Keys1.png'))
        self.ExplosionImage = pygame.image.load(ResourcePath('Images', 'Explosion.png'))
        self.PlayerDiedAudio = pygame.mixer.Sound(ResourcePath('Audios', 'PlayerDied.wav'))
        self.BulletFiredAudio = pygame.mixer.Sound(ResourcePath('Audios', 'BulletFired.wav'))
        self.EnemyExplodedAudio = pygame.mixer.Sound(ResourcePath('Audios', 'EnemyKilled.wav'))
        self.NoAudioImage = pygame.transform.scale(pygame.image.load(ResourcePath('Images', 'No Audio.png')), (32, 32))
        self.FullAudioImage = self.AudioImage = pygame.transform.scale(pygame.image.load(ResourcePath('Images', 'Audio.png')), (32, 32))
        self.BackgroundImage = pygame.transform.scale(pygame.image.load(ResourcePath('Images', 'background.png')), (self.WIDTH, self.HEIGHT))

        self.SpaceShipWidth = self.UFOImage.get_width()
        self.SpaceShipHeight = self.UFOImage.get_height()

        self.AudioRect = pygame.Rect(self.WIDTH - self.AudioImage.get_width(), self.AudioImage.get_height(), self.AudioImage.get_width(), self.AudioImage.get_height())

        pygame.display.set_icon(self.IconImage)

    def SetDefaults(self):
        '''
        Default values for game
        '''

        self.UFOSpeed = 5
        self.TotalScore = 0
        self.TotalHealth = 5
        self.TotalLevels = 0
        self.AllBullets = []
        self.AllEnemies = []
        self.IsMuted = False
        self.IsPaused = False
        self.IsSpedUp = False
        self.TotalEnemies = 2
        self.PlayerDied = False
        self.IsBulletFired = False
        self.CoolDownBulletTimer = 0
        self.IsWelcomeWindowShown = True
        self.HighScore = self.GetHighScore()

    def ReDraw(self):
        '''
        Update entire screen
        '''

        self.WIN.blit(self.BackgroundImage, (0, 0))

        for bullet in self.AllBullets:
            bullet.move()
            bullet.display()

        for enemy in self.AllEnemies:
            enemy.move()
            enemy.display()

        self.WIN.blit(self.UFOImage, (self.UFO_RECT.x, self.UFO_RECT.y))
        self.WIN.blit(self.AudioImage, (self.AudioRect.x, self.AudioRect.y))

        self.UpdateText()
        pygame.display.update()

    def DisplayText(self, text: str, size: int, color: tuple):
        '''
        Create Text Surface

        param:
            text    : Text
            size    : Size of text
            color   : Color of text
        '''

        Text = pygame.font.SysFont('Comic Sans MS', size)
        TextSurface = Text.render(text, True, color)

        return TextSurface

    def UpdateText(self):
        '''
        Update Health, Score and Levels text
        '''

        LivesText = self.DisplayText(f'Health: {self.TotalHealth}', 20, (255, 255, 255))
        ScoreText = self.DisplayText(f'Score: {self.TotalScore}', 20, (255, 255, 255))
        LevelText = self.DisplayText(f'Levels: {self.TotalLevels}', 20, (255, 255, 255))
        HighScoreText = self.DisplayText(f'HighScore: {self.HighScore}', 20, (255, 255, 255))

        self.WIN.blit(LevelText, (0, LevelText.get_height()))
        self.WIN.blit(ScoreText, (self.WIDTH - ScoreText.get_width(), 0))
        self.WIN.blit(LivesText, (0, 0))
        self.WIN.blit(HighScoreText, (self.WIDTH // 2 - HighScoreText.get_width() // 2, HighScoreText.get_height() - 20))

    def main(self):
        '''
        MainLoop
        '''

        clock = pygame.time.Clock()
        self.UFO_RECT = pygame.Rect(self.WIDTH // 2 - self.SpaceShipWidth // 2, self.HEIGHT - self.SpaceShipHeight, self.SpaceShipWidth, self.SpaceShipHeight)

        while self.IsRunning:
            clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.IsRunning = False

                if event.type == pygame.KEYDOWN:
                    if (event.key in [pygame.K_SPACE, pygame.K_s]) and self.IsPaused:
                        # Unpausing game when user presses space or 's' key when game is paused already
                        self.IsPaused = False

                    if event.key == pygame.K_p:  # When 'p' key is pressed
                        if self.IsWelcomeWindowShown is False:  # Checking if welcome window is not shown
                            if self.IsPaused:  # Unpausing game when 'p' key is pressed if the game is already paused
                                self.IsPaused = False

                            else:
                                # Pausing game when 'p' key is pressed
                                # if the game is not paused yet
                                self.IsPaused = True

                                PausedText = self.DisplayText('Paused !!!', 50, (255, 255, 255))
                                self.WIN.blit(PausedText, (self.WIDTH // 2 - PausedText.get_width() // 2, self.HEIGHT // 2 - PausedText.get_height() // 2))

                                pygame.display.update()

                    if self.PlayerDied:  # Checking if Player has died
                        if event.key == pygame.K_r:
                            # Restarting game when user presses 'r' key
                            # while GameOver window is being shown
                            self.SetDefaults()

                            self.WIN.blit(self.BackgroundImage, (0, 0))
                            self.UFO_RECT = pygame.Rect(self.WIDTH // 2 - self.SpaceShipWidth // 2, self.HEIGHT - self.SpaceShipHeight, self.SpaceShipWidth, self.SpaceShipHeight)
                            self.WIN.blit(self.UFOImage, (self.UFO_RECT.x, self.UFO_RECT.y))

                            pygame.display.update()

                        elif event.key == pygame.K_q:
                            # Quitting game when user presses 'q' key
                            # while GameOver window is being shown
                            self.IsRunning = False

                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_m) and self.IsWelcomeWindowShown is False:
                    # Muting and UnMuting when user press 'm' key
                    # or click the volume icon on the screen
                    AudioRect_X, AudioRect_Y = (self.AudioRect.x, self.AudioRect.y)

                    if pygame.mouse.get_pressed()[0]:
                        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()

                    else:
                        # Setting mouse position with respect of Audio Icon Image
                        # when user presses 'm' key. So, that code written to
                        # mute and unmute audio when left-mouse-button also
                        # works for the 'm' key
                        mouse_pos_x, mouse_pos_y = AudioRect_X + 5, AudioRect_Y + 2

                    # Checking if the mouse_pos is within the boundary of Audio-Image
                    if mouse_pos_x in range(AudioRect_X, AudioRect_X + self.AudioRect.width) and mouse_pos_y in range(AudioRect_Y, AudioRect_Y + self.AudioRect.height):
                        if self.IsMuted:  # Un-muting audio when already being muted
                            self.IsMuted = False
                            self.PlayerDiedAudio.set_volume(100)
                            self.BulletFiredAudio.set_volume(100)
                            self.EnemyExplodedAudio.set_volume(100)
                            self.AudioImage = self.FullAudioImage

                        else:  # Muting audio when audio is being played
                            self.IsMuted = True
                            self.AudioImage = self.NoAudioImage
                            self.PlayerDiedAudio.set_volume(0)
                            self.BulletFiredAudio.set_volume(0)
                            self.EnemyExplodedAudio.set_volume(0)

            if self.IsWelcomeWindowShown:  # Showing welcome text when game starts for the first time

                WelcomeText = self.DisplayText('Press any key to start', 50, (255, 255, 255))

                self.WIN.blit(self.BackgroundImage, (0, 0))
                self.WIN.blit(WelcomeText, (self.WIDTH // 2 - WelcomeText.get_width() // 2, WelcomeText.get_height() + 100))
                self.WIN.blit(self.Keys_1_Image, (self.WIDTH // 2 - self.Keys_1_Image.get_width() // 2, self.HEIGHT // 2 - WelcomeText.get_height() // 2 - self.Keys_1_Image.get_height() // 2 + 100))

                pygame.display.update()

                AnythingPressed = any(pygame.mouse.get_pressed()) or any(pygame.key.get_pressed())

                if AnythingPressed:  # Playing game when user presses any key or mouse-click
                    self.IsWelcomeWindowShown = False

            else:
                if self.IsPaused is False:
                    # Saving and Showing HighScore
                    HighScore = self.GetHighScore()

                    if self.TotalScore >= HighScore:
                        self.HighScore = self.TotalScore
                        self.SaveData()
                        self.UpdateText()

                    self.ReDraw()
                    keys = pygame.key.get_pressed()

                    if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # Move UFO to left when left-arrow or 'a' key is pressed
                        if self.UFO_RECT.x >= 4:
                            self.UFO_RECT.x -= self.UFOSpeed

                    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # Move UFO to right when right-arrow or 'd' key is pressed
                        if self.UFO_RECT.x + self.UFO_RECT.width <= self.WIDTH - 4:
                            self.UFO_RECT.x += self.UFOSpeed

                    if keys[pygame.K_SPACE] or keys[pygame.K_s]:  # Shoot bullets when space-key or 's' key is pressed
                        if self.IsBulletFired is False:
                            self.IsBulletFired = True
                            bullet = Bullet(self.UFO_RECT, self.WIN)
                            self.AllBullets.append(bullet)

                            self.BulletFiredAudio.play()

                    if self.IsBulletFired:
                        # Once bullet is fired then waiting
                        # 0.15 seconds to fire another one
                        if self.CoolDownBulletTimer <= self.FPS * self.BulletFireTimer:
                            self.CoolDownBulletTimer += 1

                        else:
                            self.IsBulletFired = False
                            self.CoolDownBulletTimer = 0

                    if len(self.AllEnemies) == 0:
                        # When the enemies are either killed or
                        # gone past the UFO then re-spawning 3
                        # more enemies combined with the current
                        # number of enemies
                        self.TotalLevels += 1
                        self.TotalEnemies += 3

                        for _ in range(self.TotalEnemies):
                            enemy = Enemy(self.WIDTH, self.WIN)
                            self.AllEnemies.append(enemy)

                    # Destroy Enemy when bullet touches enemy
                    for bullet in self.AllBullets:
                        if bullet.BulletRect.y <= 0:
                            if bullet in self.AllBullets:
                                self.AllBullets.remove(bullet)

                        for enemy in self.AllEnemies:
                            # Checking if bullet has came in contact with bullet
                            # If yes, then removing both bullet and enemy
                            if bullet.BulletRect.colliderect(enemy.EnemyRect) and enemy.EnemyRect.y >= 5:
                                if enemy in self.AllEnemies:
                                    self.AllEnemies.remove(enemy)

                                if bullet in self.AllBullets:
                                    self.AllBullets.remove(bullet)

                                self.TotalScore += 1
                                self.EnemyExplodedAudio.play()

                    for enemy in self.AllEnemies:
                        if enemy.EnemyRect.y + enemy.EnemyRect.height > self.UFO_RECT.y + 10:
                            # Deducting health when enemy goes past of UFO
                            self.TotalHealth -= 1

                            if self.TotalHealth == 0:
                                # Showing GameOver info
                                self.IsPaused = True
                                self.PlayerDied = True

                                self.ReDraw()
                                self.UpdateText()

                                GameOverText = self.DisplayText(f'Game Over', 80, (255, 0, 0))

                                self.WIN.blit(GameOverText, (self.WIDTH // 2 - GameOverText.get_width() // 2, GameOverText.get_height()))
                                self.WIN.blit(self.ExplosionImage, (self.UFO_RECT.x, self.UFO_RECT.y - 15))
                                self.WIN.blit(self.Keys_2_Image, (self.WIDTH // 2 - self.Keys_2_Image.get_width() // 2 + 10, self.HEIGHT // 2 - GameOverText.get_height() // 2 - self.Keys_2_Image.get_height() // 2 + 100))

                                self.PlayerDiedAudio.play()
                                pygame.display.update()

                            else:
                                self.AllEnemies.remove(enemy)

                    if self.TotalLevels % 5 == 0:
                        # When levels is a multiple of 5
                        # then increasing the speed of UFO
                        if self.IsSpedUp is False:
                            self.IsSpedUp = True
                            self.UFOSpeed += 1

                    else:
                        self.IsSpedUp = False

        pygame.quit()

    def SaveData(self):
        '''
        Save HighScore value to the file
        '''

        content = {
            'HighScore': self.HighScore
        }

        with open(self.DataFile, 'w') as WDF:
            json.dump(content, WDF, indent=4)

    def GetHighScore(self):
        '''
        Get HighScore from the file
        '''

        try:
            with open(self.DataFile, 'r') as RDF:
                contents = json.load(RDF)
                HighScore = contents['HighScore']

        except (json.JSONDecodeError, FileNotFoundError):
            HighScore = 0

        return HighScore


def ResourcePath(_dir, file_name):
    '''
    Get absolute path to resource from temporary directory

    In development:
        Gets path of files that are used in this script like icons, images or
        file of any extension from current directory

    After compiling to .exe with pyinstaller and using --add-data flag:
        Gets path of files that are used in this script like icons, images or
        file of any extension from temporary directory
    '''

    try:
        base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

    except AttributeError:
        base_path = os.path.dirname(__file__)

    if _dir:
        return os.path.join(base_path, 'Assets', _dir, file_name)

    return os.path.join(base_path, 'Assets', file_name)



if __name__ == '__main__':
    SpaceInvader = SpaceInvader()
    SpaceInvader.main()
