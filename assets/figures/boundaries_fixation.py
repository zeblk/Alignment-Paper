import json, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse
from matplotlib.lines import Line2D

# Regenerates assets/figures/boundaries_fixation.{pdf,svg} from the node/edge
# geometry extracted out of the original Google Slides sketches
# ("sketch 1.svg", "sketch 2.svg") into panels.json / ellipses.json.
#   python3 boundaries_fixation.py
import os
SP = os.path.dirname(os.path.abspath(__file__))
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica', 'Arial', 'DejaVu Sans'],
    'mathtext.fontset': 'custom',
    'mathtext.rm': 'Helvetica', 'mathtext.it': 'Helvetica:italic',
    'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none',
})

INK       = '#1C222B'
EDGE      = '#4A525E'
GATED     = '#7B8697'
ACCENT    = '#C4761E'
ACCENT_FL = '#FDF3E6'
MUTED     = '#6B7684'
RULE      = '#DCE0E6'

data = json.load(open(f'{SP}/panels.json'))
ells = json.load(open(f'{SP}/ellipses.json'))
for i, p in enumerate(data['b']):
    p['ell'] = ells[i]
for p in data['a']:
    p['ell'] = None

# ---------- jostling ------------------------------------------------------
# The three b-panels are the same network re-drawn after some jostling.  In the
# sketches the larger component (the parts outside the boundary) sat at 0 deg at
# t1, -60 deg at t2 and back at 0 deg at t3, so t1 and t3 read as static.  Turn
# the whole t3 panel -- nodes and boundary together -- so every step differs.
EXTRA_B_ROT = [0.0, 0.0, -110.0]      # deg, applied to row b panels as a whole

# Row b's panels are the same network re-drawn after some jostling.  Measure
# how far the *larger* component -- the parts lying outside the semi-permeable
# boundary -- has turned between b-panels, and turn row a's network by the same
# angle, so both rows depict the same underlying jostle.

def _outside(panel, el):
    """Nodes of `panel` that fall outside its boundary ellipse."""
    th = math.radians(el['angle'])
    out = []
    for x, y in panel['nodes']:
        dx, dy = x - el['cx'], y - el['cy']
        u = dx * math.cos(th) + dy * math.sin(th)
        v = -dx * math.sin(th) + dy * math.cos(th)
        if (u / el['a']) ** 2 + (v / el['b']) ** 2 > 1.0:
            out.append((x, y))
    return out

def _centre(pts):
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))

def _rotate(pts, deg, about):
    t = math.radians(deg); c, s_ = math.cos(t), math.sin(t)
    ox, oy = about
    return [(ox + (x - ox) * c - (y - oy) * s_,
             oy + (x - ox) * s_ + (y - oy) * c) for x, y in pts]

def _rotation_between(src, ref, step=0.25):
    """Rigid rotation (deg) carrying point set `src` onto `ref`, centroids aligned.

    Note the direction: to turn row a by the same amount row b turned, we ask
    for the rotation carrying the t1 reference ONTO panel i, not the inverse.
    """
    sc, rc = _centre(src), _centre(ref)
    S = [(x - sc[0], y - sc[1]) for x, y in src]
    R = [(x - rc[0], y - rc[1]) for x, y in ref]
    best = (0.0, float('inf'))
    d = 0.0
    while d < 360.0:
        Sr = _rotate(S, d, (0.0, 0.0))
        cost = (sum(min(math.dist(a, b) for b in R) for a in Sr) / len(Sr)
                + sum(min(math.dist(b, a) for a in Sr) for b in R) / len(R))
        if cost < best[1]:
            best = (d, cost)
        d += step
    return best

for i, extra in enumerate(EXTRA_B_ROT):
    if not extra:
        continue
    pan = data['b'][i]
    piv = _centre(pan['nodes'])
    pan['nodes'] = _rotate(pan['nodes'], extra, piv)
    el = pan['ell']
    (el['cx'], el['cy']) = _rotate([(el['cx'], el['cy'])], extra, piv)[0]
    el['angle'] += extra

# row a inherits the rotation of row b's larger (outside-the-boundary) component
_ref = _outside(data['b'][0], data['b'][0]['ell'])
JOSTLE = []
for i in range(3):
    deg, resid = _rotation_between(_ref, _outside(data['b'][i], data['b'][i]['ell']))
    deg = (deg + 180.0) % 360.0 - 180.0          # to (-180, 180]
    JOSTLE.append(deg)
    print(f'  row b panel {i + 1}: outside component rotated {deg:+7.2f} deg '
          f'(residual {resid:.3f} src units)')

# row a is one network, re-drawn at each time under the same jostle
_base = data['a'][0]
_pivot = _centre(_base['nodes'])
data['a'] = [{'nodes': _rotate(_base['nodes'], deg, _pivot),
              'edges': _base['edges'], 'ell': None} for deg in JOSTLE]

# ---------- true extents (rotated ellipse included) ----------------------
def extent(panel):
    xs = [p[0] for p in panel['nodes']]; ys = [p[1] for p in panel['nodes']]
    el = panel['ell']
    if el:
        th = math.radians(el['angle']); a, b = el['a'], el['b']
        hx = math.hypot(a * math.cos(th), b * math.sin(th))
        hy = math.hypot(a * math.sin(th), b * math.cos(th))
        xs += [el['cx'] - hx, el['cx'] + hx]; ys += [el['cy'] - hy, el['cy'] + hy]
    return min(xs), max(xs), min(ys), max(ys)

BOX = {k: [extent(p) for p in data[k]] for k in ('a', 'b')}
BBW = max(e[1] - e[0] for k in BOX for e in BOX[k])
BBH = {k: max(e[3] - e[2] for e in BOX[k]) for k in BOX}

# ---------------- geometry (inches) --------------------------------------
FIG_W = 7.0
M_L = M_R = 0.09
GAP   = 0.19
COL_W = (FIG_W - M_L - M_R - 2 * GAP) / 3

NODE_R_SRC = 6.5                              # source-unit node radius (for margin)
PAD   = 0.05
GRAPH_SCALE = 0.75                            # draw the networks at this fraction
                                              # of the size the column allows
SCALE = min((COL_W - 2 * PAD) / (BBW + 2 * NODE_R_SRC), 0.0095) * GRAPH_SCALE
PANEL_H = {k: (BBH[k] + 2 * NODE_R_SRC) * SCALE for k in BBH}

H_TIME, H_HEAD, H_ROWGAP, H_LEG = 0.26, 0.26, 0.17, 0.38
M_T, M_B = 0.04, 0.03
FIG_H = (M_T + H_TIME + 2 * H_HEAD + PANEL_H['a'] + PANEL_H['b']
         + H_ROWGAP + H_LEG + M_B)

fig = plt.figure(figsize=(FIG_W, FIG_H))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, FIG_W); ax.set_ylim(0, FIG_H)
ax.set_aspect('equal'); ax.axis('off')

col_x = [M_L + i * (COL_W + GAP) for i in range(3)]
y = FIG_H - M_T

# ---------------- time ruler ---------------------------------------------
ty = y - 0.15
x0 = col_x[0] + COL_W * 0.06
x1 = col_x[2] + COL_W * 0.78
ax.annotate('', xy=(x1, ty), xytext=(x0, ty),
            arrowprops=dict(arrowstyle='-|>,head_width=0.10,head_length=0.24',
                            color=RULE, lw=0.9, shrinkA=0, shrinkB=0))
for i, lab in enumerate(['$t_1$', '$t_2$', '$t_3$']):
    ax.text(col_x[i] + COL_W / 2, ty, lab, ha='center', va='center',
            fontsize=8.6, color=MUTED,
            bbox=dict(boxstyle='square,pad=0.36', fc='white', ec='none'), zorder=5)
ax.text(x1 + 0.06, ty, 'time', ha='left', va='center', fontsize=7.4,
        color=MUTED, style='italic')
y -= H_TIME

# ---------------- panels --------------------------------------------------
R_NODE = NODE_R_SRC * SCALE * 0.92

def draw_panel(panel, box, cx0, cy_top, ph):
    mnx, mxx, mny, mxy = box
    ox = cx0 + COL_W / 2 - (mnx + mxx) / 2 * SCALE
    oy = cy_top - ph / 2 + (mny + mxy) / 2 * SCALE
    T = lambda x, yy: (ox + x * SCALE, oy - yy * SCALE)

    el = panel['ell']
    if el:
        w, h = 2 * el['a'] * SCALE, 2 * el['b'] * SCALE
        c = T(el['cx'], el['cy'])
        ax.add_patch(Ellipse(c, w, h, angle=-el['angle'],
                             facecolor=ACCENT_FL, edgecolor='none', zorder=1))
        ax.add_patch(Ellipse(c, w, h, angle=-el['angle'],
                             facecolor='none', edgecolor=ACCENT, lw=1.05, zorder=4))
    ns = panel['nodes']
    for a, b, dashed in panel['edges']:
        p, q = T(*ns[a]), T(*ns[b])
        kw = dict(color=GATED, lw=1.0, ls=(0, (0.5, 1.95)), dash_capstyle='round',
                  zorder=3) if dashed else dict(color=EDGE, lw=1.0,
                                                solid_capstyle='round', zorder=2)
        ax.add_line(Line2D([p[0], q[0]], [p[1], q[1]], **kw))
    for n in ns:
        ax.add_patch(Circle(T(*n), R_NODE, facecolor='white', edgecolor=INK,
                            lw=0.95, zorder=6))

def draw_row(key, letter, title, y_top):
    ax.text(M_L + 0.005, y_top - 0.135, letter, ha='left', va='center',
            fontsize=10.5, fontweight='bold', color=INK)
    ax.text(M_L + 0.175, y_top - 0.135, title, ha='left', va='center',
            fontsize=9.5, color=INK)
    yp = y_top - H_HEAD
    for i in range(3):
        draw_panel(data[key][i], BOX[key][i], col_x[i], yp, PANEL_H[key])
    return yp - PANEL_H[key]

y = draw_row('a', 'a', 'Without boundaries', y)
y -= H_ROWGAP
y = draw_row('b', 'b', 'With semi-permeable boundaries', y)

# ---------------- legend --------------------------------------------------
ax.add_line(Line2D([M_L, FIG_W - M_R], [y - 0.10, y - 0.10], color=RULE, lw=0.7))
ly = y - 0.10 - H_LEG * 0.50

items = [('solid', 'interaction'),
         ('dotted', 'interaction limited by a boundary'),
         ('ell', 'semi-permeable boundary')]
FS, KEY_W, TXT_GAP, ITEM_GAP = 8.1, 0.25, 0.075, 0.38
rend = fig.canvas.get_renderer()
def tw(s):
    t = ax.text(0, 0, s, fontsize=FS); w = t.get_window_extent(rend).width / fig.dpi
    t.remove(); return w

total = sum(KEY_W + TXT_GAP + tw(l) for _, l in items) + ITEM_GAP * (len(items) - 1)
x = (FIG_W - total) / 2
for kind, lbl in items:
    if kind == 'solid':
        ax.add_line(Line2D([x, x + KEY_W], [ly, ly], color=EDGE, lw=1.0))
    elif kind == 'dotted':
        ax.add_line(Line2D([x, x + KEY_W], [ly, ly], color=GATED, lw=1.0,
                           ls=(0, (0.55, 2.1)), dash_capstyle='round'))
    else:
        ax.add_patch(Ellipse((x + KEY_W / 2, ly), KEY_W, KEY_W * 0.60, angle=-18,
                             facecolor=ACCENT_FL, edgecolor=ACCENT, lw=1.05))
    ax.text(x + KEY_W + TXT_GAP, ly, lbl, ha='left', va='center',
            fontsize=FS, color=MUTED)
    x += KEY_W + TXT_GAP + tw(lbl) + ITEM_GAP

out = os.path.join(SP, 'boundaries_fixation')
fig.savefig(out + '.pdf')
fig.savefig(out + '.svg')
print('fig', FIG_W, round(FIG_H, 3), 'scale', round(SCALE, 5), 'panel_h', PANEL_H)
