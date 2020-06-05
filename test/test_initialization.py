import os
import unittest
from shutil import rmtree

import imageio
import h5py
import numpy as np


class TestInitialization(unittest.TestCase):
    test_folder = './test-folder'
    root = './test-folder/data'
    tmp_folder = './test-folder/tmp'

    def setUp(self):
        os.makedirs(self.test_folder, exist_ok=True)

    def tearDown(self):
        try:
            rmtree(self.test_folder)
        except OSError:
            pass

    # TODO proper checks
    def check_dataset(self, dataset_folder, shape):
        self.assertTrue(os.path.exists(dataset_folder))

    def make_tif_data(self, im_folder, shape):
        os.makedirs(im_folder, exist_ok=True)
        for z in range(shape[0]):
            path = os.path.join(im_folder, 'z_%03i.tif' % z)
            imageio.imsave(path, np.random.rand(*shape[1:]))

    def test_init_from_tif(self):
        from mobie import initialize_dataset
        shape = (32, 128, 128)

        im_folder = os.path.join(self.test_folder, 'im-stack')
        self.make_tif_data(im_folder, shape)

        dataset_name = 'test'
        raw_name = 'test-raw'
        scales = [[1, 2, 2], [1, 2, 2], [2, 2, 2]]
        initialize_dataset(im_folder, '*.tif', self.root, dataset_name, raw_name,
                           resolution=(0.25, 1, 1), chunks=(16, 64, 64), scale_factors=scales,
                           tmp_folder=self.tmp_folder)

        self.check_dataset(os.path.join(self.root, dataset_name), shape)

    def make_hdf5_data(self, path, key, shape):
        with h5py.File(path, 'a') as f:
            f.create_dataset(key, data=np.random.rand(*shape))

    def test_init_from_hdf5(self):
        from mobie import initialize_dataset
        shape = (128, 128, 128)

        data_path = os.path.join(self.test_folder, 'data.h5')
        data_key = 'data'
        self.make_hdf5_data(data_path, data_key, shape)

        dataset_name = 'test'
        raw_name = 'test-raw'
        scales = [[2, 2, 2], [2, 2, 2], [2, 2, 2]]
        initialize_dataset(data_path, data_key, self.root, dataset_name, raw_name,
                           resolution=(1, 1, 1), chunks=(64, 64, 64), scale_factors=scales,
                           tmp_folder=self.tmp_folder)

        self.check_dataset(os.path.join(self.root, dataset_name), shape)


if __name__ == '__main__':
    unittest.main()