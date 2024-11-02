from PyPDF2 import PdfReader, PdfWriter
from PyQt5.QtWidgets import (
    QFileDialog,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MergePDFPage(QWidget):
    def __init__(self):
        super().__init__()

        # 레이아웃 설정
        layout = QVBoxLayout()

        # PDF 파일 리스트
        self.pdf_list = QListWidget()
        self.pdf_list.setDragDropMode(QListWidget.InternalMove)  # 드래그 앤 드롭 활성화
        layout.addWidget(self.pdf_list)

        # 파일 추가 버튼
        self.add_files_button = QPushButton("PDF 파일 추가하기")
        self.add_files_button.clicked.connect(self.add_files)
        layout.addWidget(self.add_files_button)

        # 파일 제거 버튼
        self.remove_file_button = QPushButton("선택한 파일 제거")
        self.remove_file_button.clicked.connect(self.remove_selected_file)
        layout.addWidget(self.remove_file_button)

        # 병합 및 저장 버튼
        self.save_button = QPushButton("PDF 파일 병합 및 저장")
        self.save_button.clicked.connect(self.save_merged_pdf)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.pdf_files = []  # 병합할 PDF 파일 리스트

    def add_files(self):
        # 파일 선택 대화상자 열기
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Select PDF Files", "", "PDF Files (*.pdf)"
        )
        for file_path in file_paths:
            # PDF 파일 경로를 QListWidget에 추가
            item = QListWidgetItem(file_path)
            self.pdf_list.addItem(item)

    def remove_selected_file(self):
        # 선택된 파일을 제거
        selected_items = self.pdf_list.selectedItems()
        if selected_items:
            for item in selected_items:
                row = self.pdf_list.row(item)
                self.pdf_list.takeItem(row)

    def save_merged_pdf(self):
        # PdfWriter 객체 생성
        writer = PdfWriter()

        # 현재 QListWidget의 순서대로 PDF 파일을 읽고 병합
        for index in range(self.pdf_list.count()):
            file_path = self.pdf_list.item(
                index
            ).text()  # 조정된 순서의 파일 경로 가져오기
            reader = PdfReader(file_path)
            for page in reader.pages:
                writer.add_page(page)

        # 병합된 PDF 파일 저장
        output_path, _ = QFileDialog.getSaveFileName(
            self, "Save Merged PDF", "", "PDF Files (*.pdf)"
        )
        if output_path:
            with open(output_path, "wb") as f:
                writer.write(f)
