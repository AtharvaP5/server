
#!/usr/bin/env python
# coding: utf-8

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Route definitions and other code...

if __name__ == '__main__':
    app.run()



import PyPDF2
import re
import string
import pandas as pd


def main():
    pdf_file = open('MCA_Sem_II_Rev_Course_Aug_Exam_2021.pdf', 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    # for subjects related things
    page = pdf_reader.pages[2]

    text = page.extract_text()

    subject_array = []

    subject_pattern = r'\s*\d.([A-Z]{3,}\d{2,})\s*([A-Z\s/]{1,})'
    for i in text.splitlines():
        subject_matches = re.findall(subject_pattern, i)
        if re.match(subject_pattern, i):
            for match in subject_matches:
                item = (match[0], match[1].strip())
                subject_array.append(item)

    # print(subject_array)

    for x in range(len(subject_array)):
        if (x == 3):
            y = ("E1", "Elective 1")
            subject_array[x] = y
        if (x == 4):
            y = ("E2", "Elective 2")
            subject_array[x] = y

    # print(subject_array)

    # print()

    names = []  # Array of student names
    marks = []  # Array of student marks
    total_marks = []

    thirdA = ('A', 'F', 'A', 'F', '--', '--', '--', '--', '--', '|', 'A', '--',
              '--', '--', '--', '|', 'A', 'F', 'A', 'F', '--', '--', '--', '--', '--')

    for i in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[i]
        text = page.extract_text()
    # print(text)

    # patterns

    namepat = r"^\s*(\d+)\s+([/A-Z\s]+)\s+([0-9\s]+)"

#     electivePattern = r"^\s*\((ELECTIVE \d+)\s*:\s*([A-Z\d]+)\s*:\s*([^)]+)\)"

    elp = r'\s*\((\w+\s*\d)\s*:(\w+):([^)]+)'

    subject_pattern = r"\d+\.([A-Z]+\d+)\s+([A-Z\s*/]+)"

    flp1 = r'^\s+(\d+|\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*([A-Z]+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(\w+)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*([A-Z])'

    flp2 = r'^\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(\w+)\s*(\b\d\b\s\b\d\b|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(\w+)\s*\((\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(\w+)\s*\((\w+)\)\s*(\w+)\s*\((\w+)\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*([A-Z])'

    flp3 = r'^\s+(\d+|\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*([A-Z]+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(\w+)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(\b\d\b\s\b\d\b|--)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*([A-Z])'

    flp4 = r'^\s+(\d+|\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*([A-Z]+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(\w+)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\b\d\s\b\d|--)\s*(\d+|--)\s*([A-Z])\s*'

    slp = r'^\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*'

    tlp1 = r'^\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)(\|)\s*(\w+)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)(\|)\s*(\w+)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)(\|)(\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*'

    tlp2 = r'^\s*(A)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(A)\s+.*'

    tlp3 = r'^\s*(\d+|--)\s*\s*(\d+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*'

    tlp4 = r'^\s*(\w+)\s*\((\w+)\s*\)\s*(\w+)\s*\((\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\b\d\b\s\b\d\b|--)\s*(\d+|--)(\|)\s*(\w+)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)(\|)\s*(\w+)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)(\|)(\w+)\s*\((\w+)\s*\)\s*(\w+)\s*\((\w+)\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*'

    tlp5 = r'^\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)(\|)\s*(\w+)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)(\|)\s*(\w+)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)(\|)(\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\b\d\b\s\b\d\b|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*'

    folp1 = r'^\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(\w+)\s+(\d+|--)\s*(\w+|--)\s*(\w+|--)\s*(\w+|--)'

    folp2 = r'^\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\b\d\b\s\b\d\b|--)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(\w+)\s+(\d+|--)\s*(\w+|--)\s*(\w+|--)\s*(\w+|--)'

    folp3 = r'^\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\d+|--)\s*(\|)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\w+)\s*\(\s*(\w+)\s*\)\s*(\d+|--)\s*(\d+|--)\s*(\w+|--)\s*(\d+|--)\s*(\b\d\b\s\b\d\b|--)\s*(\|)\s*(\w+)\s+(\d+|--)\s*(\w+|--)\s*(\w+|--)\s*(\w+|--)'

    total_marks_pattern = r'^\s*[a-zA-Z\s]+\s*(\d+(?:@\d+)?)\s*\/\s*(\d+|\d+\s*\d*)\s*(\d+)\s*(\d+)\s*(\d+\.\d+|--)\s*'

    # for name,roll no , prn number
    temp = []
    for i in text.splitlines():

        match = re.match(namepat, i)

        if match:
            # print(i)
            # print(re.findall(pattern,i))
            name = match.group(2)
            names.append(name.lstrip('/').strip())
            # print("roll no :", match.group(1), " name : ", name.lstrip(
            #     '/'), "prn : ", match.group(3).replace(" ", ""))

        # for electives
        elm = re.findall(elp, i)  # elm = elective match   #elective pattern
        if re.match(elp, i):
            print(elm)

        # first line of marks
        # flm = first line match   #flp = first line pattern #normal
        flm1 = re.findall(flp1, i)
        # flm = first line mismatch   #flp = first line pattern
        flm2 = re.findall(flp2, i)
        # flm = first line mismatch   #flp = first line pattern
        flm3 = re.findall(flp3, i)
        flm4 = re.findall(flp4, i)  # 118 - rollno
        if re.match(flp1, i):
            # print(flm1)
            for i in flm1:
                temp.append(i)
        elif re.match(flp2, i):
            # print(flm2)
            for i in flm2:
                temp.append(i)
                print(i)
        elif re.match(flp3, i):
            # print(flm3)
            for i in flm3:
                temp.append(i)
        elif re.match(flp4, i):
            # print(flm4)
            for i in flm4:
                temp.append(i)

        # second line of marks
        # slm = second line match = slm     #slp = second line pattern
        slm = re.findall(slp, str(i))
        if re.match(slp, str(i)):
            # print(slm)
            for i in slm:
                temp.append(i)

        # third line of marks
        tlm1 = re.findall(tlp1, str(i))  # normal
        tlm2 = re.findall(tlp2, str(i))  # half absent
        tlm3 = re.findall(tlp3, str(i))  # half absent
        tlm4 = re.findall(tlp4, str(i))  # 129 record mismatch pattern
        tlm5 = re.findall(tlp5, str(i))  # 119 record mismatch pattern

        if re.match(tlp1, str(i)):
            # print(tlm1)
            for i in tlm1:
                temp.append(i)
        elif re.match(tlp4, str(i)):
            # print(tlm4)
            for i in tlm4:
                temp.append(i)
        elif re.match(tlp5, str(i)):
            # print(tlm5)
            for i in tlm5:
                temp.append(i)
        elif re.match(tlp3, str(i)):
            # print(thirdA)
            temp.append(thirdA)

        # fourth line of marks

        # folp1 = fourth line of pattern normal # folm1 = fourth line of marks normal
        folm1 = re.findall(folp1, str(i))
        # folp2 = fourth line of pattern mismatch1 101 line # folm1 = fourth line of marks mismatch
        folm2 = re.findall(folp2, str(i))
        # folp3 = fourth line of pattern mismatch1 125 line # folm1 = fourth line of marks mismatch
        folm3 = re.findall(folp3, str(i))

        if re.match(folp1, str(i)):
            # print(folm1)
            for i in folm1:
                temp.append(i)
            if temp:
                print(temp)
                marks.append(temp)
                temp = []

        elif re.match(folp2, str(i)):
            # print(folm2)
            for i in folm2:
                temp.append(i)
            if temp:
                print(temp)
                marks.append(temp)
                temp = []

        elif re.match(folp3, str(i)):
            # print(folm3)
            for i in folm3:
                temp.append(i)
            if temp:
                print(temp)
                marks.append(temp)
                temp = []

        temp_marks = []
        total_marks_pattern_matches = re.findall(total_marks_pattern, str(i))
        if re.match(total_marks_pattern, str(i)):
            for i in total_marks_pattern_matches:
                for j in i:
                    if j:
                        temp_marks.append(j)
            # print(total_marks_pattern_matches[0])
            # print()
        if temp_marks:

            total_marks.append(temp_marks)


# #for subjects
#     matches = re.finditer(subject_pattern, text)


#     for match in matches:

#             item_dict = {
#                 'Code': match.group(1),
#                 'Subject': match.group(2).strip()
#             }
#             if item_dict not in subject_array:
#                 subject_array.append(item_dict)




    # print(total_marks)




    temp = []

    final = []

    for i in marks:
        for j in i:
            for k in j:

                if not k.isdigit():
                    if not k.strip('EF').isdigit():
                        if not k.replace(" ", "").isdigit():
                            temp.append(k.strip())
                        else:
                            temp.append(int(k.replace(" ", "")))
                    else:
                        temp.append(int(k.strip('EF')))
                else:

                    temp.append(int(k.strip()))

    final.append(temp)
    temp = []

# print(final)   #all students marks

    # print(final[26])  # 1st student marks in single array



    # print(names)




    # print(total_marks_pattern_matches)




    # print(final)





# import pandas as pd

# Create the DataFrame from the 'final' array
    df = pd.DataFrame(final)

# Set the max_columns option to None to display all columns
    pd.set_option('display.max_columns', None)

# Print the DataFrame
    df




    # pip install openpyxl



    # print(final)





# pip install xlsxwriter




    tp1 = []

    c = []

    for i in range(len(final)):
        c = final[i]+total_marks[i]
        tp1.append(c)
        c = []

    # print(tp1)




    df = pd.DataFrame(tp1)

# Assign names to rows and columns
# c = final + total_marks
# df.index = ['SANATH MEGHARAJ NANDINI', 'C VIKRAM ANAND NAGAMMAL', 'CHAVAN ATHARV MILIND MADHURA', 'DESHMUKH OMKAR NANDKUMAR MANGAL', 'DHURI PRAFUL VISHWANATH PALLAVI', 'DURAI NEETHI WILSON JEYAWATHY', 'KASHID KRISHNA DHANAJI CHANDRABHAGA', 'KHANDEKAR DHARMENDRA DEWANAND CHITRA', 'KHARAT SAYALI KACHARU SUNAND A', 'KOLI PRAJAKTA PRAVIN JAGRUTI', 'KOLI PRANAY MORESHWAR HARSHADA', 'KOLI VIKRANTI SANTOSH SUJATA', 'KUMAR SAGAR SUNIL ANITHA', 'MASIH JULIUS JACOB MASIH ARUNA MASIH', 'MAVELIL SANTO JAMES MINI', 'MISTRY HARSH RAJESH MISTRY KALPANA MISTRY', 'MUKALUVILA JINO REJI LALY', 'NAIK SHUBHAM BALASAHEB NAMRATA', 'NAIR GOKUL RAMESH BHADURI', 'NAIR PREETHI MAHESH GIRIJA', 'NANGARE VISHWAJEET BHASKAR MANISHA', 'PARULEKAR RUCHITA AVINASH A ARTI', 'PATIL SACHIN DHONDIBA SANJIVANI', 'PAWAR SAHIL ANANT NAMRATA', 'SAWANT MITHILA AJIT ASHWINI', 'SEMWAL SHIVAM CHANDRA PRAKASH SEMWAL NEELAM SEMWAL', 'SINGH SWARAJ MAHIPAL SADHANA', 'SRAMBIKAL ASHWIN SIVAN BINDU', 'TAMBOLI MAYURI JAN ARDHAN HIRABAI', 'YADAV PRATIKSHA KRISH NAT SANGITA', 'BAGAL AKSHATA APPASAHEB SANGITA', 'BHONG SHREYAS PRAMODRAO VIMAL', 'BISWAS SNEHA RANJAN TRISHNA', 'CHOUDHARY NIKITA HARIRAM PYA RIDEVI', 'DAMDE SAURABH KRISHNA ASHA', 'DEDHIA BHAVYA DINESH PRITI', 'DEVENDRAN MADHUBALAN VELU ESTHER', 'GUPTA ARUN  RITA', 'KANNADA VARSHAJA BHOJA VARIJA', 'KULKARNI SHUBHAM SHEKHAR SMITA', 'KURGHODE OMKAR  SUNIL JAYSHREE', 'LALGE SHUBHAM AVINASH ASHWINI', 'NADAR GOUTHAM RAJENDRAN JAYA', 'NAIK NITIN LAXMAN SUMATI', 'PAITHANKAR OMKAR RAJESH SONALI', 'SALIAN TRUSHA RAMESH HEMALATA', 'SAUDAGAR FARDEEN AYUB MEENAZ', 'SHINDE BHAGWAT POPAT VANDANA', 'SIDDIQUI AHASAN GUFRAN AHMED SIDDIQUI FARZANA SIDD', 'SRIVASTAVA ASHUTOSH KUMAR B P SRIVASTAVA VIBHA', 'THAKUR YASH VIMAL RATNESH']  # Assign row namesz
    subjects = ['MFCS-2_Externals', 'Grade', 'Internal', 'Grade', 'Total', 'Credits', 'Grade', 'Grade Points', 'C*GP', '|', 'MFCS-2', 'MFCS-2', 'MFCS-2', 'MFCS-2', 'MFCS-2', 'MFCS-2', '|', 'AIML-External', 'Grade', 'Internals', 'Grade', 'Total', 'Credit', 'Grade', 'Grade Points', 'C*GP', '|', 'AIML', 'AIML', 'AIML', 'AIML', 'AIML', 'AIML', 'AIML', 'AIML', 'AIML', 'PASS/FAIL', 'IS-External', 'Grade', 'Internals', 'Grade', 'Total', 'Credits', 'Grade', 'Grade Points', 'C*GP', '|', 'Elective-1', 'Grade', '', 'CV', 'CV', 'CV', 'CV', 'CV', 'CV', '|', 'CV', 'CV', 'CV', 'CV', 'CV', 'CV', 'CV', 'CV', 'CV', 'DMBA-Externals',
                'Grade', 'Internals', 'Grade', 'Total', 'Credits', 'Grade', 'Grade Points', 'C*GP', '|', 'DMBA', 'DMBA', 'DMBA', 'DMBA', 'DMBA', 'DMBA', '|', 'SSD-LAB', 'Credits', 'Grade', 'Grade Points', 'C*GP', '|', 'AWT-LAB', 'Grade', 'AWT-Internals', 'Grade', 'Total', 'Credits', 'Grade', 'Grade Points', 'C*GP', 'UI/UX-Lab', 'Grade', 'Internals', 'Grade', 'Total', 'Credit', 'Grade', 'Grade Points', 'C*GP', '|', 'NL-Lab', 'Grade', 'Internals', 'Grade', 'Total', 'Credits', 'Grade', 'Grade points', 'C*GP', '|', 'Mini-project', 'Credits', 'Grade', 'Grade points', 'C*GP', 'Total Marks Obtained', 'Outof', 'Credits', 'CG', 'GPA']

# combine = subjects + total_marks_pattern_matches

    df.index = [names]  # Assign row names
    df.columns = [subjects]  # Assign column names

    df           # Display the DataFrame




    df.shape




    df.info()



    df.describe()




    df[['MFCS-2_Externals']]




    df.to_excel("C:\\Users\\vicky\\Desktop\\sample.xlsx")




    excel = pd.read_excel
    # print(excel)




    df





    print(pdf_file)


