from pdf2image import convert_from_path
import json

# ~ requires installation of tesseract for ocr
# ~ windows: https://github.com/tesseract-ocr/tesseract#installing-tesseract
# ~ mac: brew install Tesseract
from PIL import Image
import pytesseract
import numpy as np


# ~ -----essentially doing pdf --> jpeg conversion
pdfs = r"/Users/juwoncha/Documents/GitHub/sat_word_freq/pdfs/2021 March SAT QAS.pdf"
# ~ TODO fix the pdf file path ^^^ before running 
pages = convert_from_path(pdfs, 350)

i = 1

all_text = ""

# ~ turn every page in the pdf into a jpeg file
for page in pages:
	image_name = "Page_" + str(i) + ".jpg"  
	page.save(image_name, "JPEG")
	i = i+1        
    # ~ -----doing the ocr for the jpegs-------
	img1 = np.array(Image.open(image_name))
	text = pytesseract.image_to_string(img1)
	all_text = all_text.__add__(text)
	print("done "+image_name)
	
with open('data.txt','w') as file:
	file.write(all_text)
	file.close()
	
# ~ TODO make upper and lower boundaries for the images so that the really weird margin areas are cut
# ~ this can help minimise the gibberish such as "ESESESESESSESESESESES" happening because of poorly-scanned pages

# ~ TODO make a way so that this only analyses the reading section (we could include the writing section also)
# ~ maybe cut the page number to a certain point (or make it detect when each section finishes???)
