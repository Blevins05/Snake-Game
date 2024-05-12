import pygame, random

pygame.init()

def generate_random_startpos():
    range_pos = (pixel_width // 2, sqr_width - pixel_width // 2, pixel_width)
    return (random.randrange(*range_pos), random.randrange(*range_pos))

def reset_game():
    food_piece.center = generate_random_startpos()
    snake_pix.center = generate_random_startpos()
    return snake_pix.copy()

def update_score():
    return snake_length-1

def is_out_of_bounds(): 
    return snake_pix.bottom > sqr_width or snake_pix.top < 0 or snake_pix.left < 0 or snake_pix.right > sqr_width

def is_collision():
    head = snake[-1]
    for part in snake[:-1]:  # Iterar sobre todos los trozos excepto la cabeza
        if head.colliderect(part):
            return True

def play_sound(sound):
    sound.play()

sqr_width = 800

screen = pygame.display.set_mode(([sqr_width]*2))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
run = True
game_active = True

# creating our snake

pixel_width = 50
snake_pix = pygame.rect.Rect([0, 0, pixel_width-2, pixel_width-2])
snake_pix.center = generate_random_startpos()
snake = [snake_pix.copy()] 
snake_direction = (0,0)
snake_length = 1

test_font = pygame.font.Font('font/Pixeltype.ttf', 30)

# food

food_piece = pygame.rect.Rect([0, 0, pixel_width-2, pixel_width-2])
food_piece.center = generate_random_startpos()

# menu of the game
black = (0,0,0) 
menu_font =  pygame.font.Font('font/Pixeltype.ttf', 150)
menu_msg = menu_font.render('Snake Game', False, black)
menu_msg_rect = menu_msg.get_rect(center = (400, 150))

play_font = pygame.font.Font('font/Pixeltype.ttf', 50)
play_again_msg = play_font.render('-Press space to play:', False, black)
play_again_rect = play_again_msg.get_rect(center =(400, 500))

# in-game sounds
apple_sound = pygame.mixer.Sound('audio/apple.wav')

high_score = 0

# Cargar la puntuación más alta desde un archivo (si existe)
try:
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    pass

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                snake_length = 1
                food_piece.center = generate_random_startpos()
                snake_pix.center = generate_random_startpos()
                snake = [snake_pix.copy()]


    if game_active:        
        screen.fill('Black')
        score = update_score()
        score_surf = test_font.render(f'Score: {score}', False, (255, 255, 255))
        score_rect = score_surf.get_rect(center = (50,20))
        screen.blit(score_surf, score_rect)

        high_score_surf = test_font.render(f"Hi-Score: {high_score}", False, (255, 255, 255))
        high_score_rect = high_score_surf.get_rect(center=(180, 20))
        screen.blit(high_score_surf, high_score_rect)

        if is_out_of_bounds():
            snake_length = 1
            food_piece.center = generate_random_startpos()
            snake_pix.center = generate_random_startpos()
            snake = [snake_pix.copy()]


        # movement
        if snake_pix.center == food_piece.center:
            food_piece.center = generate_random_startpos()
            snake_length += 1 
            snake.append(snake_pix.copy())
            apple_sound.play()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and snake_direction != (0, pixel_width): #goes up and it was not going down
            snake_direction = (0, -pixel_width)
            

        if keys[pygame.K_a] and snake_direction != (pixel_width, 0): 
            snake_direction = (-pixel_width, 0)
            

        if keys[pygame.K_s] and snake_direction != (0, -pixel_width): 
            snake_direction = (0, pixel_width)
            

        if keys[pygame.K_d] and snake_direction != (-pixel_width, 0): 
            snake_direction = (pixel_width, 0)
            

        for snake_part in snake:
            pygame.draw.rect(screen,"green", snake_part)
        pygame.draw.rect(screen,"red", food_piece)

        snake_pix.move_ip(snake_direction)
        snake.append(snake_pix.copy())
        snake = snake[-snake_length:] # snake = snake[-1:]

        if is_collision():
            game_active = False
        if score > high_score:
            high_score = score

            # Guardar la puntuación más alta en un archivo
            with open("high_score.txt", "w") as file:
                file.write(str(high_score))
    else:

        screen.fill('white')
        screen.blit(menu_msg, menu_msg_rect)
        screen.blit(play_again_msg, play_again_rect)

        last_score_surf = play_font.render(f'Last score: {score}', False, black)
        last_score_rect = last_score_surf.get_rect(center = (400, 300))
        screen.blit(last_score_surf, last_score_rect)
        
        highest = play_font.render(f"Highest: {high_score}", False, black)
        highest_rect = highest.get_rect(center=(400, 400))
        screen.blit(highest, highest_rect)
        
    pygame.display.flip()

    clock.tick(10)

pygame.quit()