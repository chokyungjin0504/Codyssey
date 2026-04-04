import json
import time
import random


class DummySensor:
    """화성 기지 환경 센서를 시뮬레이션하는 더미 센서 클래스"""

    def __init__(self):
        # 센서가 측정하는 환경 값들을 딕셔너리로 초기화 (초기값은 None)
        self.env_values = {
            'mars_base_internal_temperature': None,  # 기지 내부 온도 (°C)
            'mars_base_external_temperature': None,  # 기지 외부 온도 (°C)
            'mars_base_internal_humidity': None,     # 기지 내부 습도 (%)
            'mars_base_external_illuminance': None,  # 기지 외부 광량 (lux)
            'mars_base_internal_co2': None,          # 기지 내부 이산화탄소 농도 (%)
            'mars_base_internal_oxygen': None,       # 기지 내부 산소 농도 (%)
        }

    def set_env(self):
        """각 센서 항목에 랜덤 값을 생성하여 저장하는 메소드"""
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18.0, 30.0), 2)   # 내부 온도: 18~30°C
        self.env_values['mars_base_external_temperature'] = round(random.uniform(-80.0, 0.0), 2)   # 외부 온도: -80~0°C
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(30.0, 70.0), 2)      # 내부 습도: 30~70%
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(100.0, 900.0), 2) # 외부 광량: 100~900 lux
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.1, 1.0), 4)             # 내부 CO2 농도: 0.1~1.0%
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(19.0, 23.0), 2)        # 내부 산소 농도: 19~23%


class MissionComputer:
    """화성 기지의 환경 데이터를 수집하고 출력하는 미션 컴퓨터 클래스"""

    def __init__(self):
        # 미션 컴퓨터가 관리하는 환경 값 딕셔너리 초기화
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None,
        }
        # DummySensor를 ds라는 이름으로 인스턴스화
        self.ds = DummySensor()

    def get_sensor_data(self):
        """5초마다 센서 데이터를 읽어 JSON 형태로 출력하는 메소드"""
        while True:
            # 더미 센서에서 새로운 환경 값 생성
            self.ds.set_env()

            # 센서 값을 미션 컴퓨터의 env_values에 복사
            self.env_values = self.ds.env_values.copy()

            # 환경 정보를 JSON 형태로 출력
            print(json.dumps(self.env_values, indent=4, ensure_ascii=False))

            # 5초 대기 후 반복
            time.sleep(5)


# MissionComputer를 RunComputer라는 이름으로 인스턴스화
RunComputer = MissionComputer()

# 센서 데이터를 지속적으로 수집 및 출력 (Ctrl+C로 종료)
RunComputer.get_sensor_data()