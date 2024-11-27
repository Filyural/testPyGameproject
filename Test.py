# import pygame
#
# pygame.init()
#
# # Создаем окно
# screen = pygame.display.set_mode((800, 600))
#
# # Загружаем изображение
# image = pygame.image.load("images/icon.png")
#
# # Отражаем изображение по горизонтали
# flipped_image = pygame.transform.flip(image, True, False)
#
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     # Отрисовка
#     screen.fill((0, 0, 0))
#     screen.blit(flipped_image, (100, 100))  # Отрисовка отраженного изображения
#     pygame.display.flip()
#
# pygame.quit()
