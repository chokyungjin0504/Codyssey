# Hello Mars.py
print('Hello, Mars!')
print('=' * 50)

# main.py
def read_log_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            # 기본 출력
            for line in lines:
                print(line, end='')
            # 구분선
            print('=' * 50)
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

if __name__ == '__main__':
    read_log_file('./mission_computer_main.log')