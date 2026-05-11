# ============================================================
# door_hacking.py
# emergency_storage_key.zip 의 6자리 암호를 브루트포스로 해독한다.
# 문자셋: 숫자(0-9) + 소문자 알파벳(a-z), 특수문자·대문자 제외
# ============================================================

import zipfile       # ZIP 파일 열기·압축 해제
import string        # 문자셋 상수 (digits, ascii_lowercase)
import itertools     # 모든 조합을 순서대로 생성 (product, islice)
import time          # 시작 시간·경과 시간 측정
import warnings      # 불필요한 경고 메시지 억제
import multiprocessing  # 보너스: CPU 코어를 여러 개 동시에 활용

# zipfile 내부에서 발생하는 사소한 경고를 숨긴다.
warnings.filterwarnings('ignore')


# ────────────────────────────────────────────
# 기본 함수: 단일 프로세스 브루트포스
# ────────────────────────────────────────────
def unlock_zip(zip_path: str = 'emergency_storage_key.zip') -> str | None:
    """
    숫자와 소문자 알파벳으로 구성된 6자리 암호를 브루트포스로 찾아 ZIP 파일을 해제한다.

    브루트포스(Brute-force): 가능한 모든 조합을 하나씩 시도해
    암호를 찾아내는 방식. 시간이 걸리지만 반드시 답을 찾는다.

    Args:
        zip_path: 암호를 풀 ZIP 파일 경로 (기본값: 'emergency_storage_key.zip')

    Returns:
        찾은 암호 문자열, 실패 시 None
    """

    # ── 탐색 범위 설정 ──────────────────────────────────────
    # 숫자 10개(0~9) + 소문자 26개(a~z) = 36가지 문자
    charset = string.digits + string.ascii_lowercase  # '0123456789abcdefghijklmnopqrstuvwxyz'
    password_length = 6                               # 암호는 반드시 6자리
    total = len(charset) ** password_length           # 36^6 = 2,176,782,336 (약 21.7억 가지)

    # ── 시작 정보 출력 ──────────────────────────────────────
    start_time = time.time()  # 탐색 시작 시각 (Unix timestamp)
    print(f'[*] 시작 시간     : {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))}')
    print(f'[*] 문자셋        : {charset}')
    print(f'[*] 암호 길이     : {password_length}자리')
    print(f'[*] 전체 경우의 수: {total:,}')
    print('-' * 60)

    # ── ZIP 파일 열기 ───────────────────────────────────────
    try:
        zf = zipfile.ZipFile(zip_path)  # 암호 없이 열기 (추출 시 암호 전달)
    except FileNotFoundError:
        # 경로에 파일이 없을 때
        print(f'[!] 오류: 파일을 찾을 수 없습니다 → {zip_path}')
        return None
    except zipfile.BadZipFile:
        # 확장자는 .zip 이지만 실제로는 ZIP 형식이 아닐 때
        print(f'[!] 오류: 유효하지 않은 ZIP 파일입니다 → {zip_path}')
        return None

    # ── 브루트포스 루프 ─────────────────────────────────────
    attempt = 0           # 누적 시도 횟수
    report_interval = 500_000  # 50만 번 시도마다 진행 상황을 출력한다.

    # itertools.product: charset 에서 password_length 자리의 모든 순열을 생성
    # 예) ('0','0','0','0','0','0') → ('0','0','0','0','0','1') → ... → ('z','z','z','z','z','z')
    for combo in itertools.product(charset, repeat=password_length):
        password = ''.join(combo)  # 튜플 → 문자열 ('a','b','c','d','e','f') → 'abcdef'
        attempt += 1

        # ── 진행 상황 출력 (50만 번마다) ──────────────────
        if attempt % report_interval == 0:
            elapsed = time.time() - start_time          # 경과 시간(초)
            speed = attempt / elapsed                   # 초당 시도 횟수
            remaining = (total - attempt) / speed       # 예상 남은 시간(초)
            print(
                f'[진행] 시도 횟수: {attempt:>15,} / {total:,} | '
                f'경과: {elapsed:>8.1f}s | '
                f'속도: {speed:>10,.0f}/s | '
                f'예상 남은 시간: {remaining:>8.1f}s | '
                f'현재: {password}'
            )

        # ── 암호 시도 ──────────────────────────────────────
        try:
            # extractall: 현재 암호로 ZIP 내부 파일을 전부 추출 시도
            # 성공하면 예외 없이 통과, 실패하면 RuntimeError 발생
            zf.extractall(pwd=password.encode())  # 문자열 → bytes 변환 후 전달

            # ── 암호 발견 ──────────────────────────────────
            elapsed = time.time() - start_time
            print('-' * 60)
            print(f'[★] 암호 발견! → "{password}"')
            print(f'[*] 총 시도 횟수 : {attempt:,}번')
            print(f'[*] 총 소요 시간 : {elapsed:.2f}초')

            # ── password.txt 에 암호 저장 ─────────────────
            try:
                with open('password.txt', 'w', encoding='utf-8') as f:
                    f.write(password)
                print(f'[*] 암호가 password.txt 에 저장되었습니다.')
            except OSError as e:
                # 디스크 권한 문제 등으로 저장 실패 시
                print(f'[!] password.txt 저장 실패: {e}')

            zf.close()
            return password  # 암호 반환 후 함수 종료

        except (RuntimeError, zipfile.BadZipFile):
            # 틀린 암호일 때 발생하는 예외 → 다음 조합으로 계속 시도
            continue
        except Exception:
            # 그 외 예외(잘못된 암호로 인한 압축 해제 오류 등)는 조용히 넘어간다.
            continue

    # ── 모든 조합을 소진했지만 암호를 찾지 못한 경우 ────────
    zf.close()
    elapsed = time.time() - start_time
    print('-' * 60)
    print(f'[!] 암호를 찾지 못했습니다.')
    print(f'[*] 총 시도 횟수 : {attempt:,}번')
    print(f'[*] 총 소요 시간 : {elapsed:.2f}초')
    return None


# ────────────────────────────────────────────────────────────
# 보너스: 더 빠른 알고리즘 — 멀티프로세싱 병렬 탐색
#
# 아이디어: 전체 탐색 공간(36^6)을 CPU 코어 수만큼 균등하게
#           나눠 각 코어가 자기 구간만 독립적으로 탐색한다.
#           한 코어가 암호를 찾으면 나머지 코어를 즉시 종료한다.
# ────────────────────────────────────────────────────────────

def _worker(args: tuple) -> str | None:
    """
    멀티프로세싱 워커 함수. 각 프로세스가 독립적으로 호출한다.

    전체 조합 공간 중 [start_idx, end_idx) 구간만 탐색하고,
    암호를 찾으면 문자열을 반환, 못 찾으면 None 을 반환한다.

    Args:
        args: (zip_path, charset, length, start_idx, end_idx, worker_id) 튜플

    Returns:
        찾은 암호 문자열, 실패 시 None
    """
    zip_path, charset, length, start_idx, end_idx, worker_id = args

    # 각 워커가 독립적으로 ZIP 파일을 열어야 한다.
    # (파일 핸들은 프로세스 간 공유 불가)
    try:
        zf = zipfile.ZipFile(zip_path)
    except Exception:
        return None  # 파일 열기 실패 시 조용히 종료

    # itertools.islice: 전체 product 시퀀스에서 담당 구간만 잘라낸다.
    # product 자체가 제너레이터라 start_idx 이전 항목을 실제로 생성하므로
    # 메모리는 O(1) 이지만 앞부분 건너뛰는 시간이 소요된다.
    gen = itertools.islice(
        itertools.product(charset, repeat=length),
        start_idx,   # 이 인덱스부터
        end_idx,     # 이 인덱스 직전까지
    )

    for combo in gen:
        password = ''.join(combo)  # 튜플 → 문자열
        try:
            zf.extractall(pwd=password.encode())  # 압축 해제 시도
            zf.close()
            return password  # 성공 → 암호 반환
        except Exception:
            continue  # 실패 → 다음 조합 시도

    zf.close()
    return None  # 담당 구간 전부 실패


def unlock_zip_fast(zip_path: str = 'emergency_storage_key.zip') -> str | None:
    """
    멀티프로세싱을 활용해 CPU 코어 수만큼 병렬로 암호를 탐색한다.
    단일 프로세스 대비 코어 수에 비례하여 탐색 속도가 향상된다.
    (예: 8코어 → 약 8배 빠름)

    Args:
        zip_path: 암호를 풀 ZIP 파일 경로

    Returns:
        찾은 암호 문자열, 실패 시 None
    """
    charset = string.digits + string.ascii_lowercase  # 탐색 문자셋
    password_length = 6                               # 암호 자리 수
    total = len(charset) ** password_length           # 전체 경우의 수
    num_workers = multiprocessing.cpu_count()         # 사용 가능한 CPU 코어 수

    start_time = time.time()
    print(f'[보너스] 멀티프로세싱 브루트포스 시작')
    print(f'[*] 시작 시간     : {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))}')
    print(f'[*] 사용 코어     : {num_workers}개')
    print(f'[*] 전체 경우의 수: {total:,}')
    print('-' * 60)

    # ── 탐색 구간 분할 ──────────────────────────────────────
    # 전체 인덱스를 num_workers 등분한다.
    # 마지막 워커는 나머지(total % num_workers)까지 포함한다.
    chunk = total // num_workers
    ranges = [
        (i * chunk, (i + 1) * chunk if i < num_workers - 1 else total)
        for i in range(num_workers)
    ]

    # 각 워커에 전달할 인자 목록
    worker_args = [
        (zip_path, charset, password_length, s, e, idx)
        for idx, (s, e) in enumerate(ranges)
    ]

    # ── 병렬 실행 ───────────────────────────────────────────
    # Pool.imap_unordered: 워커가 반환하는 결과를 완료 순서대로 즉시 받는다.
    # (순서를 보장하지 않으므로 가장 먼저 찾은 결과를 빠르게 얻을 수 있다)
    with multiprocessing.Pool(processes=num_workers) as pool:
        for result in pool.imap_unordered(_worker, worker_args):
            if result is not None:
                # 암호를 찾은 워커가 있으면 나머지 워커를 강제 종료한다.
                pool.terminate()
                elapsed = time.time() - start_time
                print(f'[★] 암호 발견! → "{result}"')
                print(f'[*] 총 소요 시간 : {elapsed:.2f}초')

                # password.txt 에 암호 저장
                try:
                    with open('password.txt', 'w', encoding='utf-8') as f:
                        f.write(result)
                    print(f'[*] 암호가 password.txt 에 저장되었습니다.')
                except OSError as e:
                    print(f'[!] password.txt 저장 실패: {e}')

                return result

    # 모든 워커가 None 을 반환한 경우 → 암호 없음
    elapsed = time.time() - start_time
    print(f'[!] 암호를 찾지 못했습니다. (소요: {elapsed:.2f}초)')
    return None


# ────────────────────────────────────────────
# 진입점
# ────────────────────────────────────────────
if __name__ == '__main__':
    # 기본 방식: 단일 프로세스 브루트포스
    unlock_zip('emergency_storage_key.zip')

    # 보너스 방식: 멀티프로세싱 병렬 탐색 (더 빠름)
    # 아래 주석을 해제하고 위 unlock_zip 호출을 주석 처리하면 사용 가능
    # unlock_zip_fast('emergency_storage_key.zip')