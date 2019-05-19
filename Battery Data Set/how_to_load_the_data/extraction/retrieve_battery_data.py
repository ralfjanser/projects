import scipy.io
import os

from extraction.extract_item_into_dict import extract_impedance_from_item
from extraction.extract_item_into_dict import extract_charge_from_item
from extraction.extract_item_into_dict import extract_discharge_from_item


def _filter_mat(mat, test_type):
    """Keep only one type (e.g. impedance) from the matlab file"""
    return [x for x in mat if x[0][0] == test_type]


def _split_mat(mat):
    """Split matlab file into charge/discharge/impedance"""
    raw_charge_items = _filter_mat(mat, "charge")
    raw_discharge_items = _filter_mat(mat, "discharge")
    raw_impedance_items = _filter_mat(mat, "impedance")

    return raw_charge_items, raw_discharge_items, raw_impedance_items


def _load_mat_file(filepath):
    """Load the matlab file"""
    filename = os.path.split(filepath)[-1].split(".")[0]
    raw_mat = scipy.io.loadmat(filepath)
    mat = raw_mat[filename][0][0][0][0]

    return mat


def extract_charge_discharge_impedance(filepath):
    mat = _load_mat_file(filepath)

    raw_charge_items, raw_discharge_items, raw_impedance_items = _split_mat(mat)

    charge_items = [extract_charge_from_item(raw_charge) for raw_charge in raw_charge_items]
    discharge_items = [extract_discharge_from_item(raw_discharge) for raw_discharge in raw_discharge_items]
    impedance_items = [extract_impedance_from_item(raw_impedance) for raw_impedance in raw_impedance_items]

    return charge_items, discharge_items, impedance_items
