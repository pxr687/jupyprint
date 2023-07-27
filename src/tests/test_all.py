import numpy as _np
import pandas as _pd
import sys
import os

# ensure jupyprint module is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
package_dir = os.path.abspath(os.path.join(current_dir, ".."))+"/jupyprint/"
sys.path.append(package_dir)

from jupyprint import jupyprint, arraytex

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
        jupyprint(_np.array([1, 2, 4]))

        # numpy.array (column vector):
        jupyprint(_np.array([[1], [2], [4]]))

        # numpy.array (matrix):
        jupyprint(_np.array([[1, 2, 4], ['A', 'B', 'C']]))

        # boolean arrays
        jupyprint(_np.array([True, True, False])) 
        jupyprint(_np.array([True, True, False], dtype = object)) 
        jupyprint(_np.array([[True], [True], [False]])) 
        jupyprint(_np.array([[True], [True], [False]], dtype = object)) 

        # array with mixed elements
        jupyprint(_np.array([10, True, "Hello"], dtype = object)) 
        jupyprint(_np.array(['True', 'True', '10', 42, False, 'Hello'], dtype=object))

        # arrays chained with f-string
        x = _np.array([[10, 100, 200], [8, 9, 77]])
        y = _np.array([[1000], [-889], [43]])
        jupyprint(f"{arraytex(x)} * {arraytex(y)} = {arraytex(_np.dot(x, y))}")

        # arrays chained with f-string (with booleans)
        x = _np.array([[10, 100, 200], [8, 9, 77]])
        y = _np.array([[True], [False], [True]])
        jupyprint(f"{arraytex(x)} * {arraytex(y)} = {arraytex(_np.dot(x, y))}")

        # arrays chained with f-string and non-LaTeX strings
        x = _np.array([[10, 100, 200], [8, 9, 77]])
        jupyprint(f"""Hello, let us log this matrix: ${arraytex(x)}$. Here is
                   the logged version: $ln({arraytex(x)}) = {arraytex(_np.log(x).round(2))}$""")

        # pandas.DataFrame:
        jupyprint(_pd.DataFrame({'A': _np.repeat('A', 10)}))

    except Exception as e:
        print(f"An error occurred: {e}")
        # raise error if there was an error
        assert False, "Test failed! See Traceback for details."

if __name__ == '__main__':
    test_all_jupyprints()