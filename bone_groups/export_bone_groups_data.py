import bpy
import os

f = open('/home/sioppz/gdrive/projects.active/zenjon.2020Minecraft/on/items/groups_data', 'w')

arm = bpy.data.objects['geometry.new_player']
for group in arm.pose.bone_groups:
    f.write(group.name+'\n')

f.write("### \n")

for b in arm.pose.bones:
    f.write(b.name+":"+b.bone_group.name+'\n')

f.close()