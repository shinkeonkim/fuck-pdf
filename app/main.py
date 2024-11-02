import sys

from delete_pdf_page import DeletePDFPage
from merge_pdf_page import MergePDFPage
from odd_even_merge_page import OddEvenMergePage
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)
from rotate_pdf_page import RotatePDFPage  # rotate_pdf_page import


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fuck PDF")
        self.resize(1000, 800)  # 창 크기 설정
        self.initLayout()

    def initLayout(self):
        # 메인 레이아웃
        main_layout = QVBoxLayout()

        # 현재 페이지 라벨 (상단 영역)
        self.current_page_label = QLabel("PDF 병합 기능")
        self.current_page_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(self.current_page_label)

        # 수평 레이아웃: 왼쪽 버튼 레이아웃과 오른쪽 스택 위젯
        content_layout = QHBoxLayout()

        # 왼쪽의 기능 선택 버튼 레이아웃
        button_layout = QVBoxLayout()
        button_layout.setSpacing(15)  # 버튼 간격 설정
        button_layout.setContentsMargins(10, 10, 10, 10)  # 레이아웃 여백 설정
        content_layout.addLayout(button_layout, 1)  # 좌측 버튼 레이아웃 크기 비율 설정

        # 오른쪽의 페이지 표시 영역
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(
            self.stacked_widget, 4
        )  # 오른쪽 페이지 레이아웃 크기 비율 설정

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

        # 기능 페이지 추가
        self.merge_pdf_page = MergePDFPage()
        self.delete_pdf_page = DeletePDFPage()
        self.odd_even_merge_page = OddEvenMergePage()
        self.rotate_pdf_page = RotatePDFPage()  # 새 회전 기능 페이지

        # 스택 위젯에 페이지 추가
        self.stacked_widget.addWidget(self.merge_pdf_page)
        self.stacked_widget.addWidget(self.delete_pdf_page)
        self.stacked_widget.addWidget(self.odd_even_merge_page)
        self.stacked_widget.addWidget(self.rotate_pdf_page)  # 회전 기능 페이지 추가

        # 메인 화면 버튼 설정
        self.add_main_buttons(button_layout)

        # 기본 페이지를 PDF 병합 기능 페이지로 설정
        self.stacked_widget.setCurrentWidget(self.merge_pdf_page)

    def add_main_buttons(self, layout):
        # PDF 병합 기능 버튼
        merge_button = QPushButton("PDF 병합 기능")
        merge_button.clicked.connect(
            lambda: self.change_page(self.merge_pdf_page, "PDF 병합 기능")
        )
        layout.addWidget(merge_button)

        # PDF 페이지 삭제 기능 버튼
        delete_button = QPushButton("PDF 페이지 삭제")
        delete_button.clicked.connect(
            lambda: self.change_page(self.delete_pdf_page, "PDF 페이지 삭제")
        )
        layout.addWidget(delete_button)

        # 홀수/짝수 병합 기능 버튼
        odd_even_merge_button = QPushButton("PDF 홀수/짝수 병합 기능")
        odd_even_merge_button.clicked.connect(
            lambda: self.change_page(
                self.odd_even_merge_page, "PDF 홀수/짝수 병합 기능"
            )
        )
        layout.addWidget(odd_even_merge_button)

        # PDF 페이지 회전 기능 버튼
        rotate_button = QPushButton("PDF 페이지 회전 기능")  # 새 버튼
        rotate_button.clicked.connect(
            lambda: self.change_page(self.rotate_pdf_page, "PDF 페이지 회전 기능")
        )
        layout.addWidget(rotate_button)

        # 하단에 여백을 추가해 버튼이 위에 밀집되도록 설정
        layout.addStretch()

    def change_page(self, page, title):
        """페이지 전환 및 현재 페이지 라벨 업데이트 함수"""
        self.stacked_widget.setCurrentWidget(page)
        self.current_page_label.setText(title)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
