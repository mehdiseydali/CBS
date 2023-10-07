import time
import psutil

# Function to get current memory usage
def get_memory_usage():
    process = psutil.Process()
    mem_info = process.memory_info()
    return mem_info.rss  # Resident Set Size (memory usage)

# Function to measure execution time and memory consumption of another function
def measure_execution(func):
    def wrapper(*args, **kwargs):
        # Record start time
        start_time = time.time()
        
        # Measure memory usage before execution
        start_memory = get_memory_usage()
        
        # Execute the wrapped function
        result = func(*args, **kwargs)
        
        # Measure memory usage after execution
        end_memory = get_memory_usage()
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Calculate memory consumption
        memory_consumption_bytes = end_memory - start_memory
        memory_consumption_megabytes = memory_consumption_bytes / (1024 * 1024)  # Convert to megabytes
        
        print(f"Function '{func.__name__}' executed in {execution_time:.2f} seconds.")
        print(f"Memory consumption during execution: {memory_consumption_megabytes:.2f} MB")
        
        return result  # Return the result of the wrapped function
    
    return wrapper
