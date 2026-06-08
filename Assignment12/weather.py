# =============================================================
# mars_weather_summary.py
# 화성 날씨 데이터(CSV)를 읽어서 MySQL에 저장하는 프로그램
# =============================================================

# mysql-connector-python 라이브러리를 import 한다.
# MySQL과 Python을 연결해주는 외부 라이브러리이다.
# 설치 방법: pip install mysql-connector-python
import mysql.connector

# CSV 파일을 읽기 위해 Python 기본 내장 모듈 csv를 import 한다.
# 별도 설치 없이 사용 가능하다.
import csv


# =============================================================
# 1단계: MySQL 데이터베이스 연결
# =============================================================

# mysql.connector.connect()로 MySQL 서버에 접속한다.
# host    : MySQL 서버 주소 (내 컴퓨터면 'localhost')
# user    : MySQL 사용자 이름 (보통 'root')
# password: MySQL 비밀번호
# database: 사용할 데이터베이스 이름
connection = mysql.connector.connect(
    host='localhost',
    user='root',          # 본인의 MySQL 사용자 이름으로 변경
    password='Sarah0504!',      # 본인의 MySQL 비밀번호로 변경
    database='mars_db'    # 본인이 만든 데이터베이스 이름으로 변경
)

# cursor는 SQL 명령어를 실행하는 도구이다.
# 마치 데이터베이스에 명령을 내리는 '손'과 같은 역할을 한다.
cursor = connection.cursor()


# =============================================================
# 2단계: mars_weather 테이블 생성
# =============================================================

# 테이블 생성 SQL 쿼리를 문자열로 작성한다.
# CREATE TABLE IF NOT EXISTS : 테이블이 없을 때만 만든다 (이미 있으면 에러 없이 넘어감)
# weather_id INT AUTO_INCREMENT PRIMARY KEY : 자동으로 1씩 증가하는 기본키
# mars_date  DATETIME NOT NULL              : 날짜/시간, 반드시 입력해야 함
# temp       INT                            : 기온 (정수)
# storm      INT                            : 모래폭풍 수치 (정수)
create_table_query = '''
CREATE TABLE IF NOT EXISTS mars_weather (
    weather_id INT AUTO_INCREMENT PRIMARY KEY,
    mars_date  DATETIME NOT NULL,
    temp       INT,
    storm      INT
)
'''

# cursor.execute()로 SQL 쿼리를 실제로 실행한다.
cursor.execute(create_table_query)
print('테이블 생성 완료 (이미 존재하면 그대로 사용)')


# =============================================================
# 3단계: CSV 파일 읽기
# =============================================================

# CSV 파일 경로를 변수에 저장한다.
# 코드 파일과 CSV 파일이 같은 폴더에 있으면 파일 이름만 써도 된다.
csv_file_path = 'mars_weathers_data.CSV'

# CSV 파일을 열고 내용을 확인한다.
# open()  : 파일을 여는 Python 기본 함수
# 'r'     : 읽기(read) 모드
# encoding='utf-8' : 한글 깨짐 방지를 위한 인코딩 설정
with open(csv_file_path, 'r', encoding='utf-8') as csv_file:

    # csv.reader()로 CSV 파일을 한 줄씩 읽을 수 있게 준비한다.
    reader = csv.reader(csv_file)

    # next()로 첫 번째 줄(헤더)을 건너뛴다.
    # 헤더: weather_id, mars_date, temp, stom (원본 CSV에 오타 있음)
    header = next(reader)
    print(f'CSV 헤더 확인: {header}')

    # 몇 번째 줄을 처리하는지 세기 위한 카운터 변수
    row_count = 0

    # for 반복문으로 CSV의 나머지 줄을 한 줄씩 읽는다.
    for row in reader:

        # row는 리스트 형태이다. 예: ['1', '2050-01-01', '21.4', '56']
        # 각 위치의 값을 변수에 담는다.
        weather_id = int(row[0])    # 첫 번째 값: weather_id (문자열 → 정수 변환)
        mars_date  = row[1]         # 두 번째 값: mars_date (날짜 문자열 그대로 사용)
        temp       = int(float(row[2]))  # 세 번째 값: temp (소수점 있으므로 float 먼저, 그 후 int 변환)
        storm      = int(row[3])    # 네 번째 값: storm (문자열 → 정수 변환)

        # =============================================================
        # 4단계: INSERT 쿼리로 데이터를 테이블에 삽입
        # =============================================================

        # INSERT INTO 쿼리를 작성한다.
        # %s는 자리 표시자(placeholder)로, 실제 값은 아래 튜플에서 넣어준다.
        # 이렇게 하면 SQL Injection 공격을 방지할 수 있어 안전하다.
        insert_query = '''
        INSERT INTO mars_weather (weather_id, mars_date, temp, storm)
        VALUES (%s, %s, %s, %s)
        '''

        # cursor.execute()의 두 번째 인자로 실제 값을 튜플 형태로 전달한다.
        # 튜플: 괄호()로 묶인, 순서가 있는 값의 묶음
        cursor.execute(insert_query, (weather_id, mars_date, temp, storm))

        # 처리한 줄 수를 1 증가시킨다.
        row_count += 1

    # 모든 줄 처리 완료 후 총 건수를 출력한다.
    print(f'총 {row_count}건의 데이터를 INSERT 했습니다.')


# =============================================================
# 5단계: 변경사항 저장 및 연결 종료
# =============================================================

# connection.commit()으로 INSERT한 내용을 데이터베이스에 최종 저장한다.
# commit()을 하지 않으면 데이터가 실제로 저장되지 않는다!
connection.commit()
print('데이터베이스에 변경사항 저장 완료 (commit)')

# cursor와 connection을 닫아서 리소스를 반환한다.
# 파일을 열면 닫아야 하듯이, DB 연결도 사용 후 반드시 닫아야 한다.
cursor.close()
connection.close()
print('데이터베이스 연결 종료')
print('모든 작업이 완료되었습니다!')