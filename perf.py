import timeit
import numpy as np

setup_code = """
import numpy as np
N_GB = 2
a = np.ones(N_GB * 1024 * 1024 * 1024, 'ubyte')
b = np.ones_like(a)
"""

copy ="""
a.copy()
"""

copyto = """
np.copyto(a, b)
"""

N = 10
NREP = 3

mem_freq_hz = 2666*1e6
num_channels = 2
theoretical_mem_bandwidth = mem_freq_hz * 64//8 * num_channels 

print(f'theoretical bandwidth: {theoretical_mem_bandwidth * 1/(1024**3)} GB/s')

t0 = 1/N * np.mean(timeit.repeat(setup=setup_code, stmt=copy, repeat=NREP, number=N))
t1 = 1/N * np.mean(timeit.repeat(setup=setup_code, stmt=copyto, repeat=NREP, number=N))

print(copy, f'time: {t0}, speed: {2/t0} GB/s, read + write')
print(copyto,  f'time: {t1}, speed: {2/t1} GB/s, read + write')

