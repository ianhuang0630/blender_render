import os
import numpy as np
from tqdm import tqdm

regression_jsons = '../../orion/structedit/data/viz_showable/continuous/viz'
discrete_jsons = '../../orion/structedit/data/viz_showable/discrete/viz'

regs = [el for el in os.listdir(regression_jsons) if el.endswith('regressed_target.json')]
dels = [el for el in os.listdir(discrete_jsons) if el.endswith('source_with_del.json')]
adds = [el for el in os.listdir(discrete_jsons) if el.endswith('target_with_add.json')]

regs = sorted(regs)
dels = sorted(dels)
adds = sorted(adds)

blender_location = 'blender'
blender_file = 'boxes.blend'
blender_python_regress = 'blender_box.py'
blender_python_discrete = 'blender_adddel_annot.py'

if not os.path.exists('box_renders'): 
    os.makedirs('box_renders')

for r, d, a in tqdm(zip(regs, dels, adds)):
    
    instance_id = r.split('_')[0] # get the number at the beginning
    print('instance_id: {}'.format(instance_id))
    print('gt src')
    command = '{blender_location} --background {blender_file} --python {blender_python} -- {in_file} {out_file}'\
    .format(blender_location = blender_location,
           blender_file = blender_file,
           blender_python = blender_python_regress,
           in_file = os.path.join(discrete_jsons, d),
           out_file = 'box_renders/{}_src.png '.format(instance_id))
    os.system( command )


    print('gt target')
    command = '{blender_location} --background {blender_file} --python {blender_python} -- {in_file} {out_file}'\
    .format(blender_location = blender_location,
           blender_file = blender_file,
           blender_python = blender_python_regress,
           in_file = os.path.join(discrete_jsons, a),
           out_file = 'box_renders/{}_tgt.png '.format(instance_id))
    os.system( command )
    
    
    print('del')
    command = '{blender_location} --background {blender_file} --python {blender_python} -- {in_file} {out_file}'\
    .format(blender_location = blender_location,
           blender_file = blender_file,
           blender_python = blender_python_discrete,
           in_file= os.path.join(discrete_jsons, d),
           out_file = 'box_renders/{}_del.png '.format(instance_id))
    os.system( command )

    
    print('add')
    command = '{blender_location} --background {blender_file} --python {blender_python} -- {in_file} {out_file}'\
    .format(blender_location = blender_location,
           blender_file = blender_file,
           blender_python = blender_python_discrete,
           in_file= os.path.join(discrete_jsons, a),
           out_file = 'box_renders/{}_add.png '.format(instance_id))
    os.system( command )
    

    print ('regression')
    command = '{blender_location} --background {blender_file} --python {blender_python} -- {in_file} {out_file}'\
    .format(blender_location = blender_location,
           blender_file = blender_file,
           blender_python = blender_python_regress,
           in_file = os.path.join(regression_jsons, r),
           out_file = 'box_renders/{}_reg.png '.format(instance_id))
    os.system( command )


