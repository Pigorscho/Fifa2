from PIL import Image
import pytesseract


def recognize_digits(image_path):
    # Open the image
    img = Image.open(image_path)

    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(img, config='--psm 6 -c tessedit_char_whitelist=0123456789')

    # strip leading and trailing whitespace
    text = text.strip()

    text = ''.join([letter for letter in text if letter.isdigit()])

    # convert to integer | note: no isdigit() necessary because of tessedit_char_whitelist
    if text:
        digit = int(text)
    else:
        digit = 0

    return digit


if __name__ == '__main__':
    path = r'../../pics/transfer_list.png'
    print(recognize_digits(path))
