# Импорт необходимых библиотек
import pygame
import random
import time
import json
import os
import sys
from pathlib import Path

def resource_path(relative_path):
    """ Получает правильный путь к ресурсам для PyInstaller """
    if hasattr(sys, '_MEIPASS'):  # Если запущено из EXE
        base_path = sys._MEIPASS
    else:  # Если запущено из исходного кода
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_save_path():
    # Путь к папке AppData/Roaming/ВашаИгра
    appdata_path = os.getenv('APPDATA')
    save_dir = Path(appdata_path) / "Leak Catcher"
    
    # Создаем папку, если ее нет
    save_dir.mkdir(exist_ok=True)
    
    return save_dir / "game_results.json"

def save_results(results):
    save_path = get_save_path()
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def load_results():
    save_path = get_save_path()
    if not save_path.exists():
        return {"ЛЕГКИЙ": [], "СРЕДНИЙ": [], "СЛОЖНЫЙ": []}
        
    with open(save_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Инициализация pygame
pygame.init()
pygame.mixer.init()  # Инициализация микшера для звуков

# Настройки игрового окна
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Leak Catcher")

# Настройка игровых часов
clock = pygame.time.Clock()

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
gray = (150, 150, 150)
transparent_black = (0, 0, 0, 128)
orange = (237,118,14)

# Настройки музыки и звуков
def setup_audio():
    audio = {
        'menu_music': None,
        'game_music': [],
        'current_game_music': None,
        'egg_sound': None,
        'life_sound': None,
        'bonus_sound': None,
        'music_volume': 0.5,
        'sound_volume': 0.7
    }
    
    try:
        # Загрузка музыки меню
        try:
            menu_music_path = resource_path('menu_bg.mp3')
            if os.path.exists(menu_music_path):
                audio['menu_music'] = menu_music_path
            else:
                menu_music_path = resource_path('menu_bg.ogg')
                if os.path.exists(menu_music_path):
                    audio['menu_music'] = menu_music_path
                else:
                    menu_music_path = resource_path('menu_bg.wav')
                    if os.path.exists(menu_music_path):
                        audio['menu_music'] = menu_music_path
        except Exception as e:
            print(f"Ошибка загрузки музыки меню: {e}")

        # Загрузка игровой музыки (3 трека)
        try:
            game_music_files = []
            for i in range(1, 4):
                music_path = resource_path(f'game_music_{i}.mp3')
                if os.path.exists(music_path):
                    game_music_files.append(music_path)
                else:
                    music_path = resource_path(f'game_music_{i}.ogg')
                    if os.path.exists(music_path):
                        game_music_files.append(music_path)
                    else:
                        music_path = resource_path(f'game_music_{i}.wav')
                        if os.path.exists(music_path):
                            game_music_files.append(music_path)
            
            audio['game_music'] = game_music_files[:3]  # Берем первые 3 трека
        except Exception as e:
            print(f"Ошибка загрузки игровой музыки: {e}")

        # Загрузка звуковых эффектов
        try:
            sound_path = resource_path('egg_sound.wav')
            if os.path.exists(sound_path):
                audio['egg_sound'] = pygame.mixer.Sound(sound_path)
            else:
                audio['egg_sound'] = pygame.mixer.Sound(buffer=bytearray([random.randint(0, 255) for _ in range(1000)]))
        except Exception as e:
            print(f"Ошибка загрузки звука яйца: {e}")
            audio['egg_sound'] = pygame.mixer.Sound(buffer=bytearray([random.randint(0, 255) for _ in range(1000)]))
        
        try:
            sound_path = resource_path('life_sound.wav')
            if os.path.exists(sound_path):
                audio['life_sound'] = pygame.mixer.Sound(sound_path)
            else:
                audio['life_sound'] = pygame.mixer.Sound(buffer=bytearray([random.randint(0, 255) for _ in range(1000)]))
        except Exception as e:
            print(f"Ошибка загрузки звука жизни: {e}")
            audio['life_sound'] = pygame.mixer.Sound(buffer=bytearray([random.randint(0, 255) for _ in range(1000)]))
        
        try:
            sound_path = resource_path('bonus_sound.wav')
            if os.path.exists(sound_path):
                audio['bonus_sound'] = pygame.mixer.Sound(sound_path)
            else:
                audio['bonus_sound'] = pygame.mixer.Sound(buffer=bytearray([random.randint(0, 255) for _ in range(1000)]))
        except Exception as e:
            print(f"Ошибка загрузки звука бонуса: {e}")
            audio['bonus_sound'] = pygame.mixer.Sound(buffer=bytearray([random.randint(0, 255) for _ in range(1000)]))
        
        # Установка громкости
        pygame.mixer.music.set_volume(audio['music_volume'])
        for sound in [audio['egg_sound'], audio['life_sound'], audio['bonus_sound']]:
            if sound:
                sound.set_volume(audio['sound_volume'])
        
    except Exception as e:
        print(f"Ошибка загрузки аудио: {e}")
    
    return audio

# Инициализация аудио
audio = setup_audio()

def play_menu_music():
    if audio['menu_music']:
        try:
            pygame.mixer.music.load(audio['menu_music'])
            pygame.mixer.music.play(-1)  # Зацикливаем музыку меню
        except Exception as e:
            print(f"Ошибка воспроизведения музыки меню: {e}")

def play_game_music():
    if audio['game_music']:
        try:
            # Выбираем случайную игровую музыку
            audio['current_game_music'] = random.choice(audio['game_music'])
            pygame.mixer.music.load(audio['current_game_music'])
            pygame.mixer.music.play(-1)  # Зацикливаем игровую музыку
        except Exception as e:
            print(f"Ошибка воспроизведения игровой музыки: {e}")

def stop_music():
    pygame.mixer.music.stop()

def play_sound(sound_name):
    sound = audio.get(sound_name)
    if sound:
        try:
            sound.play()
        except Exception as e:
            print(f"Ошибка воспроизведения звука {sound_name}: {e}")

# Настройки игрока
player_width = 50
player_height = 50
player_x = screen_width / 2 - player_width / 2
player_y = screen_height - player_height
player_speed = 5

# Загрузка изображений
def load_images():
    images = {
        'player': None,
        'player_frames': [],  # Кадры анимации игрока
        'red_ball': None,
        'green_ball_frames': [],
        'purple_ball_frames': [],
        'green_square': None,
        'life_icon': None,
        'player_frame_index': 0,
        'player_animation_speed': 0.1,
        'last_player_frame_update': 0,
        'is_player_moving': False,
        'menu_background': None,
        'game_backgrounds': [],
        'current_bg_index': 0
    }
    
    try:
        # Загрузка фона меню
        try:
            bg_path = resource_path('menu_bg.png')
            if os.path.exists(bg_path):
                images['menu_background'] = pygame.image.load(bg_path).convert()
                images['menu_background'] = pygame.transform.scale(images['menu_background'], (screen_width, screen_height))
            else:
                bg_path = resource_path('menu_bg.jpg')
                if os.path.exists(bg_path):
                    images['menu_background'] = pygame.image.load(bg_path).convert()
                    images['menu_background'] = pygame.transform.scale(images['menu_background'], (screen_width, screen_height))
                else:
                    images['menu_background'] = pygame.Surface((screen_width, screen_height))
                    images['menu_background'].fill((50, 50, 150))  # Синий фон по умолчанию
        except Exception as e:
            print(f"Ошибка загрузки фона меню: {e}")
            images['menu_background'] = pygame.Surface((screen_width, screen_height))
            images['menu_background'].fill((50, 50, 150))
        
        # Загрузка фонов для игры (5 штук)
        try:
            for i in range(1, 6):
                bg_path = resource_path(f'bg{i}.png')
                if os.path.exists(bg_path):
                    img = pygame.image.load(bg_path).convert()
                    img = pygame.transform.scale(img, (screen_width, screen_height))
                    images['game_backgrounds'].append(img)
                else:
                    bg_path = resource_path(f'bg{i}.jpg')
                    if os.path.exists(bg_path):
                        img = pygame.image.load(bg_path).convert()
                        img = pygame.transform.scale(img, (screen_width, screen_height))
                        images['game_backgrounds'].append(img)
            
            # Если не нашли фоны, создаем простые цветные
            if not images['game_backgrounds']:
                colors = [(100, 100, 200), (200, 100, 100), (100, 200, 100), 
                         (200, 200, 100), (100, 200, 200)]
                for color in colors[:5]:
                    bg = pygame.Surface((screen_width, screen_height))
                    bg.fill(color)
                    images['game_backgrounds'].append(bg)
        except Exception as e:
            print(f"Ошибка загрузки игровых фонов: {e}")
            colors = [(100, 100, 200), (200, 100, 100), (100, 200, 100), 
                     (200, 200, 100), (100, 200, 200)]
            for color in colors[:5]:
                bg = pygame.Surface((screen_width, screen_height))
                bg.fill(color)
                images['game_backgrounds'].append(bg)
        
        # Загрузка анимации игрока (5 кадров)
        try:
            for i in range(1, 6):
                player_path = resource_path(f'player_{i}.png')
                if os.path.exists(player_path):
                    img = pygame.image.load(player_path).convert_alpha()
                    img = pygame.transform.scale(img, (player_width, player_height))
                    images['player_frames'].append(img)
            
            if images['player_frames']:
                images['player'] = images['player_frames'][0]  # Первый кадр по умолчанию
            else:
                img = pygame.Surface((player_width, player_height))
                img.fill(black)
                images['player_frames'].append(img)
                images['player'] = images['player_frames'][0]
        except Exception as e:
            print(f"Ошибка загрузки анимации игрока: {e}")
            img = pygame.Surface((player_width, player_height))
            img.fill(black)
            images['player_frames'].append(img)
            images['player'] = images['player_frames'][0]
        
        # Загрузка красного шара (яйца)
        try:
            ball_path = resource_path('red_ball.png')
            if os.path.exists(ball_path):
                images['red_ball'] = pygame.image.load(ball_path).convert_alpha()
                images['red_ball'] = pygame.transform.scale(images['red_ball'], (30, 30))
            else:
                images['red_ball'] = pygame.Surface((30, 30), pygame.SRCALPHA)
                pygame.draw.ellipse(images['red_ball'], (255, 0, 0), (0, 0, 30, 30))
        except Exception as e:
            print(f"Ошибка загрузки красного шара: {e}")
            images['red_ball'] = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.ellipse(images['red_ball'], (255, 0, 0), (0, 0, 30, 30))
        
        # Загрузка анимации зеленого шара (10 кадров)
        try:
            for i in range(1, 11):
                frame_num = str(i).zfill(2)
                ball_path = resource_path(f'green_ball_frame_{frame_num}.png')
                if os.path.exists(ball_path):
                    img = pygame.image.load(ball_path).convert_alpha()
                    img = pygame.transform.scale(img, (30, 30))
                    images['green_ball_frames'].append(img)
            
            if not images['green_ball_frames']:
                img = pygame.Surface((30, 30), pygame.SRCALPHA)
                pygame.draw.ellipse(img, (0, 200, 0), (0, 0, 30, 30))
                images['green_ball_frames'].append(img)
        except Exception as e:
            print(f"Ошибка загрузки зеленых шаров: {e}")
            img = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.ellipse(img, (0, 200, 0), (0, 0, 30, 30))
            images['green_ball_frames'].append(img)
        
        # Загрузка анимации фиолетового шара (16 кадров)
        try:
            for i in range(1, 17):
                frame_num = str(i).zfill(2)
                ball_path = resource_path(f'purple_ball_frame_{frame_num}.png')
                if os.path.exists(ball_path):
                    img = pygame.image.load(ball_path).convert_alpha()
                    img = pygame.transform.scale(img, (30, 30))
                    images['purple_ball_frames'].append(img)
            
            if not images['purple_ball_frames']:
                img = pygame.Surface((30, 30), pygame.SRCALPHA)
                pygame.draw.ellipse(img, (128, 0, 128), (0, 0, 30, 30))
                images['purple_ball_frames'].append(img)
        except Exception as e:
            print(f"Ошибка загрузки фиолетовых шаров: {e}")
            img = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.ellipse(img, (128, 0, 128), (0, 0, 30, 30))
            images['purple_ball_frames'].append(img)
        
        # Загрузка зеленого квадрата (жизни)
        try:
            square_path = resource_path('green_square.png')
            if os.path.exists(square_path):
                images['green_square'] = pygame.image.load(square_path).convert_alpha()
                images['green_square'] = pygame.transform.scale(images['green_square'], (20, 20))
            else:
                images['green_square'] = pygame.Surface((20, 20))
                images['green_square'].fill((0, 255, 0))
        except Exception as e:
            print(f"Ошибка загрузки зеленого квадрата: {e}")
            images['green_square'] = pygame.Surface((20, 20))
            images['green_square'].fill((0, 255, 0))
        
        # Иконка жизней
        life_text = pygame.font.SysFont(None, 20).render("Жизни:", True, white)
        images['life_icon'] = life_text 
        
    except Exception as e:
        print(f"Ошибка загрузки изображений: {e}")
    
    return images

# Загружаем все изображения
images = load_images()

# Настройки яиц
egg_width = 30
egg_height = 30
egg_x = random.randint(0, screen_width - egg_width)
egg_y = 0
egg_speed = 3

# Настройки шаров жизни
life_ball_width = 30
life_ball_height = 30
life_ball_x = random.randint(0, screen_width - life_ball_width)
life_ball_y = 0
life_ball_speed = 2
life_ball_active = False
last_life_ball_time = 0
life_ball_spawn_interval = 15

# Анимация зеленого шара
green_ball_frame_index = 0
green_ball_animation_speed = 0.1
last_green_ball_frame_update = 0

# Настройки бонусного шара
bonus_ball_width = 30
bonus_ball_height = 30
bonus_ball_x = random.randint(0, screen_width - bonus_ball_width)
bonus_ball_y = 0
bonus_ball_speed = 3
bonus_ball_active = False
last_bonus_ball_time = 0
bonus_active = False
bonus_end_time = 0
bonus_duration = 75

# Анимация фиолетового шара
purple_ball_frame_index = 0
purple_ball_animation_speed = 0.1
last_purple_ball_frame_update = 0

# Игровые переменные
score = 0
lives = 5
font = pygame.font.SysFont(None, 30)
large_font = pygame.font.SysFont(None, 50)
middle_font = pygame.font.SysFont(None, 40)

# Состояния игры
MENU = 0
GAME = 1
DIFFICULTY_SELECT = 2
GAME_OVER = 3
RESULTS = 4
RESULTS_EASY = 5
RESULTS_MEDIUM = 6
RESULTS_HARD = 7
RESULTS_ALL = 8
ENTER_NAME = 9
game_state = MENU

# Уровни сложности
difficulties = {
    "ЛЕГКИЙ": {"speed": 3, "speed_increase": 0.05, "life_interval": 15, "life_speed": 2, 
               "bonus_interval": 30, "bonus_speed": 2, "bonus_duration": 75},
    "СРЕДНИЙ": {"speed": 5, "speed_increase": 0.1, "life_interval": 25, "life_speed": 3,
               "bonus_interval": 45, "bonus_speed": 3, "bonus_duration": 50},
    "СЛОЖНЫЙ": {"speed": 7, "speed_increase": 0.15, "life_interval": 40, "life_speed": 4,
               "bonus_interval": 60, "bonus_speed": 4, "bonus_duration": 25}
}
current_difficulty = "ЛЕГКИЙ"

# Переменные для ввода имени
player_name = ""
name_active = False
name_input_rect = pygame.Rect(screen_width//2 - 100, 300, 200, 32)
name_color_active = pygame.Color('lightskyblue3')
name_color_passive = pygame.Color('gray15')
name_color = name_color_passive

def add_result(difficulty, name, score):
    results = load_results()
    results[difficulty].append({"name": name, "score": score})
    results[difficulty].sort(key=lambda x: x["score"], reverse=True)
    results[difficulty] = results[difficulty][:10]
    save_results(results)

def reset_game():
    global player_x, player_y, egg_x, egg_y, egg_speed, score, lives, player_name
    global life_ball_x, life_ball_y, life_ball_active, last_life_ball_time
    global bonus_ball_x, bonus_ball_y, bonus_ball_active, last_bonus_ball_time, bonus_active, bonus_end_time
    
    player_x = screen_width / 2 - player_width / 2
    player_y = screen_height - player_height
    egg_x = random.randint(0, screen_width - egg_width)
    egg_y = 0
    egg_speed = difficulties[current_difficulty]["speed"]
    score = 0
    lives = 5
    player_name = ""
    
    # Сброс шаров жизни
    life_ball_x = random.randint(0, screen_width - life_ball_width)
    life_ball_y = 0
    life_ball_active = False
    last_life_ball_time = time.time()
    
    # Сброс бонусного шара
    bonus_ball_x = random.randint(0, screen_width - bonus_ball_width)
    bonus_ball_y = 0
    bonus_ball_active = False
    last_bonus_ball_time = time.time()
    bonus_active = False
    bonus_end_time = 0
    
    # Смена фона игры
    if images['game_backgrounds']:
        images['current_bg_index'] = (images['current_bg_index'] + 1) % len(images['game_backgrounds'])
    
    # Запуск игровой музыки
    play_game_music()

def spawn_life_ball():
    global life_ball_x, life_ball_y, life_ball_active, last_life_ball_time
    life_ball_x = random.randint(0, screen_width - life_ball_width)
    life_ball_y = 0
    life_ball_active = True
    last_life_ball_time = time.time()
    
def spawn_bonus_ball():
    global bonus_ball_x, bonus_ball_y, bonus_ball_active, last_bonus_ball_time
    bonus_ball_x = random.randint(0, screen_width - bonus_ball_width)
    bonus_ball_y = 0
    bonus_ball_active = True
    last_bonus_ball_time = time.time()

def update_animations():
    global green_ball_frame_index, last_green_ball_frame_update
    global purple_ball_frame_index, last_purple_ball_frame_update
    global player_frame_index, last_player_frame_update, is_player_moving
    
    now = time.time()
    
    # Обновление анимации зеленого шара
    if now - last_green_ball_frame_update > green_ball_animation_speed:
        if images['green_ball_frames']:
            green_ball_frame_index = (green_ball_frame_index + 1) % len(images['green_ball_frames'])
        last_green_ball_frame_update = now
    
    # Обновление анимации фиолетового шара
    if now - last_purple_ball_frame_update > purple_ball_animation_speed:
        if images['purple_ball_frames']:
            purple_ball_frame_index = (purple_ball_frame_index + 1) % len(images['purple_ball_frames'])
        last_purple_ball_frame_update = now
    
    # Обновление анимации игрока
    if images['is_player_moving']:
        if now - images['last_player_frame_update'] > images['player_animation_speed']:
            if images['player_frames']:
                images['player_frame_index'] = (images['player_frame_index'] + 1) % len(images['player_frames'])
                images['player'] = images['player_frames'][images['player_frame_index']]
            images['last_player_frame_update'] = now
    else:
        # Когда игрок не двигается, используем первый кадр
        if images['player_frames']:
            images['player'] = images['player_frames'][0]

def draw_text_with_background(text, font, color, bg_color, x, y):
    text_surface = font.render(text, True, color)
    bg_surface = pygame.Surface((text_surface.get_width() + 20, text_surface.get_height() + 10), pygame.SRCALPHA)
    bg_surface.fill(bg_color)
    bg_surface.blit(text_surface, (10, 5))
    screen.blit(bg_surface, (x - 10, y - 5))
    return bg_surface

def draw_menu():
    # Отрисовка фона меню
    if images['menu_background']:
        screen.blit(images['menu_background'], (0, 0))
    else:
        screen.fill((50, 50, 150))  # Синий фон по умолчанию
    
    # Полупрозрачная подложка для заголовка
    title_bg = pygame.Surface((screen_width - 40, 80), pygame.SRCALPHA)
    title_bg.fill(transparent_black)
    screen.blit(title_bg, (20, 80))
    
    title = large_font.render("ЛОВЕЦ УТЕЧЕК", True, white)
    screen.blit(title, (screen_width//2 - title.get_width()//2, 100))
    
    # Кнопки с подложками
    draw_text_with_background("1. НАЧАТЬ ИГРУ", font, orange, transparent_black, 
                            screen_width//2, 250)
    draw_text_with_background("2. СЛОЖНОСТЬ", font, orange, transparent_black, 
                            screen_width//2, 300)
    draw_text_with_background("3. РЕЗУЛЬТАТЫ", font, orange, transparent_black, 
                            screen_width//2, 350)
    draw_text_with_background("4. ВЫХОД", font, orange, transparent_black, 
                            screen_width//2, 400)
    
    # Информация о сложности
    diff_bg = pygame.Surface((240, 40), pygame.SRCALPHA)
    diff_bg.fill(transparent_black)
    screen.blit(diff_bg, (screen_width//2 - 120, 500))
    
    diff_info = font.render(f"Сложность: {current_difficulty}", True, white)
    screen.blit(diff_info, (screen_width//2 - diff_info.get_width()//2, 510))
    
    pygame.display.update()

def draw_difficulty_menu():
    # Отрисовка фона меню
    if images['menu_background']:
        screen.blit(images['menu_background'], (0, 0))
    else:
        screen.fill((50, 50, 150))  # Синий фон по умолчанию
    
    # Полупрозрачная подложка для заголовка
    title_bg = pygame.Surface((screen_width - 40, 60), pygame.SRCALPHA)
    title_bg.fill(transparent_black)
    screen.blit(title_bg, (20, 90))
    
    title = middle_font.render("ВЫБЕРИТЕ СЛОЖНОСТЬ", True, white)
    screen.blit(title, (screen_width//2 - title.get_width()//2, 100))
    
    # Кнопки с подложками
    draw_text_with_background("1. ЛЕГКИЙ", font, 
                            orange if current_difficulty == "ЛЕГКИЙ" else white, 
                            transparent_black, 
                            screen_width//2, 250)
    draw_text_with_background("2. СРЕДНИЙ", font, 
                            orange if current_difficulty == "СРЕДНИЙ" else white, 
                            transparent_black, 
                            screen_width//2, 300)
    draw_text_with_background("3. СЛОЖНЫЙ", font, 
                            orange if current_difficulty == "СЛОЖНЫЙ" else white, 
                            transparent_black, 
                            screen_width//2, 350)
    
    # Кнопка назад
    draw_text_with_background("ESC - НАЗАД В МЕНЮ", font, white, transparent_black, 
                            screen_width//4, 450)
    
    pygame.display.update()

def draw_results_menu():
    # Отрисовка фона меню
    if images['menu_background']:
        screen.blit(images['menu_background'], (0, 0))
    else:
        screen.fill((50, 50, 150))  # Синий фон по умолчанию
    
    # Полупрозрачная подложка для заголовка
    title_bg = pygame.Surface((screen_width - 40, 60), pygame.SRCALPHA)
    title_bg.fill(transparent_black)
    screen.blit(title_bg, (20, 90))
    
    title = middle_font.render("РЕЗУЛЬТАТЫ", True, white)
    screen.blit(title, (screen_width//2 - title.get_width()//2, 100))
    
    # Кнопки с подложками
    draw_text_with_background("1. ЛЕГКИЙ УРОВЕНЬ", font, orange, transparent_black, 
                            screen_width//3, 200)
    draw_text_with_background("2. СРЕДНИЙ УРОВЕНЬ", font, orange, transparent_black, 
                            screen_width//3, 250)
    draw_text_with_background("3. СЛОЖНЫЙ УРОВЕНЬ", font, orange, transparent_black, 
                            screen_width//3, 300)
    draw_text_with_background("4. ВСЕ РЕЗУЛЬТАТЫ", font, orange, transparent_black, 
                            screen_width//3, 350)
    
    # Кнопка назад
    draw_text_with_background("ESC - НАЗАД В МЕНЮ", font, white, transparent_black, 
                            screen_width//4, 450)
    
    pygame.display.update()

def draw_results(difficulty=None):
    # Отрисовка фона меню
    if images['menu_background']:
        screen.blit(images['menu_background'], (0, 0))
    else:
        screen.fill((50, 50, 150))  # Синий фон по умолчанию
    
    results = load_results()
    
    if difficulty:
        title_text = f"РЕЗУЛЬТАТЫ: {difficulty}"
        scores = results.get(difficulty, [])
    else:
        title_text = "ЛУЧШИЕ РЕЗУЛЬТАТЫ"
        all_scores = []
        for diff in results:
            for res in results[diff]:
                all_scores.append((res["name"], res["score"], diff))
        all_scores.sort(key=lambda x: x[1], reverse=True)
        scores = all_scores[:10]
    
    # Полупрозрачная подложка для заголовка
    title_bg = pygame.Surface((screen_width - 40, 60), pygame.SRCALPHA)
    title_bg.fill(transparent_black)
    screen.blit(title_bg, (20, 40))
    
    title = middle_font.render(title_text, True, white)
    screen.blit(title, (screen_width//2 - title.get_width()//2, 50))
    
    if not scores:
        # Подложка для сообщения об отсутствии результатов
        no_results_bg = pygame.Surface((screen_width - 100, 40), pygame.SRCALPHA)
        no_results_bg.fill(transparent_black)
        screen.blit(no_results_bg, (50, 150))
        
        no_results = font.render("Нет сохраненных результатов", True, white)
        screen.blit(no_results, (screen_width//2 - no_results.get_width()//2, 160))
    else:
        # Подложка для списка результатов
        results_bg = pygame.Surface((screen_width - 80, min(300, len(scores)*30 + 20)), pygame.SRCALPHA)
        results_bg.fill(transparent_black)
        screen.blit(results_bg, (40, 140))
        
        for i, res in enumerate(scores[:10]):
            if difficulty:
                score_text = font.render(f"{i+1}. {res['name']}: {res['score']}", True, white)
            else:
                score_text = font.render(f"{i+1}. {res[0]}: {res[1]} ({res[2]})", True, white)
            screen.blit(score_text, (screen_width//2 - score_text.get_width()//2, 150 + i*30))
    
    # Кнопка назад
    draw_text_with_background("ESC - НАЗАД", font, white, transparent_black, 
                            screen_width//2, 500)
    
    pygame.display.update()

def draw_game():
    # Отрисовка фона игры
    if images['game_backgrounds']:
        screen.blit(images['game_backgrounds'][images['current_bg_index']], (0, 0))
    else:
        screen.fill((100, 100, 200))  # Цветной фон по умолчанию
    
    # Отрисовка игрока
    screen.blit(images['player'], (player_x, player_y))
    
    # Отрисовка красного шара (яйца)
    screen.blit(images['red_ball'], (egg_x, egg_y))
    
    # Отрисовка анимированного зеленого шара (жизни)
    if life_ball_active and images['green_ball_frames']:
        screen.blit(images['green_ball_frames'][green_ball_frame_index], (life_ball_x, life_ball_y))
    
    # Отрисовка анимированного фиолетового шара (бонуса)
    if bonus_ball_active and images['purple_ball_frames']:
        screen.blit(images['purple_ball_frames'][purple_ball_frame_index], (bonus_ball_x, bonus_ball_y))
    
    # Полупрозрачная подложка для информации
    info_bg = pygame.Surface((screen_width - 20, 100), pygame.SRCALPHA)
    info_bg.fill(transparent_black)
    screen.blit(info_bg, (10, 10))
    
    # Отображение счета и сложности
    score_text = font.render(f"Счет: {score}", True, white)
    screen.blit(score_text, (20, 20))
    
    diff_text = font.render(f"Сложность: {current_difficulty}", True, white)
    screen.blit(diff_text, (20, 50))
    
    # Отображение жизней (5 квадратиков)
    life_bg = pygame.Surface((180, 30), pygame.SRCALPHA)
    life_bg.fill(transparent_black)
    #screen.blit(life_bg, (90, 70))
    
    screen.blit(images['life_icon'], (20, 70))
    
    for i in range(5):
        if i < lives:
            screen.blit(images['green_square'], (100 + i*25, 70))
    
    # Отображение времени бонуса, если он активен
    if bonus_active:
        remaining_time = max(0, int(bonus_end_time - time.time()))
        bonus_bg = pygame.Surface((250, 30), pygame.SRCALPHA)
        bonus_bg.fill(transparent_black)
        screen.blit(bonus_bg, (screen_width//2 - 120, 120))
        
        bonus_text = font.render(f"x2 очки! Время: {remaining_time} сек", True, (200, 200, 255))
        screen.blit(bonus_text, (screen_width//2 - bonus_text.get_width()//2, 125))
    
    # Инструкции
    #controls_bg = pygame.Surface((150, 60), pygame.SRCALPHA)
    #controls_bg.fill(transparent_black)
    #screen.blit(controls_bg, (screen_width - 160, 10))
    
    pause_text = font.render("Пауза: P", True, white)
    screen.blit(pause_text, (screen_width - pause_text.get_width() - 20, 20))
    
    menu_text = font.render("Меню: ESC", True, white)
    screen.blit(menu_text, (screen_width - menu_text.get_width() - 20, 50))
    
    pygame.display.update()

def draw_pause():
    if not hasattr(draw_pause, 'pause_surface'):
        draw_pause.pause_surface = screen.copy()
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        draw_pause.pause_surface.blit(overlay, (0, 0))
        
        # Подложка для текста паузы
        pause_bg = pygame.Surface((300, 120), pygame.SRCALPHA)
        pause_bg.fill((0, 0, 0, 200))
        draw_pause.pause_surface.blit(pause_bg, 
                                    (screen_width//2 - 150, 
                                     screen_height//2 - 60))
        
        pause_text = large_font.render("ПАУЗА", True, white)
        draw_pause.pause_surface.blit(pause_text, 
                                    (screen_width//2 - pause_text.get_width()//2, 
                                     screen_height//2 - 30))
        continue_text = font.render("Нажмите P для продолжения", True, white)
        draw_pause.pause_surface.blit(continue_text, 
                                     (screen_width//2 - continue_text.get_width()//2, 
                                      screen_height//2 + 20))
    
    screen.blit(draw_pause.pause_surface, (0, 0))
    pygame.display.update()

def draw_game_over():
    # Отрисовка фона меню
    if images['menu_background']:
        screen.blit(images['menu_background'], (0, 0))
    else:
        screen.fill((50, 50, 150))  # Синий фон по умолчанию
    
    # Подложка для заголовка
    title_bg = pygame.Surface((screen_width - 40, 60), pygame.SRCALPHA)
    title_bg.fill(transparent_black)
    screen.blit(title_bg, (20, 140))
    
    title = large_font.render("ИГРА ОКОНЧЕНА!", True, (255, 100, 100))
    screen.blit(title, (screen_width//2 - title.get_width()//2, 150))
    
    # Подложка для счета
    score_bg = pygame.Surface((screen_width - 100, 40), pygame.SRCALPHA)
    score_bg.fill(transparent_black)
    screen.blit(score_bg, (50, 240))
    
    score_text = font.render(f"Ваш счет: {score}", True, white)
    screen.blit(score_text, (screen_width//2 - score_text.get_width()//2, 250))
    
    # Кнопки
    draw_text_with_background("R - Новая игра", font, orange, transparent_black, 
                            screen_width//2, 350)
    draw_text_with_background("ESC - В меню", font, orange, transparent_black, 
                            screen_width//2, 400)
    
    pygame.display.update()

def draw_enter_name():
    # Отрисовка фона меню
    if images['menu_background']:
        screen.blit(images['menu_background'], (0, 0))
    else:
        screen.fill((50, 50, 150))  # Синий фон по умолчанию
    
    # Подложка для заголовка
    title_bg = pygame.Surface((screen_width - 15, 60), pygame.SRCALPHA)
    title_bg.fill(transparent_black)
    screen.blit(title_bg, (12, 140))
    
    title = large_font.render("ВВЕДИТЕ ВАШЕ ИМЯ", True, white)
    screen.blit(title, (screen_width//2 - title.get_width()//2, 150))
    
    # Подложка для счета
    score_bg = pygame.Surface((screen_width - 100, 40), pygame.SRCALPHA)
    score_bg.fill(transparent_black)
    screen.blit(score_bg, (50, 210))
    
    score_text = font.render(f"Ваш счет: {score}", True, white)
    screen.blit(score_text, (screen_width//2 - score_text.get_width()//2, 220))
    
    # Поле ввода имени
    input_bg = pygame.Surface((220, 42), pygame.SRCALPHA)
    input_bg.fill(transparent_black)
    screen.blit(input_bg, (screen_width//2 - 110, 290))
    
    pygame.draw.rect(screen, name_color, name_input_rect, 2)
    name_surface = font.render(player_name, True, white)
    screen.blit(name_surface, (name_input_rect.x + 5, name_input_rect.y + 5))
    name_input_rect.w = max(200, name_surface.get_width() + 10)
    
    # Подсказка
    hint_bg = pygame.Surface((345, 30), pygame.SRCALPHA)
    hint_bg.fill(transparent_black)
    screen.blit(hint_bg, (screen_width//2 - 170, 340))
    
    hint_text = font.render("Нажмите ENTER для сохранения", True, white)
    screen.blit(hint_text, (screen_width//2 - hint_text.get_width()//2, 345))
    
    pygame.display.update()

# Основной игровой цикл
running = True
paused = False
pause_surface_created = False
prev_game_state = None

# Начинаем с музыки меню
play_menu_music()

while running:
    current_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if game_state == MENU:
                if event.key == pygame.K_1:
                    reset_game()
                    game_state = GAME
                elif event.key == pygame.K_2:
                    game_state = DIFFICULTY_SELECT
                elif event.key == pygame.K_3:
                    game_state = RESULTS
                elif event.key == pygame.K_4 or event.key == pygame.K_ESCAPE:
                    running = False
            
            elif game_state == DIFFICULTY_SELECT:
                if event.key == pygame.K_1:
                    current_difficulty = "ЛЕГКИЙ"
                elif event.key == pygame.K_2:
                    current_difficulty = "СРЕДНИЙ"
                elif event.key == pygame.K_3:
                    current_difficulty = "СЛОЖНЫЙ"
                elif event.key == pygame.K_ESCAPE:
                    game_state = MENU
            
            elif game_state == RESULTS:
                if event.key == pygame.K_1:
                    game_state = RESULTS_EASY
                elif event.key == pygame.K_2:
                    game_state = RESULTS_MEDIUM
                elif event.key == pygame.K_3:
                    game_state = RESULTS_HARD
                elif event.key == pygame.K_4:
                    game_state = RESULTS_ALL
                elif event.key == pygame.K_ESCAPE:
                    game_state = MENU
            
            elif game_state in [RESULTS_EASY, RESULTS_MEDIUM, RESULTS_HARD, RESULTS_ALL]:
                if event.key == pygame.K_ESCAPE:
                    game_state = RESULTS
            
            elif game_state == GAME:
                if event.key == pygame.K_ESCAPE:
                    game_state = MENU
                    stop_music()
                    play_menu_music()
                elif event.key == pygame.K_p:
                    paused = not paused
                    pause_surface_created = False
                    if paused:
                        stop_music()
                    else:
                        play_game_music()
            
            elif game_state == GAME_OVER:
                if event.key == pygame.K_r:
                    reset_game()
                    game_state = GAME
                elif event.key == pygame.K_ESCAPE:
                    game_state = ENTER_NAME
            
            elif game_state == ENTER_NAME:
                if event.key == pygame.K_RETURN:
                    if player_name.strip():
                        add_result(current_difficulty, player_name, score)
                    game_state = MENU
                    play_menu_music()
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 15 and event.unicode.isalnum():
                        player_name += event.unicode
        
        if event.type == pygame.MOUSEBUTTONDOWN and game_state == ENTER_NAME:
            if name_input_rect.collidepoint(event.pos):
                name_active = True
            else:
                name_active = False
            name_color = name_color_active if name_active else name_color_passive
    
    # Обработка изменения состояния игры для музыки
    if game_state != prev_game_state:
        if game_state == MENU and prev_game_state != MENU:
            play_menu_music()
        elif game_state == GAME and prev_game_state != GAME:
            play_game_music()
        elif game_state not in [MENU, GAME] and prev_game_state == GAME:
            stop_music()
            if game_state == ENTER_NAME:
                play_menu_music()
        
        prev_game_state = game_state
    
    if game_state == GAME and not paused:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
            images['is_player_moving'] = True
        elif keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed
            images['is_player_moving'] = True
        else:
            images['is_player_moving'] = False
        
        # Обновление анимаций
        update_animations()
        
        # Движение яйца
        egg_y += egg_speed
        
        # Движение шара жизни
        if life_ball_active:
            life_ball_y += difficulties[current_difficulty]["life_speed"]
            
            if (life_ball_y + life_ball_height > player_y and 
                life_ball_x + life_ball_width > player_x and 
                life_ball_x < player_x + player_width):
                if lives < 5:
                    lives += 1
                life_ball_active = False
                play_sound('life_sound')
            
            if life_ball_y > screen_height:
                life_ball_active = False
        
        # Движение бонусного шара
        if bonus_ball_active:
            bonus_ball_y += difficulties[current_difficulty]["bonus_speed"]
            
            if (bonus_ball_y + bonus_ball_height > player_y and 
                bonus_ball_x + bonus_ball_width > player_x and 
                bonus_ball_x < player_x + player_width):
                bonus_active = True
                bonus_end_time = time.time() + difficulties[current_difficulty]["bonus_duration"]
                bonus_ball_active = False
                score += 25
                play_sound('bonus_sound')
            
            if bonus_ball_y > screen_height:
                bonus_ball_active = False
        
        if bonus_active and time.time() > bonus_end_time:
            bonus_active = False
        
        if not life_ball_active and current_time - last_life_ball_time > difficulties[current_difficulty]["life_interval"]:
            spawn_life_ball()
        
        if not bonus_ball_active and not bonus_active and current_time - last_bonus_ball_time > difficulties[current_difficulty]["bonus_interval"]:
            spawn_bonus_ball()
        
        if (egg_y + egg_height > player_y and 
            egg_x + egg_width > player_x and 
            egg_x < player_x + player_width):
            egg_x = random.randint(0, screen_width - egg_width)
            egg_y = 0
            score += 2 if bonus_active else 1
            egg_speed += difficulties[current_difficulty]["speed_increase"]
            play_sound('egg_sound')
        
        if egg_y > screen_height:
            egg_x = random.randint(0, screen_width - egg_width)
            egg_y = 0
            egg_speed += difficulties[current_difficulty]["speed_increase"]
            lives -= 1
            
            if lives <= 0:
                game_state = ENTER_NAME
    
    # Отрисовка    
    if game_state == MENU:
        draw_menu()
    elif game_state == DIFFICULTY_SELECT:
        draw_difficulty_menu()
    elif game_state == RESULTS:
        draw_results_menu()
    elif game_state == RESULTS_EASY:
        draw_results("ЛЕГКИЙ")
    elif game_state == RESULTS_MEDIUM:
        draw_results("СРЕДНИЙ")
    elif game_state == RESULTS_HARD:
        draw_results("СЛОЖНЫЙ")
    elif game_state == RESULTS_ALL:
        draw_results()
    elif game_state == GAME:
        if paused:
            if not pause_surface_created:
                draw_game()
                draw_pause()
                pause_surface_created = True
            else:
                screen.blit(draw_pause.pause_surface, (0, 0))
                pygame.display.update()
        else:
            draw_game()
    elif game_state == GAME_OVER:
        draw_game_over()
    elif game_state == ENTER_NAME:
        draw_enter_name()
    
    clock.tick(60)

pygame.quit()