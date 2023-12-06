import pygame, random, os

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

def getNewFoodPosition():
    return (random.randint(0,screen.get_width()/20-1)*20,
            random.randint(0,screen.get_height()/20-1)*20)

headPosition = (300,300)
headDirection = "stopped"
tailPositions = []
tailColors = []
tailColorOptions = ['forestgreen','limegreen','darkgreen', 'green','springgreen',
                       'greenyellow','lawngreen', 'palegreen','seagreen']
foodPosition = getNewFoodPosition()
foodImage = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "apple.gif"))
foodImage = pygame.transform.scale(foodImage, (20, 20))
score = 0
highScore = 0
scoreFont = pygame.font.Font(None, 24)
gameSpeed = 2

running = True
while running:

    newDirection = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and headDirection != "down":
                newDirection = "up"
            elif event.key == pygame.K_s and headDirection != "up":
                newDirection = "down"
            elif event.key == pygame.K_d and headDirection != "left":
                newDirection = "right"
            elif event.key == pygame.K_a and headDirection != "right":
                newDirection = "left"
    if newDirection is not None: headDirection = newDirection

    for i in range(len(tailPositions)-1,0,-1):
        tailPositions[i] = tailPositions[i-1]
    if len(tailPositions) > 0: tailPositions[0] = headPosition

    if headDirection == "up": headPosition = (headPosition[0], headPosition[1] - 20)
    elif headDirection == "down": headPosition = (headPosition[0], headPosition[1] + 20)
    elif headDirection == "right": headPosition = (headPosition[0] + 20, headPosition[1])
    elif headDirection == "left": headPosition = (headPosition[0] - 20, headPosition[1])

    isHeadOutOfBounds = (headPosition[0] >= screen.get_width() or headPosition[0] < 0 or
                         headPosition[1] >= screen.get_height() or headPosition[1] < 0)
    
    isheadOnTail = False
    for tailPosition in tailPositions:
        if headPosition == tailPosition: isheadOnTail = True

    if isHeadOutOfBounds or isheadOnTail:
        headPosition = (300,300)
        headDirection = "stopped"
        tailPositions = []
        tailColors = []
        score = 0
        gameSpeed = 2

    elif headPosition == foodPosition:
        foodPosition = getNewFoodPosition()
        score += 1
        if score > highScore: highScore = score
        gameSpeed += 0.5
        tailPositions.append(headPosition)
        tailColors.append(random.choice(tailColorOptions))

    screen.fill("black")
    for i in range(len(tailPositions)-1,-1,-1):
        pygame.draw.rect(screen, tailColors[i], pygame.Rect(tailPositions[i], (20,20)))
    pygame.draw.rect(screen, "red", pygame.Rect(headPosition, (20,20)))
    screen.blit(foodImage, foodPosition)

    text = scoreFont.render(f"Score: {score}   High Score: {highScore}", True, "white")
    screen.blit(text, text.get_rect(center = (300,10)))

    pygame.display.flip()
    clock.tick(gameSpeed)
    
pygame.quit()