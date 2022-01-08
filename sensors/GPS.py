import serial
import pynmea2
 
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.2)
except:
    ser = None
 
def gps_read():
    try:
        recv = ser.readline().decode()
        if recv.startswith('$'):
            record = pynmea2.parse(recv)
            if recv.startswith('$GPRMC') or recv.startswith('$GNRMC'):
                print('--------------------------------')
                print('Fix Status: ', record.status)
                print('Latitude: ', record.latitude)
                print('Longitude: ', record.longitude)
                return [record.longitude, record.latitude]
            elif recv.startswith('$GPGGA') or recv.startswith('$GNGGA'):
                print('Number of Satellites availabe:', record.num_sats)
            elif recv.startswith('$GPGSV') or recv.startswith('$BDGSV') or recv.startswith('$GBGSV') or recv.startswith('$GLGSV'):
                if record.msg_num =='1':
                    print('Number of Satellites in View:', record.num_sv_in_view)
                # print("Satallites No.:  GROUP", record.msg_num+'    ','['+record.sv_prn_num_1+':'+record.snr_1+']', '['+record.sv_prn_num_2+':'+record.snr_2+']', '['+record.sv_prn_num_3+':'+record.snr_3+']', '['+record.sv_prn_num_4+':'+record.snr_4+']')
                # print("Satallites CN0: ", record.snr_1, record.snr_2, record.snr_3, record.snr_4)
            # elif recv.startswith('$GPGSA') or recv.startswith('$BDGSA') or recv.startswith('$GNGSA'):
            #         print('Fixed Satellites No.: ', record.sv_id01, record.sv_id02, record.sv_id03, record.sv_id04,record.sv_id05, record.sv_id06,record.sv_id07, record.sv_id08,record.sv_id09, record.sv_id10,record.sv_id11, record.sv_id12)
    except pynmea2.nmea.ParseError:
        print('NMEA wrong！')
    return []

def gps_close():
    ser.close()
