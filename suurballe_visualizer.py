import sys
import math
import pygame
from collections import defaultdict
from heapq import heapify, heappop, heappush


def dijkstra_heap(G, s):
    E = set()
    E.add(s)
    p = dict()
    p[s] = [s]
    d = dict()
    d[s] = 0
    edge = []
    for initial in G[s]:
        together = (initial[1], s, initial[0])
        edge.append(together)
    heapify(edge)
    while edge:
        v = heappop(edge)
        if v[2] not in E:
            E.add(v[2])
            d[v[2]] = v[0]
            p[v[2]] = p[v[1]] + [v[2]]
            for values in G[v[2]]:
                if values[0] not in E:
                    heappush(edge, (v[0] + values[1], v[2], values[0]))
        continue
    return p


def suurballe(G, start, end):
    paths = dijkstra_heap(G, start)
    first_path = paths[end]
    graph = G.copy()
    for i in range(0, len(first_path) - 1):
        graph[first_path[i]] = [(node, distance) for node, distance in graph[first_path[i]] if node != first_path[i + 1]]
        graph[first_path[i + 1]] = graph[first_path[i + 1]] + [(first_path[i], 0)]
    path_2 = dijkstra_heap(graph, start)
    second_path = path_2[end]

    output = defaultdict(list)
    for i in range(0, len(first_path) - 1):
        output[first_path[i]].append(first_path[i + 1])
    for i in range(0, len(second_path) - 1):
        output[second_path[i]].append(second_path[i + 1])

    for i in range(0, len(first_path) - 1):
        if first_path[i + 1] in output[first_path[i]] and first_path[i] in output[first_path[i + 1]]:
            output[first_path[i]].remove(first_path[i + 1])
            output[first_path[i + 1]].remove(first_path[i])

    return output


pygame.init()

WIDTH, HEIGHT = 1000, 680
FPS = 60

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (210, 213, 219)
DARK_GRAY = (110, 116, 128)
RED = (220, 50, 50)
GREEN = (40, 170, 90)
BLUE = (50, 110, 230)
YELLOW = (240, 200, 40)
PURPLE = (150, 80, 200)
ORANGE = (245, 140, 30)
PANEL = (238, 240, 244)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Suurballe Algorithm Visualizer")
clock = pygame.time.Clock()

title_font = pygame.font.SysFont(None, 60)
font = pygame.font.SysFont(None, 30)
small_font = pygame.font.SysFont(None, 24)
tiny_font = pygame.font.SysFont(None, 20)

NODE_R = 18
CANVAS_TOP = 96
CANVAS_BOTTOM = HEIGHT - 110


def draw_text(surface, text, fnt, color, center):
    text_image = fnt.render(text, True, color)
    surface.blit(text_image, text_image.get_rect(center=center))


def draw_text_left(surface, text, fnt, color, topleft):
    text_image = fnt.render(text, True, color)
    surface.blit(text_image, text_image.get_rect(topleft=topleft))


class Button:
    def __init__(self, text, center, size=(170, 46),
                 color=GRAY, hover_color=YELLOW, text_color=BLACK):
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.rect.center = center
        self.active = False

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.active:
            current_color = ORANGE
        elif self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
        else:
            current_color = self.color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        draw_text(surface, self.text, small_font, self.text_color, self.rect.center)

    def is_clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                and self.rect.collidepoint(event.pos))


def make_preset():
    nodes = [
        (90, 333),
        (230, 175), (230, 333), (230, 491),
        (390, 150), (390, 260), (390, 406), (390, 516),
        (560, 200), (560, 333), (560, 466),
        (720, 255), (720, 411),
        (880, 333),
    ]
    raw_edges = [
        (0, 1, 4), (0, 2, 2), (0, 3, 5),
        (1, 2, 2), (2, 3, 2),
        (1, 4, 3), (1, 5, 2), (2, 5, 4), (2, 6, 3), (3, 6, 2), (3, 7, 4),
        (4, 5, 2), (5, 6, 3), (6, 7, 2),
        (4, 8, 3), (5, 8, 2), (5, 9, 4), (6, 9, 3), (6, 10, 2), (7, 10, 3),
        (8, 9, 2), (9, 10, 2),
        (8, 11, 3), (9, 11, 2), (9, 12, 4), (10, 12, 2),
        (11, 12, 3),
        (11, 13, 4), (12, 13, 2),
    ]
    edges = []
    graph = defaultdict(list)
    for a, b, w in raw_edges:
        edges.append((nodes[a], nodes[b], w))
        graph[nodes[a]].append((nodes[b], w))
        graph[nodes[b]].append((nodes[a], w))
    start = nodes[0]
    end = nodes[13]
    return nodes, edges, graph, start, end


def edge_in_output(a, b, output):
    if output is None:
        return False
    return b in output[a] or a in output[b]


def trace_path(routes, start, end):
    path = [start]
    while path[-1] != end:
        path.append(routes[path[-1]].pop(0))
    return path


def main():
    game_state = "menu"
    mode = "edit"
    weight_text = ""
    pending = None

    nodes = []
    selected = []
    edges = []
    graph = defaultdict(list)
    start = None
    end = None

    output = None
    first_path = None
    result_ok = False
    status = ""

    reveal_edges = []
    reveal_count = 0
    reveal_timer = 0
    orange_edges = set()

    start_button = Button("Build Your Own", (WIDTH // 2, 300), size=(280, 56))
    preset_button = Button("Load Preset Graph", (WIDTH // 2, 374), size=(280, 56))
    instructions_button = Button("Instructions", (WIDTH // 2, 448), size=(280, 56))
    quit_button = Button("Quit", (WIDTH // 2, 522), size=(280, 56))

    y = HEIGHT - 60
    gap = 180
    start_node_button = Button("Set Start", (100 + gap * 0, y), size=(150, 46))
    end_node_button = Button("Set End", (100 + gap * 1, y), size=(150, 46))
    run_button = Button("Run Suurballe", (100 + gap * 2, y), size=(170, 46),
                        color=GREEN, hover_color=(90, 210, 130), text_color=WHITE)
    preset2_button = Button("Preset", (100 + gap * 3, y), size=(120, 46))
    clear_button = Button("Clear", (100 + gap * 3 + 150, y), size=(110, 46))
    menu_button = Button("Menu", (WIDTH - 80, y), size=(120, 46))
    build_buttons = [start_node_button, end_node_button, run_button,
                     preset2_button, clear_button, menu_button]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif game_state == "menu":
                if start_button.is_clicked(event):
                    nodes = []
                    selected = []
                    edges = []
                    graph = defaultdict(list)
                    start = None
                    end = None
                    output = None
                    result_ok = False
                    status = ""
                    game_state = "build"
                    mode = "edit"
                elif preset_button.is_clicked(event):
                    nodes, edges, graph, start, end = make_preset()
                    selected = []
                    output = None
                    result_ok = False
                    status = ""
                    game_state = "build"
                    mode = "edit"
                elif instructions_button.is_clicked(event):
                    game_state = "instructions"
                elif quit_button.is_clicked(event):
                    running = False

            elif game_state == "instructions":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_state = "menu"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    game_state = "menu"

            elif game_state == "build":
                if mode == "weight":
                    if event.type == pygame.KEYDOWN:
                        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            if weight_text:
                                a, b = pending
                                w = int(weight_text)
                                edges.append((a, b, w))
                                graph[a].append((b, w))
                                graph[b].append((a, w))
                            pending = None
                            weight_text = ""
                            selected.clear()
                            mode = "edit"
                        elif event.key == pygame.K_ESCAPE:
                            pending = None
                            weight_text = ""
                            selected.clear()
                            mode = "edit"
                        elif event.key == pygame.K_BACKSPACE:
                            weight_text = weight_text[:-1]
                        elif event.unicode.isdigit() and len(weight_text) < 4:
                            weight_text += event.unicode
                    continue

                if menu_button.is_clicked(event):
                    game_state = "menu"
                    mode = "edit"
                    output = None
                    result_ok = False
                    continue
                if clear_button.is_clicked(event):
                    nodes = []
                    selected = []
                    edges = []
                    graph = defaultdict(list)
                    start = None
                    end = None
                    output = None
                    result_ok = False
                    status = ""
                    mode = "edit"
                    continue
                if preset2_button.is_clicked(event):
                    nodes, edges, graph, start, end = make_preset()
                    selected = []
                    output = None
                    result_ok = False
                    status = ""
                    mode = "edit"
                    continue
                if start_node_button.is_clicked(event):
                    mode = "set_start" if mode != "set_start" else "edit"
                    selected.clear()
                    continue
                if end_node_button.is_clicked(event):
                    mode = "set_end" if mode != "set_end" else "edit"
                    selected.clear()
                    continue
                if run_button.is_clicked(event):
                    if start is None or end is None:
                        status = "Set a start and an end first."
                    elif start == end:
                        status = "Start and end must be different."
                    else:
                        paths = dijkstra_heap(graph, start)
                        if end not in paths:
                            output = None
                            result_ok = False
                            status = "No path from start to end."
                        else:
                            first_path = paths[end]
                            try:
                                output = suurballe(graph, start, end)
                                result_ok = True
                            except KeyError:
                                output = None
                                result_ok = False
                            status = ""
                            mode = "result"
                            reveal_edges = []
                            orange_edges = set()
                            if result_ok:
                                queue = [start]
                                seen = set()
                                while queue:
                                    u = queue.pop(0)
                                    for v in output.get(u, []):
                                        key = frozenset((u, v))
                                        if key not in seen:
                                            seen.add(key)
                                            reveal_edges.append(key)
                                            queue.append(v)
                                routes = {node: list(output[node]) for node in output}
                                one_path = trace_path(routes, start, end)
                                for i in range(0, len(one_path) - 1):
                                    orange_edges.add(frozenset((one_path[i], one_path[i + 1])))
                            else:
                                for i in range(0, len(first_path) - 1):
                                    reveal_edges.append(frozenset((first_path[i], first_path[i + 1])))
                            reveal_count = 0
                            reveal_timer = 0
                    continue

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        output = None
                        result_ok = False
                        selected.clear()
                        mode = "edit"
                    elif event.key == pygame.K_c:
                        nodes = []
                        selected = []
                        edges = []
                        graph = defaultdict(list)
                        start = None
                        end = None
                        output = None
                        result_ok = False
                        mode = "edit"

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3 and mode in ("edit", "set_start", "set_end"):
                        for node in list(nodes):
                            if math.dist(event.pos, node) <= NODE_R:
                                nodes.remove(node)
                                edges = [(a, b, w) for (a, b, w) in edges if a != node and b != node]
                                if node in graph:
                                    del graph[node]
                                for key in graph:
                                    graph[key] = [(nb, w) for (nb, w) in graph[key] if nb != node]
                                if node in selected:
                                    selected.remove(node)
                                if start == node:
                                    start = None
                                if end == node:
                                    end = None
                                output = None
                                result_ok = False
                                break
                    elif event.button == 1 and CANVAS_TOP <= event.pos[1] <= CANVAS_BOTTOM:
                        if mode == "result":
                            continue
                        clicked = None
                        for node in nodes:
                            if math.dist(event.pos, node) <= NODE_R:
                                clicked = node
                                break
                        if mode == "set_start":
                            if clicked is not None:
                                start = clicked
                                mode = "edit"
                        elif mode == "set_end":
                            if clicked is not None:
                                end = clicked
                                mode = "edit"
                        else:
                            if clicked is None:
                                nodes.append(event.pos)
                            else:
                                selected.append(clicked)
                                if len(selected) == 2:
                                    if selected[0] == selected[1]:
                                        selected.clear()
                                    else:
                                        pending = (selected[0], selected[1])
                                        weight_text = ""
                                        mode = "weight"

        if game_state == "build" and mode == "result" and reveal_count < len(reveal_edges):
            reveal_timer += 1
            if reveal_timer >= 8:
                reveal_timer = 0
                reveal_count += 1

        screen.fill(WHITE)

        if game_state == "menu":
            draw_text(screen, "Suurballe Visualizer", title_font, BLUE, (WIDTH // 2, 150))
            draw_text(screen, "Two routes that never share a road", font, DARK_GRAY, (WIDTH // 2, 205))
            start_button.draw(screen)
            preset_button.draw(screen)
            instructions_button.draw(screen)
            quit_button.draw(screen)

        elif game_state == "instructions":
            draw_text(screen, "How to use", title_font, BLUE, (WIDTH // 2, 90))
            lines = [
                "BUILD a graph:",
                "  - Click empty space to drop a numbered node.",
                "  - Click one node, then another, to start an edge.",
                "  - Type the distance (a number) and press ENTER.",
                "  - Right-click a node to delete it and its roads.",
                "",
                "CHOOSE endpoints:",
                "  - Click 'Set Start', then click a node (turns green).",
                "  - Click 'Set End', then click a node (turns red).",
                "",
                "RUN:",
                "  - Click 'Run Suurballe'.",
                "  - The two backup routes light up in green and orange.",
                "  - If only one route exists, that single route lights up instead.",
                "",
                "SHORTCUTS:  'Preset' loads a ready graph  -  'Clear' wipes it  -  ESC backs out.",
                "",
                "(Click anywhere or press ESC to go back.)",
            ]
            yy = 150
            for line in lines:
                draw_text_left(screen, line, small_font, BLACK, (120, yy))
                yy += 28

        elif game_state == "build":
            pygame.draw.rect(screen, PANEL, pygame.Rect(0, 0, WIDTH, CANVAS_TOP))
            draw_text_left(screen, "Suurballe Visualizer", font, BLACK, (20, 18))
            if mode == "edit":
                hint = "Click empty space = new node.  Click two nodes = make an edge."
            elif mode == "set_start":
                hint = "Click a node to set it as the START."
            elif mode == "set_end":
                hint = "Click a node to set it as the END."
            elif mode == "weight":
                hint = "Type the distance and press ENTER:  " + weight_text
            elif mode == "result":
                if result_ok:
                    total = 0
                    for a, b, w in edges:
                        if edge_in_output(a, b, output):
                            total += w
                    hint = "Two backup routes found with no shared road  (total length " + str(total) + ").  ESC to edit."
                else:
                    hint = "Only one route exists -- a single closed road could cut it off.  ESC to edit."
            else:
                hint = ""
            draw_text_left(screen, hint, small_font, DARK_GRAY, (20, 58))
            if status:
                draw_text_left(screen, status, small_font, RED, (WIDTH - 360, 58))

            canvas = pygame.Rect(0, CANVAS_TOP, WIDTH, CANVAS_BOTTOM - CANVAS_TOP)
            pygame.draw.rect(screen, WHITE, canvas)

            revealed = set(reveal_edges[:reveal_count])
            for a, b, w in edges:
                color = DARK_GRAY
                width = 3
                if mode == "result" and frozenset((a, b)) in revealed:
                    width = 6
                    if frozenset((a, b)) in orange_edges:
                        color = ORANGE
                    else:
                        color = GREEN
                pygame.draw.line(screen, color, a, b, width)
                mid = ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)
                pad = pygame.Rect(0, 0, 26, 22)
                pad.center = mid
                pygame.draw.rect(screen, WHITE, pad, border_radius=5)
                pygame.draw.rect(screen, GRAY, pad, 1, border_radius=5)
                draw_text(screen, str(w), tiny_font, BLACK, mid)

            if len(selected) == 1:
                pygame.draw.line(screen, PURPLE, selected[0], pygame.mouse.get_pos(), 2)

            count = 0
            for node in nodes:
                if node == start:
                    color = GREEN
                elif node == end:
                    color = RED
                elif node in selected:
                    color = PURPLE
                else:
                    color = BLUE
                pygame.draw.circle(screen, color, node, NODE_R)
                pygame.draw.circle(screen, BLACK, node, NODE_R, 2)
                draw_text(screen, str(count), small_font, WHITE, node)
                if node == start:
                    draw_text(screen, "start", tiny_font, GREEN, (node[0], node[1] + NODE_R + 12))
                elif node == end:
                    draw_text(screen, "end", tiny_font, RED, (node[0], node[1] + NODE_R + 12))
                count += 1

            pygame.draw.rect(screen, PANEL, pygame.Rect(0, CANVAS_BOTTOM, WIDTH, HEIGHT - CANVAS_BOTTOM))
            start_node_button.active = (mode == "set_start")
            end_node_button.active = (mode == "set_end")
            for button in build_buttons:
                button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
