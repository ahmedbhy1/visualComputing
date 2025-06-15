import bpy, numpy as np, math, random,json

# ---------------------------------------------------------------
# EDIT THESE -----------------------------------------------------
MUSIC_FILE = r"C:\Users\MSI\Downloads\Bayern, Des Samma Mia - Bavarian Folk Song [Lyrics  Translation].mp3"
MUSIC_FILE_FROM_JSON = r"C:\Users\MSI\Downloads\your_song_analysis.json" 
BEAT_FILE = r"C:\Users\MSI\Downloads\beats.npy"    # output of Phase 1
ARMATURE     = "Armature"                      # object in Outliner
BONES        = ["upperarm.L", "upperarm.R",
                "upperleg.L", "upperleg.R",
                "head"]                       # any bones you like
AMP_DEG      = 25                              # rotation per beat
STEP_VARIANT = 0.2                             # ±20 % random timing jitter
# ---------------------------------------------------------------

rig  = bpy.data.objects[ARMATURE]
fps  = bpy.context.scene.render.fps
beats = np.load(BEAT_FILE)
print("Beats loaded: from np", beats)

# ✅ Load beats from JSON (not from .npy!)
with open(MUSIC_FILE_FROM_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

beats = data["beats"]  # extract beat timestamps in seconds
print("Beats loaded: from json", beats)

# helper: alternating + / – so limbs go left-right-left-right
direction = {name: 1 for name in BONES}

# could you add thee code so that i can run the mp3 song file here ?


for name in BONES:
    pb = rig.pose.bones[name]
    pb.rotation_mode = 'XYZ' 
    try:
        pb.keyframe_delete(data_path="rotation_euler")
    except RuntimeError:
        pass                  # guarantee Euler

amp = math.radians(AMP_DEG)

for t in beats:
    # small jitter keeps it from looking mechanical
    t += random.uniform(-STEP_VARIANT, STEP_VARIANT) * (1 / fps)
    frame = int(round(t * fps))

    for name in BONES:
        pb = rig.pose.bones[name]
        axis = 'x' if ".leg" in name else 'z'  # legs kick forward, arms swing
        # set attribute via axis string
        rot = list(pb.rotation_euler)
        idx = 'xyz'.index(axis)
        rot[idx] = direction[name] * amp
        pb.rotation_euler = rot
        pb.keyframe_insert(data_path="rotation_euler", frame=frame)

        direction[name] *= -1                  # flip next time

# Add audio to VSE
scene = bpy.context.scene
scene.sequence_editor_create()

# Safely remove all sequences
if scene.sequence_editor:
    for s in scene.sequence_editor.sequences_all:
        scene.sequence_editor.sequences.remove(s)

scene.sequence_editor.sequences.new_sound(
    name="MusicTrack",
    filepath=MUSIC_FILE,
    channel=1,
    frame_start=0
)
scene.sync_mode = 'AUDIO_SYNC'
scene.use_audio = True
scene.use_audio_scrub = True
scene.use_preview_range = False
bpy.context.preferences.system.audio_device = 'WASAPI'

# extend timeline so we can watch everything
bpy.context.scene.frame_end = int(max(beats) * fps) + fps
bpy.context.scene.frame_current = 0
bpy.ops.screen.animation_play()

print(f"💃 Inserted {len(beats)} beats × {len(BONES)} bones. Enjoy!")