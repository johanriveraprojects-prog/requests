# part 4: scene assembly and CLI
def setup_render(sc, W, H, samples, threads=4):
    sc.render.engine = 'CYCLES'; c = sc.cycles; c.device = 'CPU'; sc.render.threads_mode = 'FIXED'; sc.render.threads = threads
    sc.render.resolution_x = W; sc.render.resolution_y = H; sc.render.resolution_percentage = 100
    c.samples = samples; c.use_adaptive_sampling = True; c.adaptive_threshold = .035; c.adaptive_min_samples = 12
    c.use_denoising = True
    try: c.denoising_input_passes = 'RGB'
    except Exception as e: print('passes:', e)
    try: c.denoiser = 'OPENIMAGEDENOISE'
    except Exception as e: print('denoiser:', e)
    c.max_bounces = 6; c.diffuse_bounces = 3; c.glossy_bounces = 3; c.transmission_bounces = 4; c.transparent_max_bounces = 10; c.volume_bounces = 1
    c.sample_clamp_indirect = 2.5; c.caustics_reflective = False; c.caustics_refractive = False
    sc.render.use_persistent_data = True
    sc.view_settings.view_transform = os.environ.get('VT', 'Khronos PBR Neutral')
    try: sc.view_settings.look = os.environ.get('LOOK', 'None')
    except Exception: pass
    sc.view_settings.exposure = float(os.environ.get('EXPO', '-0.55'))
    sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 96

def build_all(W, H, samples):
    bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene; setup_render(sc, W, H, samples)
    M = build_materials()
    for i, c in enumerate([(.85, .15, .35), (.95, .8, .15), (.95, .95, .9)]): M['flower_%d' % i] = mat_simple('flower%d' % i, c, .5)
    M['leafb'] = mat_simple('leafb', (.05, .2, .03), .5, 0., .4, .01, .4, 70.)
    sky = build_world(sc)
    build_terrain(M); build_grass(M); build_flowers(M)
    for i in range(30):
        a = RNG.random() * 6.283; r = 10 + RNG.random() * 32; rock_obj(M, math.cos(a) * r, math.sin(a) * r, .35 + RNG.random() * .5)
    for x, z, k in [(-21, 5, 0), (-17, 11, 1), (23, -8, 0), (20, -13, 1), (-24, -9, 1), (-30, -2, 0)]:
        (build_broad_tree if k == 0 else build_conifer)(M, x, z, 1.25 + RNG.random() * .35, 2.2)
    n_mid = 0
    while n_mid < 24:
        a = RNG.random() * 6.283; r = 42 + RNG.random() * 90; x, z = math.cos(a) * r, math.sin(a) * r
        if x > -8 and z > -8: continue
        (build_broad_tree if RNG.random() < .55 else build_conifer)(M, x, z, 1.0 + RNG.random() * .8, 1.0); n_mid += 1
    n_far = 0
    while n_far < 70:
        a = RNG.random() * 6.283; r = 110 + RNG.random() * 230; x, z = math.cos(a) * r, math.sin(a) * r
        if x > -8 and z > -8: continue
        build_far_clump(M, x, z, 1.4 + RNG.random() * 1.6); n_far += 1
    for x, z in [(-15, 8), (-13.5, -8), (-9.5, 15), (8, -14), (17.5, -7), (-29, 18), (31, -19), (-6, -22)]: build_palm(M, x, z, .9 + RNG.random() * .3)
    build_mountains(M)
    build_house(M)
    for nm in ('terrain', 'grass', 'mount', 'leaf', 'bark', 'frond', 'rock', 'flower'): add_haze(M[nm])
    cam = setup_camera(sc)
    return sc, sky, cam

def render_frame(sc, sky, cam, t, path):
    s = stage_at(t); apply_stage(s, t); place_sun(sky, t); place_camera(cam, t)
    sc.render.filepath = path; bpy.ops.render.render(write_still=True); return s

if __name__ == '__main__':
    import argparse, time
    ap = argparse.ArgumentParser(); ap.add_argument('--times', default=''); ap.add_argument('--frames', default=''); ap.add_argument('--w', type=int, default=540); ap.add_argument('--h', type=int, default=960)
    ap.add_argument('--samples', type=int, default=32); ap.add_argument('--out', default='/tmp/hq'); ap.add_argument('--threads', type=int, default=4); ap.add_argument('--prefix', default='f'); ap.add_argument('--hide', default=''); ap.add_argument('--fps', type=float, default=30.)
    a = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    os.makedirs(a.out, exist_ok=True); t0 = time.time()
    sc, sky, cam = build_all(a.w, a.h, a.samples); setup_render(sc, a.w, a.h, a.samples, a.threads); print('BUILD', round(time.time() - t0, 1), 's; objects', len(bpy.data.objects), flush=True)
    for nm in [x for x in a.hide.split(',') if x]:
        for o in bpy.data.objects:
            if o.name.startswith(nm): o.hide_render = True
    if a.times:
        for tt in [float(x) for x in a.times.split(',')]:
            t1 = time.time(); s = render_frame(sc, sky, cam, tt, f'{a.out}/{a.prefix}_{int(tt * 10):03d}.jpg'); print('t', tt, 'stage', round(s, 2), 'render', round(time.time() - t1, 1), 's', flush=True)
    if a.frames:
        f0, f1 = [int(x) for x in a.frames.split('-')]
        for f in range(f0, f1 + 1):
            p = f'{a.out}/{a.prefix}{f:05d}.jpg'
            if os.path.exists(p): continue
            t1 = time.time(); render_frame(sc, sky, cam, f / a.fps, p)
            if (f - f0) % 5 == 0: print('frame', f, round(time.time() - t1, 1), 's', time.strftime('%H:%M:%S'), flush=True)
        print('DONE', f0, f1, flush=True)
