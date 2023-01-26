import os
from tkinter import messagebox
from PyPDF2 import PdfReader, PdfFileWriter


class SplitPDF:
    '''
    Splitting pdf(s) as per user provided information
    '''

    def __init__(self, source_path, des_path, prefix, page_nums, output_frame, output_text_area, root_path=''):
        self.prefix = prefix
        self.des_path = des_path
        self.output_frame = output_frame
        self.output_text_area = output_text_area

        if root_path:
            self.root_path = root_path

        else:
            self.root_path = des_path

        self.page_nums = page_nums
        self.source_path = source_path

    def split(self):
        '''Real splitting is happening here'''

        # Showing output area
        self.output_frame.pack(fill='x')

        # Deleting all previous output log
        self.output_text_area.config(state='normal')
        self.output_text_area.delete('1.0', 'end')
        self.output_text_area.tag_configure('center', justify='center')

        is_duplicate_message_shown = None
        reader = PdfReader(self.source_path)  # Reading pdf

        for page_num in self.page_nums:  # Looping over each page names
            pdfWriter= PdfFileWriter()
            page_labels = f'{self.prefix}({page_num[0]}-{page_num[1]}).pdf'

            for pn in range(page_num[0] - 1, page_num[1]):
                pdfWriter.addPage(reader.getPage(pn))  # Adding pages to one pdf

            if pdfWriter.getNumPages() != 0:
                full_path = os.path.join(self.root_path, page_labels)

                # Confirming user if he/she wants to replace the pdf having same name
                if os.path.exists(full_path):
                    if is_duplicate_message_shown is None:
                        is_duplicate_message_shown = messagebox.askyesno('Confirm?', f'Some files already exists. Do you want to replace ?')

                    if is_duplicate_message_shown is False:
                        continue

                try:
                    # Saving new pdf
                    with open(full_path, 'wb') as fp:
                        pdfWriter.write(fp)
                        self.output_text_area.insert('end', page_labels + ' > Created.\n', 'center')
                        self.output_text_area.see('end')

                except PermissionError:
                    self.output_frame.pack_forget()

                    path = os.path.dirname(self.root_path)
                    messagebox.showerror('ERR', f'{path} does not have the required permission to perform file operations')

                    return

        self.output_text_area.insert('end', '\nCompleted.', 'center')
        self.output_text_area.see('end')
        self.output_text_area.config(state='disabled')

        os.startfile(self.root_path)
