import my_plcpy
import time
import tkinter as tk
from tkinter import ttk
import sqlitepractice as sp

plc = my_plcpy.PlcConnect()
act = plc.plc

db = sp.Database()



if __name__ == "__main__":
    # GUI 생성
    root = tk.Tk()
    root.title("PLC Control")
    root.geometry("300x200")

    # 연결 상태 표시 라벨
    status_label = ttk.Label(root, text="연결 상태: 미연결")
    status_label.pack(pady=10)

    def dbplc(db, plc):
        db.reset_table()
        db.create_table()
        readList = plc.ReadDeviceBlock(0,10)
        print(readList) 
        db.insert_plc(readList)
        root.after(1000, dbplc, db, plc)

    # 연결/해제 버튼
    def toggle_connection():
        if not plc.isConnected:
            if plc.connect():
                status_label.config(text="연결 상태: 연결됨")
                connect_btn.config(text="연결 해제")

                dbplc(db, plc)

        else:
            if plc.disconnect():
                status_label.config(text="연결 상태: 미연결")
                connect_btn.config(text="연결")

    connect_btn = ttk.Button(root, text="연결", command=toggle_connection)
    connect_btn.pack(pady=10)
    
    root.mainloop()


