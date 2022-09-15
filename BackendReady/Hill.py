from PIL import Image
import requests
from PIL import ImageOps
from IPython.display import display
import urllib.request
import numpy as np
from BackendReady.Utils import utils
from BackendReady.CryptoanalysisHill import ComputeInverseKey

def encode_hill_image(key, url):
    """
    Description
    -----------
    Given m(the dimension of the key matrix), the key(matrix) and a
    url of the image, it encrypts the image of the url using the key.
    Finally, the encrypted image is displayed and then saved in
    'result.pgm' file

    Parameters
    ----------
    key : 2-dimensional list or np.array ie [[1, 2], [5, 6]]
        The mxm matrix to use as a key in the Hill cipher
    url : string
        The url of the image to encrypt
    """

    try:
        utils.IsValidMatrix(key)
    except:
        return -1

    m = len(key)
    response = requests.get(url)
    urllib.request.urlretrieve(url,"static/images/image.jpg")
    img = Image.open("static/images/image.jpg")
    encryptedImg = img.convert("L")

    # Resize image as needed, the image width must be a multiple
    # of m
    if encryptedImg.width % m != 0:
        diff = m - (encryptedImg.width % m)
        encryptedImg = ImageOps.expand(encryptedImg, border=(0,0, diff, 0), fill = 0)
    
    # Iterate over each row of the image height taking at each step
    # m pixels to transform them into a new m pixels
    for y in range(0, encryptedImg.height):
        rowPixels = []
        for x in range(0, encryptedImg.width):
            if x % m == 0 and x > 0:
                # Transform the m pixels making the dot product between them and the
                # key matrix
                newRowPixels = list(np.dot(rowPixels, key))
                newRowPixels = [(i % 255) for i in newRowPixels]
                for i in range(x - m, x):
                    encryptedImg.putpixel((i,y), int(newRowPixels[i - (x-m)]))
                rowPixels = []
            
            rowPixels.append(encryptedImg.getpixel((x,y)))
    
    # Show the image and save it in a .pgm file
    encryptedImg.show()
    encryptedImg.save("static/images/result.pgm")

def decode_hill_image(decryptKey, imgPath):
    """
    Description
    -----------
    Given m(the dimension of the key matrix), the  decrypt key(the 
    inverse modulus 255 of the matrix used to encrypt) and the path
    of the image it decrypts the image in the path using the key
    and then displays it

    Parameters
    ----------
    decryptKey : 2-dimensional list or np.array
        The inverse modulus 255 of the matrix used to encrypt
    imgPath : string
        The path of the image to decrypt in the local host
    """

    try:
        utils.IsValidMatrix(decryptKey)
    except:
        return -1

    m = len(decryptKey)
    img = Image.open(imgPath)
    decryptedImg = img

    # Iterate over each row of the image height taking at each step
    # m pixels to transform them into a new m pixels
    for y in range(0, decryptedImg.height):
        rowPixels = []
        for x in range(0, decryptedImg.width):
            if x % m == 0 and x > 0:
                # Transform the m pixels making the dot product between them and the
                # key matrix
                newRowPixels = list(np.dot(rowPixels, decryptKey))
                newRowPixels = [(int(i) % 255) for i in newRowPixels]
                for i in range(x - m, x):
                    decryptedImg.putpixel((i,y), int(newRowPixels[i - (x-m)]) % 255)
                rowPixels = []
            
            rowPixels.append(decryptedImg.getpixel((x,y)))
    
    decryptedImg.show()
    decryptedImg.save("static/images/out.png")

def encode_hill_text(key, text):
    """
    Description
    -----------
    Given m(the dimension of the key matrix), the key(matrix)
    and the text, it encrypts the text using the key and then
    returns it

    Parameters
    ----------
    key : 2-dimensional list or np.array
        The mxm matrix to use as a key in the Hill cipher
    text : string
        The text to encrypt. If the text length is not a m multiple
        it will add 'f' characters as needed to make it a m multiple
    """

    try:
        utils.IsValidMatrix(key)
    except:
        return -1

    m = len(key)
    text = utils.preProcessText(text)
    encryptedText = ""

    # Resize the text as needed, the text length must be a multiple
    # of m
    if len(text) % m != 0:
        diff = m - (len(text) % m)
        text += diff*"f"
    
    # Iterate over the text taking at each step m characters to transform
    # them into a new m characters
    rowCharacters = []
    for x in range(0, len(text) + 1):
        if x % m == 0 and x > 0:
            # Transform the m characters codes making the dot product between
            # them and the key matrix
            newRowCharacters = list(np.dot(rowCharacters, key))
            newRowCharacters = [(i % 26) for i in newRowCharacters]
            for i in range(x - m, x):
                encryptedText += utils.GetLetter(int(newRowCharacters[i - (x-m)]))
            rowCharacters = []
        
        if(x != len(text)):
            rowCharacters.append(utils.GetCode(text[x]))
    
    # Return the encrypted text
    return encryptedText

def decode_hill_text(decryptKey, text):
    """
    Description
    -----------
    Given m(the dimension of the key matrix), the decrpyt key(matrix)
    and the encrypted text, it decrypts the text using the decrypt key
    and then returns it

    Parameters
    ----------
    key : 2-dimensional list or np.array
        The mxm matrix to use as a a decrypt key in the Hill cipher
    text : string
        The text to decrypt, it must be of length m
    """

    try:
        utils.IsValidMatrix(decryptKey)
    except:
        return -1

    m = len(decryptKey)
    decryptedText = ""
    
    # Iterate over the text taking at each step m characters to transform
    # them into a new m characters
    rowCharacters = []
    for x in range(0, len(text) + 1):
        if x % m == 0 and x > 0:
            # Transform the m characters codes making the dot product between
            # them and the key matrix
            newRowCharacters = list(np.dot(rowCharacters, decryptKey))
            newRowCharacters = [(i % 26) for i in newRowCharacters]
            for i in range(x - m, x):
                decryptedText += utils.GetLetter(int(newRowCharacters[i - (x-m)]))
            rowCharacters = []
        
        if(x != len(text)):
            rowCharacters.append(utils.GetCode(text[x]))
    
    # Return the encrypted text
    return decryptedText

"""
# Example 1
m = 3
n = 255
key = [[10,4,12],[3,14,4],[8,9,0]]
inverseKey = ComputeInverseKey(n, key)

EncryptImage(key, "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/600px-Cat03.jpg")
DecryptImage(inverseKey, "result.pgm")


# Example 2
m = 2
n = 26
key = [[11, 8], [3, 7]]
inverseKey = ComputeInverseKey(n, key)
text = "july"

encryptedText = EncryptText(key, text)
print(encryptedText)
decryptedText = DecryptText(inverseKey, encryptedText)
print(decryptedText)

#Good cases
https://i.scdn.co/image/ab6765630000ba8a8c04c65ceb701d64f8966e23
https://upload.wikimedia.org/wikipedia/commons/5/54/Panda_Cub_%284274178112%29.jpg
https://i.pinimg.com/originals/6f/0b/3b/6f0b3baa01e2136b2e2d93709e622e2c.jpg

# Middle cases
https://scontent.fbog4-1.fna.fbcdn.net/v/t39.30808-6/306102097_2868887480087696_8956594249965335582_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=a26aad&_nc_eui2=AeGwbIyz9fkoiaa7UKkdjKuFzzjx7ZARUSDPOPHtkBFRIMjQ5a58SSjb4-09hGz_5J4CPJ6JonpeOnxi29pbS88D&_nc_ohc=KbG5TT4GuY0AX859emw&_nc_ht=scontent.fbog4-1.fna&oh=00_AT9bTvkoUh5aRrphZRFsOt7Qu-bPy-f_uhJc3-e88uWETw&oe=6323986B

# Bad cases
https://upload.wikimedia.org/wikipedia/commons/5/56/Tux.jpg
https://www3.gobiernodecanarias.org/medusa/ecoescuela/sa/files/formidable/6/mondrian-1504681_960_720.png
"""

# # Example 2
# m = 2
# n = 26
# key = [[11, 8], [3, 7]]
# text = "july"

# encryptedText = encode_hill_text(key, text)
# print(encryptedText)
# # decryptedText = DecryptText(inverseKey, encryptedText)
# # print(decryptedText)


# # Example 1
# m = 3
# n = 255
# key = [[10,4,12],[3,14,4],[8,9,0]]
# inverseKey = ComputeInverseKey(n, key)

# encode_hill_image(key, "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/600px-Cat03.jpg")
# decode_hill_image(inverseKey, "result.pgm")
