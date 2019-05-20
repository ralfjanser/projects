"""This file tries to split one matlab item into a dictionnary"""
import numpy as np


def _convert_matlab_datetime_vector_to_utc(date_vector):
    """Convert matlab datetime format into a UTC format"""
    # f'{val:02}' TODO
    string_time = str(int(date_vector[0])) + "-" + \
        f'{int(date_vector[1]):02}' + "-" + \
        f'{int(date_vector[2]):02}' + "T" + \
        f'{int(date_vector[3]):02}' + ":" + \
        f'{int(date_vector[4]):02}' + ":" + \
        f'{float(date_vector[5]):06.3f}'

    return string_time


def _format_temperature(temp):
    """There are 3 main temparatures, if they are close we want to put them in the same category"""
    # /!\Disclaimer/!\ This is completly related to the NASA battery dataset.
    if temp < 6:
        return 4
    elif temp < 26:
        return 24
    else:
        return 43


def extract_charge_from_item(item):
    dict_item = {}

    dict_item["test_type"] = item[0][0]  # charge impedence discharge
    dict_item["ambiant_temp"] = _format_temperature(item[1][0][0])  # temperature: 4 ~24 ~43
    dict_item["datetime"] = _convert_matlab_datetime_vector_to_utc(item[2][0])

    dict_item["voltage_measured"] = item[3][0][0][0][0]  # Battery terminal voltage (Volts) floats
    dict_item["current_measured"] = item[3][0][0][1][0]  # Battery output current (Amps) floats
    dict_item["temperature_measured"] = item[3][0][0][2][0]  # Battery temperature (degree C) floats
    dict_item["current_charge"] = item[3][0][0][3][0]  # Current measured at charger (Amps) floats
    dict_item["voltage_charge"] = item[3][0][0][4][0]  # Voltage measured at charger (Volts) floats
    # MEH
    dict_item["time"] = item[3][0][0][5][0]  # Time vector for the cycle (secs) floats

    return dict_item


def extract_discharge_from_item(item):
    dict_item = {}

    dict_item["test_type"] = item[0][0]  # charge impedence discharge
    dict_item["ambiant_temp"] = _format_temperature(item[1][0][0])  # temperature: 4 ~24 ~43
    dict_item["datetime"] = _convert_matlab_datetime_vector_to_utc(item[2][0])

    dict_item["voltage_measured"] = item[3][0][0][0][0]  # Battery terminal voltage (Volts) floats
    dict_item["current_measured"] = item[3][0][0][1][0]  # Battery output current (Amps) flaots
    dict_item["temperature_measured"] = item[3][0][0][2][0]  # Battery temperature (degree C) floats
    dict_item["current_charge"] = item[3][0][0][3][0]  # Current measured at charger (Amps) floats
    dict_item["voltage_charge"] = item[3][0][0][4][0]  # Voltage measured at charger (Volts) floats
    # MEH
    dict_item["time"] = item[3][0][0][5][0]  # Time vector for the cycle (secs) floats
    dict_item["capacity"] = item[3][0][0][6][0]  # Battery capacity (Ahr) for discharge till 2.7V float_

    return dict_item


def extract_impedance_from_item(item):
    dict_item = {}

    dict_item["test_type"] = item[0][0]  # charge impedence discharge
    dict_item["ambiant_temp"] = _format_temperature(item[1][0][0])  # temperature: 4 ~24 ~43
    dict_item["datetime"] = _convert_matlab_datetime_vector_to_utc(item[2][0])

    dict_item["sense_current"] = item[3][0][0][0][0]  # Current in sense branch (Amps)| Complexes
    dict_item["sense_current_real"] = np.array([complx.real for complx in dict_item["sense_current"]])
    dict_item["sense_current_imag"] = np.array([complx.imag for complx in dict_item["sense_current"]])

    dict_item["battery_current"] = item[3][0][0][1][0]  # Current in battery branch (Amps)| Complexes
    dict_item["battery_current_real"] = np.array([complx.real for complx in dict_item["battery_current"]])
    dict_item["battery_current_imag"] = np.array([complx.imag for complx in dict_item["battery_current"]])

    dict_item["current_ratio"] = item[3][0][0][2][0]  # Ratio of the above currents| Complexes
    dict_item["current_ratio_real"] = np.array([complx.real for complx in dict_item["current_ratio"]])
    dict_item["current_ratio_imag"] = np.array([complx.imag for complx in dict_item["current_ratio"]])

    # Battery impedance (Ohms) computed from raw data| Complexes
    dict_item["battery_impedance"] = np.array([val[0] for val in item[3][0][0][3]])
    dict_item["battery_impedance_real"] = np.array([complx.real for complx in dict_item["battery_impedance"]])
    dict_item["battery_impedance_imag"] = np.array([complx.imag for complx in dict_item["battery_impedance"]])

    # Calibrated and smoothed battery impedance (Ohms)| Complexes
    dict_item["rectified_impedance"] = np.array([val[0] for val in item[3][0][0][4]])
    dict_item["rectified_impedance_real"] = np.array([complx.real for complx in dict_item["rectified_impedance"]])
    dict_item["rectified_impedance_imag"] = np.array([complx.imag for complx in dict_item["rectified_impedance"]])

    dict_item["re"] = item[3][0][0][5][0][0]  # Estimated electrolyte resistance (Ohms)| float_
    dict_item["rct"] = item[3][0][0][6][0][0]  # Estimated charge transfer resistance (Ohms)| float_

    return dict_item
