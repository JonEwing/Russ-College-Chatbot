import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import pandas as pd

# A few notes, when import excel is clicked and the proper fileis chosen
# there will be no indication of success and the window will stay open, 
# It worked just close the window.
#
# Also sometimes but not always the extra space at the end of the russ_college.yml file 
# makes the program error. Deleting the last empty line fixes the error.

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue')
canvas1.pack()

def getExcel ():
    global file, questions, answers
    ques = []
    ans = []

    pd.set_option("display.max_colwidth", 10000)
    import_file_path = filedialog.askopenfilename()
    file = pd.read_excel (import_file_path)
    answers = pd.DataFrame(file, columns= ['answer'])
    questions = pd.DataFrame(file, columns= ['question'])

    for index, row in questions.iterrows():
        s = "- - " + row.to_string()[12:]
        ques.append(s)


    for index, row in answers.iterrows():
        d = "  - " + row.to_string()[10:]
        ans.append(d)


    i = answers.shape[0] 

    path = Path("../../ChatBot/responses")

    file_path = path / "russ_college.yml"

    yaml_file_path = open(file_path, "w+")

    yaml_file_path.write("categories:")
    yaml_file_path.write('\n')
    yaml_file_path.write("- unsorted")
    yaml_file_path.write('\n')
    yaml_file_path.write('\n')
    yaml_file_path.write("conversations:")

    for index, row in answers.iterrows():
        yaml_file_path.write('\n')
        yaml_file_path.write(ques[index])
        yaml_file_path.write('\n')
        yaml_file_path.write(ans[index])
        if index < i:
            yaml_file_path.write('\n')   

    yaml_file_path.close()

browseButton_Excel = tk.Button(text='Import Excel File', command=getExcel, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 150, window=browseButton_Excel)

root.mainloop()
