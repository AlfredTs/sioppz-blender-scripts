#adds oriented empties at origins of all selected objects
import bpy
scene = bpy.context.scene

for ob in bpy.context.selected_objects:
    emp = bpy.data.objects.new('Ctrl_'+ob.name_full, None)
    emp.location = ob.location
    emp.rotation_euler = ob.rotation_euler 
    scene.collection.objects.link(emp)
