import pygame
import random as rd
import time 
import math
import pygame_gui


pygame.init()
width = 1100
height = 700
manager = pygame_gui.UIManager((width, height))
screen = pygame.display.set_mode((width, height))
block_size = 20
w = width // block_size
h = height // block_size
surface = pygame.Surface((width, height), pygame.SRCALPHA)

clock = pygame.time.Clock()
fps = 60

colors = [
        [0,0,0,255],          # 0 black
        [255,255,255,255],    # 1 white
        [126,126,126,255],    # 2 gray
        [255,0,0,255],        # 3 red
        [0,255,0,255],        # 4 green
        [0,0,50,255],         # 5 blue
        [255,0,255,255],      # 6 pink
        [0,255,255,255],      # 7 aqua
        [255,255,0,255],      # 8 yellow
        [255,77,0,255]        # 9 fire(i guess)
    ]

BACK_COLOR = colors[5]

pallete = [
        [180,180,180,255],
        [150,150,150,255],
        [126,126,126,255],
        [100,100,100,255],
        [70,70,70,255],
        [50,50,50,255],
        [25,25,25,255]
    ]

particle_settings = {
                    "spawn_coords": (width / 2, height / 2),
                    "spread": 1,              # randomize spread
                    "spawn_delay": 0.03,         # delay between spawn in seconds
                    "spawn_num": 10,          # number of particles that spawned each frame
                    "slowdown": 0.8,          # coefficient for acceleration
                    "growing": 0.8,           # added to size each frame
                    "dissolution": 0.95,      # multiplies multiplied by alpha each frame
                    "color": colors[2],       # color of the particles
                    "size": 10,               # start size of the particle
                    "life_time": 100,         # number of frames
                    "gravity": 0.1,           # added to vy each frame
                    "follow_mouse": False     # particles will spawn in mouse position
                    }


spawn_num_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((150, 10), (200, 20)),
    start_value=particle_settings["spawn_num"],
    value_range=(1, 50),
    manager=manager
)

spawn_num_text = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((10, 10), (150, 20)),
    text = f"spawn_num ({particle_settings['spawn_num']})",
    manager=manager
)

spawn_delay_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((150, 40), (200, 20)),
    start_value=particle_settings["spawn_delay"],
    value_range=(0.0, 1.0),
    manager=manager
)

spawn_delay_text = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((10, 40), (150, 20)),
    text = f"spawn_delay ({particle_settings['spawn_delay']})",
    manager=manager
)

slowdown_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((150, 70), (200, 20)),
    start_value=particle_settings["slowdown"],
    value_range=(0.0, 1.0),
    manager=manager
)

slowdown_text = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((10, 70), (150, 20)),
    text = f"slowdown ({particle_settings['slowdown']})",
    manager=manager
)

growing_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((150, 100), (200, 20)),
    start_value=particle_settings["growing"],
    value_range=(0.0, 1.0),
    manager=manager
)

growing_text = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((10, 100), (150, 20)),
    text = f"growing ({particle_settings['growing']})",
    manager=manager
)

dissolution_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((150, 130), (200, 20)),
    start_value=particle_settings["dissolution"],
    value_range=(0.0, 1.0),
    manager=manager
)

dissolution_text = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((10, 130), (150, 20)),
    text = f"dissolution ({particle_settings['dissolution']})",
    manager=manager
)

gravity_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((150, 160), (200, 20)),
    start_value=particle_settings["gravity"],
    value_range=(0.0, 1.0),
    manager=manager
)

gravity_text = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((10, 160), (150, 20)),
    text = f"gravity ({particle_settings['gravity']})",
    manager=manager
)

life_time_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((150, 190), (200, 20)),
    start_value=particle_settings["life_time"],
    value_range=(10, 200),
    manager=manager
)

life_time_text = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((10, 190), (150, 20)),
    text = f"life_time ({particle_settings['life_time']})",
    manager=manager
)

spread_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((150, 220), (200, 20)),
    start_value=particle_settings["spread"],
    value_range=(0.0, 1.0),
    manager=manager
)

spread_text = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((10, 220), (150, 20)),
    text = f"spread ({particle_settings['spread']})",
    manager=manager
)


class Particle():
    def __init__(self, x, y, ax=0, ay=0, color=colors[2], size=10, life_time=100) -> None:
        self.x = x
        self. y = y
        self.vx = 0
        self.vy = 0
        self.ax = ax
        self.ay = ay
        self.color = color.copy() # [r, g, b, a]
        self.size = size
        self.life_time = life_time

    def draw(self):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.size, self.life_time)

    def move(self):
        self.ax *= particle_settings["slowdown"]
        self.ay *= particle_settings["slowdown"]
        self.vx += self.ax
        self.vy += self.ay
        self.x += self.vx
        self.y += self.vy
        self.vy -= particle_settings["gravity"]

    def update(self):
        self.life_time -= 1
        self.color[3] *= particle_settings["dissolution"]
        self.size += particle_settings["growing"]

        self.move()
        self.draw()


def main():
    particles = []
    pressed = False
    last_particle_time = time.time()
    while True:
        surface.fill(BACK_COLOR)
        screen.fill(BACK_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pressed = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pressed = False

            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == spawn_num_slider:
                    spawn_num_text.set_text(f"spawn_num ({int(event.value)})")
                    particle_settings["spawn_num"] = int(event.value)
                elif event.ui_element == spread_slider:
                    spread_text.set_text(f"spread ({float(event.value)})")
                    particle_settings["spread"] = float(event.value)
                elif event.ui_element == spawn_delay_slider:
                    spawn_delay_text.set_text(f"spawn_delay ({float(event.value)})")
                    particle_settings["spawn_delay"] = float(event.value)
                elif event.ui_element == slowdown_slider:
                    slowdown_text.set_text(f"slowdown ({float(event.value)})")
                    particle_settings["slowdown"] = float(event.value)
                elif event.ui_element == growing_slider:
                    growing_text.set_text(f"growing ({float(event.value)})")
                    particle_settings["growing"] = float(event.value)
                elif event.ui_element == dissolution_slider:
                    dissolution_text.set_text(f"dissolution ({float(event.value)})")
                    particle_settings["dissolution"] = float(event.value)
                elif event.ui_element == gravity_slider:
                    gravity_text.set_text(f"gravity ({float(event.value)})")
                    particle_settings["gravity"] = float(event.value)
                elif event.ui_element == life_time_slider:
                    life_time_text.set_text(f"life_time ({int(event.value)})")
                    particle_settings["life_time"] = int(event.value)
                    
            manager.process_events(event)

        if pressed:
            current_time = time.time()
            if current_time - last_particle_time >= particle_settings["spawn_delay"]:
                for _ in range(particle_settings["spawn_num"]):
                    last_particle_time = current_time
                    coords = pygame.mouse.get_pos()
                    radians = math.atan2(coords[1] - particle_settings["spawn_coords"][1], coords[0] - particle_settings["spawn_coords"][0])
                    ax = math.cos(radians)+rd.uniform(-particle_settings["spread"], particle_settings["spread"])
                    ay = math.sin(radians)+rd.uniform(-particle_settings["spread"], particle_settings["spread"])
                    particle_coords = [*coords] if particle_settings["follow_mouse"] else [*particle_settings["spawn_coords"]]
                    particles.append(Particle(*particle_coords, ax, ay, particle_settings["color"], particle_settings["size"], particle_settings["life_time"]))

        for particle in particles:
            particle.update()
            if particle.life_time == 1:
                particles.remove(particle)

        screen.blit(surface, (0, 0))
        manager.update(fps)
        manager.draw_ui(screen)
        pygame.display.update()
        clock.tick(fps)
        pygame.display.set_caption(f"{len(particles)} particles  {int(clock.get_fps())} FPS")


if __name__ == "__main__":
    main()
