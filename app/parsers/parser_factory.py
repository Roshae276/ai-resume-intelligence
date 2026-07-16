import os

from app.parsers.pdf_parser import PDFParser
from app.parsers.docx_parser import DOCXParser


class ParserFactory:

    @staticmethod
    def get_parser(file_path: str):

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            return PDFParser()

        if extension == ".docx":
            return DOCXParser()

        raise ValueError("Unsupported file type.")