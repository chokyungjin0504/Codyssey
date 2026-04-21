import platform   # 운영체제(OS), CPU 등 시스템 정보를 가져오기 위한 표준 라이브러리
import json       # JSON 형식으로 데이터를 출력하기 위한 표준 라이브러리
import ctypes     # Windows API 호출을 위해 사용하는 표준 라이브러리

class MissionComputer:
    def __init__(self):
        # 생성자: 특별히 초기화할 값은 없으므로 pass 처리
        pass

    def get_mission_computer_info(self):
        """
        시스템 기본 정보를 가져오는 메서드
        - 운영체제 이름
        - 운영체제 버전
        - CPU 타입
        - 전체 메모리 크기
        """

        # 운영체제 이름 (예: Windows, Linux, Darwin 등)
        os_name = platform.system()

        # 운영체제 버전 (Windows의 경우 빌드 번호 등)
        os_version = platform.version()

        # CPU 타입 (예: Intel64 Family, AMD64 등)
        cpu_type = platform.processor()

        # Windows API를 사용하여 메모리 크기 가져오기
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),          # 구조체 길이
                ("dwMemoryLoad", ctypes.c_ulong),      # 메모리 사용률 (%)
                ("ullTotalPhys", ctypes.c_ulonglong),  # 전체 물리 메모리 크기 (bytes)
                ("ullAvailPhys", ctypes.c_ulonglong),  # 사용 가능한 물리 메모리 크기 (bytes)
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        # 구조체 초기화 및 API 호출
        memoryStatus = MEMORYSTATUSEX()
        memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus))

        # 전체 메모리 크기 (bytes 단위)
        mem_size = memoryStatus.ullTotalPhys

        # 결과를 딕셔너리로 정리
        info = {
            "OperatingSystem": os_name,
            "OSVersion": os_version,
            "CPUType": cpu_type,
            "MemorySize(bytes)": mem_size
        }

        # JSON 형식으로 출력 (들여쓰기 4칸)
        print(json.dumps(info, indent=4))
        return info

    def get_mission_computer_load(self):
        """
        시스템 부하(load) 정보를 가져오는 메서드
        - CPU 사용량 (표준 라이브러리만으로는 측정 불가 → 'Not available' 처리)
        - 메모리 실시간 사용량 (bytes)
        - 메모리 사용률 (%)
        """

        # Windows API 구조체 정의 (위와 동일)
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),      # 메모리 사용률 (%)
                ("ullTotalPhys", ctypes.c_ulonglong),  # 전체 메모리
                ("ullAvailPhys", ctypes.c_ulonglong),  # 사용 가능한 메모리
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        # API 호출
        memoryStatus = MEMORYSTATUSEX()
        memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus))

        # 메모리 사용량 계산
        mem_used = memoryStatus.ullTotalPhys - memoryStatus.ullAvailPhys
        mem_load = memoryStatus.dwMemoryLoad  # 메모리 사용률 (%)

        # CPU 사용량은 표준 라이브러리만으로는 측정 불가
        load = {
            "CPULoad": "Not available (standard lib only)",
            "MemoryUsed(bytes)": mem_used,
            "MemoryLoad(%)": mem_load
        }

        # JSON 형식으로 출력
        print(json.dumps(load, indent=4))
        return load


# 인스턴스 생성
runComputer = MissionComputer()

# 메서드 호출 → 시스템 정보와 부하 정보 출력
runComputer.get_mission_computer_info()
runComputer.get_mission_computer_load()