-- Step 1: predictive_maintenance Database already created in the PgAdmin GUI

-- Step 2: Drop existing tables to prevent conflicts when rerunning the script
DROP TABLE IF EXISTS Profile CASCADE;
DROP TABLE IF EXISTS Efficiency_Power_Signal CASCADE;
DROP TABLE IF EXISTS Vibration_Sensor CASCADE;
DROP TABLE IF EXISTS Cooling_Power CASCADE;
DROP TABLE IF EXISTS Cooling_Efficiency CASCADE;
DROP TABLE IF EXISTS Stable_Efficiency CASCADE;
DROP TABLE IF EXISTS Flow_Sensor CASCADE;
DROP TABLE IF EXISTS Pressure CASCADE;
DROP TABLE IF EXISTS Temperature CASCADE;
DROP TABLE IF EXISTS Sensor CASCADE;
DROP TABLE IF EXISTS Cycle CASCADE;

-- Step 3: Create tables for predictive_maintenance database
---- Table to store unique cycles (each cycle represents a machine operation cycle)
CREATE TABLE Cycle(
    CycleID SERIAL PRIMARY KEY
);

---- Table to store sensor details for those sensors which have more than one table per sensor(e.g Temperature, Pressure etc.)
CREATE TABLE Sensor(
    SensorID SERIAL PRIMARY KEY,
    Sensor_type VARCHAR(25) CHECK (Sensor_type IN ('TS1.txt', 'TS2.txt', 'TS3.txt', 'TS4.txt','PS1.txt','PS2.txt','PS3.txt','PS4.txt','PS5.txt','PS6.txt','FS1.txt', 'FS2.txt'))
);

---- Table to store temperature sensor readings
CREATE TABLE Temperature (
    TemperatureID SERIAL PRIMARY KEY,
    CycleID INT REFERENCES Cycle(CycleID) ON DELETE CASCADE,
    SensorID INT REFERENCES Sensor(SensorID),
    Temperature_data JSONB 
);

---- Table to store pressure sensor readings
CREATE TABLE Pressure (
    PressureID SERIAL PRIMARY KEY,
    CycleID INT REFERENCES Cycle(CycleID) ON DELETE CASCADE,
    SensorID INT REFERENCES Sensor(SensorID),
    Pressure_data JSONB
);

---- Table to store flow sensor readings
CREATE TABLE Flow_Sensor (
    Flow_SensorID SERIAL PRIMARY KEY,
    CycleID INT REFERENCES Cycle(CycleID) ON DELETE CASCADE,
    SensorID INT REFERENCES Sensor(SensorID),
    Flow_Sensor_data JSONB
);

---- Table to store stable efficiency values
CREATE TABLE Stable_Efficiency (
    Stable_EfficiencyID SERIAL PRIMARY KEY,
    CycleID INT REFERENCES Cycle(CycleID) ON DELETE CASCADE,
    Stable_Efficiency_data JSONB
);

---- Table to store cooling efficiency values
CREATE TABLE Cooling_Efficiency (
    Cooling_EfficiencyID SERIAL PRIMARY KEY,
    CycleID INT REFERENCES Cycle(CycleID) ON DELETE CASCADE,
    Cooling_Efficiency_data JSONB
);

---- Table to store cooling power readings
CREATE TABLE Cooling_Power (
    Cooling_PowerID SERIAL PRIMARY KEY,
    CycleID INT REFERENCES Cycle(CycleID) ON DELETE CASCADE,
    Cooling_Power_data JSONB
);

---- Table to store vibration sensor readings
CREATE TABLE Vibration_Sensor (
    Vibration_SensorID SERIAL PRIMARY KEY,
    CycleID INT REFERENCES Cycle(CycleID) ON DELETE CASCADE,
    Vibration_Sensor_data JSONB
);

---- Table to store efficiency power signal readings
CREATE TABLE Efficiency_Power_Signal (
    Efficiency_Power_SignalID SERIAL PRIMARY KEY,
    CycleID INT REFERENCES Cycle(CycleID) ON DELETE CASCADE,
    Efficiency_Power_Signal_data JSONB
);

---- Table to store cycle profile details(machine conditions)
CREATE TABLE Profile(
    ProfileID SERIAL PRIMARY KEY,
    CycleID INT UNIQUE REFERENCES Cycle(CycleID) ON DELETE CASCADE,
    Cooler_Condition INT CHECK (Cooler_condition IN (3,20,100)),
    Valve_Condition INT CHECK (Valve_condition IN (100,90,80,73)),
    Pump_Leakage INT CHECK (Pump_Leakage IN (0,1,2)),
    Accumulator_Condition INT CHECK (Accumulator_Condition IN (130,115,100,90)),
    Stable_Flag BOOLEAN -- 0 for stable, 1 for unstable
);

-- Step 4: Verify that tables have been
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'public'

---- Proceed to loading the data into predictive_maintenance database