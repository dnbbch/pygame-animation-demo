"""
Демонстрация параллакс-фона
Показывает эффект глубины через разную скорость движения слоев
"""

import pygame

# Инициализация
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Параллакс-фон")
clock = pygame.time.Clock()

# Слои фона с разными скоростями
class BackgroundLayer:
    def __init__(self, color, speed, height, y_offset=0):
        self.color = color
        self.speed = speed
        self.height = height
        self.y_offset = y_offset
        self.x = 0
        self.width = 800
    
    def update(self):
        """Обновляет позицию слоя"""
        self.x -= self.speed
        # Зацикливание фона
        if self.x <= -self.width:
            self.x = 0
    
    def draw(self, screen):
        """Рисует слой фона"""
        # Рисуем основной слой
        pygame.draw.rect(screen, self.color, 
                        (self.x, self.y_offset, self.width, self.height))
        # Рисуем дублирующий слой для зацикливания
        pygame.draw.rect(screen, self.color, 
                        (self.x + self.width, self.y_offset, self.width, self.height))

# Создание слоев (от дальнего к ближнему)
layers = [
    # Небо (статичное)
    BackgroundLayer((135, 206, 235), 0, 200, 0),  # Голубое небо
    
    # Дальние горы (очень медленно)
    BackgroundLayer((139, 69, 19), 0.5, 100, 200),  # Коричневые горы
    
    # Средние холмы (медленно)
    BackgroundLayer((34, 139, 34), 1, 120, 280),  # Зеленые холмы
    
    # Ближний лес (средне)
    BackgroundLayer((0, 100, 0), 2, 100, 400),  # Темно-зеленый лес
    
    # Земля (быстро)
    BackgroundLayer((139, 69, 19), 3, 100, 500),  # Коричневая земля
]

# Объекты для украшения слоев
def draw_decorations():
    """Рисует дополнительные объекты на слоях"""
    # Солнце (статичное)
    pygame.draw.circle(screen, (255, 255, 0), (700, 80), 40)
    pygame.draw.circle(screen, (255, 255, 100), (700, 80), 35)
    
    # Облака (медленно движутся)
    cloud_offset = (pygame.time.get_ticks() // 100) % 1000
    for i, x in enumerate([100, 300, 600]):
        cloud_x = (x - cloud_offset * 0.3) % 900
        # Облако из кругов
        pygame.draw.circle(screen, (255, 255, 255), (int(cloud_x), 60 + i * 20), 25)
        pygame.draw.circle(screen, (255, 255, 255), (int(cloud_x + 20), 60 + i * 20), 20)
        pygame.draw.circle(screen, (255, 255, 255), (int(cloud_x + 40), 60 + i * 20), 25)

def draw_trees_on_layer(layer_x, y_pos):
    """
    Рисует деревья на слое
    Args:
        layer_x: смещение слоя
        y_pos: вертикальная позиция
    """
    tree_positions = [150, 350, 550, 750]
    for pos in tree_positions:
        tree_x = (pos + layer_x) % 1600  # Зацикливание с учетом двух экранов
        if 0 <= tree_x <= 800:  # Рисуем только видимые деревья
            # Ствол
            pygame.draw.rect(screen, (101, 67, 33), (tree_x - 5, y_pos, 10, 30))
            # Крона
            pygame.draw.circle(screen, (0, 128, 0), (tree_x, y_pos - 10), 20)

# Переменная для управления скоростью
global_speed_multiplier = 1.0

# Основной цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Управление скоростью параллакса
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        global_speed_multiplier = -1.0  # Движение назад
    elif keys[pygame.K_RIGHT]:
        global_speed_multiplier = 2.0   # Быстрое движение вперед
    else:
        global_speed_multiplier = 1.0   # Обычная скорость
    
    # Обновление всех слоев
    for layer in layers:
        original_speed = layer.speed
        layer.speed = original_speed * global_speed_multiplier
        layer.update()
        layer.speed = original_speed  # Возвращаем исходную скорость
    
    # Отрисовка
    screen.fill((135, 206, 235))  # Базовый цвет неба
    
    # Рисуем все слои по порядку
    for i, layer in enumerate(layers):
        layer.draw(screen)
        
        # Добавляем деревья на лесной слой
        if i == 3:  # Лесной слой
            draw_trees_on_layer(layer.x, layer.y_offset + 20)
    
    # Рисуем украшения
    draw_decorations()
    
    # Интерфейс
    font = pygame.font.Font(None, 36)
    title = font.render("Параллакс-фон", True, (255, 255, 255))
    title_shadow = font.render("Параллакс-фон", True, (0, 0, 0))
    screen.blit(title_shadow, (252, 32))
    screen.blit(title, (250, 30))
    
    # Инструкции
    instruction_font = pygame.font.Font(None, 24)
    instructions = [
        "ВЛЕВО/ВПРАВО - управление направлением и скоростью",
        "Обратите внимание: дальние объекты движутся медленнее",
        "Это создает эффект глубины и объема"
    ]
    
    for i, instruction in enumerate(instructions):
        text = instruction_font.render(instruction, True, (255, 255, 255))
        text_shadow = instruction_font.render(instruction, True, (0, 0, 0))
        screen.blit(text_shadow, (21, 521 + i * 25))
        screen.blit(text, (20, 520 + i * 25))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit() 