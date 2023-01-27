from pdf2image import convert_from_path
import json

# ~ requires installation of tesseract for ocr
# ~ windows: https://github.com/tesseract-ocr/tesseract#installing-tesseract
# ~ mac: brew install Tesseract
# ~ please ensure that the version is tesseract 5.3.0

from PIL import Image
import pytesseract
import os
import numpy as np


def get_full_text(pdfs):
	# ~ -----essentially doing pdf --> jpeg conversion
	# ~ TODO fix the pdf file path ^^^ before running 
	pages = convert_from_path(pdfs, 350)
	all_text = ""
	i = 1
	# ~ turn every page in the pdf into a jpeg file
	for page in pages:
		image_name = "Page_" + str(i) + ".jpg"  
		page.save(image_name, "JPEG")
		# ~ ----cropping-----
		page = Image.open(image_name)
		width,length = page.size
		page = page.crop((0,400,width,length))
		# ~ page.show()
		page.save(image_name, quality=100)
		# ~ -----doing the ocr for the jpegs-------
		img1 = np.array(Image.open(image_name))
		text = pytesseract.image_to_string(img1)
		all_text = all_text.__add__(text)
		print("done "+image_name)
		i = i+1        
		os.remove(image_name)
	return all_text

if __name__ == "__main__":
	pdfs = r"/Users/juwoncha/Documents/GitHub/sat_word_freq/pdfs/October 2021 SAT QAS.pdf"			
	with open('data.txt','w', encoding='utf-8') as file:
		file.write(get_full_text(pdfs))
		file.close()
	
# ~ TODO make a way so that this only analyses the reading section (we could include the writing section also)
# ~ maybe cut the page number to a certain point (or make it detect when each section finishes???)
