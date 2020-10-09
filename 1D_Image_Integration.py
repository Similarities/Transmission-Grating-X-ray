import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
import os


class SingleImage1DIntegration:

    def __init__(self, filename_image, filename_background_image, rotation_angle):
        self.filename = filename_image
        self.rotation_angle = rotation_angle
        self.file_discription = str(self.filename[:-4])
        self.background_name = filename_background_image
        self.array_image = self.open_file(self.filename)
        self.array_background = self.open_file(self.background_name)
        self.convert_32_bit()
        self.array_image = self.rotate_picture(self.array_image)
        self.array_background = self.rotate_picture(self.array_background)
        self.y_min = 0
        self.x_min = 0
        self.y_max, self.x_max = self.size_of_image()
        self.background_y()
        self.line_out_counts = np.zeros([self.y_max, 1])
        self.line_out_x = np.arange(self.x_min, self.x_max)
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

        plt.figure(1)
        plt.imshow(self.array_image)
        # plt.vlines(self.x_min, 0, self.x_max)
        # plt.vlines(self.x_max, 0, self.x_max)
        plt.colorbar()
        return self.array_image

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
        plt.plot(self.line_out_x, array, label= name)
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
        return np.vstack((header_names, result, parameter_info))

    def prepare_plots(self, array, name, maximum_value):
        self.plot_lineout(array, name, maximum_value)

    def save_data(self, array, name, maximum_value):
        result = self.prepare_header(array, name)
        self.prepare_plots(array, name, maximum_value)
        print('...saving:', name)
        plt.figure(2)
        plt.savefig(name+ "linout" + ".png", bbox_inches="tight", dpi=500)
        np.savetxt(name + 'processed'+".txt", result, delimiter=' ',
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


def process_files(my_files, path):
    background_image = path + '/' + 'back/tgs_2020108__256.tif'
    integrated_over_pictures = np.zeros([1024])
    counter = 0

    for x in range(0, len(my_files)):
        counter = counter +1
        file = path + '/' + my_files[x]
        print(my_files[x], 'processing...')
        Process_files = SingleImage1DIntegration(file, background_image, -2.1)
        integrated_actual_picture = Process_files.return_lineout_integrated_counts()
        integrated_over_pictures[:] = integrated_over_pictures[:] + integrated_actual_picture
        #plt.show()
        plt.close(2)

    Process_files.save_data(integrated_over_pictures, '20201008_2x945ms_x' + str(counter), 1E5)
    plt.close(2)

    return integrated_over_pictures, Process_files.return_lineout_x()



path_picture = 'tif_2020108/5s/2cycle_945ms_10k_off'
my_files = get_file_list(path_picture)
integrated_over_pictures, x_axis = process_files(my_files, path_picture)
#plt.figure(4)
#plt.plot(x_axis, integrated_over_pictures, label = 'integrated over series of images')
#plt.legend()
#plt.show()