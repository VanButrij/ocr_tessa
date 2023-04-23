import cv2.cv2 as cv2
from matplotlib import pyplot as plt
import pytesseract
import re

url_array = [
    "https://mytessa.ru/blog/wp-content/uploads/2017/03/tessa23-26.png",
    "https://mytessa.ru/blog/wp-content/uploads/2017/03/tessa23-26.png",
    "https://mytessa.ru/blog/wp-content/uploads/2017/03/tessa23-26.png",
    "https://mytessa.ru/blog/wp-content/uploads/2017/03/tessa23-26.png",
    "https://mytessa.ru/blog/wp-content/uploads/2017/03/tessa23-26.png",
    "https://mytessa.ru/blog/wp-content/uploads/2017/03/tessa23-26.png",
    "https://mytessa.ru/blog/wp-content/uploads/2017/03/tessa23-26.png",
    "https://mytessa.ru/blog/wp-content/uploads/2017/03/tessa23-26.png",
    "https://mytessa.ru/blog/wp-content/uploads/2017/03/tessa23-26.png",
    "https://mytessa.ru/blog/wp-content/uploads/2017/03/tessa23-26.png"
]
con_pattern = re.compile("\w{2,3}-\d")
date_pattern = re.compile("\d{2}.\d{2}.\d{4}")
sum_pattern = re.compile("\d.\d.")

result_array = []


def take_screen(url_array):
    from selenium import webdriver
    DRIVER = 'edgedriver'
    driver = webdriver.Edge(DRIVER)
    for i in range(len(url_array)):
        driver.get(url_array[i])
        driver.save_screenshot(f'temp/img{i+1}.png')
    driver.quit()


def display(im_path):
    dpi = 80
    im_data = plt.imread(im_path)

    height, width = im_data.shape[:2]

    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)

    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    # Hide spines, ticks, etc.
    ax.axis('off')

    # Display the image.
    ax.imshow(im_data, cmap='gray')

    plt.show()


def extract_data(image):
    result_array.append([])

#    image = image[50:900, 100:1000]

    inverted_image = cv2.bitwise_not(image)
    cv2.imwrite("temp/inverted.jpg", inverted_image)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("temp/gray.jpg", gray_image)

    ocr_result = pytesseract.image_to_string(gray_image, lang='rus')

    ocr_result = ocr_result.split("\n")

    for item in ocr_result:
        if con_pattern.match(item[:10]):
            result_array[len(result_array)-1].append(item)
        elif date_pattern.match(item[:10]):
            result_array[len(result_array)-1].append(item[:10])
        elif sum_pattern.match(item):
            result_array[len(result_array)-1].append(item)


def save_to_csv(array):
    import csv

    # field names
    fields = ['Created', 'Sum', 'Edited', 'Number']

    with open('result', 'w') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)

        write.writerow(fields)
        write.writerows(array)

    print('Rows are saved to csv')


take_screen(url_array)

for i in range(10):
    image_file = f'src/img{i+1}.png'
    img = cv2.imread(image_file)

    extract_data(img)


if len(result_array) > 9:
    save_to_csv(result_array)



