# =============================================================
# mars_weather_summary.py
# CSV 파일 → MySQL 저장 → 100개 조회 → PNG 이미지 생성
# =============================================================


# ----------------------------
# [1] 필요한 라이브러리 불러오기
# ----------------------------

import mysql.connector   # MySQL 데이터베이스 연결 라이브러리
import csv               # CSV 파일 읽기용 (파이썬 기본 제공)
import matplotlib        # 그래프/이미지 생성 라이브러리
import matplotlib.pyplot as plt  # pyplot: 실제 그림 그릴 때 사용


# 한글 깨짐 방지 (영문 폰트 사용)
matplotlib.rcParams['font.family'] = 'DejaVu Sans'


# =============================================================
# [2] MySQLHelper 클래스 (DB 작업 쉽게 만드는 도구)
# =============================================================
class MySQLHelper:

    # 객체 생성 시 자동 실행됨 (생성자)
    def __init__(self, host, user, password, database):
        self.host = host             # DB 주소 (localhost = 내 컴퓨터)
        self.user = user             # DB 사용자 이름
        self.password = password     # DB 비밀번호
        self.database = database     # DB 이름

        self.connection = None       # DB 연결 객체 (초기에는 없음)
        self.cursor = None           # SQL 실행 도구 (초기에는 없음)

    # DB 연결하는 함수
    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        self.cursor = self.connection.cursor()  # SQL 실행할 커서 생성
        print("✅ DB 연결 완료")

    # SQL 실행 함수 (INSERT, CREATE 등)
    def execute_query(self, query, values=None):

        # 값이 있는 경우 (INSERT)
        if values:
            self.cursor.execute(query, values)

        # 값이 없는 경우 (CREATE TABLE 등)
        else:
            self.cursor.execute(query)

    # SELECT 결과 가져오는 함수
    def fetch_results(self, query):
        self.cursor.execute(query)     # SELECT 실행
        return self.cursor.fetchall()  # 모든 결과 반환

    # DB에 최종 저장
    def commit(self):
        self.connection.commit()
        print("✅ DB 저장 완료")

    # 연결 종료
    def close(self):
        self.cursor.close()
        self.connection.close()
        print("✅ DB 종료")


# =============================================================
# [3] DB 연결
# =============================================================
helper = MySQLHelper(
    "localhost",   # DB 주소
    "root",        # 사용자 이름
    "password",        # 비밀번호 (본인 환경에 맞게 수정)
    "mars_db"      # 사용할 DB 이름
)

helper.connect()  # 실제 연결 실행


# =============================================================
# [4] 테이블 생성
# =============================================================
create_table_query = """
CREATE TABLE IF NOT EXISTS mars_weather (
    weather_id INT AUTO_INCREMENT PRIMARY KEY,  -- 자동 증가 기본키
    mars_date DATETIME NOT NULL,                -- 날짜 (필수)
    temp INT,                                   -- 온도
    storm INT                                   -- 폭풍 수치
)
"""

helper.execute_query(create_table_query)
print("✅ 테이블 준비 완료")


# =============================================================
# [5] CSV 파일 읽어서 DB에 저장
# =============================================================
with open("mars_weathers_data.CSV", "r", encoding="utf-8") as file:

    reader = csv.reader(file)  # CSV 한 줄씩 읽기

    next(reader)  # 첫 줄(헤더) 건너뜀

    count = 0  # 몇 개 저장했는지 카운트

    # CSV 데이터 한 줄씩 반복
    for row in reader:

        # CSV 값 가져오기
        mars_date = row[1]               # 날짜
        temp = int(float(row[2]))        # 온도 (소수 → 정수)
        storm = int(row[3])              # 폭풍 수치

        # ✅ AUTO_INCREMENT이기 때문에 weather_id는 넣지 않음
        insert_query = """
        INSERT INTO mars_weather (mars_date, temp, storm)
        VALUES (%s, %s, %s)
        """

        # SQL 실행
        helper.execute_query(insert_query, (mars_date, temp, storm))

        count += 1  # 카운트 증가

    print(f"✅ {count}개 데이터 INSERT 완료")


# =============================================================
# [6] DB 저장 확정
# =============================================================
helper.commit()  # commit 해야 실제 DB에 반영됨


# =============================================================
# [7] ✅ 100개 데이터 조회 + PNG 이미지로 저장
# =============================================================

# DB에서 100개만 가져오기 (LIMIT 중요)
rows = helper.fetch_results(
    "SELECT weather_id, mars_date, temp, storm FROM mars_weather LIMIT 100"
)

print(f"✅ {len(rows)}개 데이터 조회 완료")

# 표 컬럼 이름 정의
col_labels = ["weather_id", "mars_date", "temp", "storm"]

# 모든 데이터를 문자열로 변환 (표는 문자열만 가능)
table_data = [[str(cell) for cell in row] for row in rows]


# ----------------------------
# matplotlib으로 표 만들기
# ----------------------------

# 그림 크기 설정 (세로 길게 해서 100줄 표시 가능)
fig, ax = plt.subplots(figsize=(10, 25))

# 축 제거 → 깔끔하게 표만 보이도록
ax.axis("off")

# 표 생성
table = ax.table(
    cellText=table_data,    # 데이터
    colLabels=col_labels,   # 컬럼 이름
    cellLoc="center",       # 가운데 정렬
    loc="center"
)

# 폰트 크기 조정
table.auto_set_font_size(False)
table.set_fontsize(8)

# 이미지 파일로 저장
plt.savefig("mars_weather_result.png", bbox_inches="tight", dpi=150)

# 메모리 정리 (중요)
plt.close()

print("✅ PNG 파일 저장 완료")


# =============================================================
# [8] DB 연결 종료
# =============================================================
helper.close()

print("🎉 모든 작업 완료!")