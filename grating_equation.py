import matplotlib.pyplot as plt
import numpy as np


def load_2_d_array(directory, col_number_y):
    px_axis = np.loadtxt(directory, skiprows=3, usecols=(0,))

    counts = np.loadtxt(directory, skiprows=3, usecols=(col_number_y,))
    return np.transpose(np.stack((px_axis, counts), axis=0))


class ConvertPxToEnergy:
    def __init__(self, input_array_2d, offset_px, input_angle, name):
        self.file_name = name
        self.c = 299792458
        self.planck_constant = 4.135667516 * 1E-15
        self.lambda_values = np.arange(0, 1024, 1.)
        self.px_array = input_array_2d[::, 0]
        self.count_array = input_array_2d[::, 1]
        self.hypertenus = 0.350
        self.correction_value = 0.125
        self.corrected_hyperthenuse = self.prepare_hyperthenuse_chip_correction()
        self.offset = offset_px
        self.offset_angle = input_angle
        self.description = 'offset_angle in degree:_' + str(self.offset_angle) + 'offset 0th. order in px_' + str(
            self.offset)
        self.sign = 1
        self.grating_per_mm = 10000E3
        self.main_processing()
        self.meter_array = self.px_to_meter()
        self.eV_array = np.arange(0, 1024, 1.)

    def main_processing(self):
        self.switch_sign()
        self.off_set_angle_0_order()

    def switch_sign(self):
        # corresponding to -1th or +1th order
        if self.offset_angle < 0:
            self.sign = -1
        return self.sign

    def px_to_meter(self):
        return self.px_array[:] * 26E-6

    def prepare_hyperthenuse_chip_correction(self):
        # the grating equation is only valid for the middle of the chip
        # as the chip is not curved (with the curvature that matches a circle of the hyperthenuse)
        array = np.arange(-512, 512, 1.)
        print(array)
        for counter, value in enumerate(array):
            value = 26E-6 * value
            array[counter] = (self.hypertenus ** 2 - value ** 2) ** 0.5
        return array

    def off_set_angle_0_order(self):
        # offset angle given in px counts from chip middle at 0°
        half_chip_in_degree = np.arctan(26 * 512 * 1E-6 / self.hypertenus) * 180 / np.pi
        print(half_chip_in_degree, 'angle of half chip')
        self.offset = np.arctan(self.offset * 26E-6 / self.hypertenus) * 180 / np.pi
        self.offset_angle = ((1 - self.correction_value) * (self.offset_angle - self.offset - half_chip_in_degree))
        self.offset_angle = self.offset_angle * np.pi / 180
        print('energy L boundary')
        self.grating_single_values(0)
        print('energy R boundary')
        self.grating_single_values(1024 * 26E-6)
        return self.offset_angle

    def grating_single_values(self, value_m):
        value_in_rad = np.arctan(value_m / self.hypertenus)
        value_in_nm = (1 / self.grating_per_mm) * (np.sin(value_in_rad + self.offset_angle))
        print(value_m, 'corresponds to nm', value_in_nm)
        print(value_m, 'corresponds to eV: ', self.convert_nm_to_ev(value_in_nm))

    def convert_nm_to_ev(self, nm_value):
        return self.planck_constant * self.c / nm_value

    def grating_equation(self):
        # grating equation is corrected for a bigger hyperthenuse, leading to a smaller overall angle
        print(self.sign, 'negative or positive order')
        alpha_px = np.arctan(self.meter_array[:] / self.corrected_hyperthenuse) * (1 - self.correction_value)
        # print(alpha_px)
        self.lambda_values[:] = (1 / self.grating_per_mm) * (np.sin(alpha_px[:] + self.offset_angle))

        self.eV_array[:] = self.planck_constant * self.c / self.lambda_values[:]
        return self.lambda_values, self.eV_array

    def plot_it(self):
        plt.figure(3)
        plt.plot(self.lambda_values * 1E9, self.count_array, label=self.file_name)
        plt.xlabel('nm')
        plt.ylabel('counts')
        plt.legend()

    def process(self):
        plt.show()
        self.grating_equation()
        self.plot_it()
        return self.eV_array, self.count_array

    def prepare_header(self):
        # insert header line and change index
        result = np.column_stack((self.lambda_values, self.eV_array, self.count_array))
        header_names = (['nm', 'eV', ' counts'])
        parameter_info = (
            [self.file_name + 'offset angle ' + str(self.offset_angle), 'in rad by:', self.description])
        return np.vstack((parameter_info, header_names, result))

    def save_data(self):
        result = self.prepare_header()
        print('...saving:', self.file_name)
        plt.figure(3)
        plt.savefig(self.file_name[:-9] + '_nm' + ".png", bbox_inches="tight", dpi=500)
        np.savetxt(self.file_name[:-9] + '_calibrated' + ".txt", result, delimiter=' ',
                   header='string', comments='',
                   fmt='%s')


class CalibrationData:

    def __init__(self, path_calibration_data, switch_case, color):
        self.file_path_calibration = path_calibration_data
        self.file_name = str(self.file_path_calibration)[:-4]
        self.nm_axis = np.loadtxt(self.file_path_calibration, skiprows=1, usecols=(1,))
        self.eV_axis = self.convert_nm_to_ev()
        self.sign = switch_case
        self.color = color

    def plot_calibration_data_ev(self, figure_number, count_value):
        plt.figure(figure_number)
        plt.vlines(self.sign * self.eV_axis, ymin=0, ymax=count_value, label=self.file_name, color=self.color)
        plt.xlabel('eV')
        plt.ylabel('counts')
        plt.legend()

    def plot_calibration_data_nm(self, figure_number, count_value):
        plt.figure(figure_number)
        plt.vlines(self.sign * self.nm_axis, ymin=0, ymax=count_value, label=self.file_name, linewidth=0.2,
                   color=self.color)
        plt.xlabel('nm')
        plt.ylabel('counts')
        # plt.legend()

    @staticmethod
    def convert_ev_to_nm(value):
        c = 299792458
        planck_constant = 4.135667516 * 1E-15
        print(value, (c * planck_constant) * 1E9 / value)
        return (c * planck_constant) * 1E9 / value

    def energy_edges(self, count_value):
        # fixed absorption edges in eV
        oxygen_ev = 542.3
        carbon_ev = 284
        nitrogene_ev = 410
        aluminium_ev = 1560

        plt.vlines(self.sign * self.convert_ev_to_nm(oxygen_ev), ymin=0, ymax=count_value, label='O-edge', color='b',
                   linewidth=0.5)
        plt.vlines(self.sign * self.convert_ev_to_nm(carbon_ev), ymin=0, ymax=count_value, label='C-edge', color='r',
                   linewidth=0.5)
        plt.vlines(self.sign * self.convert_ev_to_nm(nitrogene_ev), ymin=0, ymax=count_value, label='N-edge', color='g',
                   linewidth=0.5)
        plt.vlines(self.sign * self.convert_ev_to_nm(aluminium_ev), ymin=0, ymax=count_value, label='Al-edge_Kalpha',
                   color='c', linewidth=0.5)
        plt.vlines(self.sign * 4.38, ymin=0, ymax=count_value, label='C', color='c', linewidth=0.5)
        plt.vlines(self.sign * 12.15, ymin=0, ymax=count_value, label='Si3N4', color='c', linewidth=0.5)
        # plt.legend()

    def convert_nm_to_ev(self):
        c = 299792458
        planck_constant = 4.135667516 * 1E-15
        ev = planck_constant * c / (self.nm_axis[:] * 1E-9)
        return ev


class PlotFilterData:
    def __init__(self, filename, plus_or_minus, color, scale):
        self.path = filename
        self.name = str(self.path)[:-4]
        self.color = color
        self.sign = plus_or_minus
        self.scale = scale
        self.nm_axis = np.loadtxt(self.path, skiprows=2, usecols=(0,))
        self.count_axis = np.loadtxt(self.path, skiprows=2, usecols=(1,))

    def scale_and_plot(self, figure_number):
        plt.figure(figure_number)
        plt.plot(self.sign * self.nm_axis, self.count_axis[:] * self.scale, label=str(self.name))
        plt.legend()


file_path = 'per_second/px/'
file_name = '20201021_m4_degreeper_secondprocessed.txt'
data_input = load_2_d_array(file_path + file_name, 1)
file_description = file_name[:-4]

image_processing = ConvertPxToEnergy(data_input, -132, -4.25, file_description)
sign = image_processing.switch_sign()
my_converted_array_eV, my_counts = image_processing.process()
image_processing.save_data()

# plot overlay of Filter or line data
my_filter = PlotFilterData('Zr_filter/TG.txt', sign, 'r', 50E3)
my_filter.scale_and_plot(3)
my_filter2 = PlotFilterData('Zr_Filter/Zr_filter.txt', sign, 'y', 9E3)
my_filter2.scale_and_plot(3)
my_calibration = CalibrationData('Cu_linien/Cuxix.txt', sign, 'r')
# scaling for plot
plt.xlim(sign * 0.4, sign * 8)
plt.ylim(0, 1.0E4)
