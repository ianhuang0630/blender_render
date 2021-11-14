import os
import numpy as np
from tqdm import tqdm

def save_pt_color(folder_path, pts, colors):
    """
    saves pts into '{folder_path}/pts.txt'
    saves rgb color info into '{folder_path}/colors.txt'
    """
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)
    pts_file = os.path.join(folder_path, 'pts.txt')
    colors_file = os.path.join(folder_path, 'colors.txt')
     
    assert len(pts) == len(colors)

    with open(pts_file, 'w') as f:
        f.writelines([' '.join([str(el) for el in coord]) + '\n' for coord in pts])

    with open(colors_file, 'w') as f:
        f.writelines([' '.join([str(el) for el in rgb]) + '\n' for rgb in colors])

def get_partnet_id_from_json(source_json):
    return source_json[:-len('.json')]

magnification = 1
blender_location = 'blender'
blender_file = 'point_clouds.blend'
blender_python = 'blender_pointcloud.py'

pointcloud_data = '../../orion/structedit/data/structurenet/partnethiergeo/chair_geo/'
partnet_jsons = '../../orion/structedit/data/partnetdata/chair_hier'
renders_out_loc = 'renders_per_shape/'
if not os.path.exists(renders_out_loc):
    os.makedirs(renders_out_loc)

partnet_annot_ids_jsons = [el for el in os.listdir(partnet_jsons) if el.endswith('.json')]

for source_json in tqdm(partnet_annot_ids_jsons):
    try:
        sid_src = get_partnet_id_from_json(source_json)
        print('src: {}'.format(sid_src))
        src_vertices = np.load(os.path.join(pointcloud_data, '{}.npz'.format(sid_src)))['parts'].reshape(-1, 3)*magnification
    except:
        print('skipping: {}'.format(sid_src))
        continue

    default_color = [253, 134, 18] # orange
    src_colors = [default_color] * len(src_vertices)
    save_pt_color('/tmp/nledit_src/', src_vertices, src_colors)

    command = '{blender_location} --background {blender_file} --python {blender_python} -- {in_folder} {out_file}'\
    .format(blender_location = blender_location,
           blender_file = blender_file,
            blender_python = blender_python,
           in_folder = '/tmp/nledit_src/',
           out_file = 'renders_per_shape/{}'.format(sid_src))
    os.system( command )

    assert os.path.exists('renders_per_shape/{}.png'.format(sid_src))
    print('finished rendering source')


