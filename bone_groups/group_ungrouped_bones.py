import bpy


pose = bpy.data.objects['geometry.new_player_emotes'].pose
group_name = "UNASSIGNED"

#should prevent creation of a new group if there is already one
grp = pose.bone_groups.new(name=group_name)


for bn in pose.bones:
    if not bn.bone_group:
        bn.bone_group=grp