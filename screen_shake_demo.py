"""
Демонстрация тряски экрана
Показывает эффект тряски при нажатии пробела
"""

import pygame
import random

# Инициализация
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Тряска экрана")
clock = pygame.time.Clock()

# Параметры тряски
shake_power = 0
shake_duration = 0

def trigger_shake(power=15, duration=30):
    """
    Запускает эффект тряски экрана
    Args:
        power: сила тряски (смещение в пикселях)
        duration: продолжительность в кадрах
    """
    global shake_power, shake_duration
    shake_power = power
    shake_duration = duration

def update_shake():
    """Обновляет параметры тряски"""
    global shake_power, shake_duration
    
    if shake_duration > 0:
        shake_duration -= 1
        # Постепенное ослабление тряски
        shake_power *= 0.9
    else:
        shake_power = 0

def get_shake_offset():
    """
    Возвращает смещение для тряски
    Returns:
        tuple: (offset_x, offset_y)
    """
    if shake_power > 0:
        offset_x = random.randint(-int(shake_power), int(shake_power))
        offset_y = random.randint(-int(shake_power), int(shake_power))
        return offset_x, offset_y
    return 0, 0

def draw_scene(offset_x=0, offset_y=0):
    """
    Рисует игровую сцену с учетом смещения
    Args:
        offset_x, offset_y: смещение для тряски
    """
    # Фон
    screen.fill((20, 30, 50))
    
    # Несколько объектов для демонстрации тряски
    objects = [
        {'type': 'rect', 'pos': (100, 100), 'size': (150, 100), 'color': (255, 100, 100)},
        {'type': 'circle', 'pos': (400, 150), 'radius': 60, 'color': (100, 255, 100)},
        {'type': 'rect', 'pos': (600, 200), 'size': (120, 80), 'color': (100, 100, 255)},
        {'type': 'circle', 'pos': (250, 350), 'radius': 40, 'color': (255, 255, 100)},
        {'type': 'rect', 'pos': (500, 400), 'size': (100, 60), 'color': (255, 100, 255)}
    ]
    
    # Рисуем все объекты со смещением
    for obj in objects:
        if obj['type'] == 'rect':
            x, y = obj['pos']
            w, h = obj['size']
            pygame.draw.rect(screen, obj['color'], 
                           (x + offset_x, y + offset_y, w, h))
            pygame.draw.rect(screen, (255, 255, 255), 
                           (x + offset_x, y + offset_y, w, h), 2)
        elif obj['type'] == 'circle':
            x, y = obj['pos']
            pygame.draw.circle(screen, obj['color'], 
                             (x + offset_x, y + offset_y), obj['radius'])
            pygame.draw.circle(screen, (255, 255, 255), 
                             (x + offset_x, y + offset_y), obj['radius'], 2)

# Основной цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Запуск тряски при нажатии пробела
                trigger_shake(power=20, duration=40)
            elif event.key == pygame.K_1:
                # Слабая тряска
                trigger_shake(power=8, duration=20)
            elif event.key == pygame.K_2:
                # Средняя тряска
                trigger_shake(power=15, duration=30)
            elif event.key == pygame.K_3:
                # Сильная тряска
                trigger_shake(power=25, duration=50)
    
    # Обновление тряски
    update_shake()
    
    # Получение смещения для тряски
    shake_x, shake_y = get_shake_offset()
    
    # Отрисовка сцены с тряской
    draw_scene(shake_x, shake_y)
    
    # Интерфейс (не трясется)
    font = pygame.font.Font(None, 36)
    title = font.render("Демонстрация тряски экрана", True, (255, 255, 255))
    screen.blit(title, (200, 30))
    
    # Инструкции
    instruction_font = pygame.font.Font(None, 28)
    instructions = [
        "ПРОБЕЛ - взрыв (сильная тряска)",
        "1 - слабая тряска",
        "2 - средняя тряска", 
        "3 - очень сильная тряска"
    ]
    
    for i, instruction in enumerate(instructions):
        text = instruction_font.render(instruction, True, (200, 200, 200))
        screen.blit(text, (50, 480 + i * 25))
    
    # Индикатор силы тряски
    if shake_power > 0:
        shake_info = f"Сила тряски: {int(shake_power)}"
        shake_text = instruction_font.render(shake_info, True, (255, 100, 100))
        screen.blit(shake_text, (500, 480))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit() 