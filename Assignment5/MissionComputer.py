import platform
import json
import ctypes

class MissionComputer:
    def __init__(self):
        pass

    def get_mission_computer_info(self):
        # 운영체제 정보
        os_name = platform.system()
        # 운영체제 버전
        os_version = platform.version()
        # CPU 타입
        cpu_type = platform.processor()

        # 메모리 크기 (Windows API 호출)
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        memoryStatus = MEMORYSTATUSEX()
        memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus))
        mem_size = memoryStatus.ullTotalPhys

        info = {
            "OperatingSystem": os_name,
            "OSVersion": os_version,
            "CPUType": cpu_type,
            "MemorySize": mem_size
        }

        print(json.dumps(info, indent=4))
        return info

    def get_mission_computer_load(self):
        # CPU 사용량은 표준 라이브러리만으로는 직접 측정하기 어려움
        # 대신 Windows API로 메모리 사용량만 가져오기
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        memoryStatus = MEMORYSTATUSEX()
        memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus))

        mem_used = memoryStatus.ullTotalPhys - memoryStatus.ullAvailPhys
        mem_load = memoryStatus.dwMemoryLoad  # % 사용량

        load = {
            "CPULoad": "Not available (standard lib only)",
            "MemoryUsed(bytes)": mem_used,
            "MemoryLoad(%)": mem_load
        }

        print(json.dumps(load, indent=4))
        return load


# 인스턴스 생성
runComputer = MissionComputer()

# 메서드 호출
runComputer.get_mission_computer_info()
runComputer.get_mission_computer_load()