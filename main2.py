from math import sqrt
import alg
import pygame
import time
import sys

alg_name = ""
if __name__ == "__main__":
    alg_name = sys.argv[1]

pygame.init()
screen = pygame.display.set_mode((650,600))
pygame.display.set_caption('Binario Game')
GREY = (150,150,150)
WHITE = (255,255,255)
BLACK = (0,0,0)
COLOR1 = (66, 135, 245)
COLOR2 = (235, 158, 52)
COLOR3 = (232, 58, 28)
font = pygame.font.Font('freesansbold.ttf', 20)

next_image = pygame.image.load(r'./next.png')
back_image = pygame.image.load(r'./back.png')

# Game input
puzzle = [
    [0, 1, 0, 0, 0, 0],
    [1, 0, 0, -1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0],
    [0, 0, 0, -1, 0, 0],
    [0, 0, 0, 0, 0, 0]
]

# puzzle = [
#     [0, 1, 0, 1, 0, -1, 0, 0],
#     [1, 0, 0, 0, 0, 0, 0, 1],
#     [0, 0, 0, 0, 1, 0, 0, 0],
#     [0, 1, 0, 0, 0, 0, 0, 0],
#     [0, 0, 1, 0, 0, 1, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, -1, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0]
# ]

# trace array for game demo
trace_state = []
trace_pos_list = []

size = len(puzzle)

# start array for game demo
start = []
for row in range(size):
    start.append([0] * size)
    for col in range(size):
        if puzzle[row][col] != 0:
            start[row][col] = 1
            
print("Puzzle: ")
alg.print_puzzle(puzzle)

# trace array for game demo
p1 = []
for i in range(len(puzzle)):
    p1 += puzzle[i]
current_state = p1
trace_state.append(current_state)

start_time = time.time()

# backtracking algorithm
res = []
if alg_name == "dfs":
    res = alg.backtrackingDFS(trace_state, trace_pos_list, puzzle, 0)
elif alg_name == "hrs":
    res = alg.backtrackingHeuristic(trace_state, trace_pos_list, puzzle, 0)
    
end_time = time.time()

print(">>--------------<<")
if alg.isOk(res):
    print("Solution: ")
    alg.print_puzzle(res)
else:
    print("No solution")

print('Node = ',len(trace_state))

elapsed_time = end_time - start_time
print ("Elapsed time: {0}".format(elapsed_time) + " (secs)")
    
# Game setup
WIDTH = 50
W3 = WIDTH/3
PADDING = 5
BACK_BTN_X = 100
NEXT_BTN_X = 200
BTN_Y = 500
BTN_WIDTH = 75
running = True

# trace var for game demo
trace_count = 0
trace_pos_count = 0
trace_color = COLOR1

# step label for game demo
def stepDisplay(trace_pos):
    text = font.render(f'Step: {trace_pos}', True, COLOR1, WHITE)
    textRect = text.get_rect()
    textRect.center = (550, 100)
    screen.blit(text, textRect)

# draw state for game demo
def draw_state(state):
    size = int(sqrt(len(state)))
    for row in range(size):
        for col in range(size):
            x = (WIDTH+PADDING)*(col+0.5)
            y = (WIDTH+PADDING)*(row+0.5)
            t = row*size + col
            color = COLOR1
            if start[row][col] == 1:
                color = COLOR3
            elif trace_pos_count < len(trace_pos_list):
                if trace_pos_list[trace_pos_count] == (row,col): 
                    color = COLOR2
            pygame.draw.rect(screen, color, (x,y,WIDTH,WIDTH))
            if state[t] == 1:
                pygame.draw.rect(screen, WHITE, (x+W3,y+W3,W3,W3))
            elif state[t] == -1:
                pygame.draw.rect(screen, BLACK, (x+W3,y+W3,W3,W3))

while running:
    screen.fill(GREY)
    stepDisplay(trace_pos_count)
    m_x, m_y = pygame.mouse.get_pos()
    pygame.draw.rect(screen, WHITE, (BACK_BTN_X,BTN_Y,BTN_WIDTH,BTN_WIDTH))
    pygame.draw.rect(screen, WHITE, (NEXT_BTN_X,BTN_Y,BTN_WIDTH,BTN_WIDTH))
    screen.blit(back_image, (BACK_BTN_X, BTN_Y))
    screen.blit(next_image, (NEXT_BTN_X, BTN_Y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if touch on back button 
            if BACK_BTN_X < m_x and m_x < BACK_BTN_X + BTN_WIDTH and BTN_Y < m_y and m_y < BTN_Y + BTN_WIDTH:
                if trace_count > 0 and trace_pos_count > 0:
                    trace_count -= 1
                    trace_pos_count -= 1 
                    current_state = trace_state[trace_count]
                else: print('First')
            # if touch on next button 
            if NEXT_BTN_X < m_x and m_x < NEXT_BTN_X + BTN_WIDTH and BTN_Y < m_y and m_y < BTN_Y + BTN_WIDTH:
                if trace_count < len(trace_state)-1 and trace_pos_count < len(trace_pos_list):
                    trace_count += 1
                    trace_pos_count += 1 
                    current_state = trace_state[trace_count]
                else: print('End')
    draw_state(current_state)        
    pygame.display.flip()
pygame.quit()