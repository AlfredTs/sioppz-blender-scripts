import bpy
import os

#replace the armature name
pose = bpy.data.objects['geometry.new_player_emotes'].pose

for grp in pose.bone_groups[:]:
    pose.bone_groups.remove(grp)
