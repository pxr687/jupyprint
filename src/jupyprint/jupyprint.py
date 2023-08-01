from IPython.display import Markdown, display
import pandas as pd
import numpy as np

# ==============================================================================
# USER FACING FUNCTIONS

def jupyprint(x, quote_strings=False):
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
        and strings will be shown as text in LaTeX. If x is a pandas.DataFrame
        it will be printed in HTML, all other input types will be printed as
        Markdown/LaTeX.
    quote_strings : {False, True}
        Whether to add quotes around strings in output.

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
    >>> jupyprint(np.array([[1, 2, 4], ['A', 'B', 'C']]))

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
    display(to_md(x))


def to_md(x, quote_strings=False):
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
        Whether to add quotes around strings in output.

    Returns
    -------
    IPython.core.display.Markdown object or pandas.DataFrame
        Returns built Markdown of the input value x, for display in a Jupyter 
        notebook using the jupyprint() function. Unless x is a pandas.DataFrame,
        then it will be returned as a pandas.DataFrame.
    """
    return Markdowner(quote_strings).to_md()


class Markdowner:

    def __init__(self, quote_strings=False):
        self.quote_strings = quote_strings

    def __call__(self, x):
        # if input is a bool, dict, list, string, tuple or number, display  as
        # markdown/LaTeX (will also work for strings with LaTeX syntax e.g.
        # these will be printed as LaTeX)
        if (isinstance(x, (bool, dict, list, str, tuple, int, float, complex))):
            return Markdown(str(x))

        # if input is a numpy array convert to markdown/LaTeX, then display
        elif (isinstance(x, np.ndarray)):
            return Markdown(f"${self.arraytex(x)}$")

        # if the input is a pandas DataFrame, display it nicely rendered
        elif (isinstance(x, pd.core.frame.DataFrame)):
            return x

    # The functions below are adapted from np2latex:
    # https://github.com/madrury/np2latex/blob/master/np2latex/np2latex.py

    def arraytex(self, arr):
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
                return self._matrix(arr)

        # if the input is a column vector (1 column), display as a
        # column vector
        if (len(arr.shape) == 2):
            if (arr.shape[1] == 1):
                return self._matrix(arr.reshape(-1, 1))

        # if the input is a row vector (1 row), display as a row vector
        elif len(arr.shape) == 1:
            return self._matrix(arr.reshape(1, -1), end_str="")

        # warn user array is too high-dimensional, if this is the case
        else:
            raise ValueError("Array must be 1 or 2 dimensional.")

    # ==============================================================================
    # HIDDEN FUNCTIONS

    def _needs_latex_text(self, el):
        # add LaTex `\text{}` around elements of array, if the element is a string
        # or a bool
        if isinstance(el, (str, bool, np.str_, np.bool_)):
            return r'\text{' + str(el) + r'}'
        return el

    def _matrix(self, arr, **kwargs):
        # force dtype to object, for display (behaves better with booleans)
        arr = arr.astype(object)

        # get the number of columns
        n_cols = arr.shape[1]

        # for elements of the matrix which are strings or bools, make sure the
        # elements are shown as text in latex
        _vectorized_needs_latex_text = np.vectorize(self._needs_latex_text,
                                                    otypes = [object])
        arr = _vectorized_needs_latex_text(arr)

        # get the start and end of the latex matrix syntax
        left = "\\begin{{bmatrix}}{{{}}} ".format("")
        right = " \\end{bmatrix}"

        # get the rows of the matrix and join them to the start/end of the matrix
        rows = [self._row_f_string(n_cols, **kwargs).format(*row)
                for row in arr]
        return left + ' '.join(rows) + right

    def _row_f_string(self, n_cols, end_str=r" \\"):
        return " & ".join(["{}"]*n_cols) + end_str
