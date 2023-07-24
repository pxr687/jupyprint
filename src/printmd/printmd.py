from IPython.display import Markdown, display

def printmd(x):
    """
    Function to print markdown/LaTeX.
    
    Intended for use within Jupyter notebooks.
    
    ==================
    Examples
    
    Markdown:
    print_md("Hello world!")
    
    LaTex:
    print_md("$ \sum{(y_i - \hat{y})^2} $")
    """
    display(Markdown(x))