from tkinter import messagebox
import img2pdf


class PdfMaker:
    def __init__(self):
        self.IsFinished = False

    def Make(self, images, output_path):
        '''
        Generate pdf

        param:
            images          : List of image paths
            output_path     : Path to save generated pdf
        '''

        try:
            with open(output_path, 'wb') as op:
                converted = img2pdf.convert(images)
                op.write(converted)

        except PermissionError:
            messagebox.showerror('ERR', f'Cannot save pdf to: {output_path}')

        except:
            messagebox.showerror('ERR', 'Something went wrong')
