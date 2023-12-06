import pygame, random, os
from enum import Enum
from typing import List

# Example of enum, including associating descriptive values to each member
# Also, this is the first of many examples of basic docstrings.
class Direction(Enum):
    """
    An enum which defines movement directions.
    The value for each enum is a unit vector in that direction (or (0,0) for STOPPED).
    """
    UP = pygame.Vector2(0,-1)
    DOWN = pygame.Vector2(0,1)
    RIGHT = pygame.Vector2(1,0)
    LEFT = pygame.Vector2(-1,0)
    STOPPED = pygame.Vector2(0,0)


# Example of a base class.
class Segment():
    """
    A segment of the snake, represented by a colored rectangle.
    """

    def __init__(self, x, y, color, screen: pygame.surface.Surface):
        self.position = pygame.Vector2(x,y)
        self.color = color
        self.screen = screen

    def getRect(self):
        return pygame.Rect(self.position, (20,20))

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.getRect())

    def update(self):
        pass

# Example of inheriting from a base class for more specific functionality.
class Head(Segment):
    """
    The front of the snake. Moves forward based on its current direction.
    """

    def __init__(self, x, y, screen):
        super().__init__(x, y, "red", screen)
        self.direction: Direction = Direction.STOPPED

    def update(self):
        # An example of vector arithmetic
        if self.direction is not None: self.position += self.direction.value *20

# Another example of inheriting from the base class. Now we can do some cool polymorphism stuff!
class TailSegment(Segment):
    """
    A segment trailing behind the front of the snake. Follows the segment in front of it.
    """

    # An example of a static class member.
    tailColors = ['forestgreen','limegreen','darkgreen', 'green','springgreen',
                  'greenyellow','lawngreen', 'palegreen','seagreen']

    def __init__(self, following: Segment, screen):
        # An example of randomly choosing an item from an iterable.
        super().__init__(following.position.x, following.position.y,
                         random.choice(TailSegment.tailColors), screen)
        self.following = following

    def update(self):
        # Great example of the importance of assigning by value vs. reference!
        self.position = self.following.position.copy()


# An example of a standalone class
# This class also gives an example of loading, resizing, and displaying an image.
class Food():
    """
    The food for the snake. Appears randomly and increases the score and snake's length when collected.
    """

    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen
        # An example of robust file access.
        self.image = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "apple.gif"))
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.move()

    def getRect(self):
        return pygame.Rect(self.position, (20,20))

    def move(self):
        # An example of randomly generating numbers.
        self.position = pygame.Vector2(random.randint(0, self.screen.get_width()/20-1)*20,
                                       random.randint(0, self.screen.get_height()/20-1)*20)

    def draw(self):
        self.screen.blit(self.image, self.position)


# Another example of a standalone class
class Score():
    """
    Keeps track of the current score and high score and displays them on the screen.
    """

    def __init__(self, screen: pygame.surface.Surface):
        self.score = 0
        self.highScore = 0
        self.position = pygame.Vector2(300, 10)
        self.font = pygame.font.Font(None, 24)
        self.screen = screen

    def increase(self, increase = 1):
        self.score += increase
        if self.score > self.highScore: self.highScore = self.score

    def reset(self):
        self.score = 0

    def draw(self):
        # An example of formatted strings.
        text = self.font.render(f"Score: {self.score}   High Score: {self.highScore}", True, "white")
        self.screen.blit(text, text.get_rect(center = self.position))

# An example of access-hierarchy. The above classes do not communicate with one another,
# but instead communicate through this main class.
class SnakeGame:
    """
    The main class for the snake game. Handles interactions between each of the game objects defined above and
    controls the overall flow of the game.
    """

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        self.clock = pygame.time.Clock()

        self.head = Head(300,300, self.screen)
        # An example of polymorphism, with type hints thrown in as a bonus!
        self.segments: List[Segment] = [self.head]
        self.food = Food(self.screen)
        self.score = Score(self.screen)
        self.gameSpeed = 2

    # Lots of examples of modular design and isolating functionality here. I won't highlight them all.
    def checkEvents(self):
        
        newDirection = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and self.head.direction != Direction.DOWN:
                    newDirection = Direction.UP
                elif event.key == pygame.K_s and self.head.direction != Direction.UP:
                    newDirection = Direction.DOWN
                elif event.key == pygame.K_d and self.head.direction != Direction.LEFT:
                    newDirection = Direction.RIGHT
                elif event.key == pygame.K_a and self.head.direction != Direction.RIGHT:
                    newDirection = Direction.LEFT

        if newDirection is not None: self.head.direction = newDirection

    def isHeadOutOfBounds(self):
        # An example of a more complex conditional statment.
        return (self.head.position.x >= self.screen.get_width() or self.head.position.x < 0 or
                self.head.position.y >= self.screen.get_height() or self.head.position.y < 0)

    def isHeadOverlappingTail(self):
        # An example of list comprehension.
        return self.head.getRect().collidelist([segment.getRect() for segment in self.segments[1:]]) != -1

    def checkForGameOver(self):
        if self.isHeadOutOfBounds() or self.isHeadOverlappingTail():
            self.head.position = pygame.Vector2(300,300)
            self.head.direction = Direction.STOPPED
            self.segments = [self.head]
            self.score.reset()
            self.gameSpeed = 2
            return True
        else: return False

    def checkForFood(self):
        if self.head.getRect().colliderect(self.food.getRect()):
            self.food.move()
            self.score.increase()
            self.gameSpeed += 0.5
            self.segments.append(TailSegment(self.segments[-1], self.screen))

    def drawScreen(self):
        self.screen.fill("black")
        for segment in self.segments[::-1]:
            segment.draw()
        self.food.draw()
        self.score.draw()

    def play(self):

        self.running = True

        # An example of a while loop.
        while self.running:

            self.checkEvents()

            # An example of a for loop.
            for segment in self.segments[::-1]:
                segment.update()

            gameOver = self.checkForGameOver()
            if not gameOver: self.checkForFood()

            self.drawScreen()

            pygame.display.flip()
            self.clock.tick(self.gameSpeed)
            
        pygame.quit()


# An example of protecting main functionality from imports
if __name__ == "__main__": SnakeGame().play()