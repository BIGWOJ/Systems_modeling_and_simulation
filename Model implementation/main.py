import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parametry tłumienia
a, b, c, d = 1.0, 5.0, 0.5, 3.0

# Parametry impulsów
impulse_strength_left = 100
impulse_strength_right = 50
impulse_period = 3.0
impulse_duration = 0.2

# Symulacja – setup
t0, t_end = 0, 20
dt = 0.01
times = np.arange(t0, t_end, dt)
n = len(times)
X = np.zeros((n, 4))
X[0] = [0.2, 0.3, 0.0, 0.0]

# Klasyczne wymuszenie – brak
def F(t):
    return 0.0

# Określ, czy w danym czasie działa impuls i jaki (lewy/prawy)
def get_impulse(t):
    phase = int(t // impulse_period) % 2
    in_impulse = (t % impulse_period) < impulse_duration
    if not in_impulse:
        return 0.0
    return impulse_strength_left if phase == 0 else impulse_strength_right

# Układ równań 1. rzędu (równanie 4. rzędu)
def f(t, X):
    x1, x2, x3, x4 = X
    dx1dt = x2
    dx2dt = x3
    dx3dt = x4
    impulse = get_impulse(t)
    dx4dt = F(t) - a * x4 - b * x3 - c * x2 - d * x1 + impulse
    return np.array([dx1dt, dx2dt, dx3dt, dx4dt])

# Metoda Rungego-Kutty 4. rzędu
def rk4_step(f, t, X, dt):
    k1 = f(t, X)
    k2 = f(t + dt / 2, X + dt / 2 * k1)
    k3 = f(t + dt / 2, X + dt / 2 * k2)
    k4 = f(t + dt, X + dt * k3)
    return X + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

# Symulacja
impulse_times_left = []
impulse_times_right = []

for i in range(1, n):
    t = times[i - 1]
    impulse = get_impulse(t)
    if impulse == impulse_strength_left:
        impulse_times_left.append(t)
    elif impulse == impulse_strength_right:
        impulse_times_right.append(t)
    X[i] = rk4_step(f, t, X[i - 1], dt)

# --- Wykres ---
plt.figure(figsize=(10, 6))
plt.plot(times, X[:, 0], label=r'$\theta(t)$ (kąt)')
plt.plot(times, X[:, 1], label=r'$\dot{\theta}(t)$ (prędkość kątowa)')

# Paski impulsów
for t_imp in impulse_times_left:
    plt.axvspan(t_imp, t_imp + impulse_duration,
                color='blue', alpha=0.05, label='Impuls lewy' if t_imp == impulse_times_left[0] else "")
for t_imp in impulse_times_right:
    plt.axvspan(t_imp, t_imp + impulse_duration,
                color='green', alpha=0.05, label='Impuls prawy' if t_imp == impulse_times_right[0] else "")

plt.xlabel('Czas [s]')
plt.ylabel('Wartość')
plt.title('Ruch wahadła z naprzemiennymi impulsami i tłumieniem')
plt.legend()
plt.grid(True)
plt.show()

# --- ANIMACJA ---
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.grid()

line, = ax.plot([], [], 'o-', lw=4, color='tab:red')
time_text = ax.text(0.05, 0.95, '', transform=ax.transAxes)

impulse_left = plt.Rectangle((-1.1, -0.1), 0.2, 0.2, color='black', alpha=0.5)
impulse_right = plt.Rectangle((0.9, -0.1), 0.2, 0.2, color='black', alpha=0.5)
ax.add_patch(impulse_left)
ax.add_patch(impulse_right)

def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text, impulse_left, impulse_right

def update(frame):
    t = times[frame]
    theta = X[frame, 0]
    x = np.sin(theta)
    y = -np.cos(theta)
    line.set_data([0, x], [0, y])
    time_text.set_text(f'Czas = {t:.2f} s')

    in_impulse = (t % impulse_period) < impulse_duration
    phase = int(t // impulse_period) % 2
    impulse_left.set_color('blue' if in_impulse and phase == 0 else 'black')
    impulse_right.set_color('green' if in_impulse and phase == 1 else 'black')

    return line, time_text, impulse_left, impulse_right

ani = FuncAnimation(fig, update, frames=n, init_func=init, blit=True, interval=10)
plt.show()
