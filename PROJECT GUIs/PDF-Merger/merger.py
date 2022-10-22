import os
import subprocess
from PyPDF2 import PdfReader, PdfMerger


class Merger:
    def __init__(self):
        self.IsFinished = False

    def Merge(self, output_path, pdfs, listbox, window):
        '''
        Merge pdfs

        param:
            output_path : path to save the output-pdf
            pdfs        : List of pdf paths to merge
            listbox     : Listbox object to delete all contents
            window      : Tk object to open the location of generated pdf
        '''

        merger = PdfMerger()

        for pdf in pdfs:
            reader = PdfReader(pdf)
            merger.append(reader)

        merger.write(output_path)
        self.IsFinished = True

        listbox.delete(0, 'end')
        window.after(1100, lambda: subprocess.run([os.path.join(os.getenv('WINDIR'), 'explorer.exe'), '/select,', os.path.normpath(output_path)]))
