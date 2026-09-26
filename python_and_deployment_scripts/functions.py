import pandas as pd
import numpy as np


# Aggregating the large volumes of data for easier handling in traditional ML processes
def summary_stat_of_features(X):
    df_summary = X.map(
        lambda row: (np.mean(row), np.std(row), np.max(row), np.min(row))
        if isinstance(row, list) else (row, 0, row, row))
    return df_summary


# dropping redundant features
def removing_redundant_features_columns(X):
    columns = ['pressure_readings_2_min','pressure_readings_3_min','flow_sensor_readings_1_min','stable_efficiency_readings_1_min']
    X = X.drop(columns=columns)
    return X    


# This is for splitting the columns conatining the aggregate values into 4 columns and naming them
def split_and_rename_X_summary(X):
    columns = X.columns
    df_summary = X.copy()
    for column_name in df_summary.columns:
        df_summary[[f'{column_name}_mean',f'{column_name}_std',f'{column_name}_max',f'{column_name}_min']] = df_summary[column_name].apply(pd.Series)
    df_summary = df_summary.drop(columns = columns)
    return df_summary


# creating features that affect cooling conditions
def create_cooler_conditions_features(X):
    X['Overall Temp Change'] = X['temperature_readings_1_mean']-X['temperature_readings_4_mean']
    X['Intermediate Temp Change'] = X['temperature_readings_2_mean']-X['temperature_readings_3_mean']
    X['Cooling Effectiveness Ratio'] = ((X['temperature_readings_1_mean']-X['temperature_readings_4_mean'])/X['temperature_readings_1_mean'])


# creating features that affect pump leakage conditions
def create_pump_leakage_features(X):
    total_pressure_drop = ((X['pressure_readings_1_mean']-X['pressure_readings_2_mean']) + (X['pressure_readings_2_mean']-X['pressure_readings_3_mean']) +
                            (X['pressure_readings_3_mean']-X['pressure_readings_4_mean']) + (X['pressure_readings_4_mean']-X['pressure_readings_5_mean']) +
                            (X['pressure_readings_5_mean']-X['pressure_readings_6_mean']))
    X['Leakage Ratio_1'] =  ((X['pressure_readings_1_mean']-X['pressure_readings_2_mean'])/total_pressure_drop)
    X['Leakage Ratio_2'] =  ((X['pressure_readings_2_mean']-X['pressure_readings_3_mean'])/total_pressure_drop)
    X['Leakage Ratio_3'] =  ((X['pressure_readings_3_mean']-X['pressure_readings_4_mean'])/total_pressure_drop)
    X['Leakage Ratio_4'] =  ((X['pressure_readings_4_mean']-X['pressure_readings_5_mean'])/total_pressure_drop)
    X['Leakage Ratio_5'] =  ((X['pressure_readings_5_mean']-X['pressure_readings_6_mean'])/total_pressure_drop)
    X['Pessure Efficiency Index'] = ((X['pressure_readings_1_mean']-X['pressure_readings_6_mean'])/X['pressure_readings_1_mean'])


# creating features that affect accumulator condition
def create_accumulator_condition_features(X):
    X['Pressure drop across Acc'] = (X['pressure_readings_5_mean']-X['pressure_readings_6_mean'])
    X['Pressure ratio across Acc'] = (X['pressure_readings_5_mean']/X['pressure_readings_6_mean'])


# convert the numpy arrays after PCA to pandas dataframe for easy modelling
def convert_numpy_to_pandas(X):
    pca_column_names = [f"PC{i+1}" for i in range(12)]
    df_pca = pd.DataFrame(X[:, :12], columns=pca_column_names)
    return df_pca
 
