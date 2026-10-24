# ConstruX · escena Blender (Cycles)

Versión fotorrealista de la casa rústica en construcción. Se ejecuta con el módulo `bpy` (Blender 5.0.1) en un venv:

    python3.11 -m venv bpyenv && bpyenv/bin/pip install bpy numpy
    cat hq1.py hq2.py hq3.py hq4.py > scene_hq.py
    bpyenv/bin/python -I scene_hq.py --fps 15 --frames 0-224 --w 720 --h 1280 --samples 28 --threads 4 --out hq15

- `hq1.py` materiales procedurales y utilidades de geometría
- `hq2.py` cielo, terreno, pasto, árboles, palmeras, montañas
- `hq3.py` casa, props de obra, animación por etapas, cámara
- `hq4.py` render y línea de comandos

Cada fotograma tarda ~1 min en 4 vCPU (sin GPU). Los fotogramas no se versionan.
