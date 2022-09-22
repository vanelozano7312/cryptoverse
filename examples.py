from BackendReady.Hill import *
from BackendReady.CryptoanalysisHill import *
from BackendReady.Vigenere import *
from BackendReady.CryptoanalysisVigenere import *
"""
HILL
----

# Example 1
n = 256
key = [[167, 8, 48], [54, 107, 25], [170, 184, 107]]
inverseKey = ComputeInverseKey(n, key)
print(inverseKey)
EncryptImage(key, "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/600px-Cat03.jpg", 0)
DecryptImage(inverseKey, "result.pgm")


# Example 2
n = 26
key = [[11, 8], [3, 7]]
inverseKey = ComputeInverseKey(n, key)
text = "july"

encryptedText = EncryptText(key, text, 0)
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

#Bad matrices
n = 256
key = [[255, 8, 3], [0, 1, 7],[0,0,1]]
inverseKey = ComputeInverseKey(n, key)
EncryptImage(key, "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/600px-Cat03.jpg", 0)
DecryptImage(inverseKey, "result.pgm")

#Generate random invertible keys
n = 256
key = GetRandomInvertibleMatrix(n, 3)
print(key)
inverseKey = ComputeInverseKey(n, key)
EncryptImage(key, "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/600px-Cat03.jpg", 0)
DecryptImage(inverseKey, "result.pgm")

CRYPTOANALYSIS HILL
-------------------
#Example GuessText()

x = [[5, 17], [8, 3]]
y = [[15, 16], [2, 5]]
encryptedText = "pqcfku"

print(GuessText(x, y, encryptedText))

returns "friday"

VIGENRE
-------
print(Encrypt("CIPHER", "This Cryptosystem is not secure", 0))
print(Decrypt("CIPHER", "vpxzgiaxivwpubttmjpwizitwzt"))

CRYPTOANALYSIS VIGENERE
--------
text = "CHREEVOAHMAERATBIAXXWTNXBEEOPHBSBQMQEQERBWRVXUOAKXAOSXXWEAHBWGJMMQMNKGRFVGXWTRZXWIAKLXFPSKAUTEMNDCMGTSXMXBTUIADNGMGPSRELXNJELXVRVPRTULHDNQWTWDTYGBPHXTFALJHASVBFXNGLLCHRZBWELEKMSJIKNBHWRJGNMGJSGLXFEYPHAGNRBIEQJTAMRVLCRREMNDGLXRRIMGNSNRWCHRQHAEYEVTAQEBBIPEEWEVKAKOEWADREMXMTBHHCHRTKDNVRZCHRCLQOHPWQAIIWXNRMGWOIIFKEE"
text = utils.preProcessText(text)
print(GuessKeywordLegth(7, text))
print(GuessKeyword(5, text))
"""