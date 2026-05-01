class Calculator:
    def __init__(self):
        self.current_value = 0
        self.operator = None
        self.previous_value = None
        self.finished = False

    # -------------------------
    # 숫자 입력
    # -------------------------
    def input_number(self, number: int):
        if self.finished:
            return
        self.current_value = self.current_value * 10 + number

    # -------------------------
    # 기본 연산
    # -------------------------
    def add(self):
        self._prepare_operation("+")

    def subtract(self):
        self._prepare_operation("-")

    def multiply(self):
        self._prepare_operation("*")

    def divide(self):
        self._prepare_operation("/")

    def _prepare_operation(self, operator: str):
        if self.operator is not None:
            return
        self.previous_value = self.current_value
        self.current_value = 0
        self.operator = operator

    # -------------------------
    # 결과 계산
    # -------------------------
    def equal(self):
        if self.operator is None or self.finished:
            return

        if self.operator == "+":
            self.current_value = self.previous_value + self.current_value
        elif self.operator == "-":
            self.current_value = self.previous_value - self.current_value
        elif self.operator == "*":
            self.current_value = self.previous_value * self.current_value
        elif self.operator == "/":
            if self.current_value == 0:
                raise ZeroDivisionError("0으로 나눌 수 없습니다.")
            self.current_value = self.previous_value / self.current_value

        self.finished = True
        self.operator = None
        self.previous_value = None

    # -------------------------
    # 추가 기능
    # -------------------------
    def reset(self):
        self.current_value = 0
        self.previous_value = None
        self.operator = None
        self.finished = False

    def negative_positive(self):
        self.current_value = -self.current_value

    def percent(self):
        self.current_value = self.current_value / 100

    # -------------------------
    # 결과 출력
    # -------------------------
    def get_result(self):
        return self.current_value