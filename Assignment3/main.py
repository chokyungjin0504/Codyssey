import random
import datetime
import os


class DummySensor:
    def __init__(self):
        """
        DummySensor 클래스 초기화 메소드.
        - env_values: 센서 값들을 저장하는 딕셔너리
        - log_file: 로그 파일 이름
        - _init_log_file(): 로그 파일에 헤더를 최초 한 번만 기록
        """
        self.env_values = {
            'mars_base_internal_temperature': None,   # 화성 기지 내부 온도
            'mars_base_external_temperature': None,   # 화성 기지 외부 온도
            'mars_base_internal_humidity': None,      # 화성 기지 내부 습도
            'mars_base_external_illuminance': None,   # 화성 기지 외부 광량
            'mars_base_internal_co2': None,           # 화성 기지 내부 CO2 농도
            'mars_base_internal_oxygen': None,        # 화성 기지 내부 산소 농도
        }
        self.log_file = 'mars_env_log.txt'
        self._init_log_file()

    def _init_log_file(self):
        """
        로그 파일 초기화 메소드.
        - 파일이 존재하지 않을 경우 새로 생성
        - 헤더를 한 번만 기록하여 반복 실행 시 중복되지 않도록 함
        """
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as log_file:
                header = (
                    'DateTime, '
                    'Internal Temp (°C), '
                    'External Temp (°C), '
                    'Internal Humidity (%), '
                    'External Illuminance (W/m2), '
                    'Internal CO2 (%), '
                    'Internal Oxygen (%)'
                )
                log_file.write(header + '\n')

    def set_env(self):
        """
        환경 데이터를 랜덤 값으로 설정하는 메소드.
        각 항목은 지정된 범위 내에서 난수(random.uniform)를 사용해 생성.
        """
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)

    def get_env(self):
        """
        현재 환경 데이터를 반환하고 로그 파일에 기록하는 메소드.
        - 현재 날짜와 시간을 포함하여 로그에 저장
        - 로그는 CSV 형태로 기록되어 분석 및 유지보수에 용이
        """
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = (
            f'{now}, '
            f'{self.env_values["mars_base_internal_temperature"]:.2f}, '
            f'{self.env_values["mars_base_external_temperature"]:.2f}, '
            f'{self.env_values["mars_base_internal_humidity"]:.2f}, '
            f'{self.env_values["mars_base_external_illuminance"]:.2f}, '
            f'{self.env_values["mars_base_internal_co2"]:.4f}, '
            f'{self.env_values["mars_base_internal_oxygen"]:.2f}'
        )

        # 로그 파일에 한 줄 추가
        with open(self.log_file, 'a', encoding='utf-8') as log_file:
            log_file.write(log_line + '\n')

        # 현재 환경 값 반환
        return self.env_values


if __name__ == '__main__':
    # DummySensor 인스턴스 생성
    ds = DummySensor()

    # 랜덤 환경 값 설정
    ds.set_env()

    # 환경 값 가져오기 및 로그 기록
    values = ds.get_env()

    # 콘솔에 출력하여 확인
    print(values)