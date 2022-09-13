import numpy as np
from Utils import utils

def Round(l):
    """
    Description
    -----------
    Returns a new list where each element is rounded

    Parameters
    ----------
    l : list
        The list to apply the round function

    Returns
    -------
    A new list with each entry rounded
    """
    result = []
    for i in l:
        result.append(int(round(i)))
    return result

def adjoint_matrix(matrix):
    """
    Description
    -----------
    Tries to compute the adjoint matrix of the given
    matrix as long as its determinant is not zero. If
    the matrix is invertible, it returns its adjoint
    matrix

    Parameters
    ----------
    matrix : 2-dimensional list or np.array
        The matrix to find the adjoint matrix
    
    Returns
    -------
    A new two 2-dimensional list or np.array
    """
    try:
        determinant = np.linalg.det(matrix)
        if(determinant!=0):
            cofactor = None
            cofactor = np.linalg.inv(matrix).T * determinant
            # return cofactor matrix of the given matrix
            return cofactor.transpose()
        else:
            raise Exception("singular matrix")
    except Exception as e:
        print("could not find cofactor matrix due to",e)

def gcdExtended(a, b):
    """
    Description
    -----------
    From number theory we have ax + by = gcd(a, b). This function
    finds the value of x,y and the gcd, given a, b, and returns
    them

    Parameters
    ----------
    a: int
        First number to get the gcd
    b: int
        Second number to get the gcd
    
    Returns
    -------
    gcd : int
        The gcd(a,b)
    x : int
        The coefficient of a in the formula ax + by = gcd(a,b)
    y : int
        The coefficient of b in the formula ax + by = gcd(a,b)
    """
    # Base Case
    if a == 0 :
        return b,0,1
             
    gcd,x1,y1 = gcdExtended(b%a, a)
     
    # Update x and y using results of recursive
    # call
    x = y1 - (b//a) * x1
    y = x1
    
    return gcd,x,y

def ComputeInverseKey(n, key):
    """
    Description
    -----------
    Computes the inverse matrix of the mxm key matrix modulus n
    and then returns it.

    Parameters
    ----------
    n : int
        The modulus to find the inverse matrix
    key : 2-dimensional list or np.array
        The matrix to find the inverse modulus n
    
    Returns
    -------
    If the matrix is invertible modulus n returns the inverse. Otherwise
    it raises and exception
    """
    try:
        utils.IsValidMatrix(key)
    except:
        return -1
    
    m = len(key)
    mod = m*[m*[n]]

    # Compute Adjoint matrix of the key modulus n
    adjoint = adjoint_matrix(key)
    adjoint = np.mod(adjoint, mod)

    # Compute the inverse of the determinant of the key
    # modulus n
    det = int(np.linalg.det(key)) % n
    gcd, inverseDet, y = gcdExtended(det,n)

    # Check whether or not the given matrix is inversible
    # modulus n
    if gcd == 1:

        # Compute the inverse matrix of the key modulus n
        # In the same way, round the entries of the resulting
        # matrix
        inverse = np.dot(inverseDet, adjoint)
        inverse = np.mod(inverse, mod)
        inverse = [Round(x) for x in inverse]

        return inverse
    else:
        raise "The given matrix is not invertible modulus m"

def GuessKey(x, y, n):
    """
    Description
    -----------
    Given square matrices x and y where the x i-th row it's
    supposed to be mapped to the y i-th row using the key we
    are looking for, it tries to return that key, at least if
    the x matrix is invertible modulus n

    Parameters
    ----------
    x : 2-dimensional array or np.array ei. [[1,2], [5, 6]]
        The matrix where the rows are the values for which is
        supposed to be known its product after apply the key
    y : 2-dimensional array or np.array ie. [[4,5],[11, 9]]
        The matrix where the i-th row is the result after
        multiply x by the key
    n : int
        The modulus to use in all the operations
    
    Returns
    -------
    If the x matrix is invertible modulus n, it will return the
    key which is the product of x^-1*y. Otherwise, it will return
    -1
    """
    try:
        m = len(x)
        inverse = ComputeInverseKey(m, n, x)
        key = np.dot(inverse, y)
        mod = m*[m*[n]]
        key = np.mod(key, mod)
        return key
    except:
        return -1