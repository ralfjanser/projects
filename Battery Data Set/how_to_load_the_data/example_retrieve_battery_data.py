import os
from glob import glob

from extraction.retrieve_battery_data import extract_charge_discharge_impedance


def example_how_to_use_this_module():
    # all_folders_containing_batteries_mat_files = [
    #     "./data/BatteryAgingARC_25_26_27_28_P1/",
    #     "./data/BatteryAgingARC_25-44/",
    #     "./data/BatteryAgingARC_45_46_47_48/",
    #     "./data/BatteryAgingARC_49_50_51_52/",
    #     "./data/BatteryAgingARC_53_54_55_56/",
    #     "./data/BatteryAgingARC-FY08Q4/",
    # ]

    filepaths = [y for x in os.walk("./data/") for y in glob(os.path.join(x[0], '*.mat'))]
    filepaths = sorted(filepaths)

    # TODO warning for for the [:1]
    for filepath in filepaths[:]:
        print(filepath)
        charge_items, discharge_items, impedance_items = extract_charge_discharge_impedance(filepath)
        print(len(charge_items[0]["voltage_measured"]) == len(charge_items[1]["voltage_measured"]))
        print(len(charge_items[0]["voltage_measured"]) == len(discharge_items[0]["voltage_measured"]))
        print(len(charge_items[0]["voltage_measured"]))
        print(len(charge_items[1]["voltage_measured"]))
        print(len(discharge_items[0]["voltage_measured"]))


if __name__ == "__main__":
    example_how_to_use_this_module()
