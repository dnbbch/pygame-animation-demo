"""
Демонстрация плавного движения
Сравнивает резкое и плавное движение объектов
"""

import pygame

# Инициализация
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Плавное движение")
clock = pygame.time.Clock()

# Объекты для демонстрации
class MovingObject:
    def __init__(self, x, y, color, smooth=False):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.color = color
        self.smooth = smooth
        self.size = 25
    
    def set_target(self, target_x, target_y):
        """Устанавливает целевую позицию для движения"""
        self.target_x = target_x
        self.target_y = target_y
    
    def update(self):
        """Обновляет позицию объекта"""
        if self.smooth:
            # Плавное движение (интерполяция)
            self.x += (self.target_x - self.x) * 0.1
            self.y += (self.target_y - self.y) * 0.1
        else:
            # Резкое движение
            speed = 5
            if abs(self.target_x - self.x) > speed:
                self.x += speed if self.target_x > self.x else -speed
            else:
                self.x = self.target_x
                
            if abs(self.target_y - self.y) > speed:
                self.y += speed if self.target_y > self.y else -speed
            else:
                self.y = self.target_y
    
    def draw(self, screen):
        """Отрисовывает объект"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size, 2)

# Создание объектов
jerky_object = MovingObject(100, 200, (255, 100, 100), smooth=False)
smooth_object = MovingObject(100, 400, (100, 255, 100), smooth=True)

# Основной цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # При клике мыши - установить новую цель для движения
            mouse_x, mouse_y = pygame.mouse.get_pos()
            jerky_object.set_target(mouse_x, mouse_y - 100)  # Верхний объект
            smooth_object.set_target(mouse_x, mouse_y + 100)  # Нижний объект
    
    # Обновление объектов
    jerky_object.update()
    smooth_object.update()
    
    # Отрисовка
    screen.fill((40, 40, 60))
    
    # Рисуем объекты
    jerky_object.draw(screen)
    smooth_object.draw(screen)
    
    # Рисуем целевые точки
    pygame.draw.circle(screen, (255, 255, 100), 
                      (int(jerky_object.target_x), int(jerky_object.target_y)), 5)
    pygame.draw.circle(screen, (255, 255, 100), 
                      (int(smooth_object.target_x), int(smooth_object.target_y)), 5)
    
    # Подписи
    font = pygame.font.Font(None, 32)
    
    # Заголовок
    title = font.render("Сравнение типов движения", True, (255, 255, 255))
    screen.blit(title, (250, 50))
    
    # Подписи к объектам
    jerky_label = font.render("Резкое движение", True, (255, 100, 100))
    screen.blit(jerky_label, (50, 150))
    
    smooth_label = font.render("Плавное движение", True, (100, 255, 100))
    screen.blit(smooth_label, (50, 350))
    
    # Инструкции
    instruction_font = pygame.font.Font(None, 24)
    instructions = [
        "КЛИК МЫШИ - установить новую цель движения",
        "Желтые точки - цели движения",
        "Красный объект - резкое движение, зеленый - плавное"
    ]
    
    for i, instruction in enumerate(instructions):
        color = (255, 255, 100) if "желтые" in instruction.lower() else (200, 200, 200)
        text = instruction_font.render(instruction, True, color)
        screen.blit(text, (50, 480 + i * 25))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit() 