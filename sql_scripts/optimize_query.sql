-- Step 9: Adjust PostgreSQL memory settings for better query performance

---- Show current memory allocation for work_mem
SHOW work_mem; 

---- Increase work_mem to 512MB to allow larger operations in memory instead of disk
SET work_mem = '512MB'; 

---- Enable parallel processing to speed up query execution
SET max_parallel_workers_per_gather = 4;  
SET parallel_tuple_cost = 0;              
SET parallel_setup_cost = 0;              