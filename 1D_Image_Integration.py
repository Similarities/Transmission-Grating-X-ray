import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
import os


class SingleImage1DIntegration:

    def __init__(self, filename_image, filename_background_image, rotation_angle):
        self.filename = filename_image
        self.rotation_angle = rotation_angle
        self.file_discription = str(self.filename[:-4])
        self.array_image = self.open_file(self.filename)
        self.array_background = self.open_file(filename_background_image)
        self.y_max, self.x_max = self.size_of_image()
        self.line_out_counts = np.zeros([self.y_max, 1])
        self.line_out_x = np.arange(0, self.x_max)
        self.convert_32_bit()
        self.array_image = self.rotate_picture(self.array_image)
        self.array_background = self.rotate_picture(self.array_background)
        self.process()


    def process(self):
        self.background_y()
        self.sum_over_y()
        self.save_data(self.line_out_counts, self.file_discription, 1E4)

    def open_file(self, filename):
        temporary_image_array = plt.imread(filename)
        return temporary_image_array

    def size_of_image(self):
        self.x_max, self.y_max = np.shape(self.array_image)
        print(self.x_max, self.y_max)
        return self.x_max, self.y_max

    def convert_32_bit(self):
        self.array_image = np.float32(self.array_image)
        self.array_background = np.float32(self.array_background)
        return self.array_image, self.array_background

    def background_y(self):
        for counter, x in enumerate(self.array_image[0, ::]):
            self.array_image[::, counter] = self.array_image[::, counter] - self.array_background[::, counter]
        # self.plot_rotated_back_subbed_image()
        return self.array_image

    def plot_rotated_back_subbed_image(self):
        plt.figure(1)
        plt.imshow(self.array_image)
        plt.colorbar()

    def rotate_picture(self, array):
        return ndimage.rotate(array, self.rotation_angle, reshape=False)

    def sum_over_y(self):
        self.line_out_counts = np.sum(self.array_image, axis=0)
        return self.line_out_counts

    def return_lineout_integrated_counts(self):
        return self.line_out_counts

    def return_lineout_x(self):
        return self.line_out_x

    def plot_lineout(self, array, name, maximum_value):
        plt.figure(2)
        plt.plot(self.line_out_x, array, label=name)
        plt.xlabel('px')
        plt.ylabel('integrated counts')
        plt.ylim(0, maximum_value)
        plt.legend()

    def prepare_header(self, array, name):
        # insert header line and change index
        result = np.column_stack((self.line_out_x, array))
        header_names = (['px', 'integrated counts'])
        parameter_info = (
            [self.file_discription + 'back: ' + self.background_name, 'integrated counts_backsubbed'])
        return np.vstack((parameter_info, header_names, result))

    def prepare_plots(self, array, name, maximum_value):
        self.plot_lineout(array, name, maximum_value)

    def save_data(self, array, name, maximum_value):
        result = self.prepare_header(array, name)
        self.prepare_plots(array, name, maximum_value)
        print('...saving:', name)
        plt.figure(2)
        plt.savefig(name + "linout" + ".png", bbox_inches="tight", dpi=500)
        np.savetxt(name + 'processed' + ".txt", result, delimiter=' ',
                   header='string', comments='',
                   fmt='%s')

def get_file_list(path_picture):
    tif_files = []
    counter = 0
    for file in os.listdir(path_picture):
        try:
            if file.endswith(".tif"):
                tif_files.append(str(file))
                counter = counter + 1
                print(str(file))
            else:
                print("only other files found")
        except Exception as e:
            raise e
            print("no files found here")
    return tif_files


def process_files(my_files, path, calibration, dark_picture):
    background_image = path + '/' + dark_picture
    integrated_picture = np.zeros([1024])
    counter = 0

    for x in range(0, len(my_files)):
        counter = counter + 1
        file = path + '/' + my_files[x]
        print(my_files[x], 'processing...')
        image_processing = SingleImage1DIntegration(file, background_image, -1.)
        integrated_actual_picture = image_processing.return_lineout_integrated_counts()
        integrated_picture[:] = integrated_picture[:] + integrated_actual_picture
        plt.close(2)

    integrated_picture[:] = integrated_picture[:] / (counter * calibration)
    integrated_picture.save_data(integrated_picture, str(path_picture) + 'per_second', 3E4)
    plt.close(2)

    return integrated_picture, integrated_picture.return_lineout_x()


path_picture = '20201008_3_degree_W'
calibration_per_second = 10* 0.945
dark_picture = 'dark/tgs_2020108__336.tif'
my_files = get_file_list(path_picture)
integrated_over_pictures, x_axis = process_files(my_files, path_picture, calibration_per_second, dark_picture)

plt.show()

