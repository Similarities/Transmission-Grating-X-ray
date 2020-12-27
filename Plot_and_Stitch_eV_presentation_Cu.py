import matplotlib.pyplot as plt
import numpy as np
import os


class PlotAndStitch:
    def __init__(self, path, my_file, column_read_in, string_number, ev_or_nm):
        self.my_file = my_file
        self.my_path = path
        self.column_read_in = column_read_in
        self.string_number = string_number
        self.bool = ev_or_nm
        self.xlabel = 'nm'
        self.spectrum_x, self.spectrum_y = self.load_array()

    def ev_or_nm(self, array):
        if self.bool is True:
            array = self.convert_nm_to_ev(array)
        return array

    def convert_nm_to_ev(self, array):
        c = 299792458
        planck_constant = 4.135667516 * 1E-15
        ev = planck_constant * c / (array[::] * 1E-9)
        self.xlabel = 'eV'
        return ev

    def load_2_d_array(self, file):
        nm_axis = np.loadtxt(file, skiprows=3, usecols=(0,))
        counts_per_second = np.loadtxt(file, skiprows=3, usecols=(self.column_read_in,))
        return nm_axis, counts_per_second

    def resize_array(self, l_index, r_index):
        self.spectrum_x = self.spectrum_x[l_index: r_index]
        self.spectrum_y = self.spectrum_y[l_index: r_index]
        return self.spectrum_x, self.spectrum_y

    def plot_array(self, array_x, array_y, name, scaling_y, linewidth, color):
        plt.figure(1)
        plt.semilogx(abs(array_x), scaling_y * array_y, label=name, linewidth=linewidth, color=color)
        plt.xlabel(self.xlabel)
        plt.ylabel('counts/s')

    def load_array(self):
        file = self.my_path + '/' + self.my_file
        print(file, 'processing...')
        self.spectrum_x, self.spectrum_y = self.load_2_d_array(file)
        return self.spectrum_x, self.spectrum_y

    def process_files(self, scaling_y, line_width, scaling_x, name, color):
        self.spectrum_x = self.ev_or_nm(self.spectrum_x * scaling_x)
        self.plot_array(self.spectrum_x, self.spectrum_y, name, scaling_y, line_width, color)


def get_file_list(directory):
    my_files = []
    counter = 0
    for file in os.listdir(directory):
        try:
            if file.endswith(".txt"):
                my_files.append(str(file))
                counter = counter + 1
                print(str(file))
            else:
                print("x")
        except Exception as e:
            raise e
    return my_files


class PlotLineData:
    def __init__(self, filename, switch, color, scale):
        self.path = filename
        self.name = str(self.path)[:-4]
        self.color = color
        self.sign = switch
        self.scale = scale
        self.x_label = 'nm'
        self.nm_axis = np.loadtxt(self.path, skiprows=1, usecols=(1,))
        self.intensity = np.loadtxt(self.path, skiprows=1, usecols=(2,))
        self.ev_or_nm()

    def strong_lines_only(self):
        maximum = np.amax(self.intensity)

        for counter, value in enumerate(self.intensity):
            if value < maximum / 4:
                self.nm_axis[counter] = 0

    def ev_or_nm(self):
        if self.sign is True:
            self.convert_nm_to_ev()
            self.x_label = 'eV'
        return self.x_label

    def convert_nm_to_ev(self):
        c = 299792458
        planck_constant = 4.135667516 * 1E-15
        self.nm_axis = planck_constant * c / (self.nm_axis * 1E-9)
        return self.nm_axis

    def scale_and_plot(self, figure_number):
        plt.figure(figure_number)
        plt.vlines(self.nm_axis, ymin=0, ymax=self.scale, label=str(self.name), linewidth=0.2, color=self.color)
        plt.xlabel(self.x_label)
        # plt.legend()


file_path = 'per_second/nm/all/selection_Cu_target'
my_files_as_list = get_file_list(file_path)
#print(my_files_as_list)
single = my_files_as_list[4]

print('selection files:', single)

# classe wants: file_path, file_list, column_number x, //
# column_numbery, number_of_skipped_letters_for_string, bool (True = eV, False = nm)
Test = PlotAndStitch(file_path, str(single), 2, -25, True)
Test.resize_array(3, 960)
Test.process_files(1, 1, 1E9, 'Zr_filter', 'b')
single2 = my_files_as_list[1]

Test = PlotAndStitch(file_path, str(single2), 2, -25, True)
Test.resize_array(500, 1000)
Test.process_files(1, 1, 1E9, 'Al_filter', 'm')
single2 = my_files_as_list[2]

Test = PlotAndStitch(file_path, str(single2), 2, -25, True)
Test.resize_array(0, 700)
Test.process_files(1, 1, 1E9, 'Al_filter', 'm')
single3 = my_files_as_list[7]

Test = PlotAndStitch(file_path, str(single3), 2, -25, True)
Test.resize_array(400, 1000)
Test.process_files(1, 1, 1E9, 'Zr_filter', 'b')
single4 = my_files_as_list[6]

Test = PlotAndStitch(file_path, str(single4), 2, -25, True)
Test.resize_array(100, 800)
Test.process_files(1, 1, 1E9, 'Zr_filter', 'b')
plt.legend()

# self, filename, bool, color, scale

my_calibration = PlotLineData('Cu_linien/Cuxix.txt', True, 'r', 1E7)
my_calibration.scale_and_plot(1)
my_calibration = PlotLineData('Cu_linien/Cuxx.txt', True, 'c', 1E7)
my_calibration.scale_and_plot(1)
my_calibration = PlotLineData('Cu_linien/Cuxxi.txt', True, 'b', 1E7)
# my_calibration.strong_lines_only()
my_calibration.scale_and_plot(1)
my_calibration = PlotLineData('Cu_linien/Cuxxii.txt', True, 'y', 1E7)
# my_calibration.strong_lines_only()
my_calibration.scale_and_plot(1)
my_calibration = PlotLineData('Cu_linien/Cuxxiii.txt', True, 'm', 1E7)
my_calibration.strong_lines_only()
my_calibration.scale_and_plot(1)
my_calibration = PlotLineData('Cu_linien/Cuxviii.txt', True, 'g', 1E7)
# my_calibration.strong_lines_only()
my_calibration.scale_and_plot(1)
# my_calibration = PlotLineData('Cu_linien/Cuxvii.txt', True, 'g', 1E7)
# my_calibration.strong_lines_only()
# my_calibration.scale_and_plot(1)


filter_file_path = 'per_second/nm/filter'
my_filter_files = get_file_list(filter_file_path)
my_used_filter = my_filter_files[-1]
Filter = PlotAndStitch(filter_file_path, str(my_used_filter), 1, -4, True)
Filter.process_files(0.2E5, 1, 1, 'Zr 298nm', 'y')
my_used_filter = my_filter_files[1]
Filter = PlotAndStitch(filter_file_path, str(my_used_filter), 1, -4, True)
Filter.process_files(2.E4, 1, 1, 'Al 500nm', 'c')
my_used_filter = my_filter_files[-2]
Filter = PlotAndStitch(filter_file_path, str(my_used_filter), 1, -4, True)
Filter.process_files(2.E4, 1, 1, 'TG efficieny', 'r')
plt.legend(bbox_to_anchor=(1., 1.05))

plt.xlim(1600., 50)
plt.ylim(0, 2.5E4)

# plt.legend()
plt.savefig("stitched_XPL_Cu_in_eV_with_lines" + ".png", bbox_inches="tight", dpi=500)
plt.show()
