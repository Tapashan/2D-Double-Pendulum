import math
import pygame
import random
import matplotlib.pyplot as plt
from sys import exit

theta_1 = -(3.14/3)
theta_2 = 3.14/6
omega_1 = 0
omega_2 = 0

mass_1 = 10.00
mass_2 = 100.00

g =  9.80665

energy_values = []
time_values = []
time = 0
initial_energy = 0


def heart():
    global theta_1, theta_2, omega_1, omega_2, time

    an1 = -1 *  (mass_2 * l1 * (omega_1 ** 2) * math.sin(theta_1 - theta_2) * math.cos(theta_1 - theta_2)) + (mass_2 * g * math.sin(theta_2) * math.cos(theta_1 - theta_2)) - (mass_2 * l2 * (omega_2 ** 2) * math.sin(theta_1 - theta_2)) - ((mass_1 + mass_2) * g * math.sin(theta_1)) 
    ad1 = l1 * (mass_1 + (mass_2 * (math.sin(theta_1 - theta_2 )** 2)))

    an2 = (mass_1 + mass_2) * ((l1 * (omega_1 ** 2) * math.sin(theta_1 - theta_2)) - (g * math.sin(theta_2)) + (g * math.sin(theta_1) * math.cos(theta_1 - theta_2)) + (l2 * (omega_2 ** 2) * math.sin(theta_1 - theta_2) * math.cos(theta_1 - theta_2)))
    ad2 = l2 * (mass_1 + (mass_2 * (math.sin(theta_1 - theta_2 )** 2)))
    theta_1_acc = 1 * (an1/ad1)
    theta_2_acc = 1 * (an2/ad2)
    dt = 0.01  # Timestep

    omega_1 += theta_1_acc * dt
    omega_2 += theta_2_acc * dt

    theta_1 += omega_1
    theta_2 += omega_2

    ke1 = (0.5 * mass_1 *  (l1 ** 2) * (omega_1 ** 2))
    ke2 =  0.5 * mass_2 * ((l1 * omega_1) ** 2 + (l2 * omega_2) ** 2 + 2 * l1 * l2 * omega_1 * omega_2 * math.cos(theta_1 - theta_2))

    pe1 = (mass_1 * g * -1 * (l1 * math.cos(theta_1)))
    pe2 = (mass_2 * g *( -1 * (l1 * math.cos(theta_1)) - (l2 * math.cos(theta_2))))

    total_energy = ke1 + pe1 + ke2 + pe2
    energy_values.append(total_energy)
    time_values.append(time)
    time += dt

    initial_energy = energy_values[0]
    delta_e = total_energy - initial_energy





pygame.init()

state = [theta_1, theta_2, omega_1, omega_2]


pivot_x = 600
pivot_y = 350
ball_1_x = 600
ball_1_y = 450
ball_2_x = 600
ball_2_y = 550

pivot_pos = pygame.Vector2(pivot_x, pivot_y)
ball_1_pos = pygame.Vector2(ball_1_x, ball_1_y)
ball_2_pos = pygame.Vector2(ball_2_x, ball_2_y)

l1 = (pivot_pos - ball_1_pos).magnitude()
l2 = (ball_1_pos - ball_2_pos).magnitude()

pivot_surf = pygame.Surface((30, 30), pygame.SRCALPHA)
pivot = pygame.draw.circle(pivot_surf, "Blue", (15, 15), 15)
pivot_rect = pivot_surf.get_rect(center = pivot_pos)

ball_1_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
ball_1 = pygame.draw.circle(ball_1_surf, "Orange", (10, 10), 10)
ball_1_rect = ball_1_surf.get_rect(center = ball_1_pos)


ball_2_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
ball_2 = pygame.draw.circle(ball_2_surf, "Yellow", (10, 10), 10)
ball_2_rect = ball_2_surf.get_rect(center = ball_2_pos)

trail = []

clock = pygame.time.Clock()

screen = pygame.display.set_mode((1200, 700))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            plt.plot(time_values, energy_values)
            plt.xlabel('Time (s)')
            plt.ylabel('Total Mechanical Energy (Joules)')
            plt.title('Total Energy of Double Pendulum vs Time')
            plt.grid(True)
            plt.show()
            plt.axhline(y=energy_values[0], color='r', linestyle='--', label='Initial Energy')
            plt.legend()

            pygame.quit()
            exit()
    screen.fill("black")

    heart()

    ball_1_x = l1 * math.sin(theta_1)
    ball_1_y = -1 * (l1 * math.cos(theta_1))
    ball_2_x = ball_1_x + (l2 * math.sin(theta_2))
    ball_2_y = ball_1_y - (l2 * math.cos(theta_2))

    ball_1_rect.center = (pivot_x + ball_1_x, pivot_y - ball_1_y)
    ball_2_rect.center = (pivot_x + ball_2_x, pivot_y - ball_2_y)

    trail.append([pivot_x + ball_2_x, pivot_y - ball_2_y])

    for points in trail:
        pygame.draw.circle(screen, "yellow", (int(points[0]), int(points[1])), 1)

    pygame.draw.line(screen, "white", ball_1_rect.center, ball_2_rect.center, 2)
    pygame.draw.line(screen, "white", pivot_rect.center, ball_1_rect.center, 2)

    screen.blit(pivot_surf, pivot_rect)
    screen.blit(ball_1_surf, ball_1_rect)
    screen.blit(ball_2_surf, ball_2_rect)

    

    pygame.display.update()
    clock.tick(100)