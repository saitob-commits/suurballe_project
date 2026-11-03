"""
PyGame Starter Template
=======================

This file shows the five building blocks you need for your graph
visualization project:

    1. Importing and setting up PyGame
    2. A game loop with a simple animation (a bouncing ball)
    3. Drawing shapes (rectangles, circles, lines, polygons, text)
    4. Moving something with the keyboard
    5. Creating clickable buttons for a menu

HOW TO INSTALL PYGAME
---------------------
PyGame is not part of the standard Python library, so install it once
from a terminal (not inside the Python prompt):

    Mac / Linux:   python3 -m pip install pygame
    Windows:       py -m pip install pygame

Using "python -m pip" (instead of just "pip") makes sure PyGame gets
installed for the same Python you will use to run this file.

Check that it worked by running one of PyGame's built-in demos:

    Mac / Linux:   python3 -m pygame.examples.aliens
    Windows:       py -m pygame.examples.aliens

HOW TO RUN THIS FILE
--------------------
    python3 tutorial.py        (Windows: py tutorial.py)
"""

# =====================================================================
# SECTION 1: IMPORTS AND SETUP
# =====================================================================
import sys       # used to exit the program cleanly with sys.exit()
import pygame    # the game/graphics library (installed with pip, see above)
import math
import defaultdict from collections

# pygame.init() starts up all of PyGame's modules (display, fonts, sound,
# etc.). It must be called before you use almost anything else in PyGame.
pygame.init()

# --- Window settings ---
WIDTH, HEIGHT = 800, 600   # window size in pixels
FPS = 60                   # frames per second: how often we redraw

# --- Colors ---
# Colors are (Red, Green, Blue) tuples. Each value goes from 0 to 255.
# (0, 0, 0) is black and (255, 255, 255) is white.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
RED = (220, 50, 50)
GREEN = (50, 180, 80)
BLUE = (50, 100, 220)
YELLOW = (240, 200, 40)
PURPLE = (150, 80, 200)
ORANGE = (255, 140, 0)

# Create the window. The value returned is a "Surface" -- think of it as
# the canvas that everything gets drawn on.
#
# IMPORTANT: PyGame's coordinate system starts at the TOP-LEFT corner.
#   (0, 0) is the top-left, x grows to the RIGHT, and y grows DOWNWARD.
#   So (WIDTH, HEIGHT) is the bottom-right corner.
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyGame Starter Template")

# A Clock lets us control how fast the game loop runs (see clock.tick below).
clock = pygame.time.Clock()

# Fonts: SysFont(name, size). Passing None as the name uses PyGame's
# default font, which works on every computer.
title_font = pygame.font.SysFont(None, 64)
font = pygame.font.SysFont(None, 32)
small_font = pygame.font.SysFont(None, 24)


# =====================================================================
# SECTION 2: DRAWING SHAPES
# =====================================================================
def draw_text(surface, text, fnt, color, center):
    """Draw text centered on the point `center`.

    Text in PyGame is a two-step process:
      1. font.render() turns the string into an image (a Surface).
      2. surface.blit() copies ("stamps") that image onto the screen.
    """
    # True = smooth (anti-aliased) edges on the letters
    text_image = fnt.render(text, True, color)
    # get_rect(center=...) gives us a rectangle the same size as the text,
    # positioned so its center is at `center`. This makes centering easy.
    text_rect = text_image.get_rect(center=center)
    surface.blit(text_image, text_rect)


def draw_shapes(surface):
    """Show off the basic pygame.draw functions.

    Most draw functions follow the pattern:
        pygame.draw.SHAPE(surface, color, <position/size info>, width)
    If width is 0 (or left out) the shape is FILLED.
    If width is > 0, only the OUTLINE is drawn, that many pixels thick.
    """
    # Rectangle: pygame.Rect(x, y, width, height)
    # where (x, y) is the rectangle's top-left corner.
    pygame.draw.rect(surface, BLUE, pygame.Rect(30, 60, 120, 70))     # filled
    pygame.draw.rect(surface, RED, pygame.Rect(170, 60, 120, 70), 4)  # outline
    pygame.draw.rect(surface, GREEN, pygame.Rect(310, 60, 120, 70),
                     border_radius=15)                       # rounded corners

    # Circle: (center_x, center_y) and a radius.
    pygame.draw.circle(surface, YELLOW, (500, 95), 35)       # filled
    pygame.draw.circle(surface, PURPLE, (590, 95), 35, 5)    # outline only

    # Ellipse: drawn to fit inside the given rectangle.
    pygame.draw.ellipse(surface, GREEN, pygame.Rect(650, 70, 120, 50))

    # Polygon: a list of corner points, connected in order. This is a triangle.
    pygame.draw.polygon(surface, RED, [(60, 230), (20, 290), (100, 290)])

    # Line: start point, end point, thickness.
    pygame.draw.line(surface, BLACK, (130, 230), (280, 290), 3)

    # ---- A tiny graph! (preview of your final project) ----
    # Nodes are just circles and edges are just lines between their centers.
    # Draw the EDGES FIRST so the node circles are drawn on top of them.
    nodes = {"A": (400, 220), "B": (330, 300), "C": (470, 300)}
    edges = [("A", "B"), ("A", "C"), ("B", "C")]
    for start, end in edges:
        pygame.draw.line(surface, DARK_GRAY, nodes[start], nodes[end], 3)
    for name, position in nodes.items():
        pygame.draw.circle(surface, BLUE, position, 22)
        pygame.draw.circle(surface, BLACK, position, 22, 2)   # black border
        draw_text(surface, name, font, WHITE, position)

    # Labels so students can see which function made which shape.
    draw_text(surface, "rect / circle / ellipse", small_font, BLACK, (400, 30))
    draw_text(surface, "polygon & line", small_font, BLACK, (150, 310))
    draw_text(surface, "a tiny graph", small_font, BLACK, (400, 335))


# =====================================================================
# SECTION 5: BUTTONS
# (Defined here so the main loop below can use it.)
# =====================================================================
class Button:
    """A clickable rectangle with text on it.

    PyGame has no built-in button, so we make our own from:
      - a Rect (where the button is),
      - draw code (what it looks like),
      - a click check (did the mouse click inside the Rect?).
    """

    def __init__(self, text, center, size=(200, 50),
                 color=GRAY, hover_color=YELLOW):
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.rect.center = center   # position the button by its center point

    def draw(self, surface):
        # collidepoint(x, y) returns True if that point is inside the
        # rectangle. Here we use it to check whether the mouse is hovering
        # over the button.
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
        else:
            current_color = self.color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        # Draw a 2-pixel black border on top of the filled button.
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        draw_text(surface, self.text, font, BLACK, self.rect.center)

    def is_clicked(self, event):
        """Return True if this event is a left-click inside the button."""
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1                 # 1 = left mouse button
                and self.rect.collidepoint(event.pos))


# =====================================================================
# THE MAIN PROGRAM / GAME LOOP
# =====================================================================
def main():
    # ---- Game state ----
    # A "state" variable remembers which screen we are on. Each pass through
    # the loop we check it to decide what to draw and which input to handle.
    # Adding a new screen = adding a new state value.
    game_state = "menu"     # either "menu" or "demo"

    # ---- Menu buttons ----
    start_button = Button("Start Demo", (WIDTH // 2, 300))
    quit_button = Button("Quit", (WIDTH // 2, 380))
    instructions_button = Button("Instructions", (WIDTH // 2, 460))
    # Button shown on the demo screen to go back to the menu.
    menu_button = Button("Menu", (WIDTH - 80, HEIGHT - 40), size=(120, 40))

    # ---- SECTION 3: Animation data (the bouncing ball) ----
    # Position (x, y) and velocity (dx, dy). Velocity = how many pixels the
    # ball moves each frame in each direction.
    ball_x, ball_y = 100, 450
    ball_dx, ball_dy = 4, 3
    ball_radius = 20
    ball_paused = False

    two_ball_x, two_ball_y = 200, 550
    two_ball_dx, two_ball_dy = 4, 3
    two_ball_radius = 20
    two_ball_paused = False

    # ---- SECTION 4: Keyboard-controlled player ----
    # Using a Rect for the player gives us handy tools like .clamp_ip() below.
    player = pygame.Rect(WIDTH // 2, 450, 40, 40)
    player_speed = 5


    nodes = []
    selected = []
    edges = []
    graph = defaultdict(list)

    running = True
    while running:
        # Every game loop does the same 3 steps, over and over:
        #   1. HANDLE EVENTS  (what did the user do?)
        #   2. UPDATE         (move things / change data)
        #   3. DRAW           (redraw the whole screen)

        # ---------------- 1. HANDLE EVENTS ----------------
        # pygame.event.get() returns everything that happened since the last
        # frame: key presses, mouse clicks, closing the window, etc.
        # You MUST call it every frame, or the window will freeze.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:     # user clicked the window's X
                running = False

            elif game_state == "menu":
                if start_button.is_clicked(event):
                    game_state = "demo"
                elif instructions_button.is_clicked(event):
                    game_state = "instructions"
                elif quit_button.is_clicked(event):
                    running = False

            elif game_state == "demo":
                if menu_button.is_clicked(event):
                    game_state = "menu"
                # KEYDOWN happens ONCE at the moment a key is pressed.
                # Use it for one-time actions (toggle, select, open menu).
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        ball_paused = not ball_paused
                        two_ball_paused = not two_ball_paused
                    elif event.key == pygame.K_ESCAPE:
                        game_state = "menu"
                    elif event.key == pygame.K_EQUALS:
                        player_speed = min(20, player_speed + 1)
                    elif event.key == pygame.K_MINUS:
                        player_speed = max(1, player_speed - 1)
                    elif event.key == pygame.K_c:
                        selected.clear()
                        nodes.clear()
                        edges.clear()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and event.pos[1] > 360:
                        
                        found = False

                        for node in nodes:
                            if math.dist(event.pos, node) < 10:
                                selected.append(node)
                                found = True
                                break

                        if not found:
                            nodes.append(event.pos)
                        elif len(selected) == 2:
                            start_node = selected[0]
                            end_node = selected[1]
                            edges.append((start_node, end_node))
                            graph[start_node].append(end_node)
                            graph[end_node].append(start_node)
                            selected.clear()

            
            elif game_state == "instructions":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = "menu"
        # ---------------- 2. UPDATE ----------------
        if game_state == "demo":
            # --- Bouncing ball animation ---
            if not ball_paused:
                ball_x += ball_dx
                ball_y += ball_dy
                # If the ball's edge goes past a wall, flip the sign of its
                # velocity so it travels the opposite way ("bounces").
                if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
                    ball_dx = -ball_dx
                # The top of the bouncing area is y=360 so the ball stays
                # below the shapes demo.
                if (ball_y - ball_radius <= 360
                        or ball_y + ball_radius >= HEIGHT):
                    ball_dy = -ball_dy
            if not two_ball_paused:
                two_ball_x += two_ball_dx
                two_ball_y += two_ball_dy
                # If the ball's edge goes past a wall, flip the sign of its
                # velocity so it travels the opposite way ("bounces").
                if two_ball_x - two_ball_radius <= 0 or two_ball_x + two_ball_radius >= WIDTH:
                    two_ball_dx = -two_ball_dx
                # The top of the bouncing area is y=360 so the ball stays
                # below the shapes demo.
                if (two_ball_y - two_ball_radius <= 360
                        or two_ball_y + two_ball_radius >= HEIGHT):
                    two_ball_dy = -two_ball_dy
            # --- Keyboard movement ---
            # get_pressed() tells us which keys are HELD DOWN right now.
            # Unlike KEYDOWN, this is true every frame while the key is held,
            # so it gives smooth, continuous movement.
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.x -= player_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.x += player_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player.y -= player_speed     # remember: UP means SMALLER y
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player.y += player_speed
            # clamp_ip() pushes the rect back inside the screen if it went
            # off an edge. ("ip" = "in place": it changes `player` directly.)
            player.clamp_ip(screen.get_rect())

        # ---------------- 3. DRAW ----------------
        # Start each frame by filling the screen with a background color.
        # This erases last frame's drawing -- without it, moving objects
        # would leave a "trail" behind them.
        screen.fill(WHITE)

        if game_state == "menu":
            draw_text(screen, "Graph Visualizer", title_font, BLUE,
                      (WIDTH // 2, 150))
            draw_text(screen, "PyGame Starter Template", font, DARK_GRAY,
                      (WIDTH // 2, 210))
            start_button.draw(screen)
            quit_button.draw(screen)
            instructions_button.draw(screen)

        elif game_state == "demo":
            draw_shapes(screen)
            # Line separating the shapes area from the animation area.
            pygame.draw.line(screen, GRAY, (0, 360), (WIDTH, 360), 2)
            # Things drawn LATER appear ON TOP, so draw the background text
            # first and the moving objects after it.
            draw_text(screen,
                      "Arrows/WASD: move   SPACE: pause ball   ESC: menu",
                      small_font, DARK_GRAY, (WIDTH // 2 - 60, HEIGHT - 40))
            draw_text(screen, f"Speed: {player_speed}", font, DARK_GRAY,(WIDTH // 3, 500))
            pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
            pygame.draw.circle(screen, ORANGE, (two_ball_x, two_ball_y), two_ball_radius)
            pygame.draw.rect(screen, GREEN, player)
            menu_button.draw(screen)
            count = 1
            for start_node, end_node in edges:
                pygame.draw.line(screen, BLACK, start_node, end_node, 2)
            for node in nodes:
                if node in selected:
                    pygame.draw.circle(screen, RED, node, 10)
                else:
                    pygame.draw.circle(screen, BLUE, node, 10)
                draw_text(screen, str(count), font, WHITE, node)
                count += 1

            

        elif game_state == "instructions":
            draw_text(screen, "Instructions", title_font, BLUE,
                      (WIDTH // 2, 150))
            draw_text(screen, "Use the arrow keys or WASD to move the green square.",
                      font, DARK_GRAY, (WIDTH // 2, 250))
            draw_text(screen, "Press SPACE to pause/resume the bouncing balls.",
                      font, DARK_GRAY, (WIDTH // 2, 300))
            draw_text(screen, "Press ESC to return to the menu.",
                      font, DARK_GRAY, (WIDTH // 2, 350))
            draw_text(screen, "Press + or - to change the speed of the green square.",
                      font, DARK_GRAY, (WIDTH // 2, 400))
            draw_text(screen,
                      "The bouncing balls will bounce off the edges of the window.",
                      font, DARK_GRAY, (WIDTH // 2, 450))
            draw_text(screen,
                      "Press ESC to return to the menu.",
                      font, DARK_GRAY, (WIDTH // 2, 550))
        # Everything above was drawn to a hidden "back buffer".
        # flip() shows the finished frame on the real screen all at once,
        # which prevents flickering. Nothing appears until you call this!
        pygame.display.flip()

        # tick(FPS) pauses just long enough to keep the loop at FPS frames
        # per second. Without it, the game would run as fast as the computer
        # allows -- super fast on some machines, slow on others.
        clock.tick(FPS)

    # The loop has ended: shut PyGame down and close the program.
    pygame.quit()
    sys.exit()


# This means "only run main() if this file is run directly"
# (not when it is imported by another file).
if __name__ == "__main__":
    main()
