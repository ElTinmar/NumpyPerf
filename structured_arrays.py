# NOTE: you probably get different performance scaling once a single array is greater than L3 cache size
# and has to go into proper RAM. Preallocating matters in RAM, less so in cache ?
#
# 4000x4000 float32: 61.0 MB
# 3000x3000 float32: 34.3 MB
# 2000x2000 float32: 15.2 MB
# 1000x1000 float32: 3.8 MB

import timeit
import numpy as np
REPS = 3
N = 1000
SZ = (1800, 1800)
GIGABYTES = np.prod(SZ)*4/(1024**3)


setup_code = f"""
import numpy as np

SZ = {SZ}
array = np.random.uniform(0, 1, SZ).astype(np.float32)
array2 = np.zeros_like(array)
dt = np.dtype([
    ('index', int, (1,)),
    ('timestamp', float, (1,)), 
    ('image', np.float32, SZ),
])
struct = np.array((0, 1.00, array), dtype=dt) # array is copied
zero = np.zeros((1,), dtype=dt)
"""

assignment = """
image = array
"""

regular_copy = """
image = array.copy()
"""

preallocated_copy = """
array2[:] = array
"""

unstruct_array = """
image = np.array(array, copy=False)
"""

struct_array = """
structured_image = np.array((0, 1.00, array), dtype=dt)
"""

struct_asarray = """
structured_image = np.asarray((0, 1.00, array), dtype=dt)
"""

struct_asanyarray = """
structured_image = np.asanyarray((0, 1.00, array), dtype=dt)
"""

field_assignment = """
zero['index'] = 0
zero['timestamp'] = 1.0
zero['image'] = array
"""

tup_assignment = """
zero[0] = (0, 1.0, array)
"""

struct_array_assignment = """
zero[0] = struct
"""

# number=1000 means results in ms
t_assignment = np.mean(timeit.repeat(setup=setup_code, stmt=assignment, repeat=REPS, number=N))
t_regular_copy = np.mean(timeit.repeat(setup=setup_code, stmt=regular_copy, repeat=REPS, number=N))
t_preallocated_copy = np.mean(timeit.repeat(setup=setup_code, stmt=preallocated_copy, repeat=REPS, number=N))
t_unstruct_array = np.mean(timeit.repeat(setup=setup_code, stmt=unstruct_array, repeat=REPS, number=N))
t_struct_array = np.mean(timeit.repeat(setup=setup_code, stmt=struct_array, repeat=REPS, number=N))
t_struct_asarray = np.mean(timeit.repeat(setup=setup_code, stmt=struct_asarray, repeat=REPS, number=N))
t_struct_asanyarray = np.mean(timeit.repeat(setup=setup_code, stmt=struct_asanyarray, repeat=REPS, number=N))
t_field_assignment = np.mean(timeit.repeat(setup=setup_code, stmt=field_assignment, repeat=REPS, number=N))
t_tup_assignment = np.mean(timeit.repeat(setup=setup_code, stmt=tup_assignment, repeat=REPS, number=N))
t_struct_array_assignment = np.mean(timeit.repeat(setup=setup_code, stmt=struct_array_assignment, repeat=REPS, number=N))

print(setup_code)
print(assignment, f'{t_assignment} ms', f'{N*GIGABYTES/t_assignment} GB/s')
print(regular_copy, f'{t_regular_copy} ms', f'{N*GIGABYTES/t_regular_copy} GB/s')
print(preallocated_copy, f'{t_preallocated_copy} ms', f'{N*GIGABYTES/t_preallocated_copy} GB/s')
print(unstruct_array, f'{t_unstruct_array} ms', f'{N*GIGABYTES/t_unstruct_array} GB/s')
print(struct_array, f'{t_struct_array} ms', f'{N*GIGABYTES/t_struct_array} GB/s')
print(struct_asarray, f'{t_struct_asarray} ms', f'{N*GIGABYTES/t_struct_asarray} GB/s')
print(struct_asanyarray, f'{t_struct_asanyarray} ms', f'{N*GIGABYTES/t_struct_asanyarray} GB/s')
print(field_assignment, f'{t_field_assignment} ms', f'{N*GIGABYTES/t_field_assignment} GB/s')
print(tup_assignment, f'{t_tup_assignment} ms', f'{N*GIGABYTES/t_tup_assignment} GB/s')
print(struct_array_assignment, f'{t_struct_array_assignment} ms', f'{N*GIGABYTES/t_struct_array_assignment} GB/s')

exec(setup_code)

# checking modification of array
np.allclose(struct['image'],array) # -> returns True
array[0:100] = 0
np.allclose(struct['image'],array) # -> returns False
