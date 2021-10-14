import pygame 

def center(size, fig):
    figw = fig.get_rect()[2]
    figh = fig.get_rect()[3]
    w = size[0]
    h = size[1]
    return (w/2 - figw/2, h/2 - figh/2)

def middle_x(size, fig, y):
    figw = fig.get_rect()[2]
    figh = fig.get_rect()[3]
    w = size[0]
    return (w/2 - figw/2, y - figh/2)

def load_fig(name, size):
    fig = pygame.image.load(name)
    fig = pygame.transform.scale(fig, size)
    return fig

def render_text(text, size, font="Arial", color=(255,255,255)):
    font = pygame.font.SysFont(font, size)
    return font.render(text, True, color)

