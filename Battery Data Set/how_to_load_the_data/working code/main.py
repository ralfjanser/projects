import pandas as pd
import numpy as np
import os
import scipy.io

import random
import help_me




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


#----------------------------------------------------------------------------
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

#----------------------------------------------------------------------------


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()


#----------------------------------------------------------------------------




def mat_to_pandas(file):
    battery_nb =  file.replace('B','')
    battery_nb = battery_nb.replace('.mat','')
    battery_nb = int(battery_nb)
    
    print('working file: ' + file)
    df = pd.DataFrame()
    
    filepath = data_files+'/'+file
    
    charge_items, discharge_items, impedance_items = extract_charge_discharge_impedance(filepath)
    
    
    charge_nb = 1
    discharge_nb = 1
    print('now charge')
    
    for charge in charge_items:
        df_charge = extract_charge_items(charge, battery_nb, charge_nb)
        df = df.append(df_charge, ignore_index=True, sort=False)
        charge_nb = charge_nb + 1
    
    print('now discharge')
    
    for discharge in discharge_items:
        df_discharge = extract_discharge_items(discharge, battery_nb, discharge_nb)
        # why doesn't discharge_nb appear in the excel file? it works in here
        df = df.append(df_discharge, ignore_index=True, sort=False)
        discharge_nb = discharge_nb + 1
        
    datei_name= file + 'work' +'.xlsx'
    print('writing excel file: '+ datei_name)
    df.to_excel(datei_name)
    

#********************************************

data_files= 'data_all'
files=os.listdir(data_files)

l = len(files)


printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = l)
i=0

for file in files:
    mat_to_pandas(file)
    printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    i = i +1


