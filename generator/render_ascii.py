"""Render the background-removed headshot (face_cutout.png) as ASCII art."""
import os
import sys
from collections import deque
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

# dark -> light; reverse for dark backgrounds so the face reads like a photo
RAMP = "@%#WM8B$&kbdqmwZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

CUTOUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'face_cutout.png')

def render(width=46, gamma=1.6, sharpen=True):
    im = Image.open(CUTOUT)
    bbox = im.getchannel('A').getbbox()
    im = im.crop(bbox)

    alpha = im.getchannel('A')
    gray = im.convert('L')
    gray = ImageOps.autocontrast(gray, cutoff=2)
    if sharpen:
        gray = gray.filter(ImageFilter.UnsharpMask(radius=6, percent=120))

    # chars are ~2.1x taller than wide in monospace
    height = int(im.height / im.width * width * 0.47)
    gray = gray.resize((width, height), Image.LANCZOS)
    alpha = alpha.resize((width, height), Image.LANCZOS)
    gp, ap = gray.load(), alpha.load()

    solid = [[ap[x, y] >= 100 for x in range(width)] for y in range(height)]

    # keep only the largest connected component (drops stray fragments)
    seen = [[False] * width for _ in range(height)]
    best = set()
    for sy in range(height):
        for sx in range(width):
            if solid[sy][sx] and not seen[sy][sx]:
                comp, q = set(), deque([(sx, sy)])
                seen[sy][sx] = True
                while q:
                    x, y = q.popleft()
                    comp.add((x, y))
                    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                        nx, ny = x+dx, y+dy
                        if 0 <= nx < width and 0 <= ny < height \
                           and solid[ny][nx] and not seen[ny][nx]:
                            seen[ny][nx] = True
                            q.append((nx, ny))
                if len(comp) > len(best):
                    best = comp

    n = len(RAMP)
    lines = []
    for y in range(height):
        row = ""
        for x in range(width):
            if (x, y) in best:
                v = (gp[x, y] / 255) ** gamma
                row += RAMP[min(int(v * n), n - 1)]
            else:
                row += " "
        lines.append(row.rstrip())
    while lines and not lines[-1]:
        lines.pop()
    while lines and not lines[0]:
        lines.pop(0)
    return lines

if __name__ == "__main__":
    width = int(sys.argv[1]) if len(sys.argv) > 1 else 46
    print("\n".join(render(width)))
