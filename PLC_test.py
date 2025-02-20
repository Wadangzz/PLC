import win32com.client
import time
import tkinter as tk
from tkinter import ttk

class MXComponent:  
    def __init__(self):
        # ActUtlType COM 객체 생성
        self.act = win32com.client.Dispatch("ActUtlType.ActUtlType")

        # 통신 상태 변수
        self.connected = False

        # 논리 스테이션 번호
        self.station_number = 0

    def connect(self):
        """PLC 연결"""
        if not self.connected:
            # 논리 스테이션 번호 설정
            self.act.ActLogicalStationNumber = self.station_number

            # 통신 열기
            ret = self.act.Open()
            if ret == 0:
                self.connected = True
                # M0 디바이스 ON
                self.set_device("M0", 1)
                return True
        return False

    def disconnect(self):
        """PLC 연결 해제"""
        if self.connected:
            # M0 디바이스 OFF
            self.set_device("M0", 0)

            # 통신 닫기
            self.act.Close()
            self.connected = False
            return True
        return False

    def set_device(self, device, value):
        """PLC 디바이스 값 쓰기"""
        if self.connected:
            ret = self.act.SetDevice(device, value)
            return ret == 0
        return False

    def get_device(self, device):
        """PLC 디바이스 값 읽기"""
        if self.connected:
            ret = self.act.GetDevice(device)
            if isinstance(ret, tuple):
                return ret
            return ret
        return None

if __name__ == "__main__":
    # GUI 생성
    root = tk.Tk()
    root.title("PLC Control")
    root.geometry("300x200")

    # MXComponent 인스턴스 생성
    plc = MXComponent()

    # 연결 상태 표시 라벨
    status_label = ttk.Label(root, text="연결 상태: 미연결")
    status_label.pack(pady=10)

    # 연결/해제 버튼
    def toggle_connection():
        if not plc.connected:
            if plc.connect():
                status_label.config(text="연결 상태: 연결됨")
                connect_btn.config(text="연결 해제")
        else:
            if plc.disconnect():
                status_label.config(text="연결 상태: 미연결")
                connect_btn.config(text="연결")

    connect_btn = ttk.Button(root, text="연결", command=toggle_connection)
    connect_btn.pack(pady=10)

    # M0 상태 제어
    def toggle_m0():
        if plc.connected:
            current_value = plc.get_device("M30")
            if current_value is not None:  # None 체크 추가
                new_value = 0 if current_value == (0,1) else 1
                plc.set_device("M30", new_value)
                update_m0_status()

    def update_m0_status():
        if plc.connected:
            value = plc.get_device("M30")
            if value is not None:  # None 체크 추가
                m0_label.config(text=f"M30 상태: {value}")
        root.after(100, update_m0_status)  # 100ms마다 상태 업데이트

    m0_btn = ttk.Button(root, text="M30 토글", command=toggle_m0)
    m0_btn.pack(pady=10)

    m0_label = ttk.Label(root, text="M30 상태: -")
    m0_label.pack(pady=10)

    # 초기 상태 업데이트 시작
    update_m0_status()

    root.mainloop()