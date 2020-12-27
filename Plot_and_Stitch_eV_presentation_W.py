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
        eV = planck_constant * c / (array[::] * 1E-9)
        self.xlabel = 'eV'
        return eV

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
        # plt.legend()

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
    def __init__(self, filename, logic, color, scale):
        self.path = filename
        self.name = str(self.path)[:-4]
        self.color = color
        self.sign = logic
        self.scale = scale
        self.x_label = 'nm'
        self.nm_axis = np.loadtxt(self.path, skiprows=1, usecols=(1,))
        self.intensity = np.loadtxt(self.path, skiprows=1, usecols=(2,))
        print(self.nm_axis, self.path, len(self.nm_axis))
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


file_path = 'per_second/nm/all/W_target'
my_files_as_list = get_file_list(file_path)
print(my_files_as_list)
selection = my_files_as_list[4]

print('selection_files:', selection)

# class PlotAndStitch wants: file_path, file_list, column_number x, //
# column_numbery, number_of_skipped_letters_for_string, bool (True = eV, False = nm)
Test = PlotAndStitch(file_path, str(selection), 2, -25, True)
Test.resize_array(3, 1000)
Test.process_files(1, 1, 1E9, 'Zr_filter', 'b')
single2 = my_files_as_list[1]
print(single2, 'single 2')
Test = PlotAndStitch(file_path, str(single2), 2, -25, True)
Test.resize_array(50, 800)
Test.process_files(1, 1, 1E9, 'Al_filter', 'b')
single2 = my_files_as_list[2]
print(single2, 'single 2.2.')
Test = PlotAndStitch(file_path, str(single2), 2, -25, True)
Test.resize_array(40, 1000)
Test.process_files(1, 1, 1E9, 'Zr_filter', 'b')
single3 = my_files_as_list[7]
print(single3)
Test = PlotAndStitch(file_path, str(single3), 2, -25, True)
Test.resize_array(20, 1000)
Test.process_files(1, 1, 1E9, 'Al_filter', 'm')
single4 = my_files_as_list[9]
print(single3)
Test = PlotAndStitch(file_path, str(single4), 2, -25, True)
Test.resize_array(5, 1000)
Test.process_files(1, 1, 1E9, 'Zr_filter', 'm')
plt.legend()

filter_file_path = 'per_second/nm/filter'
my_filter_files = get_file_list(filter_file_path)
my_used_filter = my_filter_files[-1]
Filter = PlotAndStitch(filter_file_path, str(my_used_filter), 1, -4, True)
Filter.process_files(0.15E5, 1, 1, 'Zr 298nm', 'y')
my_used_filter = my_filter_files[0]
Filter = PlotAndStitch(filter_file_path, str(my_used_filter), 1, -4, True)
Filter.process_files(1.5E4, 1, 1, 'Al 200nm', 'c')
my_used_filter = my_filter_files[-2]
Filter = PlotAndStitch(filter_file_path, str(my_used_filter), 1, -4, True)
Filter.process_files(1.5E4, 1, 1, 'TG efficieny', 'r')
plt.legend(bbox_to_anchor=(1.05, 1))

plt.xlim(1650., 50)
plt.ylim(0, 1.7E4)

plt.savefig("stitched_XPL_W_in_eV" + ".png", bbox_inches="tight", dpi=500)
plt.show()
