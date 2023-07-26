from IPython.display import Markdown, display
import pandas as pd
import numpy as np

# ==============================================================================
# USER FACING FUNCTIONS

def jupyprint(x):
    """
    Function to print markdown/LaTeX, and render nice looking numpy arrays and
    pandas dataframes, within Jupyter notebooks.

    Examples
    ==================

    Markdown:
    jupyprint("Hello world!")

    Numbers:
    jupyprint(42)
    jupyprint(3.14)
    jupyprint(5 + 3j)

    LaTex:
    jupyprint("$ \sum{(y_i - \hat{y})^2} $")

    numpy.array (row vector):
    jupyprint(np.array([1, 2, 4]))

    numpy.array (column vector):
    jupyprint(np.array([[1], [2], [4]]))

    numpy.array (matrix):
    jupyprint(np.array([[1, 2, 4], ['A', 'B', 'C']]))

    pandas.DataFrame:
    jupyprint(pd.DataFrame({'A': np.repeat('A', 10)}))

    """

    # if input is a string or number, display  as markdown/LaTeX
    if (isinstance(x, str)) | (isinstance(x, (int, float, complex))):
        display(Markdown(str(x)))

    # if input is a numpy array convert to markdown/LaTeX, then display
    elif (isinstance(x, np.ndarray)):
        display(Markdown("$"+_np2latex(x)+"$"))

    # if the input is a pandas DataFrame, display it nicely rendered
    elif (isinstance(x, pd.core.frame.DataFrame)):
        display(x)

# ==============================================================================
# HIDDEN FUNCTIONS

# np2latex is adapted from: 
# https://github.com/madrury/np2latex/blob/master/np2latex/np2latex.py

def _np2latex(arr):
    """Return latex markdown representing a numpy array.

    Parameters
    ----------
    arr: array, shape (n, p), (n,) or (1, n)
        A numpy array.

    Returns
    -------
    latex: string
        A latex string.
    """
    # determine if the input is a matrix (two dimensions, more than one column),
    # display as a matrix
    if (len(arr.shape) == 2):
        if (arr.shape[1] > 1):
            return _make_matrix(arr)
    
    # if the input is a column vector (two dimensions, 1 column), display as a
    # column vector
    if (len(arr.shape) == 2):
        if (arr.shape[1] == 1):
            return _make_matrix(arr.reshape(-1, 1))

    # if the input is a row vector (1 row, no columns), display as a row vector
    elif len(arr.shape) == 1:
        return _make_matrix(arr.reshape(1, -1), end_str="")
    
    # warn user array is too high-dimensional, if this is the case
    else:
        raise ValueError("Array must be 1 or 2 dimensional.")
    
def _make_matrix(arr, **kwargs):
    n_cols = arr.shape[1]
    left = "\\begin{{bmatrix}}{{{}}} ".format("")
    right = " \\end{bmatrix}"
    rows = [_make_row_format_string(n_cols, **kwargs).format(*row) for row in arr]
    return left + ' '.join(rows) + right

def _make_row_format_string(n_cols, end_str=r" \\"):
    return " & ".join(["{}"]*n_cols) + end_str
