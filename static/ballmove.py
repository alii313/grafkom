from vpython import *
import random

# Setup the scene
scene = canvas(title='Bouncing Balls', width=800, height=600)

# Create the walls
wall_left = box(pos=vector(-5, 0, 0), size=vector(0.2, 10, 10), color=color.gray(0.5))
wall_right = box(pos=vector(5, 0, 0), size=vector(0.2, 10, 10), color=color.gray(0.5))
wall_top = box(pos=vector(0, 5, 0), size=vector(10, 0.2, 10), color=color.gray(0.5))
wall_bottom = box(pos=vector(0, -5, 0), size=vector(10, 0.2, 10), color=color.gray(0.5))
wall_back = box(pos=vector(0, 0, -5), size=vector(10, 10, 0.2), color=color.gray(0.5))

# Warna-warna yang telah ditentukan
colors = [vector(0, 0, 1),  # Biru
          vector(1, 1, 0),  # Kuning
          vector(0, 1, 0),  # Hijau
          vector(1, 0, 0),  # Merah
          vector(0, 1, 1)]  # Cyan

# Fungsi untuk menghasilkan kecepatan acak di sumbu x dan y
def random_velocity():
    return vector(random.uniform(-1, 1), random.uniform(-1, 1), 0)

# Buat bola-bola
balls = []
for i in range(5):
    ball = sphere(pos=vector(random.uniform(-4, 4), random.uniform(-4, 4), 0),
                  radius=0.5,
                  color=colors[i])
    ball.velocity = random_velocity()
    balls.append(ball)

# Bola ungu yang dapat dikendalikan
purple_ball = sphere(pos=vector(0, 0, 0), radius=0.5, color=color.purple)
purple_ball.velocity = vector(0, 0, 0)

# Variabel global untuk mode bola ungu
purple_ball_mode = 0  # 0 untuk memantul, 1 untuk membuat bola lain berhenti

# Fungsi untuk menangani tabrakan antara bola-bola
def handle_collision(ball1, ball2):
    # # Hitung vektor dari ball1 ke ball2
    # v12 = ball2.pos - ball1.pos
    
    # # Hitung arah normal dari tabrakan
    # normal = norm(v12)
    
    # # Hitung komponen kecepatan tegak lurus
    # v1n = dot(ball1.velocity, normal) * normal
    # v2n = dot(ball2.velocity, normal) * normal
    
    # # Hitung komponen kecepatan yang terpusat
    # v1t = ball1.velocity - v1n
    # v2t = ball2.velocity - v2n
    
    # # Hitung kecepatan setelah tabrakan menggunakan elastisitas sebagian
    # mass1 = ball1.radius ** 3  # asumsi massa bola proporsional dengan volume (radius^3)
    # mass2 = ball2.radius ** 3
    # new_v1n = ((mass1 - mass2) * v1n + 2 * mass2 * v2n) / (mass1 + mass2)
    # new_v2n = ((mass2 - mass1) * v2n + 2 * mass1 * v1n) / (mass1 + mass2)

    dist = mag(ball1.pos - ball2.pos)
    if dist <= ball1.radius + ball2.radius:
        if ball1.color == color.purple:
            if ball1.velocity == vector(0, 0, 0):
                ball2.velocity *= -1
                return None
        m1 = ball1.radius**3
        v1 = ball1.velocity
        v2 = ball2.velocity
        m2 = ball2.radius**3
        new_v1 = v1 - 2 * m2 / (m1 + m2) * dot(v1 - v2, ball1.pos - ball2.pos) / mag(ball1.pos - ball2.pos)**2 * (ball1.pos - ball2.pos)
        new_v2 = v2 - 2 * m1 / (m1 + m2) * dot(v2 - v1, ball2.pos - ball1.pos) / mag(ball2.pos - ball1.pos)**2 * (ball2.pos - ball1.pos)
    
    if purple_ball_mode == 0:  # Mode memantul
        # Update kecepatan bola-bola setelah tabrakan dengan faktor perpantulan lebih tinggi
        # ball1.velocity = 1.1 * (new_v1n + v1t)  # menggunakan faktor perpantulan 1.1
        # ball2.velocity = 1.1 * (new_v2n + v2t)  # menggunakan faktor perpantulan 1.1
        ball1.velocity = new_v1  # menggunakan faktor perpantulan 1.1
        ball2.velocity = new_v2  # menggunakan faktor perpantulan 1.1
    elif purple_ball_mode == 1:  # Mode membuat bola lain berhenti
        ball2.velocity = vector(0, 0, 0)  # Bola lain berhenti

# Fungsi untuk menangani input dari keyboard untuk bola ungu
def key_input(evt):
    s = evt.key
    speed = 0.1 * 7.25
    if s == 'left':
        purple_ball.pos.x -= speed
        purple_ball.velocity.x = -speed
    elif s == 'right':
        purple_ball.pos.x += speed
        purple_ball.velocity.x = speed
    elif s == 'up':
        purple_ball.pos.y += speed
        purple_ball.velocity.x = speed
    elif s == 'down':
        purple_ball.pos.y -= speed
        purple_ball.velocity.x = -speed

def key_up(evt):
    s = evt.key
    if s == 'left' or s == 'right':
        purple_ball.velocity.x = 0
    elif s == 'up' or s == 'down':
        purple_ball.velocity.y = 0

# Fungsi untuk mengubah mode bola ungu
def safeball():
    global purple_ball_mode
    purple_ball_mode = 0  # Mode memantul

def deathball():
    global purple_ball_mode
    purple_ball_mode = 1  # Mode membuat bola lain berhenti

# Buat tombol-tombol untuk mengubah mode bola ungu
button(bind=safeball, text="Menabrak Memantul", background=color.green)
scene.append_to_caption(' ')
button(bind=deathball, text="Menabrak Berhenti", background=color.red)

# Bind fungsi key_input dan key_up ke canvas
scene.bind('keydown', key_input)
scene.bind('keyup', key_up)

# Loop untuk menggerakkan bola
dt = 0.1
while True:
    rate(100)  # Tentukan kecepatan animasi
    
    for ball in balls:
        if ball.color != color.purple:
            ball.pos += ball.velocity * dt
        
        # Memantul dari dinding
        if ball.pos.x < -4.5 or ball.pos.x > 4.5:
            ball.velocity.x *= -1
        if ball.pos.y < -4.5 or ball.pos.y > 4.5:
            ball.velocity.y *= -1
        
        # Deteksi tabrakan antara bola-bola
        for other_ball in balls:
            if other_ball != ball:
                if mag(ball.pos - other_ball.pos) <= ball.radius + other_ball.radius:
                    handle_collision(ball, other_ball)
    
    # Memantul bola ungu dari tembok
    if purple_ball.pos.x < -4.5 or purple_ball.pos.x > 4.5:
        purple_ball.velocity.x *= -1
    if purple_ball.pos.y < -4.5 or purple_ball.pos.y > 4.5:
        purple_ball.velocity.y *= -1
    
    # Deteksi tabrakan antara bola ungu dan bola-bola lainnya
    for ball in balls:
        if mag(purple_ball.pos - ball.pos) <= purple_ball.radius + ball.radius:
            handle_collision(purple_ball, ball)
    
    # Update posisi bola ungu
    # purple_ball.pos += purple_ball.velocity
    purple_ball.velocity = vector(0, 0, 0)
