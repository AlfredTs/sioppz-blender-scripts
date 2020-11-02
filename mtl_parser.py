import bpy

newtag = "newmtl"


print("Starting!")
filePath = '/home/sioppz/gdrive/projects.active/aiwa.SBX100/on/scenes/assets/environment/'
f = open(filePath+'office_interior_3.txt','r')
obj_mats = []

i = 0
print("Processing all the data!")
for ln in f:
    i+=1
    ln = ln.strip()
    data = ln.split()
    if len(data)==0: continue

    if data[0]==newtag:
        mat = dict()
        mat['name'] = data[1]
        obj_mats.append(mat)
        
    elif data[0]=='map_bump':
        obj_mats[-1][data[0]] = repr(data[-1]).split('\\')[-1].replace("'",'')
        if len(data) > 2:
            obj_mats[-1]['bump'] = float(data[2])
        
    elif data[0].split("_")[0]=='map':
        #FIND HOW TO USE BACKSLASH AS A DELIMETER!
        obj_mats[-1][data[0]] = repr(data[1]).split('\\')[-1].replace("'",'')
          
    elif len(data)>2:
        x = []
        for d in data[1:]:
            x.append(float(d))
        obj_mats[-1][data[0]] = tuple(x)+(1.0,)
        
    elif data[0]!='bump':
        obj_mats[-1][data[0]] = float(data[1])
        


print(str(len(obj_mats))+" materials found in mtl processed!")
#print(obj_mats)

def addTextureNode(nodes, texture):
    path = '//textures/'+str(texture)
    print('text')
    texData = (bpy.data.images.get(texture) or bpy.data.images.load(path))
    node = nodes.new('ShaderNodeTexImage')
    node.image = texData
    return node

print('Starting applying things to materials!')
for mat in obj_mats:

    mat_name = mat['name']
    print('Staring work on '+mat_name)
    print(mat.get('Kd',(.8,.8,.8,1.0)))
    # Test if material exists
    # If it does not exist, create it:
    material = (bpy.data.materials.get(mat_name) or 
           bpy.data.materials.new(mat_name))

    # Enable 'Use nodes':
    material.use_nodes = True
    nodes = material.node_tree.nodes

    princip = nodes['Principled BSDF']
    princip.inputs['Specular'].default_value = mat.get('Ns',500)/1000
    princip.inputs['Roughness'].default_value = 1-(mat.get('Ns',500)/1000)
    princip.inputs['IOR'].default_value = mat.get('Ni',1.45)
    princip.inputs['Alpha'].default_value = mat.get('d',1.0)
    princip.inputs['Base Color'].default_value = mat.get('Kd',(.8,.8,.8,1.0))
    #princip.inputs['Specular Tint'].default_value = mat.get('Ks',(1.0,1.0,1.0,1.0))
    princip.inputs['Emission'].default_value = mat.get('Ke',(0.0,0.0,0.0,1.0))

    #load image textures
    if 'map_Kd' in mat:
        node = addTextureNode(nodes,mat['map_Kd'])
        node.location = (-500,500)
        material.node_tree.links.new(princip.inputs['Base Color'],node.outputs['Color'])
    elif 'map_d' in mat:
        node = addTextureNode(nodes,mat['map_d'])
        node.location = (-500,-500)
        material.node_tree.links.new(princip.inputs['Alpha'],node.outputs['Color'])
        pass
    elif 'map_bump' in mat:
        node = addTextureNode(nodes,mat['map_bump'])
        node.location = (-500,-900)
        bumpnode = nodes.new('ShaderNodeBump')
        if 'bump' in mat:
            bumpnode.inputs['Strength'].default_value = mat['bump']
        material.node_tree.links.new(bumpnode.inputs['Height'],node.outputs['Color'])
        material.node_tree.links.new(princip.inputs['Normal'],bumpnode.outputs['Normal'])
        pass 
    elif 'map_Ks' in mat:
        pass
    elif 'map_Ns' in mat:
        pass
    
    print('Finished material '+mat_name)
