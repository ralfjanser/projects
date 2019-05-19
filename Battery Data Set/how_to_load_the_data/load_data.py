import pandas as pd
import numpy as np
import os
import random
from extraction.retrieve_battery_data import extract_charge_discharge_impedance


def build_files(folder_to_exclude, src_dir=os.getcwd()):
    data_folder = os.path.join(src_dir, 'data')

    dict_files = {}
    for directory in os.listdir(data_folder):
        fullpath_dir = os.path.join(data_folder, directory)
        if os.path.isdir(fullpath_dir) and directory not in folder_to_exclude:
            dict_files[directory] = [os.path.join(fullpath_dir, file) for file
                                     in os.listdir(fullpath_dir) if
                                     file.endswith('.mat')]

    return dict_files


def extract_charge_items(charge, battery_nb, charge_nb):
    df_charge = pd.DataFrame(
        columns=['battery_nb', 'datetime', 'charge_nb',
                 'voltage_measured', 'current_measured',
                 'temperature_measured', 'current_charge',
                 'voltage_charge', 'ambiant_temp']
    )
    df_charge['voltage_measured'] = charge['voltage_measured']
    df_charge['current_measured'] = charge['current_measured']
    df_charge['temperature_measured'] = charge[
        'temperature_measured']
    df_charge['current_charge'] = charge['current_charge']
    df_charge['voltage_charge'] = charge['voltage_charge']
    df_charge['ambiant_temp'] = charge['ambiant_temp']
    df_charge['battery_nb'] = [battery_nb] * len(
        charge['voltage_measured'])
    df_charge['charge_nb'] = [charge_nb] * len(
        charge['voltage_measured'])
    df_charge['datetime'] = pd.Timestamp(
        charge['datetime']) + pd.to_timedelta(charge['time'],
                                              unit='s')

    return df_charge


def extract_discharge_items(discharge, battery_nb, discharge_nb):
    df_discharge = pd.DataFrame(
        columns=['battery_nb', 'datetime', 'discharge_nb',
                 'voltage_measured', 'current_measured',
                 'temperature_measured', 'current_charge',
                 'voltage_charge', 'capacity', 'ambiant_temp']
    )
    df_discharge['voltage_measured'] = discharge[
        'voltage_measured']
    df_discharge['current_measured'] = discharge[
        'current_measured']
    df_discharge['temperature_measured'] = discharge[
        'temperature_measured']
    df_discharge['current_charge'] = discharge['current_charge']
    df_discharge['voltage_charge'] = discharge['voltage_charge']
    df_discharge['capacity'] = discharge['capacity'][0] if len(
        discharge['capacity']) > 0 else [np.NaN] * len(
        discharge['voltage_measured'])
    df_discharge['ambiant_temp'] = discharge['ambiant_temp']
    df_discharge['battery_nb'] = [battery_nb] * len(
        discharge['voltage_measured'])
    df_discharge['discharge_nb'] = [discharge_nb] * len(
        discharge['voltage_measured'])
    df_discharge['datetime'] = pd.Timestamp(
        discharge['datetime']) + pd.to_timedelta(
        discharge['time'], unit='s')

    return df_discharge


def mat_to_pandas(files, bat_to_keep):
    print("Loading mat files ....")
    print("Please, wait a bit.")

    df = pd.DataFrame()
    for folder_name, filepaths in files.items():
        for filepath in filepaths:
            battery_nb = int(
                os.path.splitext(os.path.basename(filepath))[0].replace('B', '')
            )
            charge_nb = 1
            discharge_nb = 1

            if battery_nb in bat_to_keep:
                charge_items, discharge_items, impedance_items = extract_charge_discharge_impedance(
                    filepath)

                for charge in charge_items:
                    df_charge = extract_charge_items(charge, battery_nb, charge_nb)
                    df = df.append(df_charge, ignore_index=True, sort=False)

                    charge_nb = charge_nb + 1

                for discharge in discharge_items:
                    df_discharge = extract_discharge_items(discharge, battery_nb, discharge_nb)
                    df = df.append(df_discharge, ignore_index=True, sort=False)

                    discharge_nb = discharge_nb + 1

    print("Datas loaded !")

    return df


def get_splitted_datas(df, training_size=4, validation_size=1, test_size=1):
    # Check if args are numbers
    try:
        training_size = int(training_size)
        validation_size = int(validation_size)
        test_size = int(test_size)
    except:  # noqa: E720
        print(
            "Please, enter int numbers for training_size, validation_size and test_size")
        return

    # Check if sum of args is <= battery_nb
    battery_nb = df['battery_nb'].unique().tolist()
    if training_size + validation_size + test_size > len(battery_nb):
        print(
            "Ooops, size of training_size+validation_size+test_size > numbers of battery available.")
        return

    # Shuffle the list of battery_nb
    battery_nb = random.sample(battery_nb, len(battery_nb))

    # Get the batteries nb and return DFs
    training_bat = battery_nb[0:training_size]
    validation_bat = battery_nb[training_size:training_size + validation_size]
    test_bat = battery_nb[training_size + validation_size: training_size + validation_size + test_size]

    return df[df['battery_nb'].isin(training_bat)],\
        df[df['battery_nb'].isin(validation_bat)], \
        df[df['battery_nb'].isin(test_bat)]


def set_labels_Y(df):
    df_res = pd.DataFrame()
    for batt_nb in df['battery_nb'].unique():
        df_batt = df[
            df['battery_nb'] == batt_nb
        ]

        len_df = len(df_batt)

        # Sort the DF by time
        df_batt.sort_values(by=['datetime', 'charge_nb', 'discharge_nb'],
                            inplace=True)

        # Create labels array
        good_array = [1] * (len_df // 3)  # 1 = Good quality
        middle_array = [2] * (len_df // 3)  # 1 = Middle quality
        bad_array = [3] * (len_df // 3)  # 1 = Bad quality

        missing_datas_nb = len_df - ((len_df // 3) * 3)
        good_array = good_array + ([1] * missing_datas_nb)

        # Insert labels to df
        df_batt['quality'] = good_array + middle_array + bad_array

        df_res = pd.concat([df_res, df_batt])
    return df_res


def get_datas(
        folder_to_exclude=['BatteryAgingARC_25_26_27_28_P1'],
        batteries_to_keep=[25, 26, 27, 28, 33, 34],
        src_dir=os.getcwd(),
        training_size=4,
        validation_size=1,
        test_size=1
):
    dict_files = build_files(
        folder_to_exclude=folder_to_exclude,
        src_dir=src_dir
    )
    df = mat_to_pandas(files=dict_files, bat_to_keep=batteries_to_keep)
    df_training, df_validation, df_test = get_splitted_datas(
        df,
        training_size=training_size,
        validation_size=validation_size,
        test_size=test_size
    )

    return set_labels_Y(df_training), set_labels_Y(df_validation), set_labels_Y(df_test)


def example():
    df_train, df_validation, df_test = get_datas()


if __name__ == '__main__':
    example()
