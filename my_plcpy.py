import win32com.client
    

class PlcConnect:

    def __init__(self):

        self.plc = win32com.client.Dispatch("ActUtlType.ActUtlType")
        self.isConnected = False
        self.station_num = int(input('스테이션 번호를 입력하세요 : '))
        
    
    def connect(self):
        
        self.plc.ActLogicalStationNumber = self.station_num
        result = self.plc.Open()

        if result == 0:
            self.isConnected = True
            text = '연결 성공'
            return True, text
        else:
            text = f'연결 실패 (에러코드 {result})'
            return False, result
        
    def disconnect(self):

        if self.isConnected:
            self.plc.ActLogicalStationNumber = self.station_num
            result = self.plc.Close()

            if result == 0:
                self.isConnected = False
                text = '연결 해제 성공'
                return True, text
            else:
                text = f'연결 실패 (에러코드 {result})'
                return False, text
        else:
            text = 'PLC가 미연결 상태입니다.'
            return 0, text
    
    def ReadDeviceBlock(self,_device,_count):
        read_list =[]
        if self.isConnected:
            for i in range(_device,_device+_count):
                device = self.plc.GetDevice(f"D{i}")
                read_list.append(device[1])
            return read_list
        else:
            return False

    def WriteDeviceBlock(self,_device,_count):
        write_list = [0,1,2,3,4,5,6,7,8,9] 
        if self.isConnected:
            for i in range(_device,_device+_count):
                self.plc.SetDevice(f"D{i}",write_list.pop(0))
            return True
        else:
            return False
        


            