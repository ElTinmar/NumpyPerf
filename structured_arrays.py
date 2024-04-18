import timeit

setup_code = """
import numpy as np

SZ = (1800, 1800)
array = np.random.uniform(0, 1, SZ).astype(np.float32)
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
print(assignment, timeit.repeat(setup=setup_code, stmt=assignment, repeat=3, number=1000))
print(regular_copy, timeit.repeat(setup=setup_code, stmt=regular_copy, repeat=3, number=1000))
print(unstruct_array, timeit.repeat(setup=setup_code, stmt=unstruct_array, repeat=3, number=1000))
print(struct_array, timeit.repeat(setup=setup_code, stmt=struct_array, repeat=3, number=1000))
print(struct_asarray, timeit.repeat(setup=setup_code, stmt=struct_asarray, repeat=3, number=1000))
print(struct_asanyarray, timeit.repeat(setup=setup_code, stmt=struct_asanyarray, repeat=3, number=1000))
print(field_assignment, timeit.repeat(setup=setup_code, stmt=field_assignment, repeat=3, number=1000))
print(tup_assignment, timeit.repeat(setup=setup_code, stmt=tup_assignment, repeat=3, number=1000))
print(struct_array_assignment, timeit.repeat(setup=setup_code, stmt=struct_array_assignment, repeat=3, number=1000))


exec(setup_code)

# checking modification of array
np.allclose(struct['image'],array) # -> returns True
array[0:100] = 0
np.allclose(struct['image'],array) # -> returns False
