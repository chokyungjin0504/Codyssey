import zipfile
import itertools
import string
import time


def unlock_zip():
    zip_file_name = "emergency_storage_key.zip"
    password_file = "password.txt"

    # 암호 후보 문자: 숫자 + 소문자 알파벳
    characters = string.digits + string.ascii_lowercase

    start_time = time.time()
    attempt_count = 0

    print("암호 해제를 시작합니다...")
    print(f"시작 시간: {time.ctime(start_time)}")

    try:
        with zipfile.ZipFile(zip_file_name, "r") as zip_file:
            # 6자리 브루트포스
            for password_tuple in itertools.product(characters, repeat=6):
                password = "".join(password_tuple)
                attempt_count += 1

                try:
                    zip_file.extractall(pwd=password.encode())
                    end_time = time.time()

                    print("\n✅ 암호 해제 성공!")
                    print(f"암호: {password}")
                    print(f"총 시도 횟수: {attempt_count}")
                    print(f"총 소요 시간: {end_time - start_time:.2f}초")

                    # 암호 저장
                    with open(password_file, "w") as file:
                        file.write(password)

                    return

                except RuntimeError:
                    # 잘못된 암호일 경우 계속 시도
                    continue

    except FileNotFoundError:
        print("❌ ZIP 파일을 찾을 수 없습니다.")
    except zipfile.BadZipFile:
        print("❌ 올바르지 않은 ZIP 파일입니다.")


if __name__ == "__main__":
    unlock_zip()