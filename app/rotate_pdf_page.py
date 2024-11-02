import fitz  # PyMuPDF for PDF rendering (pip install pymupdf)
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


class RotatePDFPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF 페이지 회전 기능")

        # 레이아웃 설정
        layout = QVBoxLayout()

        # PDF 파일 선택 라벨 및 버튼
        self.label = QLabel("아직 PDF 파일이 선택되지 않았습니다.")
        layout.addWidget(self.label)
        self.select_button = QPushButton("PDF 파일 불러오기")
        self.select_button.clicked.connect(self.select_pdf_file)
        layout.addWidget(self.select_button)

        # 스크롤 영역에 PDF 페이지 미리보기 리스트 추가
        self.pdf_list = QListWidget()
        self.pdf_list.verticalScrollBar().setSingleStep(10)  # 스크롤 속도 조절
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.pdf_list)
        layout.addWidget(self.scroll_area)

        # 회전 버튼
        self.rotate_clockwise_button = QPushButton("시계 방향으로 90° 회전")
        self.rotate_clockwise_button.clicked.connect(lambda: self.rotate_page(90))
        layout.addWidget(self.rotate_clockwise_button)

        self.rotate_counterclockwise_button = QPushButton("반시계 방향으로 90° 회전")
        self.rotate_counterclockwise_button.clicked.connect(
            lambda: self.rotate_page(-90)
        )
        layout.addWidget(self.rotate_counterclockwise_button)

        # 저장 버튼
        self.save_button = QPushButton("변경된 PDF 저장")
        self.save_button.clicked.connect(self.save_rotated_pdf)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.pdf_file_path = None
        self.pdf_document = None
        self.rotations = {}  # 각 페이지의 회전 상태 저장

    def select_pdf_file(self):
        # PDF 파일 선택
        file_path, _ = QFileDialog.getOpenFileName(
            self, "PDF 파일 선택", "", "PDF Files (*.pdf)"
        )
        if file_path:
            self.pdf_file_path = file_path
            self.label.setText(f"Selected PDF: {file_path}")
            self.load_pdf_pages()

    def load_pdf_pages(self):
        # PDF 파일의 페이지를 미리보기로 로드
        self.pdf_list.clear()
        self.pdf_document = fitz.open(self.pdf_file_path)

        for page_number in range(len(self.pdf_document)):
            self.add_page_preview(page_number)

    def add_page_preview(self, page_number):
        """지정된 페이지 번호에 대한 미리보기를 추가합니다."""
        pix = self.pdf_document[page_number].get_pixmap(
            matrix=fitz.Matrix(0.5, 0.5)
        )  # 확대율 조정
        img = QImage(
            pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888
        )

        # 미리보기 이미지와 텍스트 라벨 생성
        item_widget = QWidget()
        item_layout = QVBoxLayout()

        image_label = QLabel()
        image_label.setPixmap(QPixmap.fromImage(img))
        page_label = QLabel(f"Page {page_number + 1}")
        page_label.setAlignment(Qt.AlignCenter)

        item_layout.addWidget(image_label)
        item_layout.addWidget(page_label)
        item_widget.setLayout(item_layout)

        # QListWidget에 아이템 추가
        item = QListWidgetItem()
        item.setData(Qt.UserRole, page_number)  # page_number 저장
        self.pdf_list.addItem(item)
        self.pdf_list.setItemWidget(item, item_widget)
        item.setSizeHint(item_widget.sizeHint())  # 아이템 크기 조정

        # 초기 회전 상태
        self.rotations[page_number] = 0

    def rotate_page(self, angle):
        # 선택된 페이지를 회전
        selected_items = self.pdf_list.selectedItems()
        if selected_items:
            for item in selected_items:
                page_number = item.data(Qt.UserRole)
                if page_number is None:
                    continue

                # 현재 회전 상태 업데이트
                self.rotations[page_number] += angle
                self.rotations[page_number] %= 360  # 360도 내로 유지

                # 미리보기를 새 회전 상태로 업데이트
                page = self.pdf_document[page_number]
                pix = page.get_pixmap(
                    matrix=fitz.Matrix(0.5, 0.5).prerotate(self.rotations[page_number])
                )
                img = QImage(
                    pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888
                )

                # 기존 미리보기 이미지 업데이트
                item_widget = self.pdf_list.itemWidget(item)
                image_label = item_widget.layout().itemAt(0).widget()
                image_label.setPixmap(QPixmap.fromImage(img))

    def save_rotated_pdf(self):
        if not self.pdf_file_path or not self.pdf_document:
            return

        # 회전이 적용된 PDF 파일 생성
        output_path, _ = QFileDialog.getSaveFileName(
            self, "PDF 파일 저장", "", "PDF Files (*.pdf)"
        )
        if output_path:
            for page_number, rotation in self.rotations.items():
                self.pdf_document[page_number].set_rotation(rotation)

            # 파일 저장 (PDF 열려 있도록 유지)
            self.pdf_document.save(output_path)
