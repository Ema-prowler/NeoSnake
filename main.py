import pygame
import time
import random

# Inicialización de Pygame
pygame.init()

# Definición de colores
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Configuración de la pantalla
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake game de ema :3')

# Configuración del reloj y tamaño de la serpiente
clock = pygame.time.Clock()
snake_block = 20  # Nuevo tamaño del bloque de la serpiente
snake_speed = 15
original_snake_speed = snake_speed

# Definición de fuentes
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

# Carga de la imagen del power-up
power_up_image = pygame.image.load('power_up.png')
power_up_image = pygame.transform.scale(power_up_image, (snake_block, snake_block))


# Función para dibujar la serpiente
def our_snake(snake_block, snake_List):
    for x in snake_List:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


# Función para mostrar mensajes
def message(msg, color, font_size):
    font = pygame.font.SysFont(None, font_size)
    mesg = font.render(msg, True, color)
    text_rect = mesg.get_rect(center=(dis_width / 2, dis_height / 2))
    dis.blit(mesg, text_rect)


# Función para verificar colisiones
def is_collision(x1, y1, x2, y2, block_size):
    return x2 <= x1 < x2 + block_size and y2 <= y1 < y2 + block_size


# Función principal del juego
def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

    # Inicialización del power-up
    power_up_x = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    power_up_y = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
    power_up_start_time = None
    power_up_duration = 0
    power_up_visible = False
    power_up_next_appearance = time.time() + random.randint(1, 10)
    power_up_end_time = 0  # Inicialización de power_up_end_time

    while not game_over:
        while game_close:
            dis.fill(blue)
            message("¡Perdiste! Presiona Q-Salir o C-Jugar de nuevo", red, 40)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Evitar que la serpiente se mueva en la dirección opuesta inmediata
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # Mover la serpiente
        x1 += x1_change
        y1 += y1_change

        # Verificar si la serpiente atraviesa los bordes de la pantalla y aparece en el lado opuesto
        if x1 >= dis_width:
            x1 = 0
        elif x1 < 0:
            x1 = dis_width - snake_block

        if y1 >= dis_height:
            y1 = 0
        elif y1 < 0:
            y1 = dis_height - snake_block

        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)

        # Generar y manejar el power-up
        current_time = time.time()
        if power_up_visible and current_time - power_up_start_time > power_up_duration:
            power_up_visible = False
        if not power_up_visible and current_time > power_up_next_appearance:
            power_up_x = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            power_up_y = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            power_up_start_time = current_time
            power_up_duration = random.randint(5, 10)
            power_up_visible = True
            power_up_next_appearance = current_time + random.randint(1, 10)

        if power_up_visible:
            dis.blit(power_up_image, (power_up_x, power_up_y))

        # Detección de colisiones con la comida
        if is_collision(x1, y1, foodx, foody, snake_block):
            print("Colisión con comida")
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1

        # Detección de colisiones con el power-up
        if power_up_visible and is_collision(x1, y1, power_up_x, power_up_y, snake_block):
            print("Colisión con power-up")
            power_up_visible = False
            snake_speed += int(original_snake_speed * 0.25)
            power_up_end_time = current_time + power_up_duration

        # Restaurar la velocidad original después de que el power-up expire
        if current_time > power_up_end_time:
            snake_speed = original_snake_speed  # Revertir la velocidad al valor original

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()