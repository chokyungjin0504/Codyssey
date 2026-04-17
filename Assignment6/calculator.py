# calculator.py
# 파이썬 3.x 버전에서 동작하는 간단한 계산기 프로그램
# 유의사항: Python 기본 내장 기능만 사용, 함수 정의 활용, 코딩 스타일 준수
# 보너스 과제: '451' 연산을 특별히 구현 (입력값에 451을 곱하는 기능)

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit

class Calculator(QWidget):
    def __init__(self):
        # QWidget 초기화
        super().__init__()
        # UI 초기화 함수 실행
        self.initUI()

    def initUI(self):
        """
        계산기 UI 초기화
        - 결과 표시창(QLineEdit)
        - 버튼(QPushButton) 생성 및 배치
        - 레이아웃(QGridLayout) 구성
        """

        # 계산 결과를 표시할 입력창 생성
        self.display = QLineEdit(self)
        self.display.setReadOnly(True)  # 직접 입력 불가
        self.display.setStyleSheet("font-size: 20px; height: 40px;")

        # 버튼들을 배치할 그리드 레이아웃 생성
        grid = QGridLayout()
        grid.addWidget(self.display, 0, 0, 1, 4)

        # 버튼 목록 정의 (텍스트, 행, 열)
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('AC', 5, 0), ('%', 5, 1), ('451', 5, 2)  # 보너스 과제 버튼 추가
        ]

        # 버튼 생성 및 이벤트 연결
        for text, row, col in buttons:
            button = QPushButton(text, self)
            button.setStyleSheet("font-size: 18px; height: 40px;")
            grid.addWidget(button, row, col)
            button.clicked.connect(lambda checked, t=text: self.onButtonClick(t))

        # 레이아웃 적용
        self.setLayout(grid)
        self.setWindowTitle('Calculator')
        self.setGeometry(300, 300, 300, 300)
        self.show()

    def onButtonClick(self, char):
        """
        버튼 클릭 시 동작 정의
        - AC: 입력창 초기화
        - = : 수식 계산
        - % : 백분율 계산
        - 451: 보너스 연산 (현재 값에 451 곱하기)
        - 그 외: 입력창에 문자 추가
        """
        if char == 'AC':
            self.display.setText('')
        elif char == '=':
            try:
                result = str(eval(self.display.text()))
                self.display.setText(result)
            except Exception:
                self.display.setText('Error')
        elif char == '%':
            try:
                value = float(self.display.text())
                self.display.setText(str(value / 100))
            except Exception:
                self.display.setText('Error')
        elif char == '451':
            try:
                # 현재 입력된 값을 숫자로 변환 후 451 곱하기
                value = float(self.display.text())
                self.display.setText(str(value * 451))
            except Exception:
                self.display.setText('Error')
        else:
            self.display.setText(self.display.text() + char)

# 프로그램 실행 진입점
if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    sys.exit(app.exec_())