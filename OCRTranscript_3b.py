try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import os
from difflib import SequenceMatcher
import progressbar

def dur(count):
    count = int(count)
    seconds = str(count % 60).zfill(2)
    minutes = str(int(count / 60)).zfill(2)
    return '(' + minutes + ':' + seconds + ')'

def similar(a,b):
    return SequenceMatcher(None,a,b).ratio()

def similar_texts(text1,text2):
    ratio = similar(text1,text2)
    if ratio > 0.8:
        return True
    else:
        return False

def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    text = text.strip()
    text = text.replace('\n',' ')
    return text

def ocr_gen(timings, videoname):
    widgets = [' [', 
         progressbar.Timer(format= 'elapsed time: %(elapsed)s'), 
         '] ', 
           progressbar.Bar('*'),' (', 
           progressbar.ETA(), ') ', 
          ]
    path = os.getcwd() + '\\files_' + videoname + '\\'
    length = len(timings)
    bar = progressbar.ProgressBar(max_value=length,  
                                widgets=widgets).start() 

    inc = length/50
    if(inc < 1):
        inc = 1

    my_path = path + 'captures'

    complete_info = [""]
    i = 1

    for folders, sub_folders, files in os.walk(my_path):
        ocr_data = []
        for f in files:
            for _ in range(2):
                try:
                    final_str = ocr_core("files_"+ videoname +"/captures/"+f)
                    break
                except:
                    continue

            if(not similar_texts(final_str, complete_info[-1])):
                #print(final_str)
                if final_str != ' ':
                    ocr_data.append(dur(timings[i]/1000)+" "+final_str)
                    complete_info.append(final_str)
            i += int(inc)
            if(i < length):
                bar.update(i)
    print('\nOCR data transcript generated')
    return ocr_data

# data = ocr_gen([0, 1714.0, 4105.0, 6836.0, 8685.0, 14273.0, 17333.0, 22977.0, 28297.0, 33579.0, 36558.0, 38914.0, 42499.0, 49050.0, 53589.0, 59859.0, 64474.99999999999, 73405.0, 77626.0, 84316.0, 89617.0]
#     ,'temp')
# print(data)