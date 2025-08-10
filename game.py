from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import random

catcher_color = (1.0, 1.0, 1.0)  # White 

catcher_y = 20          # fixed catcher vertical position
catcher_speed = 10000.0   # speed of catcher movement
score = 0
game_over = False
paused = False
last_time = 0
catcher_x = 170.00  # or 400//2 (approximate center minus half catcher width)
diamond_x = random.randint(20, 380)
diamond_y = 380
diamond_speed = 80.0  # slowed down speed
diamond_color = (1.0, 1.0, 1.0)


btn_left_x, btn_left_y = 10, 370
btn_play_x, btn_play_y = 180, 370
btn_exit_x, btn_exit_y = 360, 375
btn_size = 40

def drawLine_mda(x1,y1,x2,y2):
    dx = x2 -x1
    dy = y2-y1
    d = dy + dy -dx
    incE = dy + dy
    incNE =dy + dy -dx -dx
    x=x1
    y= y1
    for i in range(x,x2):
        if d>0:
            d = d + incNE
            y = y+1
        else:
            d = d + incE  
def FindZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    
    if abs(dx) >= abs(dy):  
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        elif dx >= 0 and dy < 0:
            return 7
    else:  
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        elif dx >= 0 and dy < 0:
            return 6


def convertToZone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def convertFromZone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def drawLine_mda_allzone(x1,y1,x2,y2):
    zone = FindZone(x1, y1, x2, y2)
    x1_0, y1_0 = convertToZone0(x1, y1, zone)
    x2_0, y2_0 = convertToZone0(x2, y2, zone)

    if x1_0 > x2_0:
        x1_0, y1_0, x2_0, y2_0 = x2_0, y2_0, x1_0, y1_0

    dx = x2_0 - x1_0
    dy = y2_0 - y1_0
    d = dy + dy -dx
    incE = dy + dy
    incNE =dy + dy -dx -dx
    x=x1_0
    y= y1_0
    while x < x2_0:
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
        x += 1
        original_x, original_y = convertFromZone0(x, y, zone)  
        draw_points(original_x, original_y)        

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 400, 0.0, 400, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 0.0)

    drawCatcher(catcher_x, catcher_y)
    glColor3f(*diamond_color)
    drawDiamond(diamond_x, diamond_y)
    glColor3f(1.0, 0.0, 0.0)  
    drawButtonLeft(btn_left_x, btn_left_y)
    drawButtonPlay(btn_play_x, btn_play_y, not paused)
    drawButtonExit(btn_exit_x, btn_exit_y)
    glFlush()
    glutSwapBuffers()

def draw_points(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def drawDiamond(center_x, center_y):
    size = 10
    drawLine_mda_allzone(center_x, center_y + size, center_x + size, center_y)
    drawLine_mda_allzone(center_x + size, center_y, center_x, center_y - size)
    drawLine_mda_allzone(center_x, center_y - size, center_x - size, center_y)
    drawLine_mda_allzone(center_x - size, center_y, center_x, center_y + size)

def initDiamond():
    global diamond_x, diamond_y, diamond_color, diamond_speed
    diamond_x = random.randint(60, 340)
    diamond_y = 360
    diamond_speed = diamond_speed + 5  # slower fall speed
    diamond_color = (random.uniform(0.5,1.0), random.uniform(0.5,1.0), random.uniform(0.5,1.0))

def resetGame():
    global diamond_x, diamond_y, diamond_speed, score, game_over, paused, catcher_x, catcher_color
    diamond_x = random.randint(20, 400 - 20)
    diamond_y = 400 - 20
    diamond_speed = 20.0
    score = 0
    game_over = False
    paused = False
    catcher_x = 400 // 2
    catcher_color = (1.0, 1.0, 1.0)
    print("Starting Over")

def drawCatcher(x, y):
    width = 60           # bottom length (shorter)
    height = 15
    top_width = 80       # top length (longer)

    bottom_left_x = x
    bottom_left_y = y

    bottom_right_x = x + width
    bottom_right_y = y

    top_left_x = x - (top_width - width) // 2
    top_left_y = y + height

    top_right_x = top_left_x + top_width
    top_right_y = y + height
    glColor3f(*catcher_color)
    drawLine_mda_allzone(bottom_left_x, bottom_left_y, bottom_right_x, bottom_right_y)  
    drawLine_mda_allzone(bottom_right_x, bottom_right_y, top_right_x, top_right_y)      
    drawLine_mda_allzone(top_right_x, top_right_y, top_left_x, top_left_y)              
    drawLine_mda_allzone(top_left_x, top_left_y, bottom_left_x, bottom_left_y)          

def drawButtonLeft(x, y):
    glColor3f(0.0, 1.0, 0.5)
    size = 13
    drawLine_mda_allzone(x + size, y + size*2, x, y + size)
    drawLine_mda_allzone(x, y + size, x + size, y)
    drawLine_mda_allzone(x + size, y, x + size, y + size*2)

def drawButtonPlay(x, y, playing):
    glColor3f(1.0, 0.0, 0.0)
    size = 10
    if playing:
        drawLine_mda_allzone(x, y, x, y + size*2)
        drawLine_mda_allzone(x + 5, y, x + 5, y + size*2)
        drawLine_mda_allzone(x, y, x + 5, y)
        drawLine_mda_allzone(x, y + size*2, x + 5, y + size*2)
        rx = x + 10
        drawLine_mda_allzone(rx, y, rx, y + size*2)
        drawLine_mda_allzone(rx + 5, y, rx + 5, y + size*2)
        drawLine_mda_allzone(rx, y, rx + 5, y)
        drawLine_mda_allzone(rx, y + size*2, rx + 5, y + size*2)
    else:
        drawLine_mda_allzone(x, y, x + size*2, y + size)
        drawLine_mda_allzone(x + size*2, y + size, x, y + size*2)
        drawLine_mda_allzone(x, y + size*2, x, y)

def drawButtonExit(x, y):
    glColor3f(1.0, 1.0, 1.0)
    size = 20
    drawLine_mda_allzone(x, y, x + size, y + size)
    drawLine_mda_allzone(x + size, y, x, y + size)

def is_diamond_missed():
    return diamond_y < catcher_y

def move_catcher_left(actual_time):
    global catcher_x
    if not game_over and not paused:
        catcher_x -= catcher_speed * actual_time
        if catcher_x < 0:
            catcher_x = 0

def move_catcher_right(actual_time):
    global catcher_x
    if not game_over and not paused:
        catcher_x += catcher_speed * actual_time
        if catcher_x > 400 - 80:
            catcher_x = 400 - 80



def keyboard_special(key, x, y):
    global last_time
    current_time = time.time()
    actual_time = current_time - last_time
    if key == GLUT_KEY_LEFT:
        move_catcher_left(actual_time)
    elif key == GLUT_KEY_RIGHT:
        move_catcher_right(actual_time)
    last_time = current_time
    glutPostRedisplay()



def mouse_click(button, state, x, y):
    global game_over, paused
    # Scale mouse coords from 500x500 window to 400x400 ortho coords
    scale_x = x * 400 / 500
    scale_y = y * 400 / 500
    screen_y = 400 - scale_y

    if state == GLUT_DOWN:
        if button == GLUT_LEFT_BUTTON:
            if btn_left_x <= scale_x <= btn_left_x + btn_size and btn_left_y <= screen_y <= btn_left_y + btn_size:
                resetGame()
                glutPostRedisplay()
                return
            
            if btn_play_x <= scale_x <= btn_play_x + btn_size and btn_play_y <= screen_y <= btn_play_y + btn_size:
                if not game_over:
                    paused = not paused
                    if paused:
                        print("Paused")
                    else:
                        print("Resumed")
                    glutPostRedisplay()
                return

            if btn_exit_x <= scale_x <= btn_exit_x + btn_size and btn_exit_y <= screen_y <= btn_exit_y + btn_size:
                print(f"Goodbye! Your score was {score}")
                glutLeaveMainLoop()
                return
        # Exit button
        if btn_exit_x <= x <= btn_exit_x + btn_size and btn_exit_y <= screen_y <= btn_exit_y + btn_size:
            print(f"Goodbye! Your score was {score}")
            glutLeaveMainLoop()
            return
            
            

def update():
    global diamond_x, diamond_y, score, game_over, diamond_speed, last_time, catcher_color

    current_time = time.time()
    if last_time == 0:
        last_time = current_time
        return

    actual_time = current_time - last_time
    last_time = current_time

    if not paused and not game_over:
        diamond_y -= diamond_speed * actual_time  # diamond falls vertically

        catcher_box = {
            'x': catcher_x - (80 - 60)//2, 'y': catcher_y, 'w': 80, 'h': 15}

        diamond_box = {'x': diamond_x - 5, 'y': diamond_y - 5, 'w': 10, 'h': 10}

        if hasCollided(catcher_box, diamond_box):
            score += 1
            print(f"Score: {score}")
            diamond_speed += 20  # increase speed gradually
            initDiamond()       # reset diamond position and color

        elif diamond_y < catcher_y:
            game_over = True
            print(f"Game Over! Your final score was {score}")
            catcher_color = (1.0, 0.0, 0.0)

    glutPostRedisplay()

def hasCollided(box1, box2):
    return (box1['x'] < box2['x'] + box2['w'] and
            box1['x'] + box1['w'] > box2['x'] and
            box1['y'] < box2['y'] + box2['h'] and
            box1['y'] + box1['h'] > box2['y'])

glutInit()
glutInitDisplayMode(GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"catch the diamond")
glutDisplayFunc(showScreen)
glClearColor(0.0, 0.0, 0.0, 1.0)
glutIdleFunc(update)
glutSpecialFunc(keyboard_special)
glutMouseFunc(mouse_click)
resetGame()
initDiamond()
glutMainLoop()

