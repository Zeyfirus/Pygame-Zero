import pgzero.game
import pgzrun

TITLE="Alien in Castle"
WIDTH=700
HEIGHT=700
back_color=(172,178,189)
tile_size=70
state='menu'
sound='on'
sounds.overworld.set_volume(.05)
sounds.overworld.play()
alien=Actor('walk/0',(tile_size*3+tile_size//2,HEIGHT-3*tile_size-3))
alien_x_vel=0
alien_y_vel=0
gravity=1
jumping=False
jumped=False
enemies =[Actor('flyfly/0',(WIDTH-2*tile_size,3*tile_size)),Actor('bee/0',(2*tile_size,HEIGHT-5*tile_size))]
flag=Actor('flag/0',topleft=(WIDTH-2*tile_size-5,tile_size))
flag.time=1.5
start=Actor('start',center=(WIDTH // 2, HEIGHT // 2.5-50))
exit=Actor('exit',center=(WIDTH // 2, HEIGHT // 2.4+80))
sounds_on=Actor('on',center=(WIDTH // 2-50, HEIGHT // 2.5+200))
sounds_off=Actor('off',center=(WIDTH // 2+50, HEIGHT // 2.5+200))
world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 2, 2, 1],
[1, 0, 2, 2, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 2, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 2, 2, 2, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
]

def world(data):
    tile_list=list()
    row_count=0
    for row in data:
        col_count=0
        for tile in row:
            if tile==1:
                img='castle_center'
                x=col_count*tile_size
                y=row_count*tile_size
                tile=(img,(x,y))
                tile_list.append(tile)
            if tile==2:
                img='castle_mid'
                x=col_count*tile_size
                y=row_count*tile_size
                tile=(img,(x,y))
                tile_list.append(tile)
            col_count+=1
        row_count+=1
    return tile_list

world=world(world_data)
tile_list=list()
for tile in world:
    tile_list.append(Actor(tile[0],topleft=tile[1]))

platform_list=list()
for tile in world:
    if tile[0]=='castle_mid':
        x1=tile[1][0]
        y1=tile[1][1]
        platform_list.append(Actor(tile[0],(x1+tile_size//2,y1+tile_size//2)))

enemy_x_speed=1
def update_enemy(enemy,vector):
    global enemy_x_speed
    enemy.x-=enemy_x_speed*vector
    if (enemy.x>=(WIDTH-tile_size)) or (enemy.x<=tile_size):
        enemy_x_speed*=-1

def walk(sprite_name,folder_name,anim_count):
    if sprite_name.time>0.1:
        sprite_name.time=0
        number=int(sprite_name.image.split('/')[-1])
        sprite_name.image=f'{folder_name}/{(number+1)%anim_count}'
def collide_check():
    collide=False
    for platform in (platform_list):
        if alien.colliderect(platform):
            collide=True
    return collide
def jumpedrecently():
    global jumped
    jumped=False
def alien_move():
    global alien_x_vel,alien_y_vel,gravity,jumping,jumped,sound
    if alien_x_vel==0 and not jumped:
        alien.image='walk/0'
    if collide_check():
        gravity=1
        alien.y-=1
    if not collide_check():
        alien.y+=gravity
        if gravity<=20:
            gravity+=0.5
    # left and right movement
    if (keyboard.left):
        if (alien.x>tile_size) and (alien_x_vel>-8):
            alien_x_vel-=2
            alien.image='walk/4left'
    if (keyboard.right):
        if (alien.x < WIDTH-tile_size) and (alien_x_vel <8):
            alien_x_vel+=2
            alien.image='walk/4'
    alien.x+=alien_x_vel
    # alien velocity
    if alien_x_vel>0:
        alien_x_vel-=1
    if alien_x_vel<0:
        alien_x_vel+=1
    if alien.x<1.5*tile_size or alien.x>WIDTH-1.5*tile_size:
        alien_x_vel=0
    # alien jumping
    if (keyboard.up) and collide_check() and not jumped:
        jumping=True
        jumped=True
        clock.schedule_unique(jumpedrecently,0.4)
        alien_y_vel=95
        if sound=='on':
            sounds.jump.set_volume(.06)
            sounds.jump.play()
    if jumping and alien_y_vel>25:
        alien_y_vel=alien_y_vel-((100-alien_y_vel)/2)
        alien.y-=alien_y_vel/3
    else:
        alien_y_vel=0
        jumping=False

def draw():
    screen.fill(back_color)
    if state =='menu':
        start.draw()
        exit.draw()
        sounds_on.draw()
        sounds_off.draw()
    if state!='menu':
        flag.draw()
        for tile in tile_list:
            tile.draw()
        alien.draw()
        for enemy in enemies:
            enemy.draw()
        if state=='win':
            screen.draw.text('YOU WIN!',fontsize=80,center=(WIDTH//2,HEIGHT//2),color='green')
        if state=='loose':
            screen.draw.text('GAME OVER!',fontsize=80,center=(WIDTH//2,HEIGHT//2),color='red')


def on_mouse_down(button,pos):
    global state,sound
    if start.collidepoint(pos):
        state='game'
    if exit.collidepoint(pos):
        pgzero.game.exit()
    if sounds_off.collidepoint(pos):
        sounds.overworld.stop()
        sound='off'
    if sounds_on.collidepoint(pos):
        sounds.overworld.set_volume(.05)
        sounds.overworld.play()
        sound='on'

for enemy in enemies:
    enemy.time =0.2

def update(dt):
    global state
    if state=='game':
        alien_move()
        enemies[0].time += dt
        walk(enemies[0], 'flyfly', 2)
        enemies[1].time += dt
        walk(enemies[1], 'bee', 2)
        flag.time += dt
        walk(flag, 'flag', 3)
        update_enemy(enemies[0], 1)
        update_enemy(enemies[1], -1)
        if alien.collidelist(enemies) != -1:
            state='loose'
            if sound=='on':
                sounds.box.set_volume(.08)
                sounds.box.play()
                sounds.overworld.stop()
        if alien.colliderect(flag):
            state='win'
            if sound=='on':
                sounds.win.set_volume(.08)
                sounds.win.play()
                sounds.overworld.stop()

pgzrun.go()
