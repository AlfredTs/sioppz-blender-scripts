import bpy
import os

file = open('/home/sioppz/gdrive/projects.active/zenjon.2020Minecraft/on/items/groups_data', 'r')

pose = bpy.data.objects['geometry.new_player_emotes'].pose


groups_made = False

for line in file:
    if not groups_made:
        if (line.rstrip()=="###"):
            groups_made = True
        else:
            if pose.bone_groups.find(line.rstrip())==-1:
             pose.bone_groups.new(name=line.rstrip())
    else:
        ld = line.split(":")
        if pose.bones.find(ld[0])!=-1:
            grp = pose.bone_groups[ld[1].rstrip()]
            pose.bones[ld[0]].bone_group = grp
        else:
            print(ld[0]+" bone not found")

file.close()