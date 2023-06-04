import pygame
import sys

def button_sur():
    pygame.init()
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    background_image = pygame.image.load("photo_2023-05-31_09-25-22.jpg")

    WHITE = (150, 150, 150)
    BLACK = (100, 100, 100)

    # Функция отображения текста на кнопке
    def draw_text(surface, text, font, color, rect):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    # Класс кнопки
    class Button:
        def __init__(self, rect, color, hover_color, text, text_color, font, callback):
            self.rect = rect
            self.color = color
            self.hover_color = hover_color
            self.text = text
            self.text_color = text_color
            self.font = font
            self.callback = callback
            self.hovered = False

        def draw(self, surface):
            if self.hovered:
                pygame.draw.rect(surface, self.hover_color, self.rect)
            else:
                pygame.draw.rect(surface, self.color, self.rect)

            draw_text(surface, self.text, self.font, self.text_color, self.rect)

        def handle_event(self, event):
            if event.type == pygame.MOUSEMOTION:
                self.hovered = self.rect.collidepoint(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
                if self.callback:
                    self.callback()
    r = None

    # Функции обратного вызова для кнопок
    def yes_button_callback():
        nonlocal r
        r = "Виски кола"
    def no_button_callback():
        nonlocal r
        r = "Виски сок"
    def vin_button_callback():
        nonlocal r
        r = "Вино"

    # Создание кнопок
    button_width, button_height = 140, 50
    button_padding = 20
    # Рассчитайте общую ширину кнопок и промежутков между ними
    total_width = (button_width + button_padding) * 3 - button_padding
    start_x = (width - total_width) // 2
    # Создайте кнопки и установите их позиции
    yes_button_rect = pygame.Rect(start_x, (height - button_height) // 1.3, button_width, button_height)
    yes_button = Button(yes_button_rect, WHITE, BLACK, "Виски кола", BLACK, pygame.font.Font(None, 30), yes_button_callback)
    no_button_rect = pygame.Rect(start_x + button_width + button_padding, (height - button_height) // 1.3, button_width, button_height)
    no_button = Button(no_button_rect, WHITE, BLACK, "Виски сок", BLACK, pygame.font.Font(None, 30), no_button_callback)
    vin_button_rect = pygame.Rect(start_x + button_width * 2.14 + button_padding, (height - button_height) // 1.3, button_width,
                                 button_height)
    vin_button = Button(vin_button_rect, WHITE, BLACK, "Вино", BLACK, pygame.font.Font(None, 30), vin_button_callback)
    # Основной цикл
    while r is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            yes_button.handle_event(event)
            no_button.handle_event(event)
            vin_button.handle_event(event)

        screen.fill(BLACK)  # Очистка экрана
        screen.blit(background_image, (0, 0))
        yes_button.draw(screen)  # Отрисовка кнопки "Да"
        no_button.draw(screen)
        vin_button.draw(screen)
        pygame.display.flip()

    return r


