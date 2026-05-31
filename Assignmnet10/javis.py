# ============================================================
# javis.py - 음성 녹음, STT 변환, CSV 저장 통합 프로그램
# ============================================================

# os: 파일/폴더 경로를 다루기 위한 파이썬 기본 모듈
# 예) 폴더 만들기, 파일 경로 합치기, 파일 목록 가져오기
import os

# csv: CSV 파일을 읽고 쓰기 위한 파이썬 기본 모듈
# CSV = 쉼표로 구분된 데이터 파일 (엑셀에서 열 수 있음)
import csv

# datetime: 현재 날짜와 시간을 가져오기 위한 파이썬 기본 모듈
from datetime import datetime

# speech_recognition: 음성을 텍스트로 변환하는 외부 라이브러리 (STT)
# STT = Speech To Text (말 → 글자)
# 설치: uv pip install SpeechRecognition
import speech_recognition as sr

# sounddevice: 마이크로 음성을 녹음하는 외부 라이브러리
# 설치: uv pip install sounddevice
import sounddevice as sd

# soundfile: 녹음된 음성 데이터를 .wav 파일로 저장하는 외부 라이브러리
# 설치: uv pip install soundfile
import soundfile as sf

# numpy: 숫자 배열을 다루는 외부 라이브러리
# 녹음된 음성 데이터가 숫자 배열 형태이기 때문에 필요
# 설치: uv pip install numpy
import numpy as np


# ============================================================
# 함수 1: records 폴더 자동 생성
# ============================================================
def create_records_folder():
    """
    records 폴더가 없으면 자동으로 만들어주는 함수
    반환값: records 폴더의 전체 경로
    """

    # __file__: 현재 실행 중인 파일(javis.py)의 경로
    # os.path.dirname(): 파일이 있는 폴더 경로만 추출
    # os.path.join(): 폴더 경로와 "records" 문자열을 합쳐서 전체 경로 생성
    # 예) C:\Users\sarah\...\Assignmnet10\records
    records_path = os.path.join(os.path.dirname(__file__), "records")

    # os.path.exists(): 해당 경로에 폴더/파일이 존재하는지 확인
    # 존재하면 True, 없으면 False 반환
    if not os.path.exists(records_path):

        # os.makedirs(): 폴더를 새로 생성
        # 중간 폴더도 없으면 함께 생성해줌
        os.makedirs(records_path)
        print(f"📁 records 폴더 생성됨: {records_path}")

    # 폴더 경로를 반환해서 다른 함수에서 사용할 수 있게 함
    return records_path


# ============================================================
# 함수 2: 마이크로 음성 녹음하고 파일로 저장
# ============================================================
def record_audio(duration=5, sample_rate=44100):
    """
    마이크로 음성을 녹음하고 records 폴더에 저장하는 함수
    duration: 녹음할 시간 (초 단위, 기본값 5초)
    sample_rate: 음질 설정 (44100 = CD 품질, 기본값)
    반환값: 저장된 파일의 전체 경로
    """

    # 함수 1 호출: records 폴더 경로 가져오기 (없으면 자동 생성)
    records_path = create_records_folder()

    # 현재 날짜와 시간 가져오기
    now = datetime.now()

    # strftime(): 날짜/시간을 원하는 형식의 문자열로 변환
    # %Y = 연도(2026), %m = 월(05), %d = 일(31)
    # %H = 시(14), %M = 분(30), %S = 초(00)
    # 결과 예시: "20260531-143000.wav"
    file_name = now.strftime("%Y%m%d-%H%M%S") + ".wav"

    # os.path.join(): records 폴더 경로와 파일 이름을 합쳐서 전체 경로 생성
    # 예) C:\Users\sarah\...\records\20260531-143000.wav
    file_path = os.path.join(records_path, file_name)

    print(f"\n🎙 녹음 시작! {duration}초 동안 말씀하세요...")

    # sd.rec(): 마이크로 녹음 시작
    # int(duration * sample_rate): 총 녹음할 샘플 수 계산
    #   예) 5초 * 44100 = 220500개의 음성 데이터 포인트
    # samplerate=sample_rate: 1초에 44100번 소리를 측정
    # channels=1: 모노 녹음 (1개 채널, 스테레오는 2)
    # dtype="float32": 음성 데이터를 32비트 실수형으로 저장
    audio_data = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="float32"
    )

    # sd.wait(): 녹음이 완전히 끝날 때까지 프로그램 대기
    # 이게 없으면 녹음 중에 다음 코드가 실행되어버림
    sd.wait()

    print("✅ 녹음 완료!")

    # sf.write(): 녹음된 데이터를 .wav 파일로 저장
    # file_path: 저장할 파일 경로
    # audio_data: 녹음된 음성 데이터 배열
    # sample_rate: 음질 정보 (파일에 함께 저장됨)
    sf.write(file_path, audio_data, sample_rate)

    print(f"💾 저장됨: {file_path}")

    # 저장된 파일 경로를 반환 (나중에 STT 변환에 사용)
    return file_path


# ============================================================
# 함수 3: 특정 폴더에서 음성 파일 목록 가져오기
# ============================================================
def get_audio_files(folder_path):
    """
    folder_path: 음성 파일들이 들어있는 폴더 경로
    반환값: 음성 파일 경로들의 리스트
    """

    # 지원하는 음성 파일 확장자 목록
    # speech_recognition 라이브러리가 지원하는 형식
    audio_extensions = [".wav", ".flac", ".aiff"]

    # 음성 파일 경로를 담을 빈 리스트 생성
    audio_files = []

    # os.listdir(): 폴더 안의 모든 파일/폴더 이름을 리스트로 반환
    for file_name in os.listdir(folder_path):

        # os.path.splitext(): 파일 이름과 확장자를 분리
        # 예) "hello.wav" → ("hello", ".wav")
        # _: 파일 이름 부분은 필요 없어서 _ 로 버림
        _, ext = os.path.splitext(file_name)

        # .lower(): 대문자를 소문자로 변환 (.WAV도 인식하기 위해)
        # 확장자가 지원 목록에 있으면 리스트에 추가
        if ext.lower() in audio_extensions:

            # os.path.join(): 폴더 경로와 파일 이름을 합쳐서 전체 경로 생성
            # 예) "audio_files" + "hello.wav" → "audio_files\hello.wav"
            full_path = os.path.join(folder_path, file_name)
            audio_files.append(full_path)

    return audio_files


# ============================================================
# 함수 4: 음성 파일 하나를 텍스트로 변환하기 (STT)
# ============================================================
def convert_speech_to_text(audio_file_path):
    """
    audio_file_path: 변환할 음성 파일의 경로
    반환값: (변환된 텍스트, 변환 시각) 튜플
            변환 실패 시 (None, 변환 시각) 반환
    """

    # Recognizer 객체 생성: 음성 인식 기능을 담당하는 객체
    recognizer = sr.Recognizer()

    # 현재 시각을 "2026-05-31 14:30:00" 형식으로 저장
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # sr.AudioFile(): 음성 파일을 열기 위한 객체
    # with 문: 파일을 안전하게 열고 작업 후 자동으로 닫아줌
    with sr.AudioFile(audio_file_path) as source:

        # recognizer.record(): 음성 파일의 내용을 전부 읽어서
        # audio 변수에 저장 (아직 텍스트 변환 전 단계)
        audio = recognizer.record(source)

    # try-except: 오류가 발생해도 프로그램이 멈추지 않도록 처리
    try:
        # recognize_google(): 구글 STT API로 음성을 텍스트로 변환
        # language="ko-KR": 한국어로 인식
        # 인터넷 연결이 필요함
        text = recognizer.recognize_google(audio, language="ko-KR")

        # 변환 성공 시 텍스트와 시각을 함께 반환
        return text, timestamp

    # UnknownValueError: 음성이 너무 작거나 잡음이 많아서 인식 못할 때
    except sr.UnknownValueError:
        print(f"  ⚠ 인식 실패: {audio_file_path} - 음성을 알아들을 수 없음")
        return None, timestamp

    # RequestError: 인터넷 연결 문제나 구글 API 문제 발생 시
    except sr.RequestError as e:
        print(f"  ⚠ API 오류: {audio_file_path} - {e}")
        return None, timestamp


# ============================================================
# 함수 5: 변환 결과를 CSV 파일로 저장하기
# ============================================================
def save_to_csv(audio_file_path, timestamp, text):
    """
    audio_file_path: 원본 음성 파일 경로
    timestamp: 변환된 시각
    text: 변환된 텍스트
    """

    # os.path.splitext(): 확장자 제거
    # 예) "records\20260531-143000.wav" → "records\20260531-143000"
    base_path, _ = os.path.splitext(audio_file_path)

    # 확장자를 .csv로 바꿔서 CSV 파일 경로 생성
    # 예) "records\20260531-143000.csv"
    csv_file_path = base_path + ".csv"

    # os.path.exists(): CSV 파일이 이미 있는지 확인
    # 있으면 헤더(컬럼명)를 다시 쓰지 않기 위해 확인
    file_exists = os.path.exists(csv_file_path)

    # open(): 파일 열기
    # mode="a": 추가 모드 (기존 내용 유지하고 뒤에 추가)
    # newline="": CSV 저장 시 빈 줄이 생기는 것 방지
    # encoding="utf-8-sig": 한글이 깨지지 않도록 설정
    with open(csv_file_path, mode="a", newline="", encoding="utf-8-sig") as csv_file:

        # csv.writer(): CSV 파일에 데이터를 쓰기 위한 객체
        writer = csv.writer(csv_file)

        # 파일이 새로 만들어지는 경우에만 헤더(컬럼명) 추가
        if not file_exists:
            # writerow(): 한 행을 CSV에 작성
            writer.writerow(["파일경로", "시간", "인식된텍스트"])

        # 실제 데이터 한 행 저장
        writer.writerow([audio_file_path, timestamp, text])

    print(f"  ✅ CSV 저장 완료: {csv_file_path}")


# ============================================================
# 함수 6: 전체 폴더의 음성 파일을 일괄 처리
# ============================================================
def process_audio_folder(folder_path):
    """
    folder_path: 음성 파일들이 있는 폴더 경로
    폴더 안의 모든 음성 파일을 STT 변환 후 CSV 저장
    """

    print(f"\n📂 폴더 스캔 중: {folder_path}")

    # 함수 3 호출: 폴더에서 음성 파일 목록 가져오기
    audio_files = get_audio_files(folder_path)

    # 음성 파일이 하나도 없으면 안내 메시지 출력 후 종료
    if not audio_files:
        print("⚠ 음성 파일이 없습니다.")
        return

    print(f"🎵 발견된 음성 파일: {len(audio_files)}개\n")

    # 음성 파일 목록을 하나씩 순서대로 처리
    for audio_file in audio_files:
        print(f"🔄 처리 중: {audio_file}")

        # 함수 4 호출: 음성 → 텍스트 변환
        text, timestamp = convert_speech_to_text(audio_file)

        # 변환 성공한 경우에만 CSV 저장
        if text is not None:
            # 함수 5 호출: CSV 파일로 저장
            save_to_csv(audio_file, timestamp, text)
        else:
            print(f"  ❌ 변환 실패로 저장 건너뜀")


# ============================================================
# 보너스 1: CSV 파일에서 키워드로 검색하기
# ============================================================
def search_keyword_in_csv(csv_file_path, keyword):
    """
    csv_file_path: 검색할 CSV 파일 경로
    keyword: 찾을 키워드
    """

    print(f"\n🔍 '{keyword}' 검색 중...\n")

    # 검색 결과가 있는지 추적하는 변수
    found = False

    # 읽기 모드로 CSV 파일 열기
    with open(csv_file_path, mode="r", encoding="utf-8-sig") as csv_file:

        # csv.reader(): CSV 파일을 한 줄씩 읽기 위한 객체
        reader = csv.reader(csv_file)

        # next(): 첫 번째 줄(헤더: 파일경로, 시간, 인식된텍스트)을 건너뜀
        next(reader)

        # 나머지 데이터 줄을 한 줄씩 확인
        for row in reader:

            # row[0] = 파일경로, row[1] = 시간, row[2] = 인식된텍스트
            # .lower(): 대소문자 구분 없이 검색하기 위해 소문자로 변환
            if keyword.lower() in row[2].lower():
                print(f"파일: {row[0]}")
                print(f"시간: {row[1]}")
                print(f"내용: {row[2]}")
                print("-" * 40)
                found = True

    if not found:
        print(f"'{keyword}'를 포함한 내용이 없습니다.")


# ============================================================
# 보너스 2: 특정 날짜 범위의 녹음 파일 보여주기
# ============================================================
def show_records_by_date(start_date, end_date):
    """
    start_date: 시작 날짜 문자열 (예: "20260501")
    end_date: 끝 날짜 문자열 (예: "20260531")
    해당 범위 안에 있는 녹음 파일 목록을 출력
    """

    # records 폴더 경로 가져오기
    records_path = create_records_folder()

    print(f"\n📅 {start_date} ~ {end_date} 녹음 파일 목록:\n")

    # 찾은 파일 수를 세는 변수
    count = 0

    # sorted(): 파일 이름을 알파벳/날짜 순서로 정렬해서 가져오기
    for file_name in sorted(os.listdir(records_path)):

        # .wav 파일만 확인 (CSV 등 다른 파일 제외)
        if not file_name.endswith(".wav"):
            continue

        # 파일 이름에서 날짜 부분만 추출
        # split("-"): "-" 기준으로 문자열 나누기
        # [0]: 첫 번째 부분 = 날짜
        # 예) "20260531-143000.wav" → ["20260531", "143000.wav"] → "20260531"
        file_date = file_name.split("-")[0]

        # 날짜 비교: 문자열 크기 비교로 날짜 범위 확인
        # "20260501" <= "20260531" <= "20260531" → True
        if start_date <= file_date <= end_date:
            print(f"  🎵 {file_name}")
            count += 1

    if count == 0:
        print("  해당 날짜 범위의 녹음 파일이 없습니다.")
    else:
        print(f"\n  총 {count}개 파일")


# ============================================================
# 프로그램 시작점
# if __name__ == "__main__": 이 파일을 직접 실행할 때만 아래 코드 실행
# 다른 파일에서 import 할 때는 실행되지 않음
# ============================================================
if __name__ == "__main__":

    # ---- 녹음 기능 실행 ----
    # 5초 동안 마이크로 녹음하고 records 폴더에 저장
    saved_file = record_audio(duration=5)

    # ---- STT 변환 실행 ----
    print("\n🔄 STT 변환 중...")

    # 함수 4 호출: 방금 녹음한 파일을 텍스트로 변환
    text, timestamp = convert_speech_to_text(saved_file)

    # 변환 성공한 경우에만 CSV 저장
    if text:
        print(f"📝 변환된 텍스트: {text}")

        # 함수 5 호출: 변환 결과를 CSV로 저장
        save_to_csv(saved_file, timestamp, text)
    else:
        print("❌ STT 변환 실패")

    # ---- 보너스 기능 (필요할 때 주석 해제해서 사용) ----

    # 날짜 범위로 녹음 파일 검색
    # show_records_by_date("20260501", "20260531")

    # CSV에서 키워드 검색
    # search_keyword_in_csv("records/20260531-143000.csv", "안녕")