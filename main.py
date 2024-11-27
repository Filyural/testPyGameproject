import time
import pygame

# my_font = pygame.font.Font('fonts/Bokor-Regular.ttf', 110)
prefix_path = "/data/data/tpga.test.testpygameapp/files/app/"
# prefix_path = ""

pygame.init()
screen_size = (612, 382)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption(prefix_path + "Test PyGame project")

icon = pygame.image.load(prefix_path + "images/icon.png").convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load(prefix_path + "images/environment/BG.png").convert_alpha()

enemy = pygame.image.load(prefix_path + "images/enemy/enemy.png").convert_alpha()
enemy = pygame.transform.smoothscale(enemy, (40, 40))
active_enemies = []
enemy_speed = 100
enemy_move_step = 0
enemy_spawn_pos = (620, 280)

bullet = pygame.image.load(prefix_path + "images/bullets/projectile.png").convert_alpha()
bullet = pygame.transform.scale(bullet, (30, 30))
bullets = []
bullets_coordinates = []
bullet_speed = 200
bullets_count = bullets_count_start = 5

player_speed = 150
player_x = player_x_start = 150
player_y = player_y_start = 280

is_jump = False
jump_steps = 15 #jump_height
jump_counter = jump_steps
jump_fall = False
jump_strength = jump_steps * 3 #can be literal value

gameplay = True

label = pygame.font.Font(prefix_path + 'fonts/Bokor-Regular.ttf', 60)
lose_text = label.render("You lose!", False, (200, 40, 40))
restart_text = label.render("RESTART", False, (40, 220, 40))
restart_text_collision = restart_text.get_rect(topleft=(180, 200))

player = pygame.image.load(prefix_path + "images/player/idle/1.png").convert_alpha()
idle_anim = [pygame.image.load(prefix_path + "images/player/idle/1.png").convert_alpha(),
             pygame.image.load(prefix_path + "images/player/idle/2.png").convert_alpha(),
             pygame.image.load(prefix_path + "images/player/idle/3.png").convert_alpha(),
             pygame.image.load(prefix_path + "images/player/idle/4.png").convert_alpha()]
walk_right = [pygame.image.load(prefix_path + "images/player/walk_right/9.png").convert_alpha(),
             pygame.image.load(prefix_path + "images/player/walk_right/10.png").convert_alpha(),
             pygame.image.load(prefix_path + "images/player/walk_right/11.png").convert_alpha(),
             pygame.image.load(prefix_path + "images/player/walk_right/12.png").convert_alpha(),
             pygame.image.load(prefix_path + "images/player/walk_right/13.png").convert_alpha(),
             pygame.image.load(prefix_path + "images/player/walk_right/14.png").convert_alpha()]

walk_left = []
for i in range(len(walk_right)):
    new_elem = pygame.transform.flip(walk_right[i], True, False)
    walk_left.append(new_elem)


bg_sound = pygame.mixer.Sound(prefix_path + "sounds/music/MenuMusic.mp3")
bg_sound.set_volume(0.1)
bg_sound.play()

delta_time = 0
counter = 0
tick_counter = 0

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 2500)


game_active = True
while game_active:

    #QUIT GAME
    all_events = pygame.event.get()
    for event in all_events:
        if event.type == pygame.QUIT:
            game_active = False
            pygame.quit()
        if event.type == enemy_timer:
            active_enemies.append(enemy.get_rect(topleft=enemy_spawn_pos))

    if not game_active:
        break

    #FINAL RESTART SCREEN
    if not gameplay:
        screen.fill((100, 100, 0))
        screen.blit(lose_text, (180, 100))
        screen.blit(restart_text, restart_text_collision)

        mouse = pygame.mouse.get_pos()
        #RESTART
        if restart_text_collision.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = player_x_start
            player_y = player_y_start
            active_enemies.clear()
            bullets.clear()
            bullets_coordinates.clear()
            bullets_count = bullets_count_start
            pygame.time.set_timer(enemy_timer, 2500)

        pygame.display.update()
        continue

    #TIME SETTINGS
    start = time.time()
    tick_counter += delta_time
    counter += 1

    #SCREEN MOVING
    bg_x = screen_size[0]
    #screen.blit(bg, ((bg_x - counter) % bg_x - bg_x, 0))   #screen moving
    #screen.blit(bg, ((bg_x - counter) % bg_x, 0))
    screen.blit(bg, (0, 0))

    #COLLISION
    player_collision = walk_left[0].get_rect(topleft=(player_x, player_y))

    #ENEMY_SPAWN_AND_DESTROY
    enemy_move_step += enemy_speed * delta_time
    enemy_move_flag = False
    if enemy_move_step >= 1:
        enemy_move_step -= 1
        enemy_move_flag = True
    for (i, active_enemy) in enumerate(active_enemies):
        screen.blit(enemy, active_enemy)
        if enemy_move_flag:
            active_enemy.x -= 1
        if player_collision.colliderect(active_enemy):
            gameplay = False
            print('You lose!')
        if active_enemy.x == -10:
            active_enemies.pop(i)
            #active_enemies.remove(active_enemy)    #that's acceptable, but we learn new features

    #print(active_enemies)

    #PLAYER MOVING
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] and player_x < 550:
        player_x += player_speed * delta_time
        screen.blit(walk_right[int(tick_counter * len(walk_right)) % len(walk_right)], (player_x, player_y))
    elif keys[pygame.K_a] and player_x > 50:
        player_x -= player_speed * delta_time
        screen.blit(walk_left[int(tick_counter * len(walk_left)) % len(walk_left)], (player_x, player_y))
    else:
        screen.blit(idle_anim[int(tick_counter * len(idle_anim)) % len(idle_anim)], (player_x, player_y))

    #SHOOTING
    for event in all_events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT and bullets_count > 0:
            new_bullet = bullet.get_rect(topleft=(player_x + 30, player_y))
            bullets.append(new_bullet)
            bullets_coordinates.append((new_bullet.x, new_bullet.y))
            bullets_count -= 1


    #BULLETS DRAWING
    for (i, elem) in enumerate(bullets):
        screen.blit(bullet, (elem.x, elem.y))
        bullets_coordinates[i] = (bullets_coordinates[i][0] + bullet_speed * delta_time, bullets_coordinates[i][1])
        elem.x = bullets_coordinates[i][0]

        if elem.x > screen_size[0]:
            bullets.pop(i)
            bullets_coordinates.pop(i)

        for (j, active_enemy) in enumerate(active_enemies):
            if elem.colliderect(active_enemy):
                active_enemies.pop(j)
                bullets.pop(i)
                bullets_coordinates.pop(i)

    #JUMPING
    if not is_jump:
        if keys[pygame.K_SPACE]:
            is_jump = True
    else:
        if jump_counter > 0 and not jump_fall:
            jump_counter -= delta_time * jump_strength
            player_y -= jump_counter * delta_time * jump_strength
        elif jump_counter < jump_steps:
            jump_fall = True
            jump_counter += delta_time * jump_strength
            #avoid deeper falling without collisions in the game
            new_y = player_y + jump_counter * delta_time * jump_strength
            player_y = (new_y if new_y < player_y_start else player_y_start)

        else:
            is_jump = False
            jump_fall = False
            #jump_counter = round(jump_counter)





    pygame.display.update()


    delta_time = time.time() - start
