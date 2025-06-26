"""
Демонстрация мигающих объектов
Показывает различные способы создания мигающих эффектов
"""

import pygame
import math

# Инициализация
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Мигающие объекты")
clock = pygame.time.Clock()

# Переменные анимации
timer = 0

def draw_blinking_star(x, y, timer):
    """
    Рисует мигающую звезду
    Args:
        x, y: координаты звезды
        timer: текущий кадр для анимации
    """
    # Мигание через изменение прозрачности
    alpha = int(128 + 127 * math.sin(timer * 0.1))
    color = (255, 255, 100, alpha)
    
    # Создаем поверхность с альфа-каналом
    star_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
    
    # Рисуем звезду (простой ромб)
    points = [(20, 0), (30, 15), (20, 30), (10, 15)]
    pygame.draw.polygon(star_surface, color, points)
    
    screen.blit(star_surface, (x - 20, y - 20))

def draw_pulsing_circle(x, y, timer):
    """
    Рисует пульсирующий круг
    Args:
        x, y: координаты центра
        timer: текущий кадр для анимации
    """
    # Пульсация через изменение размера
    radius = int(30 + 15 * math.sin(timer * 0.15))
    color_intensity = int(150 + 105 * math.sin(timer * 0.15))
    color = (color_intensity, 100, 255)
    
    pygame.draw.circle(screen, color, (x, y), radius)
    pygame.draw.circle(screen, (255, 255, 255), (x, y), radius, 2)

def draw_flashing_rectangle(x, y, timer):
    """
    Рисует мигающий прямоугольник
    Args:
        x, y: координаты левого верхнего угла
        timer: текущий кадр для анимации
    """
    # Быстрое мигание (включено/выключено)
    if (timer // 10) % 2 == 0:  # Меняется каждые 10 кадров
        color = (255, 50, 50)
        pygame.draw.rect(screen, color, (x, y, 80, 50))
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 80, 50), 3)

def draw_color_shifting_diamond(x, y, timer):
    """
    Рисует ромб с изменяющимся цветом
    Args:
        x, y: координаты центра
        timer: текущий кадр для анимации
    """
    # Плавное изменение цвета
    red = int(128 + 127 * math.sin(timer * 0.05))
    green = int(128 + 127 * math.sin(timer * 0.07))
    blue = int(128 + 127 * math.sin(timer * 0.09))
    
    points = [(x, y - 25), (x + 25, y), (x, y + 25), (x - 25, y)]
    pygame.draw.polygon(screen, (red, green, blue), points)

# Основной цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Обновление таймера
    timer += 1
    
    # Отрисовка
    screen.fill((30, 30, 50))  # Темно-синий фон
    
    # Различные мигающие объекты
    draw_blinking_star(150, 150, timer)
    draw_pulsing_circle(400, 150, timer)
    draw_flashing_rectangle(600, 125, timer)
    draw_color_shifting_diamond(300, 350, timer)
    
    # Заголовки для каждого эффекта
    font = pygame.font.Font(None, 24)
    
    texts = [
        ("Мигающая звезда", 100, 200),
        ("Пульсирующий круг", 340, 200),
        ("Быстрое мигание", 600, 200),
        ("Смена цвета", 250, 400)
    ]
    
    for text, x, y in texts:
        surface = font.render(text, True, (255, 255, 255))
        screen.blit(surface, (x, y))
    
    # Общий заголовок
    title_font = pygame.font.Font(None, 48)
    title = title_font.render("Виды мигающих эффектов", True, (255, 255, 100))
    screen.blit(title, (200, 50))
    
    # Инструкции
    instruction_font = pygame.font.Font(None, 20)
    instructions = [
        "Демонстрация различных техник анимации:",
        "• Прозрачность (альфа-канал) • Изменение размера",
        "• Включение/выключение • Плавная смена цвета"
    ]
    
    for i, instruction in enumerate(instructions):
        color = (255, 255, 255) if i == 0 else (200, 200, 200)
        text = instruction_font.render(instruction, True, color)
        screen.blit(text, (50, 480 + i * 25))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit() 