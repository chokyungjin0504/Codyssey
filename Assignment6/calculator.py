# ─────────────────────────────────────────────
# 필요한 모듈(라이브러리) 불러오기
# ─────────────────────────────────────────────

# sys: 파이썬 기본 모듈. 프로그램 종료(sys.exit) 등에 사용
import sys

# PyQt5: 파이썬으로 GUI 창 프로그램을 만들 수 있게 해주는 외부 라이브러리
# QApplication : 앱 전체를 관리하는 객체. PyQt5 프로그램에는 반드시 하나 있어야 함
# QWidget      : 빈 창(Window)을 만드는 기본 클래스. 우리 Calculator 클래스가 이걸 상속받음
# QVBoxLayout  : 위젯을 위→아래(세로) 순서로 쌓아주는 레이아웃
# QGridLayout  : 위젯을 격자(행/열) 형태로 배치하는 레이아웃 (버튼 배열에 사용)
# QPushButton  : 클릭 가능한 버튼 위젯
# QLabel       : 텍스트를 화면에 표시하는 위젯 (숫자 디스플레이에 사용)
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel

# Qt: 정렬 방향 등 다양한 상수값을 제공 (예: Qt.AlignRight = 오른쪽 정렬)
from PyQt5.QtCore import Qt

# QFont: 글꼴(폰트) 종류, 크기, 굵기 등을 설정할 때 사용
from PyQt5.QtGui import QFont


# ─────────────────────────────────────────────
# Calculator 클래스 정의
# QWidget을 상속받아 창(Window) 기능을 그대로 가져옴
# ─────────────────────────────────────────────
class Calculator(QWidget):

    # __init__: 객체가 처음 만들어질 때 자동으로 실행되는 초기화 함수
    def __init__(self):
        # 부모 클래스(QWidget)의 초기화도 함께 실행 (반드시 호출해야 창이 정상 작동)
        super().__init__()

        # 현재 입력 중인 수식을 저장하는 문자열 변수 (예: "12+34")
        self.expression = ""

        # =을 눌러 결과가 표시된 상태인지 추적하는 변수
        # True일 때 숫자를 누르면 새로운 계산을 시작함
        self.result_shown = False

        # UI(화면 구성)를 초기화하는 함수 호출
        self.init_ui()

    # ─────────────────────────────────────────────
    # init_ui: 화면(창, 버튼, 디스플레이 등)을 구성하는 함수
    # ─────────────────────────────────────────────
    def init_ui(self):
        # 창 제목 표시줄에 나타나는 이름 설정
        self.setWindowTitle("Calculator")

        # 창 크기를 가로 480px, 세로 720px로 고정 (사용자가 크기 변경 불가)
        self.setFixedSize(480, 720)

        # 창 전체 배경색을 어두운 색(#1c1c1e)으로 설정 (아이폰 계산기 스타일)
        self.setStyleSheet("background-color: #1c1c1e;")

        # 세로 방향 레이아웃 생성 (디스플레이 + 버튼 그리드를 위→아래로 배치)
        main_layout = QVBoxLayout()

        # 레이아웃 바깥 여백 설정: 왼쪽16, 위50, 오른쪽16, 아래16 (단위: px)
        main_layout.setContentsMargins(16, 50, 16, 16)

        # 레이아웃 안의 위젯들 사이 간격을 14px로 설정
        main_layout.setSpacing(14)

        # ── 숫자 디스플레이 (QLabel) 설정 ──
        # 초기값 "0"을 표시하는 라벨 생성
        self.display = QLabel("0")

        # 텍스트를 오른쪽(AlignRight) + 아래쪽(AlignBottom)에 붙여서 정렬
        # | 는 두 옵션을 동시에 적용하는 기호
        self.display.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        # 폰트: Arial, 크기 40, Light(얇은) 굵기
        self.display.setFont(QFont("Arial", 40, QFont.Light))

        # 글자색 흰색, 안쪽 여백(padding) 설정
        self.display.setStyleSheet("color: white; padding: 10px 8px 0px 8px;")

        # 디스플레이 영역의 최소 높이를 150px로 설정
        self.display.setMinimumHeight(150)

        # 텍스트가 길어도 줄바꿈 하지 않도록 설정
        self.display.setWordWrap(False)

        # 디스플레이 라벨을 메인 레이아웃에 추가
        main_layout.addWidget(self.display)

        # ── 버튼 격자 레이아웃 생성 ──
        grid = QGridLayout()

        # 버튼 사이 간격 14px
        grid.setSpacing(14)

        # ── 버튼 목록 정의 ──
        # 각 항목: (버튼글자, 행, 열, 글자색, 배경색)
        # 행/열은 0부터 시작 (0행=맨 위, 3열=맨 오른쪽)
        buttons = [
            ("AC",  0, 0, "#1c1c1e", "#a5a5a5"),  # 전체 초기화 버튼 (회색)
            ("+/-", 0, 1, "#1c1c1e", "#a5a5a5"),  # 양수/음수 전환 버튼 (회색)
            ("%",   0, 2, "#1c1c1e", "#a5a5a5"),  # 퍼센트 버튼 (회색)
            ("÷",   0, 3, "white",   "#ff9f0a"),  # 나누기 버튼 (주황)

            ("7", 1, 0, "white", "#333333"),       # 숫자 7 (어두운 회색)
            ("8", 1, 1, "white", "#333333"),       # 숫자 8
            ("9", 1, 2, "white", "#333333"),       # 숫자 9
            ("×", 1, 3, "white", "#ff9f0a"),       # 곱하기 버튼 (주황)

            ("4", 2, 0, "white", "#333333"),       # 숫자 4
            ("5", 2, 1, "white", "#333333"),       # 숫자 5
            ("6", 2, 2, "white", "#333333"),       # 숫자 6
            ("−", 2, 3, "white", "#ff9f0a"),       # 빼기 버튼 (주황)

            ("1", 3, 0, "white", "#333333"),       # 숫자 1
            ("2", 3, 1, "white", "#333333"),       # 숫자 2
            ("3", 3, 2, "white", "#333333"),       # 숫자 3
            ("+", 3, 3, "white", "#ff9f0a"),       # 더하기 버튼 (주황)

            ("0", 4, 0, "white", "#333333"),       # 숫자 0 (가로로 2칸 차지하는 넓은 버튼)
            (".", 4, 2, "white", "#333333"),       # 소수점 버튼
            ("=", 4, 3, "white", "#ff9f0a"),       # 등호(계산 실행) 버튼 (주황)
        ]

        # 버튼 목록을 순서대로 꺼내서 하나씩 버튼 위젯으로 만들기
        for item in buttons:
            # 튜플을 각각의 변수로 분리
            label, row, col, fg, bg = item

            # 버튼 위젯 생성 (label = 버튼에 표시될 글자)
            btn = QPushButton(label)

            # 버튼 글꼴: Arial, 크기 22, 일반 굵기
            btn.setFont(QFont("Arial", 22, QFont.Normal))

            # 버튼 높이 고정: 96px
            btn.setFixedHeight(96)

            if label == "0":
                # "0" 버튼은 2칸을 차지하는 넓은 버튼으로 만들기
                btn.setFixedWidth(210)                        # 넓이 210px
                btn.setStyleSheet(self._btn_style(fg, bg, wide=True))  # 왼쪽 정렬 스타일
                grid.addWidget(btn, row, col, 1, 2)          # (행, 열, 행span, 열span): 1행 2열 차지
            else:
                # 일반 버튼: 정사각형 96px
                btn.setFixedWidth(96)
                btn.setStyleSheet(self._btn_style(fg, bg))
                grid.addWidget(btn, row, col)                 # 해당 행, 열에 배치

            # 버튼 클릭 시 on_button_click 함수 연결 (시그널-슬롯)
            # lambda를 사용해 어떤 버튼이 눌렸는지 label 값을 함께 전달
            # b=label 로 현재 label 값을 캡처 (루프 변수 캡처 문제 방지)
            btn.clicked.connect(lambda _, b=label: self.on_button_click(b))

        # 버튼 그리드를 메인 레이아웃에 추가
        main_layout.addLayout(grid)

        # 완성된 레이아웃을 창에 적용
        self.setLayout(main_layout)

    # ─────────────────────────────────────────────
    # _btn_style: 버튼의 CSS 스타일 문자열을 반환하는 함수
    # fg: 글자색, bg: 배경색, wide: "0" 버튼처럼 넓은 버튼인지 여부
    # ─────────────────────────────────────────────
    def _btn_style(self, fg, bg, wide=False):
        # f-string으로 CSS 스타일시트 문자열 생성
        # {{ }} 는 f-string에서 중괄호 자체를 출력할 때 사용 (CSS 문법의 { } )
        return f"""
            QPushButton {{
                background-color: {bg};
                color: {fg};
                border-radius: 48px;
                text-align: {"left" if wide else "center"};
                padding-left: {"36px" if wide else "0px"};
            }}
            QPushButton:pressed {{
                background-color: {"#c8c8c8" if bg == "#a5a5a5" else
                                   "#ffbe4f" if bg == "#ff9f0a" else "#4d4d4d"};
            }}
        """
        # border-radius: 48px → 버튼을 둥글게 만듦
        # QPushButton:pressed → 버튼을 누르고 있을 때 배경색 변경 (눌림 효과)

    # ─────────────────────────────────────────────
    # on_button_click: 버튼이 클릭될 때 실행되는 함수
    # btn: 클릭된 버튼의 글자 (예: "1", "+", "AC" 등)
    # ─────────────────────────────────────────────
    def on_button_click(self, btn):

        if btn == "AC":
            # AC(All Clear): 모든 입력을 초기화하고 "0"으로 돌아감
            self.expression = ""
            self.result_shown = False
            self.display.setText("0")

        elif btn == "+/-":
            # 현재 숫자의 부호를 바꿈 (양수 → 음수, 음수 → 양수)
            if self.expression and self.expression != "0":
                if self.expression.startswith("-"):
                    # 이미 음수면 맨 앞의 "-" 제거
                    self.expression = self.expression[1:]
                else:
                    # 양수면 맨 앞에 "-" 추가
                    self.expression = "-" + self.expression
                self._update_display(self.expression)

        elif btn == "%":
            # 현재 숫자를 100으로 나눔 (예: 50 → 0.5)
            try:
                val = float(self.expression) / 100
                self.expression = self._format_number(val)
                self._update_display(self.expression)
            except Exception:
                # 변환 실패 시 아무것도 안 함
                pass

        elif btn in ("÷", "×", "−", "+"):
            # 사칙연산 버튼: 화면에 표시되는 기호를 파이썬이 계산할 수 있는 기호로 변환
            # 예: "÷" → "/", "×" → "*", "−" → "-"
            op_map = {"÷": "/", "×": "*", "−": "-", "+": "+"}
            op = op_map[btn]

            if self.expression:
                if self.expression[-1] in "/*-+":
                    # 수식 맨 끝이 이미 연산자면 → 새 연산자로 교체
                    # 예: "12+" 상태에서 "×"를 누르면 "12*"로 변경
                    self.expression = self.expression[:-1] + op
                else:
                    # 그 외엔 연산자 추가 (예: "12" → "12+")
                    self.expression += op

            self.result_shown = False
            # 화면에는 사용자가 누른 기호 그대로 표시 (예: "÷")
            self._update_display(btn)

        elif btn == "=":
            # 현재 수식을 계산하여 결과를 표시
            try:
                # eval(): 문자열로 된 수식을 실제로 계산해주는 파이썬 내장 함수
                # 예: eval("12+34") → 46
                result = eval(self.expression)
                self.expression = self._format_number(result)
                self._update_display(self.expression)
                self.result_shown = True  # 결과 표시 상태로 전환
            except Exception:
                # 계산 불가능한 수식이면 오류 표시 후 초기화
                self.display.setText("오류")
                self.expression = ""

        elif btn == ".":
            # 소수점 버튼: 현재 숫자에 소수점이 없을 때만 추가
            # 현재 수식을 "+" 기준으로 쪼개서 마지막 숫자 부분만 확인
            parts = self.expression.replace("*", "+").replace("/", "+").replace("-", "+").split("+")
            last = parts[-1] if parts else ""

            if "." not in last:
                # 마지막 숫자에 소수점이 없을 때만 추가
                if not self.expression or self.expression[-1] in "/*-+":
                    # 수식이 비어있거나 연산자로 끝나면 "0."을 먼저 붙임
                    # 예: "12+" → "12+0."
                    self.expression += "0."
                else:
                    # 그 외엔 그냥 "." 추가 (예: "12" → "12.")
                    self.expression += "."
                self._update_display(self.expression)

        else:
            # 숫자 버튼(0~9)을 눌렀을 때
            if self.result_shown:
                # 직전에 = 을 눌러 결과가 표시된 상태라면
                # 새로운 계산 시작: 누른 숫자로 expression을 새로 시작
                self.expression = btn
                self.result_shown = False
            else:
                if self.expression == "0":
                    # 현재 "0"만 있으면 그냥 교체 (앞에 0이 붙지 않도록)
                    self.expression = btn
                else:
                    # 그 외엔 뒤에 숫자 추가 (예: "12" + "3" → "123")
                    self.expression += btn
            self._update_display(self.expression)

    # ─────────────────────────────────────────────
    # _format_number: 숫자를 깔끔하게 문자열로 변환하는 함수
    # 예: 5.0 → "5", 3.14 → "3.14"
    # ─────────────────────────────────────────────
    def _format_number(self, val):
        if val == int(val):
            # 소수점 아래가 0이면 정수로 표시 (예: 5.0 → "5")
            return str(int(val))
        else:
            # 소수점이 있으면 최대 10자리까지 표시, 불필요한 0 제거
            # 예: 3.1400000000 → "3.14"
            return f"{val:.10g}"

    # ─────────────────────────────────────────────
    # _update_display: 화면(디스플레이)을 업데이트하는 함수
    # text: 화면에 표시할 수식 또는 숫자 문자열
    # ─────────────────────────────────────────────
    def _update_display(self, text):
        # 내부 수식의 연산자(/, *)를 화면용 기호(÷, ×)로 변환해서 표시
        display_map = {"/": "÷", "*": "×"}
        display_text = text
        for k, v in display_map.items():
            display_text = display_text.replace(k, v)

        # 표시할 텍스트 길이에 따라 폰트 크기를 자동 조절
        # 숫자가 길어질수록 글자를 작게 만들어 디스플레이를 벗어나지 않게 함
        length = len(display_text)
        if length <= 6:
            font_size = 52   # 짧으면 크게
        elif length <= 9:
            font_size = 38   # 중간이면 중간
        else:
            font_size = 28   # 길면 작게

        # 폰트 크기 적용
        self.display.setFont(QFont("Arial", font_size, QFont.Light))

        # 디스플레이 라벨의 텍스트를 업데이트
        self.display.setText(display_text)


# ─────────────────────────────────────────────
# 프로그램 시작점
# 이 파일을 직접 실행할 때만 아래 코드가 실행됨
# (다른 파일에서 import할 때는 실행되지 않음)
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # QApplication 객체 생성 (sys.argv: 명령줄 인수 전달, 보통 그냥 넣어둠)
    app = QApplication(sys.argv)

    # Calculator 창 객체 생성 → __init__ 자동 실행
    window = Calculator()

    # 창을 화면에 표시
    window.show()

    # 이벤트 루프 실행: 사용자 입력(클릭, 키보드 등)을 계속 기다림
    # app.exec_()가 끝나면(창을 닫으면) sys.exit()로 프로그램 종료
    sys.exit(app.exec_())