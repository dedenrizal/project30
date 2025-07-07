from ursina import *
import random

app = Ursina()
window.color = color.white


player = Entity(
    model='cube',
    color=color.black,
    scale=(2, 0.5, 1),
    position=(0, -4, 0),
    collider='box'
)

Sky()
camera.orthographic = True
camera.fov = 10

meteors = []

def spawn_meteor():
    x_pos = random.uniform(-4, 4)
    meteor = Entity(
        model='cube',
        color=color.blue,
        scale=0.5,
        position=(x_pos, 5, 0),
        collider='box'
    )
    meteors.append(meteor)

game_over = False
text_gameover = Text('', origin=(0,0), scale=2, color=color.red)

def update():
    update_game()
    update_meteor()

def update_game():
    global game_over

    if game_over:
        return

    if held_keys['a']:
        player.x -= 5 * time.dt
    if held_keys['d']:
        player.x += 5 * time.dt

    for meteor in meteors[:]:
        meteor.y -= 3 * time.dt

        if meteor.intersects(player).hit:
            destroy(meteor)
            meteors.remove(meteor)

        elif meteor.y +1 < player.y:
            text_gameover.text = "💥 GAME OVER 💥 (Press R)"
            game_over = True

def input(key):
    if key == 'r' and game_over:
        reset_game()

def reset_game():
    global game_over
    player.position = (0, -4, 0)
    for meteor in meteors:
        destroy(meteor)
    meteors.clear()
    text_gameover.text = ''
    game_over = False

meteor_timer = 0
def update_meteor():
    global meteor_timer
    meteor_timer += time.dt
    if meteor_timer > 1: 
        spawn_meteor()
        meteor_timer = 0

app.run()
