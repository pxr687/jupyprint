from IPython.display import Markdown, display
import pandas as pd
import numpy as np

# ==============================================================================
# USER FACING FUNCTIONS

def jupyprint(x, quote_strings=True, strings_in_typefont=True):
    """ Nice-looking Jupyter notebook display for value x.

    This function will display the value as Markdown/LaTeX if `x` is of type
    string, LaTeX string, number (int, float, complex), boolean, list,
    dictionary, tuple, or a 1D/2D numpy array. If `x` is a pandas.DataFrame, it
    will be rendered as HTML.

    Parameters
    ----------
    x : str or int or float or complex or bool or list or dict or tuple or 
        numpy.ndarray or pandas.DataFrame
        The input data to be printed. x can be a string, LaTeX string, a number
        (int, float, complex), a boolean, a list, a dictionary, a tuple, a 1D 
        numpy array  (row or column vector), a 2D numpy array or a 
        pandas.DataFrame. Numpy arrays can contain elements of any dtype - bools
        and strings will be shown as text in LaTeX (if the array contains mixed
        datatypes, ensure you use "dtype = object" when constructing the array -
        otherwise all elements will be shown as strings). If x is a 
        pandas.DataFrame it will be printed in HTML, all other input types will
        be printed as Markdown/LaTeX.
    quote_strings : {False, True}
        Whether to add quotes around strings in output, where the output is a
        vector or matrix.

    Returns
    -------
    None
        It prints input value x as markdown/LaTeX/HTML, which can be rendered in
        a Jupyter notebook.

    Examples
    --------
    Markdown:
    >>> jupyprint("Hello world!")

    Numbers:
    >>> jupyprint(42)
    >>> jupyprint(3.14)
    >>> jupyprint(5 + 3j)

    LaTex:
    >>> jupyprint("$ \sum{(y_i - \hat{y})^2} $")

    numpy.array (row vector):
    >>> import numpy as np
    >>> jupyprint(np.array([1, 2, 4]))

    numpy.array (column vector):
    >>> import numpy as np
    >>> jupyprint(np.array([[1], [2], [4]]))

    numpy.array (matrix):
    >>> import numpy as np
    >>> jupyprint(np.array([[1, 2, 4], ['A', 'B', 'C']], dtype = object))
    >>> # NOTE: where arrays contain mixed dtypes, use "dtype = object" to 
    >>> # ensure dtypes are shown correctly, otherwise they will all be shown
    >>> # strings...

    pandas.DataFrame:
    >>> import pandas as pd
    >>> import numpy as np
    >>> jupyprint(pd.DataFrame({'A': np.repeat('A', 10)}))

    arrays chained with f-string (in combination with the jupyprint.arraytex() 
    function - this example also uses numpy.dot):
    >>> import numpy as np
    >>> x = np.array([[10, 100, 200], [8, 9, 77]])
    >>> y = np.array([[1000], [-889], [43]])
    >>> jupyprint(f"{arraytex(x)} * {arraytex(y)} = {arraytex(np.dot(x, y))}")
    """

    # jupyprint the input
    display(to_md(x, quote_strings=quote_strings, 
                  strings_in_typefont=strings_in_typefont))

def to_md(x, quote_strings=True, strings_in_typefont=True):
    """
    Build a Markdown object for input value `x`. 

    Parameters
    ----------
    x : str or int or float or complex or bool or list or dict or tuple or 
        numpy.ndarray or pandas.DataFrame
        The input data to be converted to a Markdown object (where necessary
        for nice-looking printing in a Jupyter notebook e.g. pandas.DataFrame
        inputs do not need to be converted to Markdown, but other input types
        do).
    quote_strings : {False, True}
        Whether to add quotes around strings in output, where the output is a
        vector or matrix.

    Returns
    -------
    IPython.core.display.Markdown object or pandas.DataFrame
        Returns built Markdown of the input value x, for display in a Jupyter 
        notebook using the jupyprint() function. Unless x is a pandas.DataFrame,
        then it will be returned as a pandas.DataFrame.
    """
    # if input is a bool, string, dict, list, tuple or number, display  as 
    # markdown/LaTeX (will also work for strings with LaTeX syntax e.g. these 
    # will be printed as LaTeX)
    if (isinstance(x, (bool, np.bool_, str, np.str_, dict, list, tuple, int,
                       float, complex))):
        return Markdown(str(x)) 
    
    # if input is a numpy array convert to markdown/LaTeX, then display
    elif (isinstance(x, np.ndarray)):
        return Markdown(f"${arraytex(x, quote_strings=quote_strings, strings_in_typefont=strings_in_typefont)}$")

    # if the input is a pandas DataFrame, display it nicely rendered
    elif (isinstance(x, pd.core.frame.DataFrame)):
        return x

    # The functions below are adapted from np2latex:
    # https://github.com/madrury/np2latex/blob/master/np2latex/np2latex.py

def arraytex(arr, quote_strings=True, strings_in_typefont=True):
    """Convert a 1D or 2D numpy array to latex markdown.

    Parameters
    ----------
    arr: array, shape (n, p), (n,) or (1, n)
        A numpy array.
    
    quote_strings : {False, True}
        Whether to add quotes around strings in output.

    Returns
    -------
    latex: string
        A latex string.
    """
    # determine if the input is a matrix (two dimensions, more than one column),
    # display as a matrix
    if (len(arr.shape) == 2):
        if (arr.shape[1] > 1):
            return _matrix(arr, quote_strings=quote_strings, 
            strings_in_typefont=strings_in_typefont)

    # if the input is a column vector (1 column), display as a
    # column vector
    if (len(arr.shape) == 2):
        if (arr.shape[1] == 1):
            return _matrix(arr.reshape(-1, 1), quote_strings=quote_strings, 
            strings_in_typefont=strings_in_typefont)

    # if the input is a row vector (1 row), display as a row vector
    elif len(arr.shape) == 1:
        return _matrix(arr.reshape(1, -1), quote_strings=quote_strings,
        strings_in_typefont=strings_in_typefont,
                        end_string="")

    # warn user array is too high-dimensional, if this is the case
    else:
        raise ValueError("Array must be 1 or 2 dimensional.")

# ==============================================================================
# HIDDEN FUNCTIONS

def _matrix(arr, quote_strings=True, strings_in_typefont=True, 
            end_string=r" \\"):

    # get the number of columns
    n_cols = arr.shape[1]

    # original shape of array
    original_shape = arr.shape

    # flattened array 
    flattened_array = arr.flatten()

    # for elements of the matrix which are strings or bools, make sure the
    # elements are shown as text in latex
    flattened_array = np.array([_needs_latex_text(el, \
                        quote_strings=quote_strings,
                        strings_in_typefont=strings_in_typefont) \
                        for el in flattened_array])
    
    # reshape to shape of original array
    arr = flattened_array.reshape(original_shape)

    # get the start and end of the latex matrix syntax
    left = "\\begin{{bmatrix}}{{{}}} ".format("")
    right = " \\end{bmatrix}"

    # get the rows of the matrix and join them to the start/end of the matrix
    rows = [_row_f_string(n_cols, end_string=end_string).format(*row)
            for row in arr]
    return left + ' '.join(rows) + right

def _needs_latex_text(el, quote_strings=True, strings_in_typefont=True):
    # add LaTex `\text{}` around elements of array, if the element is a 
    # string or a bool
    if isinstance(el, (bool, np.bool_)):
        return r'\text{' + str(el) + r'}'
    
    elif isinstance(el, (str, np.str_)) and (quote_strings == True) \
        and (strings_in_typefont == True):
        return r"{\tt'" + str(el) + r"'}"
    
    elif isinstance(el, (str, np.str_)) and (quote_strings == False) \
        and (strings_in_typefont == True):
        return r'{\tt ' + str(el) + r'}'
    
    elif isinstance(el, (str, np.str_)) and (quote_strings == True) \
        and (strings_in_typefont == False):
        return r"\text{''" + str(el) + r"''}"
    
    elif isinstance(el, (str, np.str_)) and (quote_strings == False) \
        and (strings_in_typefont == False):
        return r'\text{' + str(el) + r'}'
    
    else:
        return el

def _row_f_string(n_cols, end_string=r" \\"):
    return " & ".join(["{}"]*n_cols) + end_string
