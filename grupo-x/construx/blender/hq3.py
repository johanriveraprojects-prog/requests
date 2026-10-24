# part 3: the house, site props, stage animation, camera, render
L, D, BASE, SB, WH, T = 11., 7.5, .45, 1.25, 3.4, .46
RH = 2.7; SLOPE = math.atan2(RH, D / 2 + .7); RL = math.hypot(RH, D / 2 + .7); EAVE = BASE + WH + .3
PARTS = []; REVEALS = {}; LIGHTS = []; ANIM = {}
KEYS = [[0, 0], [3.6, .14], [7.2, .30], [9.0, .52], [10.8, .78], [11.7, .90], [13.6, 1], [15, 1]]
def stage_at(t):
    for i in range(1, len(KEYS)):
        if t <= KEYS[i][0]:
            t0, s0 = KEYS[i - 1]; t1, s1 = KEYS[i]; return lerp(s0, s1, sm(clamp((t - t0) / (t1 - t0))))
    return 1.
def part(obj, a, b, mode='rise', leave=None):
    obj.rotation_mode = 'XYZ'; PARTS.append(dict(obj=obj, a=a, b=b, mode=mode, leave=leave, z0=obj.location.z, sc0=obj.scale.copy(), kids=list(obj.children_recursive))); return obj
def empty(name, pos3, rot=(0, 0, 0)):
    e = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(e); e.location = V(*pos3); e.rotation_euler = rot; return e
def ocyl(name, r, h, pos3, mat, axis='Z', parent=None, sides=14, base=False):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=sides, radius1=r, radius2=r, depth=h)
    if base: bmesh.ops.translate(bm, vec=(0, 0, h / 2), verts=bm.verts)
    o = bmesh_to_obj(bm, name, mat); o.location = V(*pos3) - (Vector((0, 0, 0)) if not base else Vector((0, 0, 0)))
    if axis == 'X': o.rotation_euler = (0, math.pi / 2, 0)
    elif axis == 'Y': o.rotation_euler = (math.pi / 2, 0, 0)
    if parent is not None: o.parent = parent
    return o
def osphere(name, r, pos3, mat, parent=None, scale=(1, 1, 1), sub=2):
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=r); o = bmesh_to_obj(bm, name, mat); o.location = V(*pos3); o.scale = scale
    if parent is not None: o.parent = parent
    return o


RM = []
class RevealMesh:
    """Pieces appear by scaling their own geometry (no transparency): kind = stone|plank|slat|pop."""
    def __init__(self, obj, rec, kind, ths, soft, fn, zb=None):
        me = obj.data; n = len(me.vertices); co = np.empty(n * 3, np.float32); me.vertices.foreach_get('co', co); self.co0 = co.reshape(n, 3).copy()
        self.pid = np.zeros(n, np.int32)
        for i, (a, b, c) in enumerate(rec): self.pid[a:b] = i
        self.ctr = np.array([[c.x, c.y, c.z] for (a, b, c) in rec], np.float32); self.th = np.array(ths, np.float32); self.kind = kind; self.soft = soft; self.fn = fn
        self.zb = np.array(zb, np.float32) if zb is not None else None; self.obj = obj; self.last = None; RM.append(self)
    def update(self, s):
        R = self.fn(s)
        if self.last is not None and abs(R - self.last) < 1e-6: return
        self.last = R; k = np.clip((R - self.th) / self.soft, 0, 1); sc = 1 - (1 - k) ** 3; sv = sc[self.pid]; c = self.ctr[self.pid]; co = self.co0
        if self.kind == 'stone': new = c + (co - c) * sv[:, None]; new[:, 2] += (1 - sv) * 1.2
        elif self.kind == 'pop': new = c + (co - c) * sv[:, None]
        elif self.kind == 'plank': new = co.copy(); zb = self.zb[self.pid]; new[:, 2] = zb + (co[:, 2] - zb) * np.maximum(sv, .0005)
        else: new = co.copy(); new[:, 1] = c[:, 1] + (co[:, 1] - c[:, 1]) * np.maximum(sv, .0005)
        self.obj.data.vertices.foreach_set('co', new.astype(np.float32).ravel()); self.obj.data.update()

def build_house(M):
    # survey stakes + string
    for x, z in [(-L / 2 - 1.2, -D / 2 - 1.2), (L / 2 + 1.2, -D / 2 - 1.2), (L / 2 + 1.2, D / 2 + 1.2), (-L / 2 - 1.2, D / 2 + 1.2)]:
        part(obox('stake', (.08, 1.2, .08), (x, .6, z), M['stakes'], bevel=.01), 0, .03, 'rise')
    # rebar grid
    bm = new_bm(); 
    for i in range(23): piece(bm, Vector((-L / 2 - .1 + i * ((L + .2) / 22), 0, .1)), (.025, D + .4, .025))
    for j in range(17): piece(bm, Vector((0, -(-D / 2 - .1 + j * ((D + .2) / 16)), .12)), (L + .4, .025, .025))
    part(bmesh_to_obj(bm, 'rebar', M['rebar']), .04, .08, 'rise', leave=.10)
    # slab
    slab = obox('slab', (L + 1, BASE, D + 1), (0, BASE / 2, 0), M['conc'], bevel=.03); part(slab, .08, .17, 'rise')
    # stone base: bevelled stones in one mesh, laid course by course
    bm = new_bm(('tint',)); rec = []; ths = []
    for ln, cx, cz, rot, off in [(L, 0, D / 2 - T / 2, 0, 0), (L, 0, -D / 2 + T / 2, 0, 1), (D - 2 * T + .02, L / 2 - T / 2, 0, 1, 2), (D - 2 * T + .02, -L / 2 + T / 2, 0, 1, 3)]:
        y = BASE
        for c in range(6):
            h = .17 + RNG.random() * .09; u = -ln / 2 + (c % 2) * .22
            while u < ln / 2 - .12:
                w = min(.32 + RNG.random() * .4, ln / 2 - u); th = (c + RNG.random() * .6) / (6 + .6)
                if rot: sx, sy, px, pz = T + (RNG.random() - .5) * .06, w, cx, cz + u + w / 2
                else: sx, sy, px, pz = w, T + (RNG.random() - .5) * .06, cx + u + w / 2, cz
                n0 = len(bm.verts); piece(bm, V(px, y + h / 2, pz), (sx, sy, h), rot=(0, 0, (RNG.random() - .5) * .05), bevel=.028, seg=2, attrs={'tint': RNG.random()})
                rec.append((n0, len(bm.verts), V(px, y + h / 2, pz))); ths.append(th); u += w + .015
            y += h + .01
    RevealMesh(bmesh_to_obj(bm, 'stones', M['stone']), rec, 'stone', ths, .12, lambda s: clamp((s - .22) / .30))
    bm = new_bm(('tint',)); rec = []; ths = []
    for c in range(36):
        for k in range(6):
            a_ = k / 6 * 6.2832; w = .46 + RNG.random() * .2; d = .46 + RNG.random() * .2; h = .19 + RNG.random() * .06; cp = V(3.2 + math.cos(a_) * .52, BASE + c * .22 + .1, -1.2 + math.sin(a_) * .52)
            n0 = len(bm.verts); piece(bm, cp, (w, d, h), rot=(0, 0, a_ + .3), bevel=.028, seg=2, attrs={'tint': RNG.random()}); rec.append((n0, len(bm.verts), cp)); ths.append(c / 40 * .88 + RNG.random() * .02)
    RevealMesh(bmesh_to_obj(bm, 'chimney', M['stone']), rec, 'stone', ths, .12, lambda s: clamp((s - .62) / .16))
    part(obox('chimcap', (1.3, .14, 1.3), (3.2, BASE + 6.9, -1.2), M['conc'], bevel=.02), .84, .9, 'drop')
    # timber frame
    for x in [-L / 2 + .2, -L / 4, 0, L / 4, L / 2 - .2]:
        for z in [-D / 2 + .2, D / 2 - .2]:
            hh = WH - SB + .2; part(obox('post', (.28, hh, .28), (x, BASE + SB + hh / 2 - .05, z), M['wood_z'], bevel=.02), .36, .50, 'rise')
    for z in (D / 2 - .05, -D / 2 + .05): part(obox('plate', (L + .7, .3, .3), (0, BASE + WH + .15, z), M['wood_x'], bevel=.02, base=False), .50, .56, 'drop')
    for sx in (-1, 1): part(obox('plate', (.3, .3, D + .7), (sx * (L / 2 - .05), BASE + WH + .15, 0), M['wood_y'], bevel=.02, base=False), .52, .58, 'drop')
    # windows spec (needed to cut boards)
    WIN = [(3.2, 1.5, 1.4, True), (-3.9, 1.5, 1.4, True), (1.8, 1.0, 1.4, True), (-1.6, 1.6, 1.4, False), (2.6, 1.6, 1.4, False)]
    # vertical plank cladding (one mesh; boards grow upward)
    bm = new_bm(('tint',)); y0 = BASE + SB; H2 = WH - SB - .02; pw = .23; rec = []; ths = []; zbs = []
    def add_board(px, py, rotw, ylo, yhi, th, tn):
        hgt_ = yhi - ylo
        if hgt_ < .05: return
        size = (.23, .05, hgt_) if not rotw else (.05, .23, hgt_); cp = Vector((px, py, ylo + hgt_ / 2)); n0 = len(bm.verts)
        piece(bm, cp, size, bevel=.012, attrs={'tint': tn}); rec.append((n0, len(bm.verts), cp)); ths.append(th); zbs.append(ylo)
    for ln, cx, cz, rotw, isfb, sgn in [(L, 0, D / 2 + .02, False, True, 1), (L, 0, -D / 2 - .02, False, True, -1), (D, L / 2 + .02, 0, True, False, 1), (D, -L / 2 - .02, 0, True, False, -1)]:
        u = -ln / 2 + pw / 2
        while u < ln / 2:
            th = (RNG.random() * .6 + (u + ln / 2) / ln * .4) * .8; tn = RNG.random(); segs = [(y0, y0 + H2)]
            if isfb:
                wx = cx + u; gap = []
                for (wcx, ww, wh, front) in WIN:
                    if (front and sgn == 1) or ((not front) and sgn == -1):
                        if abs(wx - wcx) < ww / 2 + .26: gap.append((BASE + 2.1 - wh / 2 - .08, BASE + 2.1 + wh / 2 + .08))
                if sgn == 1 and abs(wx - (-1.0)) < .8: gap.append((y0 - 1, BASE + 2.9))
                for g0, g1 in gap:
                    new = []
                    for a_, b_ in segs:
                        if g1 <= a_ or g0 >= b_: new.append((a_, b_))
                        else:
                            if g0 > a_: new.append((a_, g0))
                            if g1 < b_: new.append((g1, b_))
                    segs = new
            for a_, b_ in segs:
                px = cx + u if isfb else cx; py = -cz if isfb else -(cz + u)
                add_board(px, py, rotw, a_, b_, th, tn)
            u += pw + .01
    RevealMesh(bmesh_to_obj(bm, 'planks', M['plank_z']), rec, 'plank', ths, .2, lambda s: clamp((s - .48) / .22), zb=zbs)
    # gables: horizontal slats, growing from the centre
    bm = new_bm(('tint',)); rec = []; ths = []
    for sx in (-1, 1):
        for r in range(11):
            y = BASE + WH + .3 + r * .2; half = (D / 2) * (1 - (r * .2) / 2.7)
            if half > .15:
                cp = V(sx * (L / 2), y, 0); n0 = len(bm.verts); piece(bm, cp, (.05, half * 2, .17), bevel=.01, attrs={'tint': RNG.random()}); rec.append((n0, len(bm.verts), cp)); ths.append((r / 11) * .7)
    RevealMesh(bmesh_to_obj(bm, 'gables', M['slat_x']), rec, 'slat', ths, .3, lambda s: clamp((s - .60) / .14))
    # roof: rafters, deck, shingles, ridge, fascia
    for i in range(14):
        for sz in (-1, 1):
            o = obox('rafter', (.16, .2, RL + .2), (-L / 2 - .6 + i * ((L + 1.2) / 13), EAVE + RH / 2, sz * ((D / 2 + .7) / 2)), M['wood_y'], rot=(sz * SLOPE, 0, 0), bevel=.015, base=False); part(o, .60 + i * .003, .66 + i * .003, 'drop')
    part(obox('ridgebeam', (L + 1.3, .24, .24), (0, EAVE + RH + .02, 0), M['wood_x'], bevel=.02, base=False), .62, .68, 'drop')
    for sz in (-1, 1):
        o = obox('deck', (L + 1.3, .08, RL + .3), (0, EAVE + RH / 2 + .12, sz * ((D / 2 + .7) / 2)), M['dark_x'], rot=(sz * SLOPE, 0, 0), bevel=.01, base=False); part(o, .66, .72, 'slide')
    bm = new_bm(('tint',)); nR = 15; rec = []; ths = []
    for sz in (-1, 1):
        for r in range(nR):
            t = (r + .5) / nR; yy = EAVE + RH * t + .22; zz = sz * ((D / 2 + .7) * (1 - t)); th = .72 + (r / nR) * .12
            x = -L / 2 - .7
            while x < L / 2 + .7:
                jit = (RNG.random() - .5) * .03; cp = V(x + .13, yy + .015, zz + jit * sz); n0 = len(bm.verts)
                piece(bm, cp, (.26, .50, .03), rot=(sz * (SLOPE + .02 * (RNG.random() - .5)), 0, 0), bevel=.007, attrs={'tint': RNG.random()})
                rec.append((n0, len(bm.verts), cp)); ths.append(th); x += .27
    RevealMesh(bmesh_to_obj(bm, 'shingles', M['shingle']), rec, 'pop', ths, .02, lambda s: s)
    for sz in (-1, 1): part(obox('fascia', (L + 1.5, .2, .06), (0, EAVE - .02, sz * (D / 2 + .72)), M['wood_x'], bevel=.01, base=False), .78, .84, 'drop')
    part(obox('ridgecap', (L + 1.5, .12, .3), (0, EAVE + RH + .2, 0), M['dark_x'], bevel=.02, base=False), .86, .9, 'drop')
    # windows
    for k, (wx, ww, wh, front) in enumerate(WIN):
        z = (D / 2 + .08) if front else (-D / 2 - .08)
        g = empty('window', (wx, BASE + 2.1, z), rot=(0, 0, 0 if front else math.pi))
        P = lambda nm, sz3, pos3, mat, bevel=.01: obox(nm, sz3, pos3, mat, bevel=bevel, parent=g, base=False)
        for yy in (wh / 2 + .05, -wh / 2 - .05): P('wf', (ww + .2, .1, .12), (0, yy, 0), M['wood_x'])
        for xx in (ww / 2 + .05, -ww / 2 - .05): P('wf', (.1, wh, .12), (xx, 0, 0), M['wood_z'])
        P('glass', (ww, wh, .02), (0, 0, .02), M['glass'], .001); P('mull', (.04, wh, .05), (0, 0, .03), M['wood_z']); P('mull', (ww, .04, .05), (0, 0, .03), M['wood_x'])
        P('interior', (ww + .3, wh + .3, .04), (0, 0, -.45), M['interior'], .001); gp = P('glowpane', (ww * .9, wh * .9, .01), (0, 0, -.40), M['glow_in'], .001)
        P('sill', (ww + .42, .09, .3), (0, -(wh / 2 + .17), .09), M['stone_static']); P('head', (ww + .34, .1, .22), (0, wh / 2 + .16, .07), M['wood_x'])
        for sgn in (-1, 1):
            P('shutter', (ww / 2, wh, .05), (sgn * (ww / 2 + ww / 4 + .1), 0, .06), M['plank_s'] if 'plank_s' in M else M['wood_z'])
            for yy in (-wh * .32, wh * .32): P('hinge', (.18, .03, .035), (sgn * (ww / 2 + .14), yy, .1), M['metal'], .004)
        P('flowerbox', (ww * .9, .16, .22), (0, -(wh / 2 + .32), .18), M['wood_x'])
        for i in range(8):
            fl = osphere('flower', .06 + RNG.random() * .02, (-ww * .38 + i * ww * .76 / 7, -(wh / 2 + .2), .2), M['flower_%d' % (i % 3)], parent=g, sub=1)
        for i in range(5):
            osphere('leafb', .09, (-ww * .4 + i * ww * .2, -(wh / 2 + .21), .2), M['leafb'], parent=g, sub=1)
        part(g, .88 + k * .01, .93 + k * .01, 'rise')
        ANIM.setdefault('glows', []).append(gp)
    # door
    g = empty('door', (-1.0, BASE + 1.2, D / 2 + .08)); 
    obox('dframe', (1.3, 2.4, .12), (0, 0, 0), M['dark_x'], parent=g, base=False); obox('dpanel', (1.1, 2.2, .15), (0, 0, .03), M['wood_z'], parent=g, base=False)
    for yy in (-.55, .55): obox('dp', (.8, .8, .03), (0, yy, .11), M['dark_x'], parent=g, base=False)
    obox('handle', (.06, .5, .1), (.38, 0, .12), M['metal'], parent=g, base=False, bevel=.01); obox('dhead', (1.5, .1, .3), (0, 1.3, .08), M['wood_x'], parent=g, base=False)
    part(g, .90, .95, 'rise')
    # porch
    pg = empty('porch', (-.6, BASE, D / 2 + 1.3))
    obox('pfloor', (4.6, .2, 2.2), (0, .1, 0), M['deck_x'], parent=pg, base=False, bevel=.015)
    for x in (-2.1, 2.1): obox('ppost', (.2, 2.5, .2), (x, 1.35, .9), M['wood_z'], parent=pg, base=False, bevel=.015)
    obox('pbeam', (4.8, .16, .2), (0, 2.55, .9), M['wood_x'], parent=pg, base=False, bevel=.015)
    for i in range(12): obox('bal', (.05, .85, .05), (-2 + i * .364, .62, 1.0), M['wood_z'], parent=pg, base=False, bevel=.006)
    obox('prail', (4.2, .06, .08), (0, 1.05, 1.0), M['wood_x'], parent=pg, base=False, bevel=.006)
    obox('proof', (5.0, .08, 2.6), (0, 2.78, .15), M['dark_x'], parent=pg, base=False, rot=(.16, 0, 0), bevel=.01)
    part(pg, .92, .99, 'rise')
    # gutters, downspouts, lanterns, steps, chair, pots
    for sz in (-1, 1): part(ocyl('gutter', .07, L + 1.4, (0, EAVE - .16, sz * (D / 2 + .78)), M['metal'], 'X'), .84, .9, 'drop')
    for x in (L / 2 + .55, -L / 2 - .55): part(ocyl('spout', .045, WH + .2, (x, BASE + WH / 2 + .1, D / 2 + .78), M['metal'], 'Z'), .88, .93, 'rise')
    for x, z in [(-2.6, D / 2 + 1.9), (1.4, D / 2 + 1.9)]:
        lg = empty('lantern', (x, BASE + 2.25, z)); obox('lbody', (.2, .26, .2), (0, -.1, 0), M['black'], parent=lg, base=False, bevel=.01); obox('lglow', (.15, .2, .15), (0, -.1, 0), M['lantern'], parent=lg, base=False, bevel=.005); part(lg, .95, .99, 'drop')
    part(obox('step1', (3.8, .2, .6), (-.6, .1, D / 2 + 2.8), M['stone_static'], bevel=.025), .94, .98, 'rise'); part(obox('step2', (3.4, .2, .5), (-.6, .3, D / 2 + 2.55), M['stone_static'], bevel=.025), .95, .99, 'rise')
    cg = empty('chair', (.9, BASE + .2, D / 2 + 1.7), rot=(0, 0, .3))
    obox('cs', (.7, .06, .6), (0, .45, 0), M['deck_x'], parent=cg, base=False); obox('cb', (.7, .75, .06), (0, .85, -.3), M['deck_x'], parent=cg, base=False, rot=(.18, 0, 0))
    for sx in (-.34, .34):
        obox('cr', (.05, .06, .9), (sx, .06, 0), M['wood_y'], parent=cg, base=False); obox('cl', (.05, .45, .05), (sx, .26, .22), M['wood_z'], parent=cg, base=False); obox('cl', (.05, .45, .05), (sx, .26, -.22), M['wood_z'], parent=cg, base=False)
    part(cg, .96, 1., 'rise')
    for x, z in [(-2.95, D / 2 + 2.2), (1.75, D / 2 + 2.2), (-.6, D / 2 + .35)]:
        pg2 = empty('pot', (x, BASE + .2, z)); ocyl('pot', .22, .32, (0, .16, 0), M['pot'], 'Z', parent=pg2, sides=16)
        for i in range(5): osphere('pl', .16 + RNG.random() * .06, ((RNG.random() - .5) * .3, .45 + RNG.random() * .2, (RNG.random() - .5) * .3), M['leafb'], parent=pg2, sub=2)
        part(pg2, .95 + RNG.random() * .02, 1., 'rise')
    # fence
    fz = D / 2 + 8; secs = []
    x = -13.
    while x <= 13.:
        if x < -2.4 or x > 1.6: secs.append((x, fz, 0))
        x += 2.2
    z = fz - 2.2
    while z > -6: secs.append((-13, z, 1)); secs.append((13, z, 1)); z -= 2.2
    for i, (x, z, side) in enumerate(secs):
        fg = empty('fence', (x, hgt(x, z), z)); obox('fpost', (.14, 1.25, .14), (0, .62, 0), M['wood_z'], parent=fg, base=False, bevel=.02)
        for yy in (.45, .9): obox('frail', (.1 if side else 2.2, .09, 2.2 if side else .1), (0 if side else 1.1, yy, -1.1 if side else 0), M['wood_y'] if side else M['wood_x'], parent=fg, base=False, bevel=.015)
        part(fg, .9 + i * .0025, .96 + i * .0025, 'rise')
    # firewood
    fw = empty('firewood', (L / 2 + .6, 0, 1.2), rot=(0, 0, math.pi / 2))
    for r in range(4):
        for c in range(8 - r): ocyl('log', .09, .8, (c * .19 + r * .095, .1 + r * .17, 0), M['wood_z'], 'Y', parent=fw, sides=9)
    part(fw, .93, .99, 'rise')
    # stepping stones
    for i in range(9): part(obox('flag', (1.1, .08, .7), (-.8 + math.sin(i) * .25, .04, D / 2 + 3.0 + i * .85), M['stone_static'], bevel=.02), .95 + i * .004, 1.0, 'rise')
    # truck
    tg = empty('truck', (12.5, 0, 3.2), rot=(0, 0, 0.55))
    P = lambda nm, s3, p3, mt, bv=.04: obox(nm, s3, p3, mt, parent=tg, base=False, bevel=bv)
    P('chassis', (1.9, .18, 4.4), (0, .55, 0), M['black']); P('cabb', (1.85, .6, 1.5), (0, .98, 1.15), M['red'], .1); P('cabt', (1.8, .5, 1.0), (0, 1.5, 1.05), M['red'], .12); P('wind', (1.62, .36, .04), (0, 1.5, 1.57), M['glass'], .003)
    P('bedf', (1.85, .5, 2.6), (0, .98, -1.3), M['red']);
    for sx in (-.9, .9): P('bedside', (.06, .5, 2.6), (sx, 1.4, -1.3), M['red'], .02)
    P('bedback', (1.8, .5, .06), (0, 1.4, -2.55), M['red'], .02); P('bumper', (1.9, .22, .12), (0, .5, 2.28), M['metal'], .03)
    for wx, wz in [(-.95, 1.35), (.95, 1.35), (-.95, -1.35), (.95, -1.35)]:
        ocyl('tire', .42, .28, (wx, .42, wz), M['tire'], 'X', parent=tg, sides=22); ocyl('hub', .21, .3, (wx, .42, wz), M['metal'], 'X', parent=tg, sides=12)
    for i in range(6): P('sack', (.7, .22, .45), (-.45 + (i % 2) * .9, 1.35 + (i // 4) * .22, -1.8 + (i // 2) * .5), M['sack'], .05)
    part(tg, .02, .04, 'rise', leave=.88)
    for i in range(8): part(obox('sack', (.7, .22, .45), (7.2 + (i % 4) * .55, .12 + (i // 4) * .22, 8.2 + (i % 2) * .1), M['sack'], bevel=.05), .06, .1, 'rise', leave=.9)
    # scaffold
    sg = empty('scaffold', (0, 0, 0))
    for i in range(7):
        x = -L / 2 + i * (L / 6)
        for z in (D / 2 + 1.6, D / 2 + .75): ocyl('pole', .035, 5., (x, 2.5, z), M['metal'], 'Z', parent=sg, sides=8)
    for y in (1.5, 3.0, 4.5):
        for z in (D / 2 + 1.6, D / 2 + .75): ocyl('tube', .03, L, (0, y, z), M['metal'], 'X', parent=sg, sides=8)
        obox('board', (L, .05, .9), (0, y - .04, D / 2 + 1.18), M['deck_x'], parent=sg, base=False, bevel=.01)
    part(sg, .34, .5, 'rise', leave=.9)
    # piles (planks + blocks + sand)
    pl = empty('piles', (0, 0, 0))
    for k in range(6):
        for j in range(4): obox('pp', (4.2, .1, .26), (-10, .06 + k * .11, 4 + j * .3), M['deck_x'], parent=pl, base=False, bevel=.01)
    for i in range(6):
        for k in range(4): obox('blk', (.8, .3, .6), (8.6 + (i % 3) * .85, .15 + k * .3, 6 + (i // 3) * .7), M['conc'], parent=pl, base=False, bevel=.02)
    cone = bmesh.new(); bmesh.ops.create_cone(cone, cap_ends=False, segments=28, radius1=1.7, radius2=.05, depth=1.2); so_ = bmesh_to_obj(cone, 'sand', M['sand']); so_.location = V(-8.5, .6, -6.5); so_.parent = pl
    part(pl, .05, .14, 'rise', leave=.96)
    # excavator
    eg = empty('excavator', (-10, 0, -2), rot=(0, 0, -.5))
    for sz in (-.62, .62):
        obox('track', (2.6, .55, .5), (0, .3, sz), M['black'], parent=eg, base=False, bevel=.12); 
    obox('exbody', (2.0, .95, 1.5), (0, 1.0, 0), M['yellow'], parent=eg, base=False, bevel=.08); obox('cab', (.9, .9, .9), (-.3, 1.8, 0), M['yellow'], parent=eg, base=False, bevel=.06); obox('cabg', (.78, .62, .82), (-.3, 1.85, 0), M['glass'], parent=eg, base=False, bevel=.003)
    boom = empty('boom', (.8, 1.2, 0)); boom.parent = eg; boom.location = V(.8, 1.2, 0)
    obox('boomb', (2.4, .3, .3), (1.2, 0, 0), M['yellow'], parent=boom, base=False, bevel=.04)
    arm = empty('arm', (2.4, 0, 0)); arm.parent = boom; arm.location = V(2.4, 0, 0)
    obox('armb', (1.8, .25, .25), (.9, 0, 0), M['yellow'], parent=arm, base=False, bevel=.04); obox('bucket', (.6, .5, .6), (1.9, -.1, 0), M['metal'], parent=arm, base=False, bevel=.05)
    part(eg, .0, .02, 'rise', leave=.34); ANIM['boom'] = boom; ANIM['arm'] = arm
    # workers
    ANIM['workers'] = []
    for x, z, ph in [(3.5, 7.3, 0), (-3.2, 6.6, 1.7), (9.2, 3.5, 3.1), (-1, -6, 4.2)]:
        wg = empty('worker', (x, 0, z)); 
        obox('torso', (.4, .62, .26), (0, 1.1, 0), M['orange'], parent=wg, base=False, bevel=.07)
        for sx in (-.1, .1): obox('leg', (.15, .75, .17), (sx, .38, 0), M['black'], parent=wg, base=False, bevel=.04)
        for sx in (-.27, .27): obox('arm', (.11, .6, .12), (sx, 1.1, 0), M['orange'], parent=wg, base=False, bevel=.04)
        osphere('head', .12, (0, 1.58, 0), M['skin'], parent=wg); hat = osphere('hat', .14, (0, 1.64, 0), M['yellow'], parent=wg, scale=(1, 1, .8))
        wg['ph'] = ph; wg['x'] = x; wg['z'] = z; part(wg, .1, .14, 'rise', leave=.88); ANIM['workers'].append(wg)
    # shrubs along the front (end)
    for i in range(16):
        sh = osphere('shrub', .4 + RNG.random() * .25, (-L / 2 - .4 + i * .75, .38, D / 2 + 3.2 + (i % 2) * .2), M['leafb'], sub=2); part(sh, .94 + i * .002, 1.0, 'rise')
    # warm lights
    for x, z in [(-2.6, D / 2 + 1.8), (1.4, D / 2 + 1.8)]:
        li = bpy.data.lights.new('warm', 'POINT'); li.energy = 0; li.color = (1., .62, .3); li.shadow_soft_size = .3
        lo = bpy.data.objects.new('warm', li); bpy.context.scene.collection.objects.link(lo); lo.location = V(x, BASE + 2.0, z); LIGHTS.append(li)
    # smoke: a few soft spheres (volume-less) skipped; handled in compositing if desired
    return None

def apply_stage(s, t):
    for p in PARTS:
        q = clamp((s - p['a']) / (p['b'] - p['a'])); o = p['obj']; vis = q > 0 and not (p['leave'] is not None and s >= p['leave'])
        o.hide_render = not vis; o.hide_viewport = not vis
        for kd in p['kids']: kd.hide_render = not vis
        if not vis: continue
        if p['mode'] == 'rise': o.scale = (p['sc0'].x, p['sc0'].y, p['sc0'].z * max(.001, ease(q)))
        elif p['mode'] == 'drop': o.location.z = p['z0'] + (1 - ease(q)) * 6
        elif p['mode'] == 'slide': o.scale = (p['sc0'].x, p['sc0'].y * max(.001, ease(q)), p['sc0'].z)
    # reveal-driven meshes
    for rm in RM: rm.update(s)
    # life
    ANIM['boom'].rotation_euler = (0, -(.55 + .12 * math.sin(t * 1.3)), 0); ANIM['arm'].rotation_euler = (0, -(-.9 + .25 * math.sin(t * 1.3 + 1.2)), 0)
    for w in ANIM['workers']:
        w.location.z = abs(math.sin(t * 2.4 + w['ph'])) * .04; w.rotation_euler = (0, 0, math.sin(t * .8 + w['ph']) * .9)
    on = clamp((s - .96) / .04)
    for li in LIGHTS: li.energy = 650 * on
    MATS['lantern'].node_tree.nodes['emit'].inputs['Strength'].default_value = 25 * on
    for g in ANIM.get('glows', []): pass
    MATS['glow_in'].node_tree.nodes['emit'].inputs['Strength'].default_value = 9 * on
    # chimney smoke handled elsewhere

def setup_camera(sc):
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam
    cd = cam.data; cd.sensor_fit = 'VERTICAL'; cd.angle_y = math.radians(42); cd.clip_start = .3; cd.clip_end = 6000
    cd.shift_y = 420 / 1920; cd.dof.use_dof = True; cd.dof.aperture_fstop = 5.6; cd.dof.focus_distance = 42
    return cam
def place_camera(cam, t, DUR=15.):
    k = clamp(t / DUR); a = math.radians(lerp(18, 50, sm(k))); el = lerp(8, 5.5, k); dist = lerp(46, 37, sm(k))
    jx = .03 * math.sin(t * 1.7) + .015 * math.sin(t * 4.1); jz = .02 * math.sin(t * 1.3 + 1)
    pos = V(math.sin(a) * dist + jx, el + hgt(0, 0), math.cos(a) * dist) + Vector((0, 0, jz))
    cam.location = pos; tgt = V(0, 3.0, 0); d = tgt - pos
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); cam.data.dof.focus_distance = d.length
def place_sun(sky, t, DUR=15.):
    k = clamp(t / DUR); e = lerp(40, 13, sm(k)); az = lerp(70, 105, k)
    sky.sun_elevation = math.radians(e); sky.sun_rotation = math.radians(180 - az)
