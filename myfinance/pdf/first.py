#%% Import all libraries
from pdfminer.high_level import extract_text,extract_pages
from pdfminer.layout import LTTextContainer,LTChar
import time
import PyPDF2

#%%

file = "data/Reliance2020.pdf"

with open(file, 'rb') as pdfFileObject:
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
    print(" No. Of Pages :", pdfReader.numPages)
    pageObject = pdfReader.getPage(16)
    text = pageObject. extractText()
    pdfFileObject.close()

# tic = time.time()
# pages = extract_pages((file))

# i= 0
# for page in pages:
#     i += 1
#     print(i)
#     if i<15:
#         continue
#     for element in page:
#         if isinstance(element, LTTextContainer):
#             print(element.get_text())
            # for text_line in element:
            #     if tp == 1:
            #         break
            #     for character in text_line:
            #         if isinstance(character, LTChar):
            #             print(character.fontname)
            #             print(character.size)
            #             tp = 1
            #             break

# toc = time.time()
#
# print(toc-tic)

#%% Function to extract MD&A
def extract_mda(file,start_page):
    with open(file, 'rb') as pdfFileObject:
        pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
        print(" No. Of Pages :", pdfReader.numPages)
        pageObject = pdfReader.getPage(start_page)
        text = pageObject.extractText()

        # text = extract_text(file, page_numbers=[start_page])
        found = []
        not_found = []
        mda = []
        temp = []
        i = start_page
        iter = 0
        while len(text):
            if found:
                print(text)
            if text.lower().find('management discussion and analysis') != -1:

                found.append(i)
                print(text)
                if i-1 in not_found and i-2 in found:
                    mda.append(temp)
                mda.append(text)
            else:
                not_found.append(i)
                temp = text
                if i-2 in found and i-1 in not_found:
                    print("Hello")
                    if len(mda)>1:
                        pdfFileObject.close()
                        return mda
                    if iter == 1:
                        if len(mda) < len(prev_mda):
                            pdfFileObject.close()
                            return prev_mda
                        pdfFileObject.close()
                        return mda
                    iter = 1
                    prev_mda = mda
                    mda = []
                else:
                    print("HI")

            if iter >= 2:
                break
            print(i)
            i += 1
            # text = extract_text(file, page_numbers=[i])
            pageObject = pdfReader.getPage(i)
            text = pageObject.extractText()

#%%
file = "data/Reliance2020.pdf"
tic = time.time()
mda = extract_mda(file,5)
toc = time.time()
print(toc-tic)

#%%
summ = 0
for i in mda:
    print(len(i))
    summ += len(i)
print(summ)


