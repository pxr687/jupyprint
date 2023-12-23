# jupyprint

A simple python package to print markdown/LaTeX in Jupyter notebooks. 

jupyprint can print LaTeX equations (including 'live' variables), it will show
numpy arrays as LaTeX matrices, and will also render nice-looking pandas
dataframes.

See `jupyprint_demo.ipynb` for a demo.

```python
# either import jupytext as jp, then use jp.jupyprint() and jp.arraytex()
# or use the following:
from jupyprint import jupyprint, arraytex

# import other packages
import numpy as np
import pandas as pd

# use jupyprint to add the title and intro!
jupyprint("# Jupyprint Demo")
jupyprint("Below are some ways of using jupyprint...")
```


# Jupyprint Demo



Below are some ways of using jupyprint...



```python
# strings (printed as markdown):
jupyprint("Hello world!")
```


Hello world!



```python
# numbers (printed as markdown):
jupyprint(42)
jupyprint(3.14)
jupyprint(5 + 3j)  
```


42



3.14



(5+3j)



```python
# LaTeX strings:
jupyprint("$ \Large \\frac{\sum{(y_i - \hat{y_i})^2}}{n} $")
```


$ \Large \frac{\sum{(y_i - \hat{y_i})^2}}{n} $



```python
# numpy.array (row vector):
jupyprint(np.array([1, 2, 4]))
```


$\begin{bmatrix}{} 1 & 2 & 4 \end{bmatrix}$



```python
# numpy.array (column vector):
jupyprint(np.array([[1], [2], [4]]))
```


$\begin{bmatrix}{} 1 \\ 2 \\ 4 \\ \end{bmatrix}$



```python
# numpy.array (matrix):
jupyprint(np.array([[1, 2, 4], ['A', 'B', 'C']]))
```


$\begin{bmatrix}{} {\tt'1'} & {\tt'2'} & {\tt'4'} \\ {\tt'A'} & {\tt'B'} & {\tt'C'} \\ \end{bmatrix}$



```python
# array with mixed elements
jupyprint(np.array([10, True, "Hello"], dtype = object)) 
jupyprint(np.array(['True', 'True', '10', 42, False, 'String with multiple words!'], dtype=object))
```


$\begin{bmatrix}{} 10 & \text{True} & {\tt'Hello'} \end{bmatrix}$



$\begin{bmatrix}{} {\tt'True'} & {\tt'True'} & {\tt'10'} & 42 & \text{False} & {\tt'String~~with~~multiple~~words!'} \end{bmatrix}$



```python
# arrays chained with f-string
x = np.array([[10, 100, 200], [8, 9, 77]])
y = np.array([[1000], [-889], [43]])
jupyprint(f"${arraytex(x)} * {arraytex(y)} = {arraytex(np.dot(x, y))}$")
```


$\begin{bmatrix}{} 10 & 100 & 200 \\ 8 & 9 & 77 \\ \end{bmatrix} * \begin{bmatrix}{} 1000 \\ -889 \\ 43 \\ \end{bmatrix} = \begin{bmatrix}{} -70300 \\ 3310 \\ \end{bmatrix}$



```python
# arrays chained with f-string (with booleans)
x = np.array([[10, 100, 200], [8, 9, 77]])
y = np.array([[True], [False], [True]])
jupyprint(f"${arraytex(x)} * {arraytex(y)} = {arraytex(np.dot(x, y))}$")
```


$\begin{bmatrix}{} 10 & 100 & 200 \\ 8 & 9 & 77 \\ \end{bmatrix} * \begin{bmatrix}{} \text{True} \\ \text{False} \\ \text{True} \\ \end{bmatrix} = \begin{bmatrix}{} 210 \\ 85 \\ \end{bmatrix}$



```python
# arrays chained with f-string and non-LaTeX strings
x = np.array([[10, 100, 200], [8, 9, 77]])
jupyprint(f"""Hello, let us log this matrix: ${arraytex(x)}$. Here is
           the logged version: $ln({arraytex(x)}) = {arraytex(np.log(x).round(2))}$""")
jupyprint("Here is some LaTeX $\hat{y} = b_0 + b_1x_1$." + f"It is chained with LaTeX printouts of some matrix multiplication with the numpy arrays above: ${arraytex(x)} * {arraytex(y)} = {arraytex(np.dot(x, y))}$")
```


Hello, let us log this matrix: $\begin{bmatrix}{} 10 & 100 & 200 \\ 8 & 9 & 77 \\ \end{bmatrix}$. Here is
           the logged version: $ln(\begin{bmatrix}{} 10 & 100 & 200 \\ 8 & 9 & 77 \\ \end{bmatrix}) = \begin{bmatrix}{} 2.3 & 4.61 & 5.3 \\ 2.08 & 2.2 & 4.34 \\ \end{bmatrix}$



Here is some LaTeX $\hat{y} = b_0 + b_1x_1$.It is chained with LaTeX printouts of some matrix multiplication with the numpy arrays above: $\begin{bmatrix}{} 10 & 100 & 200 \\ 8 & 9 & 77 \\ \end{bmatrix} * \begin{bmatrix}{} \text{True} \\ \text{False} \\ \text{True} \\ \end{bmatrix} = \begin{bmatrix}{} 210 \\ 85 \\ \end{bmatrix}$



```python
# showing symbolic representations of models alongside versions with "live" variables

# linear regression model with symbols
design_matrix = np.array([np.repeat(1, 5), np.repeat("$x_1$", 5), np.repeat("$x_2$", 5)]).T

beta_vector = np.array(['$b_'+ str(i) + '$' for i in np.arange(0, 3)]).reshape(3, 1)

y_vector = np.array(['$\hat{y_'+ str(i) + '}$' for i in np.arange(1, 6)]).reshape(5, 1)

jupyprint("# The Linear Model:")
jupyprint(f"${arraytex(y_vector, contains_latex=True)} = {arraytex(design_matrix, contains_latex=True)} * {arraytex(beta_vector, contains_latex=True)}$")

# linear regression model with "live" variables
jupyprint("### The linear model with 'live' data and parameters (instead of symbols):")
design_matrix = np.array([np.repeat(1, 5),
                          np.random.normal(100, 10, 5).round(2),
                          np.random.poisson(5, 5)]).T

beta_vector = np.array([1, 3, 0.6]).reshape(3, 1)

y_hat_vector = np.dot(design_matrix, beta_vector).round(2)

jupyprint(f"${arraytex(y_hat_vector)} = {arraytex(design_matrix)} * {arraytex(beta_vector)}$")
```


# The Linear Model:



$\begin{bmatrix}{} \text{$\hat{y_1}$} \\ \text{$\hat{y_2}$} \\ \text{$\hat{y_3}$} \\ \text{$\hat{y_4}$} \\ \text{$\hat{y_5}$} \\ \end{bmatrix} = \begin{bmatrix}{} \text{1} & \text{$x_1$} & \text{$x_2$} \\ \text{1} & \text{$x_1$} & \text{$x_2$} \\ \text{1} & \text{$x_1$} & \text{$x_2$} \\ \text{1} & \text{$x_1$} & \text{$x_2$} \\ \text{1} & \text{$x_1$} & \text{$x_2$} \\ \end{bmatrix} * \begin{bmatrix}{} \text{$b_0$} \\ \text{$b_1$} \\ \text{$b_2$} \\ \end{bmatrix}$



### The linear model with 'live' data and parameters (instead of symbols):



$\begin{bmatrix}{} 313.48 \\ 337.6 \\ 270.13 \\ 277.87 \\ 286.03 \\ \end{bmatrix} = \begin{bmatrix}{} 1.0 & 102.56 & 8.0 \\ 1.0 & 111.8 & 2.0 \\ 1.0 & 88.91 & 4.0 \\ 1.0 & 91.29 & 5.0 \\ 1.0 & 94.21 & 4.0 \\ \end{bmatrix} * \begin{bmatrix}{} 1.0 \\ 3.0 \\ 0.6 \\ \end{bmatrix}$



```python
# pandas.DataFrame:
jupyprint(pd.DataFrame({'A': np.repeat('A', 10),
                           'B': np.repeat('B', 10)}))
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
      <td>B</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A</td>
      <td>B</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A</td>
      <td>B</td>
    </tr>
    <tr>
      <th>3</th>
      <td>A</td>
      <td>B</td>
    </tr>
    <tr>
      <th>4</th>
      <td>A</td>
      <td>B</td>
    </tr>
    <tr>
      <th>5</th>
      <td>A</td>
      <td>B</td>
    </tr>
    <tr>
      <th>6</th>
      <td>A</td>
      <td>B</td>
    </tr>
    <tr>
      <th>7</th>
      <td>A</td>
      <td>B</td>
    </tr>
    <tr>
      <th>8</th>
      <td>A</td>
      <td>B</td>
    </tr>
    <tr>
      <th>9</th>
      <td>A</td>
      <td>B</td>
    </tr>
  </tbody>
</table>
</div>


