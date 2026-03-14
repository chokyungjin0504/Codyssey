# main.py
def read_log_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f'Error: {filename} 파일을 찾을 수 없습니다.')
    except PermissionError:
        print(f'Error: {filename} 파일에 접근 권한이 없습니다.')
    except Exception as e:
        print(f'예상치 못한 오류 발생: {e}')

if __name__ == '__main__':
    read_log_file('./mission_computer_main.log')