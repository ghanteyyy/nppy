import os
import sys
import json
import random
import pygame


class Snake:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.SetDefaults()

        self.FoodsImages = []
        self.FruitsImagePath = self.ResourcePath('Images', 'Fruits')

        for image in os.listdir(self.FruitsImagePath):
            image_path = os.path.join(self.FruitsImagePath, image)
            image_load = pygame.image.load(image_path)
            resized_image = pygame.transform.scale(image_load, (32, 32))

            self.FoodsImages.append(resized_image)

        self.GameOverAudio = self.ResourcePath('Audio', 'Game Over.mp3')
        self.IconImage = pygame.image.load(self.ResourcePath('Images', 'icon.png'))
        self.InfoImage = pygame.transform.scale(pygame.image.load(self.ResourcePath('Images', 'Keys1.png')), (512, 512))
        self.GameOverInfoImage = pygame.transform.scale(pygame.image.load(self.ResourcePath('Images', 'Keys2.png')), (350, 350))
        self.BackgroundImage = pygame.transform.scale(pygame.image.load(self.ResourcePath('Images', 'background.png')), (self.WIDTH, self.HEIGHT))

    def SetDefaults(self):
        '''
        Default values for the game
        '''

        self.FPS = 25
        self.Score = 0
        self.Direction = ''
        self.SnakeBody = []
        self.SnakeLength = 1
        self.FoodAte = False
        self.GameOver = False
        self.IsPaused = False
        self.IsRunning = True
        self.HasStarted = False
        self.FoodDisplayed = False
        self.LengthOfEachPiece = 15
        self.GameOverAudioPlayed = False
        self.WIDTH, self.HEIGHT = 800, 600
        self.DataFile = self.ResourcePath(None, 'data.json')

        SnakeHead = pygame.Rect(self.WIDTH // 2 - self.LengthOfEachPiece // 2, self.HEIGHT // 2 - self.LengthOfEachPiece // 2,
                                self.LengthOfEachPiece, self.LengthOfEachPiece)
        self.SnakeBody.append(SnakeHead)

    def ChangePositionOfSnakeBody(self):
        '''
        Change the position of preceding block with the successive block. For
        example: 2nd block gets the position of 1st block, 3rd block gets the
        position of 2nd block and so on.
        '''

        if self.HasStarted:
            for i in range(self.SnakeLength - 1, 0, -1):
                self.SnakeBody[i].x = self.SnakeBody[i - 1].x
                self.SnakeBody[i].y = self.SnakeBody[i - 1].y

    def GrowSnake(self):
        '''
        Increase the length of the snake by one block whenever snake eats food
        '''

        self.Score += 1
        self.SnakeLength += 1
        SnakeNewBody = pygame.Rect(self.SnakeBody[0].x, self.SnakeBody[0].y, self.LengthOfEachPiece, self.LengthOfEachPiece)

        self.SnakeBody.append(SnakeNewBody)

    def SnakeAteItself(self):
        '''
        Check if Head of the Snake touches any one part of its body. If yes,
        then the game gets over
        '''

        for rect in self.SnakeBody[3:]:
            if self.SnakeBody[0].colliderect(rect):
                if self.FoodAte is False:
                    self.HasStarted = False
                    self.GameOver = True
                    break

    def MoveAutomatically(self):
        '''
        Move snake with respect to user's input
        '''

        self.SnakeAteItself()

        if self.HasStarted:
            self.ChangePositionOfSnakeBody()

            if self.FoodDisplayed is False:
                self.RandomFood()

            if self.Direction == 'L':
                self.SnakeBody[0].x -= self.LengthOfEachPiece + 1

            if self.Direction == 'R':
                self.SnakeBody[0].x += self.LengthOfEachPiece + 1

            if self.Direction == 'U':
                self.SnakeBody[0].y -= self.LengthOfEachPiece + 1

            if self.Direction == 'D':
                self.SnakeBody[0].y += self.LengthOfEachPiece + 1

            # Make snake appears from another end when it disappears from one end
            # of the edge of screen
            if self.SnakeBody[0].x + 5 >= self.WIDTH:
                self.SnakeBody[0].x = 1

            if self.SnakeBody[0].x <= 0:
                self.SnakeBody[0].x = self.WIDTH

            if self.SnakeBody[0].y + 5 >= self.HEIGHT:
                self.SnakeBody[0].y = 2

            if self.SnakeBody[0].y <= 0:
                self.SnakeBody[0].y = self.HEIGHT

            # Generate new food after eating the previous one
            if self.SnakeBody[0].colliderect(self.FoodRect):
                self.FoodDisplayed = False
                self.FoodAte = True
                self.GrowSnake()

    def GetUserDirection(self):
        '''
        Get user direction to move snake towards to that direction
        '''

        keys = pygame.key.get_pressed()

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.Direction != 'R':  # Move Left
            self.Direction = 'L'
            self.HasStarted = True

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.Direction != 'L':  # Move Right
            self.Direction = 'R'
            self.HasStarted = True

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.Direction != 'D':  # Move Up
            self.Direction = 'U'
            self.HasStarted = True

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.Direction != 'U':  # Move Down
            self.Direction = 'D'
            self.HasStarted = True

    def RandomFood(self):
        '''
        Set food to the random position of the screen
        '''

        self.FoodAte = False
        self.FoodDisplayed = True
        self.Food = random.choice(self.FoodsImages)
        self.food_x = random.randint(self.LengthOfEachPiece, self.WIDTH - self.LengthOfEachPiece * 2)
        self.food_y = random.randint(self.LengthOfEachPiece, self.HEIGHT - self.LengthOfEachPiece * 2)
        self.FoodRect = pygame.Rect(self.food_x, self.food_y, self.Food.get_width(), self.Food.get_height())

    def DisplayText(self, text: str, size: int, color: tuple, use_custom_font=False):
        '''
        Create Text Surface

        param:
            text    : Text
            size    : Size of text
            color   : Color of text
        '''

        if use_custom_font is False:
            Text = pygame.font.SysFont('Comic Sans MS', size)

        else:
            font_path = self.ResourcePath(None, 'Font.otf')
            Text = pygame.font.Font(font_path, size)

        TextSurface = Text.render(text, True, color)

        return TextSurface

    def UpdateText(self):
        '''
        Update Health, Score and Levels text
        '''

        ScoreText = self.DisplayText(f'Score: {self.Score}', 20, (255, 255, 255))
        self.WIN.blit(ScoreText, (0, 0))

        HighScoreText = self.DisplayText(f'HighScore: {self.HighScore}', 20, (255, 255, 255))
        self.WIN.blit(HighScoreText, (self.WIDTH - HighScoreText.get_width(), 0))

        if self.GameOver:  # Show GameOver info when snake eats itself
            if self.GameOverAudioPlayed is False:
                self.GameOverAudioPlayed = True
                pygame.mixer.music.load(self.GameOverAudio)
                pygame.mixer.music.play()

            GameOverText = self.DisplayText('Game Over', 100, (204,0,25,255), True)
            self.WIN.blit(GameOverText, (self.WIDTH // 2 - GameOverText.get_width()// 2, self.HEIGHT // 2 - GameOverText.get_height() // 2 - 100))
            self.WIN.blit(self.GameOverInfoImage, (self.WIDTH // 2 - self.GameOverInfoImage.get_width()// 2, self.HEIGHT // 2 - self.GameOverInfoImage.get_height() // 2 + 100))

    def ReDraw(self):
        '''
        Update everything to be displayed
        '''

        self.WIN.blit(self.BackgroundImage, (0, 0))

        for snake in self.SnakeBody:
            pygame.draw.rect(self.WIN, (255, 0, 0), snake)

        if self.FoodDisplayed:
            self.WIN.blit(self.Food, (self.food_x, self.food_y))

        if self.HasStarted is False and self.GameOver is False:
            self.WIN.blit(self.InfoImage, (self.WIDTH // 2 - self.InfoImage.get_width()// 2, self.HEIGHT // 2 - self.InfoImage.get_height() // 2))

        self.UpdateText()
        pygame.display.update()

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

    def main(self):
        '''
        Run the game
        '''

        Clock = pygame.time.Clock()
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Snake')
        pygame.display.set_icon(self.IconImage)

        self.HighScore = self.GetHighScore()

        while self.IsRunning:
            Clock.tick(self.FPS)

            if self.IsPaused is False:
                # Saving and Showing HighScore
                HighScore = self.GetHighScore()

                if self.Score >= HighScore:
                    self.HighScore = self.Score
                    self.SaveData()
                    self.UpdateText()

                self.GetUserDirection()
                self.MoveAutomatically()
                self.ReDraw()

            else:  # Show Paused text when game gets paused
                PausedText = self.DisplayText('Paused !!!', 50, (255, 255, 255))
                self.WIN.blit(PausedText, (self.WIDTH // 2 - PausedText.get_width() // 2, self.HEIGHT // 2 - PausedText.get_height() // 2))
                pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.IsRunning = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_SPACE:  # Pause and UnPause Game
                        if self.IsPaused:
                            self.IsPaused = False

                        else:
                            if self.HasStarted:
                                self.IsPaused = True

                    if event.key == pygame.K_r:  # Restart game when Player dies
                        if self.GameOver:
                            self.SetDefaults()
                            self.HasStarted = True

                    if event.key == pygame.K_q:
                        self.IsRunning = False

        pygame.quit()

    def ResourcePath(self, _dir, file_name):
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
    snake = Snake()
    snake.main()
