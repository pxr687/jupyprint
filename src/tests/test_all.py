import numpy as np
import pandas as pd
import sys
import os

# ensure jupyprint module is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
package_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(package_dir)

from jupyprint.jupyprint import jupyprint

def test_all_jupyprints():
    """Test all intended jupyprint inputs and outputs.
    """
    try:
        # markdown:
        jupyprint("Hello world!")

        # numbers:
        jupyprint(42)
        jupyprint(3.14)
        jupyprint(5 + 3j)  

        # LaTex:
        jupyprint("$ \sum{(y_i - \hat{y})^2} $")

        # numpy.array (row vector):
        jupyprint(np.array([1, 2, 4]))

        # numpy.array (column vector):
        jupyprint(np.array([[1], [2], [4]]))

        # numpy.array (matrix):
        jupyprint(np.array([[1, 2, 4], ['A', 'B', 'C']]))

        # pandas.DataFrame:
        jupyprint(pd.DataFrame({'A': np.repeat('A', 10)}))

    except Exception as e:
        print(f"An error occurred: {e}")
        # raise error if there was an error
        assert False, "Test failed! See Traceback for details."

if __name__ == '__main__':
    test_all_jupyprints()