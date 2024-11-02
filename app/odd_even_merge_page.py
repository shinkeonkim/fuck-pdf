from PyPDF2 import PdfReader, PdfWriter
from PyQt5.QtWidgets import QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget


class OddEvenMergePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF 홀수/짝수 병합 기능 페이지")

        # 레이아웃 설정
        layout = QVBoxLayout()

        # 홀수 파일 선택 버튼 및 라벨
        self.odd_label = QLabel("홀수 페이지 PDF: 선택된 파일 없음")
        layout.addWidget(self.odd_label)
        self.odd_button = QPushButton("홀수 페이지 PDF 선택")
        self.odd_button.clicked.connect(self.select_odd_pdf)
        layout.addWidget(self.odd_button)

        # 짝수 파일 선택 버튼 및 라벨
        self.even_label = QLabel("짝수 페이지 PDF: 선택된 파일 없음")
        layout.addWidget(self.even_label)
        self.even_button = QPushButton("짝수 페이지 PDF 선택")
        self.even_button.clicked.connect(self.select_even_pdf)
        layout.addWidget(self.even_button)

        # 병합 및 저장 버튼
        self.merge_button = QPushButton("PDF 홀수/짝수 병합 및 저장")
        self.merge_button.clicked.connect(self.save_merged_pdf)
        layout.addWidget(self.merge_button)

        self.setLayout(layout)
        self.odd_pdf_path = None  # 홀수 페이지 파일 경로 저장
        self.even_pdf_path = None  # 짝수 페이지 파일 경로 저장

    def select_odd_pdf(self):
        # 홀수 페이지 PDF 파일 선택
        file_path, _ = QFileDialog.getOpenFileName(
            self, "홀수 페이지 PDF 선택", "", "PDF Files (*.pdf)"
        )
        if file_path:
            self.odd_pdf_path = file_path
            self.odd_label.setText(f"Odd Pages PDF: {file_path}")

    def select_even_pdf(self):
        # 짝수 페이지 PDF 파일 선택
        file_path, _ = QFileDialog.getOpenFileName(
            self, "짝수 페이지 PDF 선택", "", "PDF Files (*.pdf)"
        )
        if file_path:
            self.even_pdf_path = file_path
            self.even_label.setText(f"Even Pages PDF: {file_path}")

    def save_merged_pdf(self):
        # 두 PDF 파일이 선택되었는지 확인
        if not self.odd_pdf_path or not self.even_pdf_path:
            return

        # PDF 파일을 병합하기 위한 PdfWriter 인스턴스 생성
        writer = PdfWriter()
        odd_reader = PdfReader(self.odd_pdf_path)
        even_reader = PdfReader(self.even_pdf_path)

        # 두 파일의 페이지를 번갈아 가면서 추가
        max_pages = max(len(odd_reader.pages), len(even_reader.pages))
        for i in range(max_pages):
            if i < len(odd_reader.pages):
                writer.add_page(odd_reader.pages[i])
            if i < len(even_reader.pages):
                writer.add_page(even_reader.pages[i])

        # 병합된 PDF 파일 저장
        output_path, _ = QFileDialog.getSaveFileName(
            self, "Save Merged PDF", "", "PDF Files (*.pdf)"
        )
        if output_path:
            with open(output_path, "wb") as f:
                writer.write(f)
