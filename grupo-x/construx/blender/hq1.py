# ConstruX HQ scene (Blender Cycles) — part 1: infrastructure, materials, geometry helpers
import bpy, bmesh, math, random, sys, os
import numpy as np
from mathutils import Vector, Matrix, Euler

RNG = random.Random(7); NPR = np.random.default_rng(11)
def clamp(v, a=0., b=1.): return max(a, min(b, v))
def lerp(a, b, t): return a + (b - a) * t
def sm(t): return t * t * (3 - 2 * t)
def ease(t): return 1 - (1 - t) ** 3
def V(x, y, z): return Vector((x, -z, y))           # three.js-style (x, up, z) -> Blender (x, -z, up)

# ---------------------------------------------------------------- node helpers
def N(nt, typ, loc=None, **kw):
    n = nt.nodes.new(typ)
    for k, v in kw.items(): setattr(n, k, v)
    return n
def link(nt, a, b): nt.links.new(a, b)
def new_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    return m, nt
def finish(nt, shader):
    out = N(nt, 'ShaderNodeOutputMaterial'); link(nt, shader, out.inputs['Surface']); return out
def bsdf(nt, **inputs):
    b = N(nt, 'ShaderNodeBsdfPrincipled')
    for k, v in inputs.items():
        if k in b.inputs: b.inputs[k].default_value = v
    return b
def ramp(nt, fac, stops):
    r = N(nt, 'ShaderNodeValToRGB')
    el = r.color_ramp.elements
    while len(el) < len(stops): el.new(.5)
    for e, (p, c) in zip(el, stops): e.position = p; e.color = c
    link(nt, fac, r.inputs['Fac']); return r
def noise(nt, coord, scale, detail=6., rough=.55, distortion=0.):
    n = N(nt, 'ShaderNodeTexNoise'); n.inputs['Scale'].default_value = scale; n.inputs['Detail'].default_value = detail
    n.inputs['Roughness'].default_value = rough; n.inputs['Distortion'].default_value = distortion
    link(nt, coord, n.inputs['Vector']); return n
def mapping(nt, coord, scale=(1, 1, 1)):
    m = N(nt, 'ShaderNodeMapping'); m.inputs['Scale'].default_value = scale; link(nt, coord, m.inputs['Vector']); return m
def bump(nt, height, strength=.3, dist=.02):
    b = N(nt, 'ShaderNodeBump'); b.inputs['Strength'].default_value = strength; b.inputs['Distance'].default_value = dist
    link(nt, height, b.inputs['Height']); return b
def attr(nt, name):
    a = N(nt, 'ShaderNodeAttribute'); a.attribute_name = name; a.attribute_type = 'GEOMETRY'; return a
def math_node(nt, op, a=None, b=None, clampit=False):
    m = N(nt, 'ShaderNodeMath'); m.operation = op; m.use_clamp = clampit
    if a is not None:
        if isinstance(a, (int, float)): m.inputs[0].default_value = a
        else: link(nt, a, m.inputs[0])
    if b is not None:
        if isinstance(b, (int, float)): m.inputs[1].default_value = b
        else: link(nt, b, m.inputs[1])
    return m
def reveal_wrap(nt, shader, mat, th_attr='th', soft=.05, name='reveal', grow=False):
    """Mix a shader with Transparent by per-vertex threshold: visible when reveal > th."""
    rv = N(nt, 'ShaderNodeValue'); rv.name = name; rv.label = name; rv.outputs[0].default_value = 0.
    th = attr(nt, th_attr)
    sub = math_node(nt, 'SUBTRACT', rv.outputs[0], th.outputs['Fac'])
    div = math_node(nt, 'DIVIDE', sub.outputs[0], soft, clampit=True)
    tr = N(nt, 'ShaderNodeBsdfTransparent'); mix = N(nt, 'ShaderNodeMixShader')
    fac = div
    if grow:   # visible only where normalized height/extent hn is below the grown fraction
        hn = attr(nt, 'hn'); ez = math_node(nt, 'SUBTRACT', 1., div.outputs[0]); ez2 = math_node(nt, 'POWER', ez.outputs[0], 3.); ezz = math_node(nt, 'SUBTRACT', 1., ez2.outputs[0])
        ezz2 = math_node(nt, 'ADD', ezz.outputs[0], .003); lt = math_node(nt, 'LESS_THAN', hn.outputs['Fac'], ezz2.outputs[0]); act = math_node(nt, 'MULTIPLY', div.outputs[0], 1000., True); fac = math_node(nt, 'MULTIPLY', lt.outputs[0], act.outputs[0])
    link(nt, fac.outputs[0], mix.inputs['Fac']); link(nt, tr.outputs[0], mix.inputs[1]); link(nt, shader, mix.inputs[2])
    mat['reveal_node'] = name
    return mix

# ---------------------------------------------------------------- materials
MATS = {}
def mat_wood(name, c1, c2, grain='Z', rough=.72, bumpk=.5, reveal=False, tint=False, soft=.05, grow=False):
    m, nt = new_mat(name); tc = N(nt, 'ShaderNodeTexCoord')
    sc = {'Z': (45, 45, 3.5), 'X': (3.5, 45, 45), 'Y': (45, 3.5, 45)}[grain]
    mp = mapping(nt, tc.outputs['Object'], sc)
    n1 = noise(nt, mp.outputs[0], 1., 3, .6, .35); n2 = noise(nt, mp.outputs[0], 7., 1, .5)
    mx = math_node(nt, 'ADD', n1.outputs['Fac'], n2.outputs['Fac']); mxs = math_node(nt, 'MULTIPLY', mx.outputs[0], .5)
    rp = ramp(nt, mxs.outputs[0], [(.28, c1), (.62, c2)])
    col = rp.outputs['Color']
    if tint:
        t = attr(nt, 'tint'); mixc = N(nt, 'ShaderNodeMix'); mixc.data_type = 'RGBA'; mixc.blend_type = 'MULTIPLY'
        mixc.inputs['Factor'].default_value = .5
        link(nt, rp.outputs['Color'], mixc.inputs[6])
        tr = ramp(nt, t.outputs['Fac'], [(0, (.78, .72, .66, 1)), (1, (1.15, 1.05, .95, 1))]); link(nt, tr.outputs['Color'], mixc.inputs[7]); col = mixc.outputs[2]
    bp = bump(nt, mxs.outputs[0], bumpk, .015)
    b = bsdf(nt, Roughness=rough); link(nt, col, b.inputs['Base Color']); link(nt, bp.outputs[0], b.inputs['Normal'])
    sh = b.outputs[0]
    if reveal: sh = reveal_wrap(nt, b.outputs[0], m, soft=soft, grow=grow).outputs[0]
    finish(nt, sh); return m
def mat_stone(name='stone', reveal=False, soft=.12):
    m, nt = new_mat(name); tc = N(nt, 'ShaderNodeTexCoord'); mp = mapping(nt, tc.outputs['Object'], (1, 1, 1))
    t = attr(nt, 'tint'); nz = noise(nt, mp.outputs[0], 22., 4, .6)
    vor = N(nt, 'ShaderNodeTexVoronoi'); vor.feature = 'F1'; vor.inputs['Scale'].default_value = 38.; link(nt, mp.outputs[0], vor.inputs['Vector'])
    base = ramp(nt, t.outputs['Fac'], [(0, (.17, .14, .11, 1)), (.5, (.33, .28, .22, 1)), (1, (.50, .44, .36, 1))])
    var = ramp(nt, nz.outputs['Fac'], [(.3, (.80, .80, .78, 1)), (.7, (1.1, 1.08, 1.04, 1))])
    mixc = N(nt, 'ShaderNodeMix'); mixc.data_type = 'RGBA'; mixc.blend_type = 'MULTIPLY'; mixc.inputs['Factor'].default_value = 1.
    link(nt, base.outputs['Color'], mixc.inputs[6]); link(nt, var.outputs['Color'], mixc.inputs[7])
    hh = math_node(nt, 'ADD', nz.outputs['Fac'], vor.outputs['Distance']); bp = bump(nt, hh.outputs[0], .9, .03)
    b = bsdf(nt, Roughness=.88); link(nt, mixc.outputs[2], b.inputs['Base Color']); link(nt, bp.outputs[0], b.inputs['Normal'])
    sh = b.outputs[0]
    if reveal: sh = reveal_wrap(nt, b.outputs[0], m, soft=soft).outputs[0]
    finish(nt, sh); return m
def mat_simple(name, color, rough=.6, metal=0., spec=.5, bumpscale=0., bumpk=.3, nscale=40.):
    m, nt = new_mat(name); tc = N(nt, 'ShaderNodeTexCoord'); mp = mapping(nt, tc.outputs['Object'])
    nz = noise(nt, mp.outputs[0], nscale, 3, .6); b = bsdf(nt, Roughness=rough, Metallic=metal)
    var = ramp(nt, nz.outputs['Fac'], [(.3, tuple(c * .78 for c in color) + (1,)), (.7, tuple(min(1., c * 1.1) for c in color) + (1,))])
    link(nt, var.outputs['Color'], b.inputs['Base Color'])
    if bumpscale: bp = bump(nt, nz.outputs['Fac'], bumpk, bumpscale); link(nt, bp.outputs[0], b.inputs['Normal'])
    finish(nt, b.outputs[0]); return m
def mat_glass():
    m, nt = new_mat('glass'); lw = N(nt, 'ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = .35
    tr = N(nt, 'ShaderNodeBsdfTransparent'); gl = N(nt, 'ShaderNodeBsdfGlossy'); gl.inputs['Roughness'].default_value = .02; gl.inputs['Color'].default_value = (.85, .92, 1., 1.)
    mixf = math_node(nt, 'MULTIPLY', lw.outputs['Fresnel'], .85, True); mixa = math_node(nt, 'ADD', mixf.outputs[0], .09, True)
    mx = N(nt, 'ShaderNodeMixShader'); link(nt, mixa.outputs[0], mx.inputs['Fac']); link(nt, tr.outputs[0], mx.inputs[1]); link(nt, gl.outputs[0], mx.inputs[2])
    finish(nt, mx.outputs[0]); return m
def mat_emit(name, color, strength=0.):
    m, nt = new_mat(name); e = N(nt, 'ShaderNodeEmission'); e.inputs['Color'].default_value = color; e.inputs['Strength'].default_value = strength
    e.name = 'emit'; finish(nt, e.outputs[0]); return m
def mat_vcol(name, rough=.5, trans=0., sss=0., spec=.4, attrname='col', reveal=False):
    m, nt = new_mat(name); a = attr(nt, attrname); b = bsdf(nt, Roughness=rough)
    link(nt, a.outputs['Color'], b.inputs['Base Color']); sh = b.outputs[0]
    if trans:
        t = N(nt, 'ShaderNodeBsdfTranslucent'); link(nt, a.outputs['Color'], t.inputs['Color']); mx = N(nt, 'ShaderNodeMixShader'); mx.inputs['Fac'].default_value = trans
        link(nt, sh, mx.inputs[1]); link(nt, t.outputs[0], mx.inputs[2]); sh = mx.outputs[0]
    finish(nt, sh); return m
def mat_bark():
    m, nt = new_mat('bark'); tc = N(nt, 'ShaderNodeTexCoord'); mp = mapping(nt, tc.outputs['Object'], (14, 14, 2.2))
    nz = noise(nt, mp.outputs[0], 4., 4, .65, .3); vor = N(nt, 'ShaderNodeTexVoronoi'); vor.feature = 'DISTANCE_TO_EDGE'; vor.inputs['Scale'].default_value = 5.; link(nt, mp.outputs[0], vor.inputs['Vector'])
    c = ramp(nt, nz.outputs['Fac'], [(.3, (.10, .075, .055, 1)), (.7, (.24, .19, .15, 1))]); hh = math_node(nt, 'ADD', nz.outputs['Fac'], vor.outputs['Distance']); bp = bump(nt, hh.outputs[0], 1.2, .05)
    b = bsdf(nt, Roughness=.9); link(nt, c.outputs['Color'], b.inputs['Base Color']); link(nt, bp.outputs[0], b.inputs['Normal']); finish(nt, b.outputs[0]); return m
def mat_terrain():
    m, nt = new_mat('terrain'); tc = N(nt, 'ShaderNodeTexCoord'); d = attr(nt, 'dirt')
    big = noise(nt, tc.outputs['Object'], .09, 3, .5); mid = noise(nt, tc.outputs['Object'], 1.3, 3, .55); fine = noise(nt, tc.outputs['Object'], 60., 3, .6)
    g1 = ramp(nt, big.outputs['Fac'], [(.35, (.05, .12, .02, 1)), (.65, (.16, .26, .05, 1))])
    g2 = ramp(nt, mid.outputs['Fac'], [(.3, (.78, .78, .72, 1)), (.7, (1.18, 1.14, 1.0, 1))])
    gm = N(nt, 'ShaderNodeMix'); gm.data_type = 'RGBA'; gm.blend_type = 'MULTIPLY'; gm.inputs['Factor'].default_value = 1.; link(nt, g1.outputs['Color'], gm.inputs[6]); link(nt, g2.outputs['Color'], gm.inputs[7])
    soil = ramp(nt, fine.outputs['Fac'], [(.3, (.17, .08, .045, 1)), (.7, (.31, .16, .09, 1))])
    mx = N(nt, 'ShaderNodeMix'); mx.data_type = 'RGBA'; link(nt, d.outputs['Fac'], mx.inputs['Factor']); link(nt, gm.outputs[2], mx.inputs[6]); link(nt, soil.outputs['Color'], mx.inputs[7])
    bp = bump(nt, fine.outputs['Fac'], .5, .03); b = bsdf(nt, Roughness=.95); link(nt, mx.outputs[2], b.inputs['Base Color']); link(nt, bp.outputs[0], b.inputs['Normal']); finish(nt, b.outputs[0]); return m

def build_materials():
    M = MATS
    M['wood_z'] = mat_wood('wood_z', (.045, .02, .009, 1), (.22, .105, .045, 1), 'Z')
    M['wood_x'] = mat_wood('wood_x', (.045, .02, .009, 1), (.22, .105, .045, 1), 'X')
    M['wood_y'] = mat_wood('wood_y', (.045, .02, .009, 1), (.22, .105, .045, 1), 'Y')
    M['plank_z'] = mat_wood('plank_z', (.05, .022, .01, 1), (.25, .115, .048, 1), 'Z', tint=True)
    M['slat_x'] = mat_wood('slat_x', (.05, .022, .01, 1), (.25, .115, .048, 1), 'X', tint=True)
    M['deck_x'] = mat_wood('deck_x', (.30, .20, .12, 1), (.58, .42, .26, 1), 'X')
    M['dark_x'] = mat_wood('dark_x', (.03, .02, .012, 1), (.10, .06, .035, 1), 'X')
    M['stone'] = mat_stone('stone'); M['stone_c'] = M['stone']
    M['stone_static'] = mat_stone('stone_static')
    M['conc'] = mat_simple('conc', (.24, .235, .22), .92, 0., .3, .02, .5, 18.)
    M['metal'] = mat_simple('metal', (.55, .57, .6), .38, .9, .5, .005, .2, 80.)
    M['yellow'] = mat_simple('yellow', (.80, .52, .04), .45, .15, .5, .003, .2, 60.)
    M['black'] = mat_simple('black', (.02, .02, .02), .8)
    M['tire'] = mat_simple('tire', (.03, .03, .03), .9, 0., .3, .01, .6, 90.)
    M['red'] = mat_simple('red', (.55, .07, .04), .35, .25, .5, .002, .15, 50.)
    M['sack'] = mat_simple('sack', (.48, .44, .36), .95, 0., .3, .01, .6, 70.)
    M['sand'] = mat_simple('sand', (.55, .45, .28), 1., 0., .3, .02, .8, 90.)
    M['pot'] = mat_simple('pot', (.50, .20, .11), .85, 0., .4, .01, .5, 60.)
    M['skin'] = mat_simple('skin', (.55, .36, .26), .6)
    M['orange'] = mat_simple('orange', (.85, .32, .04), .6)
    M['shingle'] = mat_wood('shingle', (.035, .016, .008, 1), (.17, .08, .04, 1), 'Y', rough=.8, bumpk=.7, tint=True)
    M['rebar'] = mat_simple('rebar', (.25, .12, .06), .6, .8, .5, .004, .3, 90.)
    M['glass'] = mat_glass()
    M['glow_in'] = mat_emit('glow_in', (1., .62, .26, 1.), 0.)
    M['lantern'] = mat_emit('lantern', (1., .66, .3, 1.), 0.)
    M['interior'] = mat_simple('interior', (.12, .07, .04), .8)
    M['grass'] = mat_vcol('grass', .5, .3); M['leaf'] = mat_vcol('leaf', .45, .38); M['flower'] = mat_vcol('flower', .5, .15)
    M['frond'] = mat_vcol('frond', .4, .4); M['rock'] = mat_vcol('rock', .9, 0.)
    M['bark'] = mat_bark(); M['terrain'] = mat_terrain()
    M['mount'] = mat_vcol('mount', .95, 0.)
    M['stakes'] = mat_simple('stakes', (.75, .6, .2), .7)
    return M

# ---------------------------------------------------------------- geometry helpers
def mk_obj(name, mesh, mat=None, parent=None):
    o = bpy.data.objects.new(name, mesh); bpy.context.scene.collection.objects.link(o)
    if mat is not None: mesh.materials.append(mat)
    if parent is not None: o.parent = parent
    return o
def bmesh_to_obj(bm, name, mat):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.update()
    for p in me.polygons: p.use_smooth = True
    return mk_obj(name, me, mat)
def piece(bm, loc, size, rot=(0, 0, 0), bevel=0., attrs=None, seg=1):
    """Add a (bevelled) box with three-style size (w, h, d) -> Blender (w, d, h). loc is Blender coords."""
    n0 = len(bm.verts)
    ret = bmesh.ops.create_cube(bm, size=1.)
    verts = ret['verts']
    M = Matrix.Translation(loc) @ Euler(rot, 'XYZ').to_matrix().to_4x4() @ Matrix.Diagonal((size[0], size[1], size[2], 1.))
    bmesh.ops.transform(bm, matrix=M, verts=verts)
    if bevel > 0:
        es = list({e for v in verts for e in v.link_edges})
        bmesh.ops.bevel(bm, geom=es, offset=bevel, segments=seg, affect='EDGES')
    bm.verts.ensure_lookup_table()
    if attrs:
        for v in list(bm.verts)[n0:]:
            for k, val in attrs.items():
                lay = bm.verts.layers.float.get(k) if not isinstance(val, tuple) else bm.verts.layers.color.get(k)
                if lay is not None: v[lay] = val
    return verts
def obox(name, size3, pos3, mat, rot=(0, 0, 0), bevel=0.012, parent=None, base=True):
    """Object box: three-style size (w,h,d) and centre (x,y,z). If base: origin at bottom centre (for 'rise')."""
    w, h, d = size3; bm = new_bm(('tint',))
    c = V(*pos3)
    off = Vector((0, 0, h / 2)) if base else Vector((0, 0, 0))
    piece(bm, off, (w, d, h), bevel=min(bevel, min(w, h, d) * .3), attrs={'tint': RNG.random()})
    o = bmesh_to_obj(bm, name, mat); o.location = c - (Vector((0, 0, h / 2)) if base else Vector((0, 0, 0)))
    o.rotation_euler = rot
    if parent is not None: o.parent = parent
    return o
def new_bm(layers_float=(), layers_color=()):
    bm = bmesh.new()
    for l in layers_float: bm.verts.layers.float.new(l)
    for l in layers_color: bm.verts.layers.color.new(l)
    return bm
def mesh_np(name, verts, faces, colors=None, mat=None, extra=None):
    me = bpy.data.meshes.new(name); nv = len(verts); nf = len(faces); k = faces.shape[1]
    me.vertices.add(nv); me.vertices.foreach_set('co', verts.astype(np.float32).ravel())
    me.loops.add(nf * k); me.polygons.add(nf)
    me.loops.foreach_set('vertex_index', faces.astype(np.int32).ravel())
    me.polygons.foreach_set('loop_start', np.arange(0, nf * k, k, dtype=np.int32)); me.polygons.foreach_set('loop_total', np.full(nf, k, dtype=np.int32))
    me.update(calc_edges=True)
    if colors is not None:
        ca = me.color_attributes.new('col', 'FLOAT_COLOR', 'POINT'); ca.data.foreach_set('color', colors.astype(np.float32).ravel())
    if extra:
        for nm, arr in extra.items():
            at = me.attributes.new(nm, 'FLOAT', 'POINT'); at.data.foreach_set('value', arr.astype(np.float32))
    for p in me.polygons: p.use_smooth = True
    return mk_obj(name, me, mat)

def add_haze(mat, k=.0016, color=(.42, .52, .68)):
    nt = mat.node_tree; out = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]; lk = out.inputs['Surface'].links[0]; src = lk.from_socket
    cd = N(nt, 'ShaderNodeCameraData'); neg = math_node(nt, 'MULTIPLY', cd.outputs['View Z Depth'], -k); ex = math_node(nt, 'EXPONENT', neg.outputs[0]); f = math_node(nt, 'SUBTRACT', 1., ex.outputs[0], True)
    em = N(nt, 'ShaderNodeEmission'); em.inputs['Color'].default_value = color + (1.,); em.inputs['Strength'].default_value = 1.
    mx = N(nt, 'ShaderNodeMixShader'); link(nt, f.outputs[0], mx.inputs['Fac']); link(nt, src, mx.inputs[1]); link(nt, em.outputs[0], mx.inputs[2]); link(nt, mx.outputs[0], out.inputs['Surface'])
