import fitz  # PyMuPDF for PDF rendering (pip install pymupdf)
from PyPDF2 import PdfReader, PdfWriter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
    QFileDialog,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class DeletePDFPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF 페이지 삭제 기능 페이지")

        # 레이아웃 설정
        layout = QVBoxLayout()

        # PDF 미리보기 리스트를 스크롤 영역에 추가
        self.pdf_list = QListWidget()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.pdf_list)
        layout.addWidget(self.scroll_area)

        # 파일 불러오기 버튼
        self.load_button = QPushButton("PDF 파일 선택")
        self.load_button.clicked.connect(self.load_pdf)
        layout.addWidget(self.load_button)

        # 페이지 삭제 버튼
        self.delete_button = QPushButton("선택한 페이지 삭제")
        self.delete_button.clicked.connect(self.delete_page)
        layout.addWidget(self.delete_button)

        # 변경된 파일 저장 버튼
        self.save_button = QPushButton("변경된 PDF 저장")
        self.save_button.clicked.connect(self.save_pdf)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.pdf_data = None
        self.pdf_file_path = None
        self.pages_to_keep = []  # 유지할 페이지 목록을 저장

        # 스크롤 속도 조절
        self.pdf_list.verticalScrollBar().setSingleStep(
            10
        )  # 스크롤 속도를 조절하는 값 (기본값은 20)

    def load_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "PDF 파일 선택", "", "PDF Files (*.pdf)"
        )
        if file_path:
            self.pdf_data = PdfReader(file_path)
            self.pdf_file_path = file_path
            self.pdf_list.clear()
            self.pages_to_keep = list(
                range(len(self.pdf_data.pages))
            )  # 초기화: 모든 페이지 유지

            # PDF 페이지 미리보기 추가
            for page_number in range(len(self.pdf_data.pages)):
                self.add_page_preview(page_number)

    def add_page_preview(self, page_number):
        """지정된 페이지 번호에 대한 미리보기를 추가합니다."""
        pix = (
            fitz.open(self.pdf_file_path)
            .load_page(page_number)
            .get_pixmap(matrix=fitz.Matrix(1, 1))
        )
        img = QImage(
            pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888
        )

        # QListWidgetItem으로 아이템을 추가하고 아이템에 QLabel을 배치
        item_widget = QWidget()
        item_layout = QVBoxLayout()

        # 이미지와 텍스트 라벨 생성
        image_label = QLabel()
        image_label.setPixmap(QPixmap.fromImage(img))
        page_label = QLabel(
            f"Page {page_number + 1}"
        )  # 여기서 page_number는 전체 페이지 인덱스가 아니라 실제 번호를 매깁니다
        page_label.setAlignment(Qt.AlignCenter)

        # 레이아웃에 이미지와 텍스트 라벨 추가
        item_layout.addWidget(image_label)
        item_layout.addWidget(page_label)
        item_widget.setLayout(item_layout)

        # QListWidget에 최종 항목 추가
        item = QListWidgetItem()
        self.pdf_list.addItem(item)
        self.pdf_list.setItemWidget(item, item_widget)
        item.setSizeHint(item_widget.sizeHint())  # 아이템 크기 조정

    def delete_page(self):
        selected_items = self.pdf_list.selectedItems()
        if selected_items:
            for item in selected_items:
                row = self.pdf_list.row(item)
                self.pdf_list.takeItem(row)
                if row in self.pages_to_keep:
                    self.pages_to_keep.remove(row)  # 유지할 페이지에서 삭제

            # 페이지 삭제 후 페이지 번호 라벨 업데이트
            self.update_page_labels()

    def update_page_labels(self):
        """페이지 번호 라벨을 삭제 후 새로 업데이트합니다."""
        # pages_to_keep을 인덱스 0부터 다시 설정
        self.pages_to_keep = list(range(len(self.pages_to_keep)))
        self.pdf_list.clear()  # 모든 항목 제거 후 새로 추가

        # 유지할 페이지에 대한 미리보기와 번호 재설정
        for new_index in self.pages_to_keep:
            self.add_page_preview(new_index)

    def save_pdf(self):
        if not self.pdf_data:
            return
        writer = PdfWriter()

        # 유지할 페이지만 추가
        for page_num in self.pages_to_keep:
            writer.add_page(self.pdf_data.pages[page_num])

        output_path, _ = QFileDialog.getSaveFileName(
            self, "PDF 파일 저장", "", "PDF Files (*.pdf)"
        )
        if output_path:
            with open(output_path, "wb") as f:
                writer.write(f)
