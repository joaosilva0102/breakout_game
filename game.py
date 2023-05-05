import pygame
import random
pygame.init()
pygame.font.init()

FONT = pygame.font.SysFont("arial", 20)

B = True
E = False

grid = [
    [B, B, B, B, B, B, B, B, B, B, B],
    [B, B, B, B, B, B, B, B, B, B, B],
    [B, B, B, B, B, B, B, B, B, B, B],
    [B, B, B, B, B, B, B, B, B, B, B],
    [B, B, B, B, B, B, B, B, B, B, B]
]

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 900

PLAYER_WIDTH = 150
PLAYER_HEIGHT = 20

BLOCK_WIDTH = SCREEN_WIDTH / len(grid[0])
BLOCK_HEIGHT = 50

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
tick = 30

class Player:
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((x, y), (width, height)))
    
    def draw(self):
        self.rect = pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((self.x, self.y), (self.width, self.height)))

    def move(self, dx):
        if self.rect.left + dx >= 0 and self.rect.right + dx <= SCREEN_WIDTH:
            self.x += dx
            
    def get_rect(self):
        return self.rect

class Block:
    
    def __init__(self, x, y, width, height, r, g, b, border):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.r = r
        self.g = g
        self.b = b
        self.border = border
        self.rect_b = pygame.draw.rect(screen, (r - 50, g - 50, b - 50), pygame.Rect((x, y), (width, height)), border)
        self.rect_f = pygame.draw.rect(screen, (r, g, b), pygame.Rect((x + border, y + border), (width - self.border, height - self.border)))
        
    
    def draw(self):
        self.rect_b = pygame.draw.rect(screen, (self.r - 50, self.g - 50, self.b - 50), pygame.Rect((self.x, self.y), (self.width, self.height)), self.border)
        self.rect_f = pygame.draw.rect(screen, (self.r, self.g, self.b), pygame.Rect((self.x + self.border, self.y + self.border), (self.width - self.border - 5, self.height - self.border - 5)))

    def get_block(self):
        return self.rect_b
class Ball:
    
    def __init__(self, x, y, radius):
        self.radius = radius
        self.xFac = 1
        self.yFac = 1
        self.vel = 10
        self.x = x
        self.y = y
        self.ball = pygame.draw.circle(screen, (255, 255, 255), (x, y), radius)
        self.hit_bottom = 0
        
    def move(self):
        self.x += self.vel * self.xFac
        self.y += self.vel * self.yFac
        
        if self.x - self.radius <= 0 or self.x + self.radius >= SCREEN_WIDTH:
            self.xFac *= -1
        
        if self.y - self.radius <= 0:
            self.yFac *= -1     
            
        if self.y + self.radius >= SCREEN_HEIGHT:
            self.hit_bottom = 1
        
    def draw(self):
        self.ball = pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius)
    
    def reset(self, x, y):
        self.xFac = 1
        self.yFac = 1
        self.x = x
        self.y = y
        self.hit_bottom = 0
    
    def hit_ground(self):
        return self.hit_bottom
        
    def get_ball(self):
        return self.ball

    def hit(self):
        self.yFac *= -1

def create_grid():
    
    blocks = []
    
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y]:
                pos_x = y * BLOCK_WIDTH
                pos_y = x * BLOCK_HEIGHT
                r = random.randint(50, 215)
                g = random.randint(50, 215)
                b = random.randint(50, 215)
                block = Block(pos_x, pos_y, BLOCK_WIDTH, BLOCK_HEIGHT, r, g, b, 5)
                blocks.append(block)
                
    return blocks

def draw_window(player, game_grid, ball): 
    screen.fill((0,0,0))          
    for block in game_grid:
        block.draw()
    
    ball.draw()     
    player.draw()
    pygame.display.update()

def game_over():
    screen.fill((0, 0, 0))
    
    text = FONT.render("GAME OVER", 1, (255, 255, 255))
    text_rect = text.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    screen.blit(text, text_rect)
    pygame.display.update()

def main():
    running = True
    player = Player(SCREEN_WIDTH // 2 - (PLAYER_WIDTH // 2), SCREEN_HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    game_grid = create_grid()
    ball = Ball(SCREEN_HEIGHT - 300, SCREEN_WIDTH // 2, 10)
    state = "game"
    
    while running:
        clock.tick(tick)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            player.move(10)
            
        if key[pygame.K_a]:
            player.move(-10)
        
        if pygame.Rect.colliderect(player.get_rect(), ball.get_ball()):
            ball.hit()
        
        for block in game_grid:
            if pygame.Rect.colliderect(block.get_block(), ball.get_ball()):
                game_grid.remove(block)
                del block
                ball.hit()
        
        if ball.hit_ground():
            state = "over"
    
        if state == "over":
            game_over()
            if key[pygame.K_SPACE]:
                ball.reset(SCREEN_HEIGHT - 300, SCREEN_WIDTH // 2)
                state = "game"
                
        if state == "game":
            ball.move()
            draw_window(player, game_grid, ball)
        
if __name__ == "__main__":
    main()