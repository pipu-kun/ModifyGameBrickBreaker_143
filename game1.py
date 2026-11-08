import pygame
import random

pygame.init()

# Dimensions of the screen
WIDTH, HEIGHT = 600, 500

# Colors
BLACK = (12, 18, 35)
WHITE = (235, 244, 255)
GREEN = (55, 215, 165)
RED = (255, 105, 115)
BLUE = (75, 190, 255)

font = pygame.font.Font('freesansbold.ttf', 15)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker")

# to control the frame rate
clock = pygame.time.Clock()
FPS = 30
EXPLOSION_RADIUS = 75


# Striker class
class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.speed = speed
        self.color = color

        # The rect variable is used to handle the placement
        # and the collisions of the object
        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height)
        self.striker = pygame.draw.rect(screen, 
                               self.color, self.strikerRect)

    # Used to render the object on the screen
    def display(self):
        pygame.draw.rect(
            screen, (25, 82, 130), self.strikerRect.move(0, 3),
            border_radius=8)
        self.striker = pygame.draw.rect(
            screen, self.color, self.strikerRect, border_radius=8)
        pygame.draw.line(
            screen, WHITE, (self.posx + 12, self.posy + 3),
            (self.posx + self.width - 12, self.posy + 3), 2)

    # Used to update the state of the object
    def update(self, xFac):
        self.posx += self.speed*xFac

        # Restricting the striker to be in between the 
        # left and right edges of the screen
        if self.posx <= 0:
            self.posx = 0
        elif self.posx+self.width >= WIDTH:
            self.posx = WIDTH-self.width

        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height)

    # Returns the rect of the object
    def getRect(self):
        return self.strikerRect


# Block Class
class Block:
    def __init__(self, posx, posy, width, height, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.color = color
        self.damage = 100
        self.isExplosive = color == RED

        # The white blocks have the health of 200. So, 
        # the ball must hit it twice to break
        if color == WHITE:
            self.health = 200
        else:
            self.health = 100

        # The rect variable is used to handle the placement 
        # and the collisions of the object
        self.blockRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height)
        self.block = pygame.draw.rect(screen, self.color, 
                                      self.blockRect)

    # Used to render the object on the screen if and only 
    # if its health is greater than 0
    def display(self):
        if self.health > 0:
            color = self.color
            if self.color == WHITE and self.health < 200:
                color = (145, 165, 195)

            pygame.draw.rect(
                screen, (18, 25, 45), self.blockRect.move(0, 3),
                border_radius=5)
            self.brick = pygame.draw.rect(
                screen, color, self.blockRect, border_radius=5)
            pygame.draw.rect(
                screen, WHITE, self.blockRect, 1, border_radius=5)

    # Used to decrease the health of the block
    def hit(self):
        self.health -= self.damage

    # Used to get the rect of the object
    def getRect(self):
        return self.blockRect

    # Used to get the health of the object
    def getHealth(self):
        return self.health


# Ball Class
class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx, self.posy = posx, posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac, self.yFac = 1, 1

        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx,
                                 self.posy), self.radius)

    # Used to display the object on the screen
    def display(self):
        center = (self.posx, self.posy)
        pygame.draw.circle(screen, (30, 65, 100), center, self.radius + 4)
        self.ball = pygame.draw.circle(
            screen, self.color, center, self.radius)
        pygame.draw.circle(
            screen, BLUE, (self.posx - 2, self.posy - 2),
            max(2, self.radius // 3))

    # Used to update the state of the object
    def update(self):
        self.posx += self.xFac*self.speed
        self.posy += self.yFac*self.speed

        # Reflecting the ball if it touches
        # either of the vertical edges
        if self.posx <= 0 or self.posx >= WIDTH:
            self.xFac *= -1

        # Reflection from the top most edge of the screen
        if self.posy <= 0:
            self.yFac *= -1

        # If the ball touches the bottom most edge of 
        # the screen, True value is returned
        if self.posy >= HEIGHT:
            return True

        return False

    # Resets the position of the ball
    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT - 100
        self.xFac, self.yFac = 1, -1

    # Used to change the direction along Y axis
    def hit(self):
        self.yFac *= -1

    # Returns the rect of the ball. In this case,
    # it is the ball itself
    def getRect(self):
        return self.ball

# Helper Functions

def drawBackground():
    screen.fill(BLACK)
    gridColor = (21, 30, 51)

    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, gridColor, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, gridColor, (0, y), (WIDTH, y))


# Function used to check collisions between any two entities


def collisionChecker(rect, ball):
    if pygame.Rect.colliderect(rect, ball):
        return True

    return False


def explodeBlock(block, listOfBlocks):
    destroyedBlocks = []
    blockCenterX, blockCenterY = block.getRect().center
    radiusSquared = EXPLOSION_RADIUS ** 2

    for nearbyBlock in listOfBlocks:
        if nearbyBlock is block:
            continue

        nearbyCenterX, nearbyCenterY = nearbyBlock.getRect().center
        distanceSquared = (
            (blockCenterX - nearbyCenterX) ** 2
            + (blockCenterY - nearbyCenterY) ** 2
        )
        if distanceSquared <= radiusSquared:
            destroyedBlocks.append(nearbyBlock)

    for nearbyBlock in destroyedBlocks:
        listOfBlocks.remove(nearbyBlock)

    return len(destroyedBlocks)


# Function used to populate the blocks
def populateBlocks(blockWidth, blockHeight, 
                   horizontalGap, verticalGap):
    listOfBlocks = []
    positions = []

    for i in range(0, WIDTH, blockWidth+horizontalGap):
        for j in range(0, HEIGHT//2, blockHeight+verticalGap):
            positions.append((i, j))

    blockCount = len(positions) * 3 // 4
    for i, j in random.sample(positions, blockCount):
        listOfBlocks.append(
            Block(i, j, blockWidth, blockHeight,
                  random.choice([WHITE, WHITE, GREEN, GREEN, RED])))

    return listOfBlocks


# Show the result and wait for space bar or exit
def gameOver(message):
    drawBackground()
    panel = pygame.Rect(100, 175, WIDTH - 200, 130)
    pygame.draw.rect(screen, (23, 33, 55), panel, border_radius=12)
    pygame.draw.rect(screen, BLUE, panel, 2, border_radius=12)

    title = pygame.font.Font(None, 52).render(message, True, WHITE)
    prompt = font.render("Press SPACE to play again", True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 220)))
    screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, 270)))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
        clock.tick(FPS)


# Game Manager
def main():
    running = True
    lives = 3
    score = 0

    striker = Striker(0, HEIGHT-50, 100, 20, 10, BLUE)
    strikerXFac = 0

    ball = Ball(WIDTH // 2, HEIGHT-100, 7, 5, WHITE)

    blockWidth, blockHeight = 40, 15
    horizontalGap, verticalGap = 20, 20

    listOfBlocks = populateBlocks(
        blockWidth, blockHeight, horizontalGap, verticalGap)

    # Game loop
    while running:
        drawBackground()

        if lives <= 0:
            running = gameOver("YOU LOSE!")
            if not running:
                break
            lives = 3
            score = 0
            listOfBlocks = populateBlocks(
                blockWidth, blockHeight, horizontalGap, verticalGap)
            ball.reset()
            strikerXFac = 0
            continue

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    strikerXFac = -1
                if event.key == pygame.K_RIGHT:
                    strikerXFac = 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    strikerXFac = 0

        # Collision check
        if(collisionChecker(striker.getRect(),
                            ball.getRect())):
            ball.hit()
        for block in listOfBlocks[:]:
            if(collisionChecker(block.getRect(), ball.getRect())):
                ball.hit()
                block.hit()

                if block.getHealth() <= 0:
                    listOfBlocks.remove(block)
                    score += 5
                    if block.isExplosive:
                        score += 5 * explodeBlock(block, listOfBlocks)
                break

        if not listOfBlocks:
            running = gameOver("YOU WIN!")
            if not running:
                break
            lives = 3
            score = 0
            listOfBlocks = populateBlocks(
                blockWidth, blockHeight, horizontalGap, verticalGap)
            ball.reset()
            strikerXFac = 0
            continue

        # Update
        striker.update(strikerXFac)
        lifeLost = ball.update()

        if lifeLost:
            lives -= 1
            ball.reset()
            print(lives)

        # Display
        striker.display()
        ball.display()

        for block in listOfBlocks:
            block.display()

        pygame.draw.rect(
            screen, (23, 33, 55), (0, HEIGHT - 25, WIDTH, 25))
        pygame.draw.line(
            screen, (50, 75, 110), (0, HEIGHT - 25), (WIDTH, HEIGHT - 25))
        scoreText = font.render("SCORE  " + str(score), True, WHITE)
        livesText = font.render("LIVES  " + str(lives), True, WHITE)
        screen.blit(scoreText, (20, HEIGHT - 21))
        screen.blit(livesText, (WIDTH - 100, HEIGHT - 21))

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()