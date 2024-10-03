import pygame
import threading
import time

# Pygame
pygame.init()
start_time = time.time()

object_radius = 20
window_width = 480
window_height = 200


screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Simple Ray Tracing")


object_position = (window_width / 2, window_height / 2)

# Paralelizacija
num_threads = 4

def trace_ray(start, end, color):
    for x in range(start[0], end[0]):
        for y in range(start[1], end[1]):
            distance = ((x - object_position[0]) ** 2 + (y - object_position[1]) ** 2) ** 0.5
            if distance < object_radius:
                screen.set_at((x, y), color)

# Main function
def render():
    screen.fill((0, 0, 0))  # Fill the screen with black

    segment_width = window_width // num_threads
    threads = []

    for i in range(num_threads):
        start_x = i * segment_width
        end_x = (i + 1) * segment_width

        thread = threading.Thread(target=trace_ray, args=((start_x, 0), (end_x, window_height), (255, 255, 255)))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    pygame.display.flip()

print(f'The script took {time.time() - start_time} seconds from opening the window to displaying rays.')

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    render()
    clock.tick(60)
pygame.quit()
