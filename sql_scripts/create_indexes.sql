-- Step 5: Create indexes to optimize search performance

---- Index foreign keys for faster joins
-- Drop the index if it already exists
DROP INDEX IF EXISTS idx_temperature_cycle;
CREATE INDEX idx_temperature_cycle ON Temperature (CycleID);

DROP INDEX IF EXISTS idx_pressure_cycle;
CREATE INDEX idx_pressure_cycle ON Pressure (CycleID);

DROP INDEX IF EXISTS idx_flow_sensor_cycle;
CREATE INDEX idx_flow_sensor_cycle ON Flow_Sensor (CycleID);

DROP INDEX IF EXISTS idx_stable_efficiency_cycle;
CREATE INDEX idx_stable_efficiency_cycle ON Stable_Efficiency (CycleID);

DROP INDEX IF EXISTS idx_cooling_efficiency_cycle;
CREATE INDEX idx_cooling_efficiency_cycle ON Cooling_Efficiency (CycleID);

DROP INDEX IF EXISTS idx_cooling_power_cycle;
CREATE INDEX idx_cooling_power_cycle ON Cooling_Power (CycleID);

DROP INDEX IF EXISTS idx_vibration_sensor_cycle;
CREATE INDEX idx_vibration_sensor_cycle ON Vibration_Sensor (CycleID);

DROP INDEX IF EXISTS idx_efficiency_power_signal_cycle;
CREATE INDEX idx_efficiency_power_signal_cycle ON Efficiency_Power_Signal (CycleID);

DROP INDEX IF EXISTS idx_profile_cycle;
CREATE INDEX idx_profile_cycle ON Profile (CycleID);

---- Index JSONB fields for better query performance on sensor readings
DROP INDEX IF EXISTS idx_temperature_data;
CREATE INDEX idx_temperature_data ON Temperature USING gin (Temperature_data);

DROP INDEX IF EXISTS idx_pressure_data;
CREATE INDEX idx_pressure_data ON Pressure USING gin (Pressure_data);

DROP INDEX IF EXISTS idx_flow_sensor_data;
CREATE INDEX idx_flow_sensor_data ON Flow_Sensor USING gin (Flow_Sensor_data);

DROP INDEX IF EXISTS idx_stable_efficiency_data;
CREATE INDEX idx_stable_efficiency_data ON Stable_Efficiency USING gin (Stable_Efficiency_data);

DROP INDEX IF EXISTS idx_cooling_efficiency_data;
CREATE INDEX idx_cooling_efficiency_data ON Cooling_Efficiency USING gin (Cooling_Efficiency_data);

DROP INDEX IF EXISTS idx_cooling_power_data;
CREATE INDEX idx_cooling_power_data ON Cooling_Power USING gin (Cooling_Power_data);

DROP INDEX IF EXISTS idx_vibration_sensor_data;
CREATE INDEX idx_vibration_sensor_data ON Vibration_Sensor USING gin (Vibration_Sensor_data);

DROP INDEX IF EXISTS idx_efficiency_power_signal_data;
CREATE INDEX idx_efficiency_power_signal_data ON Efficiency_Power_Signal USING gin (Efficiency_Power_Signal_data);

---- Index conditions for optimized filtering
DROP INDEX IF EXISTS idx_profile_stable_flag;
CREATE INDEX idx_profile_stable_flag ON Profile (Stable_Flag);


-- Step 6: Verify or check the list of indexes created
SELECT 
    indexname, 
    tablename, 
    indexdef 
FROM pg_indexes 
WHERE schemaname = 'public'
ORDER BY tablename;