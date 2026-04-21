# Hello Mars.py
print('--- HelloMars 테스트 ---')
print('Hello, Mars!')

# main.py
def read_log_file(filename):
    try:

        with open(filename, 'r', encoding='utf-8') as file:
            print(f'\n--- {filename} 내용 출력 ---')
            lines = file.readlines()
            # 기본 출력
            for line in lines:
                print(line, end='')
            # 구분선
            print(f'\n--- {filename} 내용 역순 출력 ---')
            # 역순 출력
            lines.reverse()
            for line in lines:
                print(line, end='')

    except FileNotFoundError:
        print(f'Error: {filename} 파일을 찾을 수 없습니다.')
    except PermissionError:
        print(f'Error: {filename} 파일에 접근 권한이 없습니다.')
    except Exception as e:
        print(f'예상치 못한 오류 발생: {e}')


# 이 파일만 테스트해보고싶을 때
if __name__ == '__main__':
    read_log_file('mission_computer_main.log')