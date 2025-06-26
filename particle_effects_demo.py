"""
Демонстрация системы частиц
Показывает создание искр и фейерверков при клике мыши
"""

import pygame
import random

# Инициализация
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Система частиц - Искры")
clock = pygame.time.Clock()

# Список частиц
particles = []

def create_explosion(x, y, count=15):
    """
    Создает взрыв частиц в указанной точке
    Args:
        x, y: координаты взрыва
        count: количество частиц
    """
    for _ in range(count):
        particle = {
            'x': x,
            'y': y,
            'speed_x': random.uniform(-8, 8),
            'speed_y': random.uniform(-8, 8),
            'life': random.randint(30, 80),
            'color': [random.randint(150, 255), random.randint(100, 255), random.randint(50, 255)]
        }
        particles.append(particle)

def update_particles():
    """Обновляет состояние всех частиц"""
    global particles
    for particle in particles[:]:  # Копия списка для безопасного удаления
        # Движение частицы
        particle['x'] += particle['speed_x']
        particle['y'] += particle['speed_y']
        
        # Гравитация
        particle['speed_y'] += 0.2
        
        # Затухание
        particle['life'] -= 1
        
        # Изменение цвета (затемнение)
        for i in range(3):
            particle['color'][i] = max(0, particle['color'][i] - 3)
        
        # Удаление мертвых частиц
        if particle['life'] <= 0:
            particles.remove(particle)

def draw_particles():
    """Отрисовывает все частицы"""
    for particle in particles:
        # Размер частицы зависит от времени жизни
        size = max(1, particle['life'] // 10)
        pygame.draw.circle(screen, particle['color'], 
                         (int(particle['x']), int(particle['y'])), size)

# Основной цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Создание взрыва в точке клика
            mouse_x, mouse_y = pygame.mouse.get_pos()
            create_explosion(mouse_x, mouse_y)
    
    # Обновление
    update_particles()
    
    # Отрисовка
    screen.fill((20, 20, 40))  # Темный фон
    draw_particles()
    
    # Инструкции
    font = pygame.font.Font(None, 36)
    text = font.render("Кликайте мышкой для создания фейерверков!", True, (255, 255, 255))
    screen.blit(text, (50, 50))
    
    # Дополнительная информация
    info_font = pygame.font.Font(None, 24)
    info_lines = [
        "Частицы имеют физику: гравитация, затухание цвета и размера",
        f"Активных частиц: {len(particles)}"
    ]
    
    for i, line in enumerate(info_lines):
        color = (200, 200, 200) if i == 0 else (255, 255, 100)
        text = info_font.render(line, True, color)
        screen.blit(text, (50, 530 + i * 25))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit() 