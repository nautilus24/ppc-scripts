import pytesseract
from PIL import Image
import cv2
import pandas as pd



# Open an image file
img = Image.open('C:/Users/priya/OneDrive/Pictures/test.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

text = pytesseract.image_to_string(gray)

rows = text.split('\n')

data = []
for row in rows:
    cells = row.split('\t')
    data.append(cells)

df = pd.DataFrame(data)

print(df)