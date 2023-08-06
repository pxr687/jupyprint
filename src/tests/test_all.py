import numpy as np
import pandas as pd
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
        jupyprint(np.array([1, 2, 4]))

        # numpy.array (column vector):
        jupyprint(np.array([[1], [2], [4]]))

        # numpy.array (matrix):
        jupyprint(np.array([[1, 2, 4], ['A', 'B', 'C']]))
        jupyprint(np.array([[1, 2, 4], ['A', 'B', 'C']], dtype = object))
        jupyprint(np.array([[1, 2, 4], ['A', 'B', 'C']]), quote_strings=False)
        jupyprint(np.array([[1, 2, 4], ['A', 'B', 'C']], dtype = object), 
                  quote_strings=False)

        # boolean arrays
        jupyprint(np.array([True, True, False])) 
        jupyprint(np.array([True, True, False], dtype = object)) 
        jupyprint(np.array([[True], [True], [False]])) 
        jupyprint(np.array([[True], [True], [False]], dtype = object)) 

        # array with mixed elements
        jupyprint(np.array([10, True, "Hello"], dtype = object)) 
        jupyprint(np.array(['True', 'True', '10', 42, False, 'Hello'],
                            dtype=object))
        jupyprint(np.array([10, True, "Hello"], dtype = object), 
                  quote_strings= True) 
        jupyprint(np.array(['True', 'True', '10', 42, False, 'Hello'],
                            dtype=object), quote_strings=False)

        # arrays chained with f-string
        x = np.array([[10, 100, 200], [8, 9, 77]])
        y = np.array([[1000], [-889], [43]])
        jupyprint(f"{arraytex(x)} * {arraytex(y)} = {arraytex(np.dot(x, y))}")

        # arrays chained with f-string (with booleans)
        x = np.array([[10, 100, 200], [8, 9, 77]])
        y = np.array([[True], [False], [True]])
        jupyprint(f"{arraytex(x)} * {arraytex(y)} = {arraytex(np.dot(x, y))}")

        # arrays chained with f-string and non-LaTeX strings
        x = np.array([[10, 100, 200], [8, 9, 77]])
        jupyprint(f"""Hello, let us log this matrix: ${arraytex(x)}$. Here is
                   the logged version: $ln({arraytex(x)}) = {arraytex(np.log(x).round(2))}$""")
        jupyprint("Here is some LaTeX $\hat{y} = b_0 + b_1x_1$." + f"It is chained with LaTeX printouts of some matrix multiplication with the numpy arrays above: ${arraytex(x)} * {arraytex(y)} = {arraytex(np.dot(x, y))}$")

        # arrays chained with f-string and non-LaTeX strings
        x = np.array([[10, "100", 200], [8, False, "77"]], dtype = object)
        jupyprint(f"""Hello, here is a matrix: ${arraytex(x)}$. Here is another
                  sentence.""")
        jupyprint(f"""Hello, here is a matrix: ${arraytex(x, 
                    quote_strings=False)}$. Here is another
                  sentence.""")
        
        # linear regression model with symbols
        design_matrix = np.array([np.repeat(1, 5), np.repeat("$x_1$", 5), np.repeat("$x_2$", 5)]).T
        beta_vector = np.array(['$b_'+ str(i) + '$' for i in np.arange(0, 3)]).reshape(3, 1)
        y_vector = np.array(['$\hat{y_'+ str(i) + '}$' for i in np.arange(1, 6)]).reshape(5, 1)
        jupyprint("# The Linear Model:")
        jupyprint(f"${arraytex(y_vector)} = {arraytex(design_matrix)} * {arraytex(beta_vector)}$")

        # linear regression model with "live" variables
        jupyprint("### The linear model with 'live' data and parameters (instead of symbols):")
        design_matrix = np.array([np.repeat(1, 5),
                                np.random.normal(100, 10, 5).round(2),
                                np.random.poisson(5, 5)]).T
        beta_vector = np.array([1, 3, 0.6]).reshape(3, 1)
        y_hat_vector = np.dot(design_matrix, beta_vector).round(2)
        jupyprint(f"${arraytex(y_hat_vector)} = {arraytex(design_matrix)} * {arraytex(beta_vector)}$")

        # pandas.DataFrame:
        jupyprint(pd.DataFrame({'A': np.repeat('A', 10)}))

    except Exception as e:
        print(f"An error occurred: {e}")
        # raise error if there was an error
        assert False, "Test failed! See Traceback for details."

if __name__ == '__main__':
    test_all_jupyprints()