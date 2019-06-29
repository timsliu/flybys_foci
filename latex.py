# helper functions for LaTex output
#
# Table of contents
# make_table  - turns a python list into a LaTex formatted table
# text2tex    - converts plain formatted text string into
#               LaTex format by handling quotation marks and special
#               characters
# excel2pdf   - main function for converting excel spreadsheet to
#               a pdf
# parse_sheet - parse a single excel sheet; helper for excel2pdf
# list2string - convert an excel formatted list to a string
#               helper function for excel2pdf


# Revision history
# 06/26/19    Tim Liu    copied make_table from b2_extra.py
# 06/26/19    Tim Liu    wrote text2tex
# 06/26/19    Tim Liu    copied make_pdf main and helper functions - 
#                        TODO make functions generic


# libraries
import pandas as pd
import datetime as dt
import math

# TODO - remove global variables and make generic
# global - workbook to open
# WORKBOOK = "test.xlsx"           # excel workbook to open and parse
WORKBOOK = "feedback.xlsx"

# global - list of sheets in workbook; MUST match sheets of WORKBOOK

# sheets in the test excel file
TEST_SHEETS = ["Planes", "Trains"]                 
# sheets in the actual answer excel
ANSWER_SHEETS = ["OS and PDK", "Dev kit", "Tools", "Use cases", "Additional"]
# match sheets to the file being read       
SHEETS = ANSWER_SHEETS


def make_table(c, r, data, title):
    '''prints string of latex formatted table
    inputs: c - list of colum labels
            r - list of row labels
            data - 2D array of data
            title - title of plot
    outputs: prints latex string
    return: none'''
    
    #print formatting
    print('\\begin{center}')
    print('\\begin{tabular}{' + (len(c) + 1)* '|m{1.7 cm}', '|}')
    print('\hline')
    print('\multicolumn{%d}{|c|}{%s}\\\ \hline' %((len(c)+1), title))
    for col in c:
        print('&', col, end='')
    print('\\\ \hline')
    #iterate through data and print data
    for row in range(len(r)):
        print(r[row], end='  ')        
        for col in range(len(c)):
            print(' & ', '%.3f' %data[col][row], end = '')
        print('\\\ \hline')
    print('\end{tabular}')
    print('\end{center}')
    return


def text2tex(f_in_name, f_out_name):
    '''converts a plain text string to a LaTex formatted
    string. Currently corrects double quotation marks and the following
    special characters: #, %, &, $, >, <
    inputs: f_in_name - input file name
            f_out_name - output file name

    the tex string is saved to a text file under the name f_out_name.
    The function does not handle double nested quotes'''

    print("Parsing file: ", f_in_name)

    
    f_in = open(f_in_name, "r")       # open the input file w/ plaintext
    input_string = f_in.read()        # read contents of the file
    output_string = ""                # string to output

    # convert quotation marks to open and close marks
    open_quote = False                # flag for indicating if quote is open
    for char in input_string:
        if char != '"':
            # directly copy any non quotation character
            output_string += char
        else:
            # handle quotation marks
            if open_quote:
                # close quote
                output_string += "``"
                open_quote = False
            else:
                # start of a new quote
                output_string += '"'
                open_quote = True

    # handle special characters
    output_string = output_string.replace("#", "\\#")
    output_string = output_string.replace("%", "\\%")
    output_string = output_string.replace("&", "\\&")
    output_string = output_string.replace("$", "\\$")
    output_string = output_string.replace(">", "$>$")
    output_string = output_string.replace("<", "$<$")

    # open output file
    f_out = open(f_out_name, "w", encoding='utf-8')
    f_out.write(output_string)

    # close input file and generated file
    f_in.close()
    f_out.close()

    print("Tex format file saved!")

    return





def excel2pdf():
    '''main function - opens input spreadsheet and generates LaTex output
    '''

    print("Generating LaTeX from: ", WORKBOOK)

    output_string = ""                  # output string to write to .tex file

    header = open("header.txt", "r");        # open file with LaTeX header
    # format target name to include time
    currentDT = dt.datetime.now()
    timestamp = currentDT.strftime("%m-%d_%H-%M")
    target_name = "target_" + timestamp + ".tex"
    # open target file to write to
    target = open(target_name, "w", encoding='utf-8');

    # read in the header
    header_str = header.read()
    # string to add to the header
    output_string = ""

    # parse each sheet
    for s in SHEETS:
        output_string += "\n\\newpage"
        output_string += "\n\\section{" + s + "}\n"
        output_string += parse_sheet(s)

    # add ending to the file
    output_string += "\n\\end{document}"

    # handle special characters
    output_string = output_string.replace("#", "\\#")
    output_string = output_string.replace("%", "\\%")
    output_string = output_string.replace("&", "\\&")
    output_string = output_string.replace("$", "\\$")
    output_string = output_string.replace(">", "$>$")
    output_string = output_string.replace("<", "$<$")
 
    # write to file
    target.write(header_str + output_string)

    # close header file and TeX output
    header.close()
    target.close()

    print("Done! - " + target_name + " saved :D")

    return

def parse_sheet(s):
    '''parses the excel in a sheet
    inputs: s - sheet name to parse
    outputs: sheet_string - TeX string for the sheet'''

    print("Parsing sheet: ", s)

    # open sheet of excel workbook
    data_sheet = pd.read_excel(WORKBOOK, sheet_name=s)
    response_df = pd.DataFrame(data_sheet)

    # map columns to useful labels
    type_col = response_df.columns[0]     # column identifying question type
    q_col    = response_df.columns[1]     # column identifying question     
    partners = response_df.columns[2:]    # columns with partner names

    
    sheet_string = ""                  # TeX string representation of the sheet
    question_type = "none"             # current question type

    # iterate through the rows
    for index, row in response_df.iterrows():

        # check if row has a new question type
        if row[type_col] != question_type:
            # add subsection with new question category
            sheet_string += "\n\\subsection{" + row[type_col] + "}\n"
            # update to the new question type
            question_type = row[type_col]

        # write the question
        sheet_string += "\n\\textbf{" + row[q_col] + "}\n"
        # list with responses from each partner for a single questions
        q_responses = []
        for partner in partners:
            # extract partner response and add to list
            # include partner name as first field
            q_responses.append([partner, row[partner]])
        # convert partner list to string
        sheet_string += list2string(q_responses)

    # close excel file
    # print what had been parsed

    return sheet_string

def list2string(q_responses):
    '''converts the list of partner responses to a LaTeX string
    inputs: q_responses - list of partner responses [[partner, response]]
    outputs: q_string - string representing responses to a question'''

    # TODO - sort the response by persona

    # string for each question
    q_string = ""

    for response in q_responses:
        # convert response to LaTeX format
        if type(response[1]) != type("string") and math.isnan(response[1]):
            # response is blank - skip and go on to next respondent
            continue
        q_string += "\n\\underline{" + response[0] + ":} "
        q_string += "\n" + str(response[1]) + "\n"

    return q_string

