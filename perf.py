import timeit
import numpy as np

N_GB = 2

setup_code = f"""
import numpy as np
from multiprocessing import RawArray

N_GB = {N_GB}
numbytes = N_GB * 1024 * 1024 * 1024
a = np.ones(numbytes, 'B')
b = np.ones_like(a)
data = RawArray('B', numbytes) 
buffer = np.frombuffer(
    data, 
    dtype = 'B', 
    count = numbytes,
    offset = 0
)
"""

copy = """
a.copy()
"""

copyto = """
np.copyto(a, b)
"""

copy_to_rawarray = """
np.copyto(a, buffer)
"""

copy_to_rawarray2 = """
memoryview(data).cast('B')[:] = a
"""

N = 10
NREP = 3

mem_freq_hz = 2666*1e6
num_channels = 2
theoretical_mem_bandwidth = mem_freq_hz * 64//8 * num_channels 

print(f'theoretical bandwidth: {theoretical_mem_bandwidth * 1/(1024**3)} GB/s')

t0 = 1/N * np.mean(timeit.repeat(setup=setup_code, stmt=copy, repeat=NREP, number=N))
t1 = 1/N * np.mean(timeit.repeat(setup=setup_code, stmt=copyto, repeat=NREP, number=N))
t2 = 1/N * np.mean(timeit.repeat(setup=setup_code, stmt=copy_to_rawarray, repeat=NREP, number=N))
t3 = 1/N * np.mean(timeit.repeat(setup=setup_code, stmt=copy_to_rawarray2, repeat=NREP, number=N))

print(setup_code)
print(copy, f'time: {t0}, speed: {N_GB/t0} GB/s, read + write')
print(copyto,  f'time: {t1}, speed: {N_GB/t1} GB/s, read + write')
print(copy_to_rawarray,  f'time: {t2}, speed: {N_GB/t2} GB/s, read + write')
print(copy_to_rawarray2,  f'time: {t3}, speed: {N_GB/t3} GB/s, read + write')
