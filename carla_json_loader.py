
__doc__ = """
Utilities to export original CARLA dill data to json and visualize the loaded json.

Author: Nick Rhinehart
"""

import attrdict
import json
import matplotlib.pyplot as plt
import numpy as np
import os

# The colors.
COLORS = """#377eb8
#ff7f00
#4daf4a
#984ea3
#ffd54f""".split('\n')

def plot_datum(datum, meters_max=50):
    """Plot a loaded datum by displaying each agent's past and future positions overlaid upon each channel of the BEV.

    :param datum: the loaded datum (the return from load_json())
    :param meters_max: the half-width of each plot in meters
    :returns: the Matplotlib Figure
    """

    fig, axes = plt.subplots(2, 2, figsize=(10,10))
    bev_side_pixels = datum.overhead_features.shape[0] / 2.
    bev_meters = bev_side_pixels / datum.lidar_params['pixels_per_meter'] 
    
    for axidx, ax in enumerate(axes.ravel()):
        flabel = None if axidx > 0 else 'Car 1 future'
        plabel = None if axidx > 0 else 'Car 1 past'
        ax.scatter(datum.player_future[:,0], datum.player_future[:,1], label=flabel, marker='s', facecolor='None', edgecolor=COLORS[0])
        ax.scatter(datum.player_past[:,0], datum.player_past[:,1], label=plabel, marker='d', facecolor='None', edgecolor=COLORS[0])
        for other_idx, (af, ap) in enumerate(zip(datum.agent_futures, datum.agent_pasts)):
            flabel = None if axidx > 0 else 'Car {} future'.format(other_idx + 2)
            plabel = None if axidx > 0 else 'Car {} past'.format(other_idx + 2)
            ax.scatter(af[:,0], af[:,1], label=flabel, facecolor='None', edgecolor=COLORS[other_idx + 1], marker='s')
            ax.scatter(ap[:,0], ap[:,1], label=plabel, facecolor='None', edgecolor=COLORS[other_idx + 1], marker='d')
        ax.imshow(datum.overhead_features[...,axidx], extent=(-bev_meters, bev_meters, bev_meters, -bev_meters), cmap='Reds')
        ax.set_title("BEV channel {}".format(axidx))
        ax.set_xlim([-meters_max, meters_max])
        ax.set_ylim([meters_max, -meters_max])
    fig.tight_layout()
    fig.legend(bbox_to_anchor=(1., 1.), loc="upper left", fontsize=14)
    return fig

def load_json(json_fn):
    """Load a json datum.

    :param json_fn: <str> the path to the json datum.
    :returns: dict of postprocess json data.
    """
    assert(os.path.isfile(json_fn))
    json_datum = json.load(open(json_fn, 'r'))
    postprocessed_datum = from_json_dict(json_datum)
    return postprocessed_datum
    
def from_json_dict(json_datum):
    """Postprocess the json datum to ndarray-ify things

    :param json_datum: dict of the loaded json datum.
    :returns: dict of the postprocessed json datum.
    """
    pp = attrdict.AttrDict()
    for k, v in json_datum.items():
        if isinstance(v, list):
            pp[k] = np.asarray(v)
        elif isinstance(v, dict) or isinstance(v, int) or isinstance(v, str):
            pp[k] = v
        else:
            raise ValueError("Unrecognized type")
    return pp

class NumpyEncoder(json.JSONEncoder):
    """
    The encoding object used to serialize np.ndarrays
    """
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
        
def dill_to_json(dill_datum, out_fn):
    """Convert and save the original dill data to a more portable json representation

    :param dill_datum: <MultiagentMotionDatum> the datum
    :param out_fn: <str> the path to save the json representation to.
    :returns: <str> the path the json was saved to
    """
    
    dd = dill_to_json_dict(dill_datum)
    assert(not os.path.isfile(out_fn))
    with open(out_fn, 'w') as f:
        json.dump(dd, f, cls=NumpyEncoder)
    return out_fn

def dill_to_json_dict(dill_datum):
    """Convert the original dill data to a more portable json representation

    :param dill_datum: <MultiagentMotionDatum> the datum
    :returns: <dict> of the datum ready for jsonification
    """
    
    x = {
        # T_past x 3
        'player_past': dill_datum.player_past,
        # T x 3
        'player_future': dill_datum.player_future,
        # list, T x 3 ndarray
        'agent_pasts': dill_datum.agent_pasts,
        # list, T x 3 ndarray
        'agent_futures': dill_datum.agent_futures,
        # H x W x C ndarray
        'overhead_features': dill_datum.overhead_features,
        # 4 x 4 rotation and translation of player at current time.
        'player_transform': dill_datum.transform.matrix,
        # list of 4 x 4 rotation and translation of the other agents.
        'agent_transforms': [_.matrix for _ in dill_datum.agent_transforms],
        # dict of parameters used to create the overhead features.
        'lidar_params': dill_datum.lidar_params
    }
    try:
        y = {
            # str name of the episode
            'episode': dill_datum.metadata['episode'].split('/')[-1],
            # int frame of the episode
            'frame': dill_datum.metadata['frame']
        }
        x.update(y)
    except AttributeError:
        pass
    return x
