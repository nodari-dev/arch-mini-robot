def draw_eye(fb, x, y, w, h, r, color):
    for i in range(h):
        if i < r:
            offset = int((r*r - (r-i)*(r-i))**0.5)
        elif i >= h - r:
            dy = i - (h - r)
            offset = int((r*r - dy*dy)**0.5)
        else:
            offset = r

        fb.hline(x + r - offset, y + i, w - 2*(r - offset), color)

def fill_circle(fb, cx, cy, r, color):
    for y in range(-r, r+1):
        for x in range(-r, r+1):
            if x*x + y*y <= r*r:
                fb.pixel(cx + x, cy + y, color)

def fill_triangle(fb, x1, y1, x2, y2, x3, y3, color):
    points = sorted([(x1,y1), (x2,y2), (x3,y3)], key=lambda p: p[1])
    x1,y1 = points[0]
    x2,y2 = points[1]
    x3,y3 = points[2]

    def interp(y, y0, x0, y1, x1):
        if y1 == y0:
            return x0
        return int(x0 + (y - y0) * (x1 - x0) / (y1 - y0))

    for y in range(y1, y3+1):
        if y < y2:
            xa = interp(y, y1, x1, y3, x3)
            xb = interp(y, y1, x1, y2, x2)
        else:
            xa = interp(y, y1, x1, y3, x3)
            xb = interp(y, y2, x2, y3, x3)

        if xa > xb:
            xa, xb = xb, xa

        fb.hline(xa, y, xb - xa, color)

def draw_heart(fb, cx, cy, size, color):
    r = size // 2

    fill_circle(fb, cx - r//2 - 1//2, cy - r//2 + 2, r//2 + 2, color)
    fill_circle(fb, cx + r//2 - 1//2 , cy - r//2 + 2, r//2 + 2, color)

    fill_triangle(
        fb,
        cx - r, cy - r//4,
        cx + r, cy - r//4,
        cx,     cy + r,
        color
    )
