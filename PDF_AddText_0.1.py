import tkinter as tk
from tkinter import filedialog, simpledialog, Canvas, Frame, Scrollbar, HORIZONTAL, VERTICAL
import pandas as pd
import fitz  # PyMuPDF
import os
import time
from PIL import Image, ImageTk


def select_files_and_height():
    root = tk.Tk()
    root.withdraw()

    pdf_file_path = filedialog.askopenfilename(title="选择 PDF 文件", filetypes=[("PDF 文件", "*.pdf")])
    if not pdf_file_path:
        print("未选择 PDF 文件，正在退出。")
        return None, None, None

    excel_file_path = filedialog.askopenfilename(title="选择 Excel 文件", filetypes=[("Excel 文件", "*.xlsx;*.xls")])
    if not excel_file_path:
        print("未选择 Excel 文件，正在退出。")
        return None, None, None

    preview_win = tk.Toplevel(root)
    preview_win.title("PDF 高度预览")

    # Load the first page of the PDF document
    pdf_document = fitz.open(pdf_file_path)
    first_page = pdf_document[0]
    pix = first_page.get_pixmap()
    image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    img = ImageTk.PhotoImage(image)

    canvas = Canvas(preview_win, width=pix.width, height=pix.height)
    canvas.pack(side=tk.TOP, padx=5, pady=5)
    canvas.create_image(0, 0, anchor=tk.NW, image=img)

    def update_preview(event):
        height_ratio = height_scale.get() / 100.0
        canvas.delete("preview_line")
        y_position = pix.height * height_ratio
        canvas.create_line(0, y_position, pix.width, y_position, fill="red", tags="preview_line")

    height_scale = tk.Scale(preview_win, from_=0, to=100, orient=HORIZONTAL, command=update_preview)
    height_scale.set(86)
    height_scale.pack(side=tk.TOP, padx=5, pady=5)

    submit_button = tk.Button(preview_win, text="确认", command=preview_win.quit)
    submit_button.pack(side=tk.TOP, padx=5, pady=5)

    preview_win.mainloop()

    height_ratio = height_scale.get() / 100.0
    preview_win.destroy()

    return pdf_file_path, excel_file_path, height_ratio


def add_excel_text_to_pdf(pdf_path, excel_path, font_path, height_ratio):
    try:
        df = pd.read_excel(excel_path, engine='openpyxl')
        print("处理中，请等候。。。")
    except Exception as e:
        print(f"读取 Excel 文件时出错: {e}")
        return
    if df.shape[1] < 2:
        print("Excel 文件没有至少两个列.")
        return

    pdf_document = fitz.open(pdf_path)
    fontsize = 12
    color = (0, 0, 0)

    for index, page in enumerate(pdf_document):
        if index >= len(df):
            break

        text1 = str(df.iloc[index, 0])
        text2 = str(df.iloc[index, 1])
        combined_text = f"{text1} {text2}"

        rect = page.rect
        text_rect = fitz.Rect(0, rect.height * height_ratio, rect.width, rect.height)

        try:
            page.insert_textbox(text_rect, combined_text, fontsize=fontsize, fontname="simsun", fontfile=font_path,
                                color=color, align=fitz.TEXT_ALIGN_CENTER)
        except Exception as e:
            print(f"插入文本框时出错: {e}")
            return

    updated_pdf_path = "updated_" + os.path.basename(pdf_path)

    try:
        pdf_document.save(updated_pdf_path)
        print(f"更新后的 PDF 已保存为 {updated_pdf_path}")
    except Exception as e:
        print(f"保存 PDF 文件时出错: {e}")
        timestamp = time.strftime("%Y%m%d%H%M%S")
        updated_pdf_path = f"updated_{timestamp}_" + os.path.basename(pdf_path)
        try:
            pdf_document.save(updated_pdf_path)
            print(f"更新后的 PDF 已保存为 {updated_pdf_path}")
        except Exception as e:
            print(f"保存 PDF 文件时再次出错: {e}")
    finally:
        pdf_document.close()


if __name__ == "__main__":
    pdf_path, excel_path, height_ratio = select_files_and_height()
    if pdf_path and excel_path and height_ratio is not None:
        font_path = r'C:\Windows\Fonts\simsun.ttc'
        add_excel_text_to_pdf(pdf_path, excel_path, font_path, height_ratio)