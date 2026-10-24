# part 2: world, terrain, grass, flowers, rocks, trees, palms, mountains
import colorsys
def hgt(x, z):
    r = math.hypot(x, z); k = clamp((r - 22) / 50)
    return k * k * (6 * math.sin(x * .03 + 1) * math.cos(z * .028) + 4 * math.sin(z * .045 - x * .02) + 2 * math.sin(x * .08))
hgt_v = np.vectorize(hgt)
def lin(c): return np.power(np.clip(c, 0, 1), 2.2)
def hsl(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h % 1, l, s); return (r, g, b)

def build_world(sc):
    w = bpy.data.worlds.new('world'); sc.world = w; w.use_nodes = True; nt = w.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = N(nt, 'ShaderNodeOutputWorld'); bg = N(nt, 'ShaderNodeBackground')
    sky = N(nt, 'ShaderNodeTexSky'); sky.sky_type = 'MULTIPLE_SCATTERING'; sky.sun_elevation = math.radians(30); sky.sun_rotation = 0.
    sky.air_density = 1.15; sky.aerosol_density = .35; sky.ozone_density = 1.0; sky.sun_size = math.radians(.6); sky.sun_intensity = 1.0; sky.altitude = 80.
    # procedural clouds painted on the sky dome (projected plane)
    gen = N(nt, 'ShaderNodeNewGeometry')
    sep = N(nt, 'ShaderNodeSeparateXYZ'); link(nt, gen.outputs['Incoming'], sep.inputs[0])
    negz = math_node(nt, 'MULTIPLY', sep.outputs['Z'], -1.)               # incoming points toward the surface: negate -> view direction
    negx = math_node(nt, 'MULTIPLY', sep.outputs['X'], -1.); negy = math_node(nt, 'MULTIPLY', sep.outputs['Y'], -1.)
    den = math_node(nt, 'ADD', negz.outputs[0], .16, False); den2 = math_node(nt, 'MAXIMUM', den.outputs[0], .05)
    px = math_node(nt, 'DIVIDE', negx.outputs[0], den2.outputs[0]); py = math_node(nt, 'DIVIDE', negy.outputs[0], den2.outputs[0])
    comb = N(nt, 'ShaderNodeCombineXYZ'); link(nt, px.outputs[0], comb.inputs['X']); link(nt, py.outputs[0], comb.inputs['Y'])
    mp = N(nt, 'ShaderNodeMapping'); mp.inputs['Scale'].default_value = (.55, .55, .55); mp.inputs['Location'].default_value = (3., 7., 0.); link(nt, comb.outputs[0], mp.inputs['Vector'])
    nz = noise(nt, mp.outputs[0], 1.4, 8, .55, .25); cr = ramp(nt, nz.outputs['Fac'], [(.44, (0, 0, 0, 1)), (.66, (1, 1, 1, 1))])
    horizon = math_node(nt, 'SMOOTH_MINIMUM', negz.outputs[0], 0., None) if False else None
    up = math_node(nt, 'MULTIPLY', negz.outputs[0], 6., True)                 # fade clouds below horizon
    mk = N(nt, 'ShaderNodeMix'); mk.data_type = 'FLOAT'; mk.blend_type = 'MULTIPLY'; mk.inputs['Factor'].default_value = 1.
    sepc = N(nt, 'ShaderNodeSeparateColor'); link(nt, cr.outputs['Color'], sepc.inputs[0])
    m2 = math_node(nt, 'MULTIPLY', sepc.outputs['Red'], up.outputs[0], True)
    cloudcol = N(nt, 'ShaderNodeRGB'); cloudcol.outputs[0].default_value = (1., .97, .93, 1.)
    boost = N(nt, 'ShaderNodeMix'); boost.data_type = 'RGBA'; boost.blend_type = 'MIX'; link(nt, m2.outputs[0], boost.inputs['Factor'])
    link(nt, sky.outputs['Color'], boost.inputs[6]); link(nt, cloudcol.outputs[0], boost.inputs[7])
    # clouds multiply a little brightness so they read against the sky
    mulc = N(nt, 'ShaderNodeMix'); mulc.data_type = 'RGBA'; mulc.blend_type = 'MULTIPLY'; mulc.inputs['Factor'].default_value = 1.
    link(nt, boost.outputs[2], mulc.inputs[6]); gain = N(nt, 'ShaderNodeRGB'); gain.outputs[0].default_value = (1.35, 1.35, 1.35, 1.)
    gm = N(nt, 'ShaderNodeMix'); gm.data_type = 'RGBA'; gm.blend_type = 'MIX'; link(nt, m2.outputs[0], gm.inputs['Factor']); gm.inputs[6].default_value = (1, 1, 1, 1); link(nt, gain.outputs[0], gm.inputs[7])
    link(nt, gm.outputs[2], mulc.inputs[7])
    link(nt, mulc.outputs[2], bg.inputs['Color']); bg.inputs['Strength'].default_value = 1.0
    link(nt, bg.outputs[0], out.inputs['Surface'])
    return sky

def build_terrain(M):
    n = 420; u = np.linspace(-1, 1, n); xs = 520 * np.sign(u) * np.abs(u) ** 2.6
    X, Zt = np.meshgrid(xs, xs); X = X.ravel(); Zt = Zt.ravel()
    H = hgt_v(X, Zt)
    r = np.hypot(X, Zt); d = np.clip(1 - r / 15, 0, 1) ** 1.5
    road = np.clip(1 - np.abs(X - (-2 + 6 * np.sin(Zt * .06))) / 2.4, 0, 1) * (Zt > 4)
    dirt = np.clip(np.maximum(d * 1.2, road), 0, 1)
    verts = np.stack([X, -Zt, H], 1)
    idx = np.arange(n * n).reshape(n, n); a = idx[:-1, :-1].ravel(); b = idx[:-1, 1:].ravel(); c = idx[1:, 1:].ravel(); dd = idx[1:, :-1].ravel()
    faces = np.stack([a, dd, c, b], 1)
    o = mesh_np('terrain', verts, faces, None, M['terrain'], extra={'dirt': dirt})
    return o, dirt

def build_grass(M):
    blades = []
    def sample(count, rmin, rmax, hrange, wrange):
        r = np.sqrt(NPR.uniform(rmin ** 2, rmax ** 2, count * 2)); a = NPR.uniform(0, 6.2832, count * 2)
        x = np.cos(a) * r; z = np.sin(a) * r
        keep = ~((np.abs(x) < 7.9) & (np.abs(z) < 6.6))
        keep &= ~((x > 9.5) & (x < 15.5) & (z > 0) & (z < 6.5))            # truck footprint stays cleaner
        roadd = np.clip(1 - np.abs(x - (-2 + 6 * np.sin(z * .06))) / 2.4, 0, 1) * (z > 4)
        keep &= NPR.uniform(0, 1, len(x)) > np.clip(roadd * 1.6, 0, 1)
        x, z = x[keep][:count], z[keep][:count]; n = len(x)
        h = NPR.uniform(*hrange, n) * (1 + .5 * (NPR.uniform(0, 1, n) > .93)); w = NPR.uniform(*wrange, n)
        return x, z, h, w
    parts = [sample(240000, 6, 24, (.22, .55), (.014, .024)), sample(120000, 24, 55, (.30, .70), (.03, .05)), sample(40000, 55, 110, (.45, .95), (.06, .1))]
    allv = []; allf = []; allc = []; off = 0
    for x, z, h, w in parts:
        n = len(x); y = hgt_v(x, z); ang = NPR.uniform(0, 6.2832, n); px = -np.sin(ang); py = np.cos(ang)  # perpendicular
        bend = NPR.uniform(.05, .3, n) * h; dx = np.cos(ang); dy = np.sin(ang)
        bx, by, bz = x, -z, y
        def P(t, wid, bd):   # point along blade at fraction t
            return np.stack([bx + dx * bd * t * t + px * wid, by + dy * bd * t * t + py * wid, bz + h * t], 1)
        bl = P(0, -w / 2, bend); br = P(0, w / 2, bend); ml = P(.55, -w * .33, bend); mr = P(.55, w * .33, bend); tp = P(1, 0, bend)
        v = np.concatenate([bl, br, ml, mr, tp], 1).reshape(n * 5, 3)
        base = np.arange(n) * 5 + off; f = np.concatenate([np.stack([base, base + 1, base + 3], 1), np.stack([base, base + 3, base + 2], 1), np.stack([base + 2, base + 3, base + 4], 1)])
        dry = NPR.uniform(0, 1, n) > .9; hue = np.where(dry, NPR.uniform(.12, .17, n), NPR.uniform(.22, .30, n)); lt = NPR.uniform(.5, 1, n)
        cb = np.stack([lin(np.array([hsl(hh, .65, .06 * l + .02) for hh, l in zip(hue, lt)])) for _ in [0]], 0)[0]
        ct = np.stack([lin(np.array([hsl(hh, .6, .17 * l + .06) for hh, l in zip(hue, lt)])) for _ in [0]], 0)[0]
        cm = (cb + ct) / 2
        col = np.stack([cb, cb, cm, cm, ct], 1).reshape(n * 5, 3); col = np.concatenate([col, np.ones((n * 5, 1))], 1)
        allv.append(v); allf.append(f); allc.append(col); off += n * 5
    V_ = np.concatenate(allv); F_ = np.concatenate(allf); C_ = np.concatenate(allc)
    return mesh_np('grass', V_, F_, C_, M['grass'])

def build_flowers(M):
    n = 4200; r = np.sqrt(NPR.uniform(9 ** 2, 48 ** 2, n)); a = NPR.uniform(0, 6.28, n); x = np.cos(a) * r; z = np.sin(a) * r
    keep = ~((np.abs(x) < 7.9) & (np.abs(z) < 6.6)); x, z = x[keep], z[keep]; n = len(x)
    y = hgt_v(x, z) + NPR.uniform(.18, .42, n); rad = NPR.uniform(.025, .05, n); ang = np.linspace(0, 6.2832, 7)[:-1]
    cols = np.array([(.95, .85, .2), (1, 1, 1), (.9, .35, .6), (.6, .5, 1)]); cc = lin(cols[NPR.integers(0, 4, n)])
    vs = []; fs = []; cs = []
    cen = np.stack([x, -z, y], 1); tilt = NPR.uniform(-.4, .4, (n, 2))
    ring = np.stack([np.stack([np.cos(t) * rad, np.sin(t) * rad, np.zeros(n)], 1) for t in ang], 1)   # n,6,3
    ring[:, :, 0] += ring[:, :, 2] * 0; verts = np.concatenate([cen[:, None, :], cen[:, None, :] + ring], 1).reshape(n * 7, 3)
    base = np.arange(n) * 7; f = np.concatenate([np.stack([base, base + 1 + k, base + 1 + (k + 1) % 6], 1) for k in range(6)])
    col = np.repeat(cc, 7, 0); col = np.concatenate([col, np.ones((len(col), 1))], 1)
    return mesh_np('flowers', verts, f, col, M['flower'])

def rock_obj(M, x, z, s):
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=3, radius=1.)
    k = RNG.random() * 100
    for v in bm.verts:
        p = v.co; d = 1 + .22 * math.sin(p.x * 3.1 + k) * math.cos(p.y * 2.7 + k) + .1 * math.sin(p.z * 6 + k * 2)
        v.co = Vector((p.x * d * 1.25, p.y * d, p.z * d * .6))
    col = bm.verts.layers.color.new('col')
    for v in bm.verts:
        g = .13 + .08 * RNG.random(); v[col] = (g * 1.0, g * .96, g * .88, 1.)
    me = bpy.data.meshes.new('rock'); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    o = mk_obj('rock', me, M['rock']); o.scale = (s, s, s); o.rotation_euler = (0, 0, RNG.random() * 6.28); o.location = V(x, hgt(x, z) + s * .15, z); return o

def leaf_cloud(centers, radii, counts, size, hue, lrange, rseed, up_bias=.0):
    """Leaf diamonds on/in spheres. Returns verts, faces(quads), colors."""
    vs = []; cs = []
    for c, R, n in zip(centers, radii, counts):
        rr = R * (.35 + .65 * NPR.uniform(0, 1, n) ** .45); th = np.arccos(NPR.uniform(-1, 1, n)); ph = NPR.uniform(0, 6.2832, n)
        d = np.stack([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th) * (.8 + .0)], 1); p = c + d * rr[:, None]
        nrm = d + NPR.normal(0, .5, (n, 3)); nrm /= np.linalg.norm(nrm, axis=1, keepdims=True)
        t1 = np.cross(nrm, NPR.normal(0, 1, (n, 3))); t1 /= np.linalg.norm(t1, axis=1, keepdims=True) + 1e-9; t2 = np.cross(nrm, t1)
        s = size * NPR.uniform(.7, 1.3, n)[:, None]
        v = np.stack([p - t1 * s, p - t2 * s * .5, p + t1 * s, p + t2 * s * .5], 1)
        vs.append(v)
        top = np.clip((d[:, 2] + 1) / 2, 0, 1); l = lrange[0] + (lrange[1] - lrange[0]) * (.35 * top + .65 * NPR.uniform(0, 1, n))
        hh = hue[0] + (hue[1] - hue[0]) * NPR.uniform(0, 1, n); cc = lin(np.array([hsl(a, .62, b) for a, b in zip(hh, l)]))
        cs.append(np.repeat(cc[:, None, :], 4, 1))
    v = np.concatenate(vs); n = len(v); c = np.concatenate(cs)
    verts = v.reshape(n * 4, 3); f = (np.arange(n) * 4)[:, None] + np.array([0, 1, 2, 3])[None, :]
    col = np.concatenate([c.reshape(n * 4, 3), np.ones((n * 4, 1))], 1)
    return verts, f, col

def tube(p0, p1, r0, r1, sides=7, segs=4, wob=0.):
    """Tapered tube between points (numpy). Returns verts, quad faces."""
    p0 = np.array(p0, float); p1 = np.array(p1, float); ax = p1 - p0; L = np.linalg.norm(ax); ax /= L
    t1 = np.cross(ax, [0, 0, 1.]); t1 = t1 / np.linalg.norm(t1) if np.linalg.norm(t1) > 1e-6 else np.array([1., 0, 0]); t2 = np.cross(ax, t1)
    rings = []
    for i in range(segs + 1):
        t = i / segs; c = p0 + (p1 - p0) * t + wob * np.array([math.sin(t * 5 + p0[0]), math.cos(t * 4 + p0[1]), 0]) * t; r = lerp(r0, r1, t)
        a = np.linspace(0, 6.2832, sides, endpoint=False); rings.append(c[None, :] + r * (np.cos(a)[:, None] * t1 + np.sin(a)[:, None] * t2))
    v = np.concatenate(rings); f = []
    for i in range(segs):
        for k in range(sides):
            a_ = i * sides + k; b_ = i * sides + (k + 1) % sides; f.append([a_, b_, b_ + sides, a_ + sides])
    return v, np.array(f)

def build_broad_tree(M, x, z, s, detail):
    y0 = hgt(x, z); base = np.array([x, -z, y0]); trunkH = 3.0 * s
    tv, tf = tube(base, base + [0, 0, trunkH], .36 * s, .2 * s, 9, 6, wob=.18 * s)
    verts = [tv]; faces = [tf]; off = len(tv)
    crowns = []; nb = 5 if detail > 1 else 3
    for i in range(nb):
        a = i / nb * 6.2832 + RNG.random() * .8; rad = (1.4 + RNG.random() * .8) * s
        c = base + np.array([math.cos(a) * rad * .9, math.sin(a) * rad * .9, trunkH + (1.2 + RNG.random() * 1.6) * s])
        bv, bf = tube(base + [0, 0, trunkH * .75], c - [0, 0, .5 * s], .13 * s, .05 * s, 6, 3); faces.append(bf + off); verts.append(bv); off += len(bv); crowns.append(c)
    crowns.append(base + np.array([0, 0, trunkH + 2.4 * s])); radii = [(1.5 + RNG.random() * .5) * s for _ in crowns]
    lv, lf, lc = leaf_cloud(np.array(crowns), radii, [int(1800 * detail * (r / s)) for r in radii], .13 * s ** .5 * (1.7 if detail < 1.5 else 1.), (.21, .31), (.10, .30), 0)
    tvv = np.concatenate(verts); tff = np.concatenate(faces)
    mesh_np('trunk', tvv, tff, None, M['bark']); mesh_np('crown', lv, lf, lc, M['leaf'])

def build_conifer(M, x, z, s, detail):
    y0 = hgt(x, z); base = np.array([x, -z, y0]); H = 9.5 * s; vs = []; fs = []; cs = []; off = 0
    tv, tf = tube(base, base + [0, 0, 2 * s], .2 * s, .12 * s, 7, 3); mesh_np('ctrunk', tv, tf, None, M['bark'])
    tiers = 6; sides = 28 if detail > 1 else 16
    for i in range(tiers):
        r = (2.3 - i * .33) * s; zb = (1.5 + i * 1.25) * s; h = 2.6 * s
        a = np.linspace(0, 6.2832, sides, endpoint=False); jag = 1 + .22 * np.sin(a * 5 + i) + .1 * NPR.uniform(-1, 1, sides)
        ring = np.stack([np.cos(a) * r * jag, np.sin(a) * r * jag, np.full(sides, zb) + .35 * s * np.sin(a * 3 + i)], 1) + base
        ring2 = np.stack([np.cos(a) * r * jag * .55, np.sin(a) * r * jag * .55, np.full(sides, zb + h * .5)], 1) + base
        tip = (base + [0, 0, zb + h])[None, :]
        v = np.concatenate([ring, ring2, tip]); f = []
        for k in range(sides):
            k2 = (k + 1) % sides; f.append([k, k2, sides + k2, sides + k]); f.append([sides + k, sides + k2, 2 * sides, 2 * sides])
        g = hsl(.34 + RNG.random() * .02, .55, .07 + RNG.random() * .04); cc = np.tile(lin(np.array(g)), (len(v), 1)); cc = cc * (.7 + .5 * np.clip((v[:, 2:3] - base[2]) / (H), 0, 1))
        cc = np.concatenate([cc, np.ones((len(v), 1))], 1)
        vs.append(v); fs.append(np.array(f) + off); cs.append(cc); off += len(v)
    # tris collapse to degenerate quads: fine
    mesh_np('conifer', np.concatenate(vs), np.concatenate(fs), np.concatenate(cs), M['leaf'])
    # needle cards for a fuzzy silhouette
    if detail > 1:
        pts = []; 
        for i in range(tiers):
            r = (2.2 - i * .3) * s; zb = (1.7 + i * 1.25) * s
            pts.append(base + [0, 0, zb + .8 * s])
        lv, lf, lc = leaf_cloud(np.array(pts), [2.0 * s * (1 - i * .12) for i in range(tiers)], [int(1100 * detail)] * tiers, .11 * s ** .5, (.32, .36), (.05, .14), 0)
        mesh_np('cneedles', lv, lf, lc, M['leaf'])

def build_far_clump(M, x, z, s):
    y0 = hgt(x, z); bm = bmesh.new(); col = bm.verts.layers.color.new('col'); cx = Vector((x, -z, y0 + 4.2 * s))
    for k in range(3):
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.)
    bm.free()
    verts = []; faces = []; cols = []; off = 0
    for k in range(3):
        c = np.array([x + NPR.normal(0, 1.2 * s), -z + NPR.normal(0, 1.2 * s), y0 + (3.4 + k * .9) * s]); R = (2.4 - k * .35) * s
        a = np.linspace(0, 6.2832, 14, endpoint=False); b = np.linspace(.25, 2.9, 8)
        v = []
        for bb in b:
            for aa in a: rr = R * (1 + .22 * math.sin(aa * 4 + bb * 3 + k) ); v.append([c[0] + rr * math.sin(bb) * math.cos(aa), c[1] + rr * math.sin(bb) * math.sin(aa), c[2] + rr * math.cos(bb) * .9])
        v = np.array(v); f = []
        for i in range(len(b) - 1):
            for j in range(len(a)): f.append([i * 14 + j, i * 14 + (j + 1) % 14, (i + 1) * 14 + (j + 1) % 14, (i + 1) * 14 + j])
        g = hsl(.24 + RNG.random() * .06, .5, .09 + RNG.random() * .05); cc = np.tile(lin(np.array(g)), (len(v), 1)) * (.8 + .5 * np.clip((v[:, 2:3] - y0) / (8 * s), 0, 1)); cc = np.concatenate([cc, np.ones((len(v), 1))], 1)
        verts.append(v); faces.append(np.array(f) + off); cols.append(cc); off += len(v)
    tv, tf = tube([x, -z, y0], [x, -z, y0 + 3.4 * s], .25 * s, .15 * s, 6, 2); verts.append(tv); faces.append(tf + off); cols.append(np.tile([.05, .035, .025, 1], (len(tv), 1)))
    mesh_np('clump', np.concatenate(verts), np.concatenate(faces), np.concatenate(cols), M['leaf'])

def build_palm(M, x, z, sc):
    y0 = hgt(x, z); base = np.array([x, -z, y0]); lean = (RNG.random() - .5) * .5; n = 12; pts = []; 
    for i in range(n + 1):
        t = i / n; pts.append(base + np.array([lean * 3.2 * t * t * sc, lean * 1.2 * t * t * sc, 9.6 * sc * t]))
    vs = []; fs = []; off = 0; sides = 9
    for i in range(n):
        v, f = tube(pts[i], pts[i + 1], .21 * sc * (1 - i * .035), .21 * sc * (1 - (i + 1) * .035) * 1.04, sides, 1); vs.append(v); fs.append(f + off); off += len(v)
    mesh_np('palm_trunk', np.concatenate(vs), np.concatenate(fs), None, M['bark'])
    top = pts[-1]; lv = []; lf = []; lc = []; o2 = 0
    for fr in range(15):
        ang = fr / 15 * 6.2832 + RNG.random() * .25; pitch = .55 + RNG.random() * .5; Lr = (3.6 + RNG.random() * 1.0) * sc; segs = 24
        d = np.array([math.cos(ang), math.sin(ang), 0.]); rach = []
        for i in range(segs + 1):
            t = i / segs; rach.append(top + d * (Lr * t * math.cos(pitch * (1 - .6 * t))) + np.array([0, 0, Lr * (math.sin(pitch) * t - 1.15 * t * t)]))
        side = np.array([-d[1], d[0], 0.])
        for i in range(segs):
            t = i / segs; ll = (.85 * math.sin(math.pi * min(1, t * .92 + .08))) * sc * 1.0; p = rach[i]
            for sgn in (-1, 1):
                tip = p + side * sgn * ll * .95 + d * ll * .5 + np.array([0, 0, -ll * (.45 + .5 * t)])
                v = np.array([p, rach[i + 1], tip]); lv.append(v); lf.append(np.array([0, 1, 2, 2]) + o2); o2 += 3
                g = hsl(.26 + RNG.random() * .05, .6, .12 + .14 * (1 - t)); c = lin(np.array(g)); lc.append(np.tile(np.append(c, 1), (3, 1)))
    mesh_np('palm_fronds', np.concatenate(lv), np.array(lf), np.concatenate(lc), M['frond'])

def vnoise(x, y, seed=0.):
    xi = np.floor(x); yi = np.floor(y); xf = x - xi; yf = y - yi; u = xf * xf * (3 - 2 * xf); v = yf * yf * (3 - 2 * yf)
    def h(ix, iy): return np.modf(np.sin(ix * 127.1 + iy * 311.7 + seed * 74.7) * 43758.5453)[0] % 1.0
    a = h(xi, yi); b = h(xi + 1, yi); c = h(xi, yi + 1); d = h(xi + 1, yi + 1)
    return (a * (1 - u) + b * u) * (1 - v) + (c * (1 - u) + d * u) * v
def fbm(x, y, oct=6, seed=0., lac=2.03, gain=.5):
    s = np.zeros_like(x); amp = 1.; tot = 0.
    for o in range(oct): s += amp * vnoise(x, y, seed + o * 3.1); tot += amp; x = x * lac + 17.3; y = y * lac - 9.1; amp *= gain
    return s / tot
def build_mountains(M):
    nx, nz = 640, 220; xs = np.linspace(-1800, 1800, nx); zs = np.linspace(-240, -1500, nz); X, Z = np.meshgrid(xs, zs)
    far = np.clip((-Z - 240) / 160, 0, 1)
    ridge = 1 - np.abs(2 * fbm(X / 420, Z / 420, 6, 1.3) - 1); base = (18 + 120 * ridge ** 2.2 * (.55 + .45 * fbm(X / 900, Z / 900, 3, 4.))) * far
    def cone(cx, cz, R, Hh, crater):
        dx = X - cx; dz = Z - cz; r = np.hypot(dx, dz); ang = np.arctan2(dz, dx); Rr = R * (1 + .16 * (fbm(np.cos(ang) * 3 + 5, np.sin(ang) * 3 + 5, 4, 8.) - .5) + .05 * np.sin(ang * 9))
        t = np.clip(1 - r / Rr, 0, 1); prof = t ** 1.55 * (1 + .12 * np.sin(ang * 23 + fbm(X / 60, Z / 60, 3, 2.) * 6) * (1 - t))
        hh = Hh * prof - crater * np.clip(1 - r / (Rr * .09), 0, 1) ** .8 * (t > .85)
        return hh
    vol = cone(190, -640, 420, 205, 28) + cone(-640, -540, 360, 190, 0) + cone(900, -760, 380, 210, 0)
    Hh = base + vol + 6 * fbm(X / 40, Z / 40, 4, 7.) * far
    verts = np.stack([X.ravel(), -Z.ravel(), Hh.ravel() - 3], 1)
    idx = np.arange(nx * nz).reshape(nz, nx); a = idx[:-1, :-1].ravel(); b = idx[:-1, 1:].ravel(); c = idx[1:, 1:].ravel(); d = idx[1:, :-1].ravel(); faces = np.stack([a, d, c, b], 1)
    gz, gx = np.gradient(Hh, zs, xs); slope = np.clip(np.hypot(gx, gz) / 1.0, 0, 2).ravel(); hh = Hh.ravel(); nn = fbm(X.ravel() / 25, Z.ravel() / 25, 3, 5.)
    green1 = lin(np.array([.04, .12, .03])); green2 = lin(np.array([.07, .16, .04])); rock = lin(np.array([.22, .20, .19])); dark = lin(np.array([.03, .07, .03]))
    veg = np.clip(1 - np.clip((hh - 200) / 120, 0, 1) - np.clip((slope - .9) / .6, 0, 1), 0, 1)[:, None]
    col = (green1[None, :] * (1 - nn[:, None]) + green2[None, :] * nn[:, None]) * (.75 + .5 * (fbm(X.ravel() / 8, Z.ravel() / 8, 3, 9.))[:, None]); col = col * veg + rock[None, :] * (1 - veg) * (.7 + .6 * nn[:, None])
    col = np.concatenate([col, np.ones((len(col), 1))], 1)
    return mesh_np('mountains', verts, faces, col, M['mount'])
