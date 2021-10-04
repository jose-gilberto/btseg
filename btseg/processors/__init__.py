import glob
import os

from btseg.time_series import generate_time_series, save_time_series
from btseg.slices import selecting_slice
import pandas as pd

class ImageToTimesProcessor:

    def __init__(self) -> None:
        super().__init__()

    def run(self, running_dir):
        running_dir = running_dir

        dataset = {
            'id': [],
            'slice_path': [],
            'times_series': []
        }
        
        folders = glob.glob(running_dir + '*/')
        for f in folders:
            id = f.split('_')[-1].replace('\\', '')
            slice_path = selecting_slice(f)
            times = generate_time_series(slice_path)

            dataset['id'].append(id)
            dataset['slice_path'].append(slice_path)
            dataset['times_series'].append(times)

            save_time_series(times, f'../data/Times/{id}.txt')

        dataset = pd.DataFrame(dataset)
        dataset.to_csv('../data/dataset.csv', sep=',')
