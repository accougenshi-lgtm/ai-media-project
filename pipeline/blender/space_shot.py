"""Blender (Cycles, CPU, headless) cinematic space shot: procedural planet + atmosphere + star field + moving camera.
Run: blender -b -P pipeline/blender/space_shot.py -- --out output/bl/test_ --frames 48 --res 1080x1920 --samples 16 --kind moon
"""
import bpy, sys, math, argparse
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--out", default="//shot_"); ap.add_argument("--frames", type=int, default=48)
ap.add_argument("--res", default="1080x1920"); ap.add_argument("--samples", type=int, default=16)
ap.add_argument("--kind", default="moon"); ap.add_argument("--fps", type=int, default=24)
a = ap.parse_args(argv)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
W, H = map(int, a.res.split("x"))
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = a.samples
sc.cycles.use_denoising = False  # Ubuntu build lacks OIDN
try: sc.cycles.denoiser = "OPENIMAGEDENOISE"
except Exception: pass
sc.render.resolution_x, sc.render.resolution_y = W, H; sc.render.fps = a.fps
sc.frame_start, sc.frame_end = 1, a.frames
sc.render.image_settings.file_format = "PNG"; sc.render.filepath = a.out
sc.view_settings.view_transform = "Filmic" if "Filmic" in [v.identifier for v in sc.view_settings.bl_rna.properties["view_transform"].enum_items] else "Standard"
sc.view_settings.look = "None"

# --- world: black with procedural stars ---
world = bpy.data.worlds.new("W"); sc.world = world; world.use_nodes = True
nt = world.node_tree; nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputWorld"); bg = nt.nodes.new("ShaderNodeBackground")
tc = nt.nodes.new("ShaderNodeTexCoord"); vor = nt.nodes.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 260
ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].position = 0.0; ramp.color_ramp.elements[1].position = 0.06
ramp.color_ramp.elements[0].color = (1, 1, 1, 1); ramp.color_ramp.elements[1].color = (0, 0, 0, 1)
nt.links.new(tc.outputs["Generated"], vor.inputs["Vector"]); nt.links.new(vor.outputs["Distance"], ramp.inputs["Fac"])
nt.links.new(ramp.outputs["Color"], bg.inputs["Color"]); bg.inputs["Strength"].default_value = 1.4
nt.links.new(bg.outputs["Background"], out.inputs["Surface"])

# --- planet ---
bpy.ops.mesh.primitive_uv_sphere_add(segments=128, ring_count=64, radius=1.0)
planet = bpy.context.object; bpy.ops.object.shade_smooth()
mat = bpy.data.materials.new("Planet"); mat.use_nodes = True; planet.data.materials.append(mat)
n = mat.node_tree.nodes; l = mat.node_tree.links; bsdf = n["Principled BSDF"]
noise = n.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 3.0; noise.inputs["Detail"].default_value = 12
cr = n.new("ShaderNodeValToRGB"); cr.color_ramp.elements[0].position = 0.5; cr.color_ramp.elements[1].position = 0.53
pal = {"moon": [(0.18, 0.18, 0.19, 1), (0.62, 0.61, 0.58, 1)], "mars": [(0.32, 0.1, 0.05, 1), (0.78, 0.38, 0.2, 1)],
       "earth": [(0.01, 0.05, 0.22, 1), (0.16, 0.3, 0.1, 1)]}[a.kind]
cr.color_ramp.elements[0].color, cr.color_ramp.elements[1].color = pal
l.new(noise.outputs["Fac"], cr.inputs["Fac"]); l.new(cr.outputs["Color"], bsdf.inputs["Base Color"])
bump = n.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.12 if a.kind != "moon" else 0.25
fine = n.new("ShaderNodeTexNoise"); fine.inputs["Scale"].default_value = 40; fine.inputs["Detail"].default_value = 8
l.new(fine.outputs["Fac"], bump.inputs["Height"]); l.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
if a.kind == "earth":  # oceans glossier than land
    l.new(cr.outputs["Color"], bsdf.inputs["Base Color"]); bsdf.inputs["Roughness"].default_value = 0.6
bsdf.inputs["Roughness"].default_value = 0.95
planet.rotation_euler = (0.3, 0, 0)
planet.keyframe_insert("rotation_euler", frame=1); planet.rotation_euler[2] = math.radians(6); planet.keyframe_insert("rotation_euler", frame=a.frames)

# atmosphere rim for earth/mars
if a.kind in ("earth", "mars"):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, radius=1.03); atm = bpy.context.object; bpy.ops.object.shade_smooth()
    am = bpy.data.materials.new("Atm"); am.use_nodes = True; atm.data.materials.append(am); am.blend_method = "BLEND"
    an = am.node_tree.nodes; an.clear(); ao = an.new("ShaderNodeOutputMaterial")
    lw = an.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.35
    em = an.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (0.35, 0.6, 1, 1) if a.kind == "earth" else (1, 0.6, 0.4, 1)
    em.inputs["Strength"].default_value = 2.2
    tr_ = an.new("ShaderNodeBsdfTransparent"); mix = an.new("ShaderNodeMixShader")
    pw = an.new("ShaderNodeMath"); pw.operation = "POWER"; pw.inputs[1].default_value = 2.5
    am.node_tree.links.new(lw.outputs["Facing"], pw.inputs[0]); am.node_tree.links.new(pw.outputs[0], mix.inputs["Fac"])
    am.node_tree.links.new(tr_.outputs[0], mix.inputs[1]); am.node_tree.links.new(em.outputs[0], mix.inputs[2])
    am.node_tree.links.new(mix.outputs[0], ao.inputs["Surface"])

# --- sun light ---
bpy.ops.object.light_add(type="SUN", rotation=(math.radians(60), math.radians(-20), math.radians(-50)))
bpy.context.object.data.energy = 4.5; bpy.context.object.data.angle = math.radians(0.6)

# --- camera: slow dolly-in + drift (cinematic) ---
bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam; cam.data.lens = 50
cam.data.dof.use_dof = False
def place(f, x, y, z):
    cam.location = (x, y, z); cam.keyframe_insert("location", frame=f)
place(1, 0.9, -6.2, 0.6); place(a.frames, 0.25, -4.4, 0.2)
tr = cam.constraints.new("TRACK_TO"); tr.target = planet; tr.track_axis = "TRACK_NEGATIVE_Z"; tr.up_axis = "UP_Y"
for fc in cam.animation_data.action.fcurves:
    for k in fc.keyframe_points: k.interpolation = "BEZIER"
bpy.ops.render.render(animation=True)
