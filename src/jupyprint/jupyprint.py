from IPython.display import _Markdown, _display
import pandas as _pd
import numpy as _np

# ==============================================================================
# USER FACING FUNCTIONS

def jupyprint(x):
    """
    Function to print markdown/LaTeX, and render nice looking numpy arrays and
    pandas dataframes, within Jupyter notebooks.

    Parameters
    ----------
    x: thing to be printed in markdown/LaTeX. Can be a string, LaTeX string, a
       number (int, float, complex), a boolean, a list, a dict, a tuple, a 1D
       numpy array (row or column vector) or a 2D numpy array. (Numpy arrays
       can contain elements of any dtype - bools and strings will be shown
       as text in LaTeX).

    Returns
    -------
    None. It prints x as markdown/LaTeX, which can be rendered in a Jupyter
    notebook.

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
    jupyprint(_np.array([1, 2, 4]))

    numpy.array (column vector):
    jupyprint(_np.array([[1], [2], [4]]))

    numpy.array (matrix):
    jupyprint(_np.array([[1, 2, 4], ['A', 'B', 'C']]))

    pandas.DataFrame:
    jupyprint(_pd.DataFrame({'A': _np.repeat('A', 10)}))

    arrays chained with f-string (in combination with the jupyprint.arraytex() 
    function - this example also uses numpy.dot):
    x = _np.array([[10, 100, 200], [8, 9, 77]])
    y = _np.array([[1000], [-889], [43]])
    jupyprint(f"{arraytex(x)} * {arraytex(y)} = {arraytex(np.dot(x, y))}")

    """

    # if input is a bool, dict, list, string, tuple or number, display  as 
    # markdown/LaTeX (will also work for strings with LaTeX syntax e.g. these
    # will be printed as LaTeX)
    if (isinstance(x, (bool, dict, list, str, tuple, int, float, complex))):
        _display(_Markdown(str(x)))

    # if input is a numpy array convert to markdown/LaTeX, then display
    elif (isinstance(x, _np.ndarray)):
        _display(_Markdown("$"+arraytex(x)+"$"))

    # if the input is a pandas DataFrame, display it nicely rendered
    elif (isinstance(x, _pd.core.frame.DataFrame)):
        _display(x)

# The functions below are adapted from np2latex: 
# https://github.com/madrury/np2latex/blob/master/np2latex/np2latex.py

def arraytex(arr):
    """Convert a 1D or 2D numpy array to latex markdown.

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
            return _matrix(arr)
    
    # if the input is a column vector (1 column), display as a
    # column vector
    if (len(arr.shape) == 2):
        if (arr.shape[1] == 1):
            return _matrix(arr.reshape(-1, 1))

    # if the input is a row vector (1 row), display as a row vector
    elif len(arr.shape) == 1:
        return _matrix(arr.reshape(1, -1), end_str="")
    
    # warn user array is too high-dimensional, if this is the case
    else:
        raise ValueError("Array must be 1 or 2 dimensional.")

# ==============================================================================
# HIDDEN FUNCTIONS

def _needs_latex_text(el):
    # add LaTex `\text{}` around elements of array, if the element is a string
    # or a bool
    if isinstance(el, (str, bool, _np.str_, _np.bool_)):
        return r'\text{' + str(el) + r'}'
    return el
    
def _matrix(arr, **kwargs):

    # force dtype to object, for display (behaves better with booleans)
    arr = arr.astype(object)

    # get the number of columns
    n_cols = arr.shape[1]

    # for elements of the matrix which are strings or bools, make sure the 
    # elements are shown as text in latex
    _vectorized_needs_latex_text = _np.vectorize(_needs_latex_text, 
                                                 otypes = [object])
    arr = _vectorized_needs_latex_text(arr)
    
    # get the start and end of the latex matrix syntax
    left = "\\begin{{bmatrix}}{{{}}} ".format("")
    right = " \\end{bmatrix}"

    # get the rows of the matrix and join them to the start/end of the matrix
    rows = [_row_f_string(n_cols, **kwargs).format(*row) for row in arr]
    return left + ' '.join(rows) + right

def _row_f_string(n_cols, end_str=r" \\"):
    return " & ".join(["{}"]*n_cols) + end_str