"""
Демонстрация анимированных спрайтов
Пример реализации системы анимации персонажа

Добавление новых состояний анимации:

Доступные анимации в спрайт-листе:
- stance (4 кадра) - базовая стойка
- run (8 кадров) - бег
- swing (4 кадра) - удар мечом
- block (2 кадра) - блок щитом
- hit_die (6 кадров) - получение урона/смерть
- cast (4 кадра) - применение магии
- shoot (4 кадра) - стрельба
- walk (8 кадров) - ходьба
- duck (2 кадра) - приседание
- jump (6 кадров) - прыжок
- stairs_up (8 кадров) - подъём по лестнице
- stairs_down (8 кадров) - спуск по лестнице
- stand (1 кадр) - статичная поза

Для добавления новой анимации:
1. Найти соответствующий блок обработки клавиш в функции main()
2. Добавить условие вида: elif keys[pygame.K_key]: hero.change_animation("animation_name")
3. Обновить список инструкций в выводе на экран

Пример добавления анимации смерти на клавишу H:
    elif keys[pygame.K_h]:
        hero.change_animation("hit_die")

Система автоматически загружает все кадры из спрайт-листа и обеспечивает
циклическое воспроизведение анимаций.
"""

import pygame

# Инициализация библиотеки Pygame
pygame.init()

# Константы экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60  # Частота обновления кадров

# Параметры спрайтов
SPRITE_SIZE = 64  # Размер кадра спрайта в пикселях
ANIMATION_SPEED = 8  # Задержка между кадрами анимации

# Физические параметры
GRAVITY = 0.4  # Ускорение свободного падения
JUMP_POWER = -10  # Начальная скорость прыжка
WALK_SPEED = 2  # Скорость ходьбы
RUN_SPEED = 4   # Скорость бега


class Hero:
    """
    Класс персонажа с системой анимации
    Управляет состояниями анимации и физикой персонажа
    """
    
    def __init__(self, x, y):
        """
        Инициализация персонажа
        Args:
            x, y: начальные координаты персонажа
        """
        # Позиция персонажа
        self.x = x
        self.y = y
        
        # Состояние анимации
        self.current_animation = "stance"  # Текущая анимация
        self.current_frame = 0  # Текущий кадр анимации
        self.animation_timer = 0  # Таймер смены кадров
        
        # Загрузка спрайт-листа
        self.sprite_sheet = pygame.image.load("hero_spritesheet.png").convert_alpha()
        
        # Конфигурация анимаций: (название, количество кадров)
        self.animations = [
            ("stance", 4),    # базовая стойка
            ("run", 8),       # бег
            ("swing", 4),     # атака мечом
            ("block", 2),     # защита
            ("hit_die", 6),   # получение урона
            ("cast", 4),      # применение магии
            ("shoot", 4),     # дальняя атака
            ("walk", 8),      # ходьба
            ("duck", 2),      # приседание
            ("jump", 6),      # прыжок
            ("stairs_up", 8), # движение вверх по лестнице
            ("stairs_down", 8), # движение вниз по лестнице
            ("stand", 1),     # статичная поза
        ]
        
        # Хранилище кадров анимации
        self.animation_frames = {}
        
        # Физические параметры
        self.speed_y = 0  # Вертикальная скорость
        self.ground_level = y  # Уровень поверхности
        self.facing_right = True  # Направление взгляда
        
        # Инициализация анимационных кадров
        self._load_all_animations()
    
    def _load_all_animations(self):
        """
        Загружает все кадры анимации из спрайт-листа
        Обрабатывает спрайт-лист последовательно слева направо, сверху вниз
        """
        # Параметры спрайт-листа
        sheet_width = self.sprite_sheet.get_width()
        sheet_height = self.sprite_sheet.get_height()
        
        # Количество кадров в строке
        frames_per_row = sheet_width // SPRITE_SIZE
        
        frame_number = 0  # Индекс текущего кадра
        
        # Обработка каждой анимации
        for animation_name, frame_count in self.animations:
            frames = []  # Список кадров текущей анимации
            
            # Извлечение кадров
            for _ in range(frame_count):
                # Вычисление позиции кадра в сетке
                column = frame_number % frames_per_row
                row = frame_number // frames_per_row
                
                # Определение области кадра
                frame_rect = pygame.Rect(
                    column * SPRITE_SIZE,
                    row * SPRITE_SIZE,
                    SPRITE_SIZE,
                    SPRITE_SIZE
                )
                
                # Извлечение кадра из спрайт-листа
                frame = self.sprite_sheet.subsurface(frame_rect)
                frames.append(frame)
                frame_number += 1
            
            # Сохранение кадров анимации
            self.animation_frames[animation_name] = frames
    
    def change_animation(self, new_animation):
        """
        Изменяет текущую анимацию персонажа
        Args:
            new_animation: название новой анимации
        """
        # Проверка валидности и необходимости смены анимации
        if (new_animation in self.animation_frames and 
            new_animation != self.current_animation):
            self.current_animation = new_animation
            self.current_frame = 0  # Сброс к первому кадру
            self.animation_timer = 0  # Сброс таймера
    
    def update(self):
        """
        Обновление состояния персонажа
        Обрабатывает физику и анимацию
        """
        # Физическое моделирование
        self.speed_y += GRAVITY
        self.y += self.speed_y
        
        # Обработка столкновения с поверхностью
        if self.y >= self.ground_level:
            self.y = self.ground_level
            self.speed_y = 0
            
            # Возврат к базовой анимации после приземления
            if self.current_animation == "jump":
                self.change_animation("stance")
        
        # Обновление анимации
        self.animation_timer += 1
        
        # Смена кадра анимации
        if self.animation_timer >= ANIMATION_SPEED:
            frames_in_animation = len(self.animation_frames[self.current_animation])
            self.current_frame = (self.current_frame + 1) % frames_in_animation
            self.animation_timer = 0
    
    def draw(self, screen):
        """
        Отрисовка персонажа на экране
        Args:
            screen: поверхность для отрисовки
        """
        # Получение текущего кадра
        current_image = self.animation_frames[self.current_animation][self.current_frame]
        
        # Отражение спрайта при движении влево
        if not self.facing_right:
            current_image = pygame.transform.flip(current_image, True, False)
        
        # Отрисовка спрайта
        screen.blit(current_image, (self.x, self.y))


def main():
    """
    Основная функция приложения
    Содержит игровой цикл и обработку событий
    """
    # Инициализация окна
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Анимированный герой")
    
    # Инициализация таймера
    clock = pygame.time.Clock()
    
    # Создание экземпляра персонажа
    try:
        hero = Hero(SCREEN_WIDTH // 2 - 32, SCREEN_HEIGHT // 2 - 32)
    except pygame.error:
        print("Ошибка: файл 'hero_spritesheet.png' не найден!")
        print("Поместите файл спрайт-листа в директорию с программой")
        return
    
    # Основной игровой цикл
    game_running = True
    while game_running:
        
        # Обработка системных событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
        
        # Обработка пользовательского ввода
        keys = pygame.key.get_pressed()
        
        # Флаг активности персонажа
        is_moving = False
        
        # Определение режима движения
        is_running = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        
        # Обработка горизонтального движения
        if keys[pygame.K_a]:
            hero.facing_right = False
            speed = RUN_SPEED if is_running else WALK_SPEED
            hero.x -= speed
            hero.change_animation("run" if is_running else "walk")
            is_moving = True
        
        if keys[pygame.K_d]:
            hero.facing_right = True
            speed = RUN_SPEED if is_running else WALK_SPEED
            hero.x += speed
            hero.change_animation("run" if is_running else "walk")
            is_moving = True
        
        # Обработка прыжка
        if keys[pygame.K_w] and hero.speed_y == 0:
            hero.speed_y = JUMP_POWER
            hero.change_animation("jump")
        
        # Обработка приседания
        if keys[pygame.K_s] and hero.speed_y == 0:
            hero.change_animation("duck")
            is_moving = True
        
        # Обработка боевых действий
        if keys[pygame.K_z]:
            hero.change_animation("swing")
            is_moving = True
        elif keys[pygame.K_x]:
            hero.change_animation("cast")
            is_moving = True
        elif keys[pygame.K_c]:
            hero.change_animation("shoot")
            is_moving = True
        elif keys[pygame.K_v]:
            hero.change_animation("block")
            is_moving = True
        
        # Возврат к базовой анимации при бездействии
        if not is_moving and hero.speed_y == 0:
            hero.change_animation("stance")
        
        # Обновление состояния персонажа
        hero.update()
        
        # Отрисовка сцены
        screen.fill((30, 30, 60))  # Очистка экрана
        
        hero.draw(screen)
        
        # Отображение интерфейса
        font = pygame.font.Font(None, 28)
        
        instructions = [
            "УПРАВЛЕНИЕ:",
            "A/D - движение влево/вправо",
            "Shift + A/D - бег", 
            "W - прыжок",
            "S - приседание",
            "Z - атака мечом",
            "X - применение магии",
            "C - дальняя атака",
            "V - защита"
        ]
        
        # Отрисовка инструкций
        for i, text in enumerate(instructions):
            color = (255, 255, 100) if i == 0 else (255, 255, 255)
            instruction_surface = font.render(text, True, color)
            screen.blit(instruction_surface, (10, 10 + i * 25))
        
        # Отображение текущего состояния
        status_font = pygame.font.Font(None, 32)
        status_text = f"Анимация: {hero.current_animation}"
        status_surface = status_font.render(status_text, True, (255, 255, 0))
        screen.blit(status_surface, (10, 260))
        
        # Обновление дисплея
        pygame.display.flip()
        
        # Контроль частоты кадров
        clock.tick(FPS)
    
    # Завершение работы
    pygame.quit()


# Точка входа в программу
if __name__ == "__main__":
    main() 