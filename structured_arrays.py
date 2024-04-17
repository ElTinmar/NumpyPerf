import timeit

setup_code = """
import numpy as np
from numpy.lib import recfunctions as rfn

SZ = (1800, 1800)
array = np.random.uniform(0, 1, SZ).astype(np.float32)
dt = np.dtype([
    ('index', int, (1,)),
    ('timestamp', float, (1,)), 
    ('image', np.float32, SZ),
])
struct = np.array((0, 1.00, array), dtype=dt)
unstruct = rfn.structured_to_unstructured(struct).astype(np.float32)
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

unstruct_to_struct = """
structured_image2 = rfn.unstructured_to_structured(unstruct, dtype=dt)
"""


timeit.repeat(setup=setup_code, stmt=regular_copy, repeat=3, number=1000)
timeit.repeat(setup=setup_code, stmt=unstruct_array, repeat=3, number=1000)
timeit.repeat(setup=setup_code, stmt=struct_array, repeat=3, number=1000)
timeit.repeat(setup=setup_code, stmt=unstruct_to_struct, repeat=3, number=1000)