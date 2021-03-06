# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 16:36:59 2021

@author: LaoHu

$ pip install pdf2docx
"""
import argparse
from pdf2docx import Converter

def main(pdf_file,docx_file):
    cv = Converter(pdf_file)
    cv.convert(docx_file, start=0, end=None)
    cv.close()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf_file",type=str)
    parser.add_argument('--docx_file',type=str)
    args = parser.parse_args()
    main(args.pdf_file,args.docx_file)

"""
python pdf2word.py --pdf_file  pdf文件路径\example.pdf --docx_file 输出word文件的路径\example.docx
"""