import timeit
import numpy as np

REPS = 3
N = 1000
SZ = (3000, 3000)
GIGABYTES = np.prod(SZ)*4/(1024**3)

setup_code = f"""
import numpy as np

SZ = {SZ}
float32_array = np.random.uniform(0, 1, SZ).astype(np.float32)
uint8_array = np.random.randint(0, 255, SZ, dtype = np.uint8)
"""

inplace_32_to_8 = """
float32_array = float32_array.astype(np.uint8)
""" 

not_inplace_32_to_8 = """
array = float32_array.astype(np.uint8)
"""

inplace_8_to_32 = """
uint8_array = uint8_array.astype(np.float32)
""" 

not_inplace_8_to_32 = """
array = uint8_array.astype(np.float32)
"""

t_inplace_32_to_8 = np.mean(timeit.repeat(setup=setup_code, stmt=inplace_32_to_8, repeat=REPS, number=N))
t_not_inplace_32_to_8 = np.mean(timeit.repeat(setup=setup_code, stmt=not_inplace_32_to_8, repeat=REPS, number=N))
t_inplace_8_to_32 = np.mean(timeit.repeat(setup=setup_code, stmt=inplace_8_to_32, repeat=REPS, number=N))
t_not_inplace_8_to_32= np.mean(timeit.repeat(setup=setup_code, stmt=not_inplace_8_to_32, repeat=REPS, number=N))


print(setup_code)
print(inplace_32_to_8, f'{t_inplace_32_to_8} ms', f'{N*GIGABYTES/t_inplace_32_to_8} GB/s')
print(not_inplace_32_to_8, f'{t_not_inplace_32_to_8} ms', f'{N*GIGABYTES/t_not_inplace_32_to_8} GB/s')
print(inplace_8_to_32, f'{t_inplace_8_to_32} ms', f'{N*GIGABYTES/t_inplace_8_to_32} GB/s')
print(not_inplace_8_to_32, f'{t_not_inplace_8_to_32} ms', f'{N*GIGABYTES/t_not_inplace_8_to_32} GB/s')