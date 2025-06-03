import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parametry fizyczne
g = 9.81
L = 3  # długość ramion

# Parametry impulsów
impulse_strength_left = 5.0
impulse_strength_right = 3.0
impulse_period = 3.0
impulse_duration = 0.2

# Czas
t0, t_end = 0,20
dt = 0.01
times = np.arange(t0, t_end, dt)
X = np.zeros((len(times), 4))
X[0] = [np.pi / 2, np.pi / 2, 0.0, 0.0]  # [theta1, theta2, omega1, omega2]

impulse_times_left = []
impulse_times_right = []

# Funkcja impulsu – działa naprzemiennie co okres
def get_impulse(t):
    phase = int(t // impulse_period) % 2
    in_impulse = (t % impulse_period) < impulse_duration
    if not in_impulse:
        return 0.0
    return impulse_strength_left if phase == 0 else impulse_strength_right

# Układ równań dla podwójnego wahadła (przekształcony do 1. rzędu)
def f(t, X):
    theta1, theta2, omega1, omega2 = X
    delta = theta2 - theta1

    den1 = L * (2 - np.cos(2 * delta))
    den2 = den1  # dla uproszczenia

    impulse = get_impulse(t)

    dtheta1 = omega1
    dtheta2 = omega2

    num1 = (-g * (2 * np.sin(theta1)) - np.sin(delta) * (omega2 ** 2 * L + omega1 ** 2 * L * np.cos(delta))
            + impulse)
    domega1 = num1 / den1

    num2 = (2 * np.sin(delta) * (omega1 ** 2 * L + g * np.cos(theta1)))
    domega2 = num2 / den2

    return np.array([dtheta1, dtheta2, domega1, domega2])

# Metoda RK4
def rk4_step(f, t, X, dt):
    k1 = f(t, X)
    k2 = f(t + dt / 2, X + dt / 2 * k1)
    k3 = f(t + dt / 2, X + dt / 2 * k2)
    k4 = f(t + dt, X + dt * k3)
    return X + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

# Symulacja
for i in range(1, len(times)):
    t = times[i - 1]
    impulse = get_impulse(t)
    if impulse == impulse_strength_left:
        impulse_times_left.append(t)
    elif impulse == impulse_strength_right:
        impulse_times_right.append(t)
    X[i] = rk4_step(f, t, X[i - 1], dt)

# --- WYKRESY ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Wykres dla pierwszego wahadła
ax1.plot(times, X[:, 0], label='Kąt')
ax1.plot(times, X[:, 2], label='Prędkość kątowa')

for t_imp in impulse_times_left:
    ax1.axvspan(t_imp, t_imp + impulse_duration, color='blue', alpha=0.1,
                label='Impuls lewy' if t_imp == impulse_times_left[0] else "")
for t_imp in impulse_times_right:
    ax1.axvspan(t_imp, t_imp + impulse_duration, color='green', alpha=0.1,
                label='Impuls prawy' if t_imp == impulse_times_right[0] else "")

ax1.set_ylabel('Wartość')
ax1.set_title('Pierwsze wahadło')
ax1.legend()
ax1.grid(True)

# Wykres dla drugiego wahadła
ax2.plot(times, X[:, 1], label='Kąt')
ax2.plot(times, X[:, 3], label='Prędkość kątowa')

for t_imp in impulse_times_left:
    ax2.axvspan(t_imp, t_imp + impulse_duration, color='blue', alpha=0.1,
                label='Impuls lewy' if t_imp == impulse_times_left[0] else "")
for t_imp in impulse_times_right:
    ax2.axvspan(t_imp, t_imp + impulse_duration, color='green', alpha=0.1,
                label='Impuls prawy' if t_imp == impulse_times_right[0] else "")

ax2.set_xlabel('Czas [s]')
ax2.set_ylabel('Wartość')
ax2.set_title('Drugie wahadło')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()


# --- ANIMACJA ---
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-2.2, 2.2)
ax.set_ylim(-2.2, 2.2)
ax.set_aspect('equal')
ax.grid()

line, = ax.plot([], [], 'o-', lw=4, color='tab:red')
time_text = ax.text(0.05, 0.95, '', transform=ax.transAxes)

impulse_left_rect = plt.Rectangle((-2, 0), 0.3, 0.3, color='black', alpha=0.5)
impulse_right_rect = plt.Rectangle((1.7, 0), 0.3, 0.3, color='black', alpha=0.5)

ax.add_patch(impulse_left_rect)
ax.add_patch(impulse_right_rect)

def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text, impulse_left_rect, impulse_right_rect

def update(frame):
    theta1, theta2 = X[frame, 0], X[frame, 1]
    x1 = L * np.sin(theta1)
    y1 = -L * np.cos(theta1)
    x2 = x1 + L * np.sin(theta2)
    y2 = y1 - L * np.cos(theta2)
    line.set_data([0, x1, x2], [0, y1, y2])
    time_text.set_text(f'Czas = {times[frame]:.2f} s')

    # Impulsy w animacji
    t = times[frame]
    in_impulse = (t % impulse_period) < impulse_duration
    phase = int(t // impulse_period) % 2
    impulse_left_rect.set_color('blue' if in_impulse and phase == 0 else 'black')
    impulse_right_rect.set_color('green' if in_impulse and phase == 1 else 'black')

    return line, time_text, impulse_left_rect, impulse_right_rect

ani = FuncAnimation(fig, update, frames=len(times), init_func=init,
                    blit=True, interval=10)
plt.show()
