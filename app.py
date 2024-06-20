from zk import ZK, const
from datetime import datetime

zkDevicesList = [
    {
        "deviceName": "DMM-IT 4th Floor",
        "IP": "172.16.37.50",
        "port": "4370"
    },
    {
        "deviceName": "DMM-Accounting 2nd Floor",
        "IP": "192.168.23.212",
        "port": "4370"
    },
    {
        "deviceName": "DMM-HR",
        "IP": "172.16.37.51",
        "port": "4370"
    }
]





def welcome():
    print("***** ZK CLI APP")
    print("***** Created By Ali Alhashim")
    print("***** to view help menu enter -h")

def list_devices():
    print("***** List of Devices *****")
    for device in zkDevicesList:
        print(f"Device Name: {device['deviceName']}, IP: {device['IP']}, Port: {device['port']}")

def restart_device(ip):
    try: 
        zk = ZK(ip, port=4370, password=0, force_udp=False, ommit_ping=False, timeout=5)
        conn = zk.connect()
        conn.restart()
        conn.disconnect()
        print(f"Device at IP {ip} has been restarted.")
    
    except Exception as e:
        print(e)


def setTimeDate(ip, timeDate):
    #set_time
    #"2024-06-20 14:55:00"

    try:
        zk = ZK(ip, port=4370, password=0, force_udp=False, ommit_ping=False, timeout=5)
        conn = zk.connect()
        date_format = "%Y-%m-%d %H:%M:%S"
        CtimeDate = datetime.strptime(timeDate, date_format).timestamp()
        conn.set_time(timestamp=CtimeDate)
    except Exception as e:
        print(e)

def info(ip):
    try:
        zk = ZK(ip, port=4370, password=0, force_udp=False, ommit_ping=False, timeout=5)
        conn = zk.connect()
        conn.disable_device()
        serial_number = conn.get_serialnumber()
        machine_name  = conn.get_device_name()
        print(f"            IP   : {ip}")
        print(f" Serial Number   : {serial_number}")
        print(f"  Machine Name   : {machine_name}")
        print(f"Firmware Version :{conn.get_firmware_version()}")
        print(f"MAC Address      :{conn.get_mac()}")
        print(f"the memory ussage:{conn.read_sizes()}")
        print(f"machine's time   :{conn.get_time()}")
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.enable_device()  
            conn.disconnect()


# #attendances = conn.get_attendance()

       

def list_users(ip):
    try:
        zk = ZK(ip, port=4370, password=0, force_udp=False, ommit_ping=False, timeout=5)
        conn = zk.connect()
        conn.test_voice() # Say Thank you
        conn.disable_device()
        users = conn.get_users()
        print(f"Users for device at IP {ip}:")
        for user in users:
            print(f"ID: {user.user_id}, Name: {user.name}, Privilege: {user.privilege}, Password: {user.password}, Group ID: {user.group_id}, Card: {user.card}")   
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.enable_device()  
            conn.disconnect()

def main():
    welcome()
    while True:
        userInput = input()
        if userInput.lower() == "-h":
            print("***** list all devices                               -list")
            print("***** restart device: restart IP address example,    -restart 192.168.23.212")
            print("***** list all users in device -userlist IP example, -userlist 192.168.23.212")
            print("***** devise info                                    -info 192.168.23.212")
            print("***** set Time %Y-%m-%d %H:%M:%S                     -setTime 192.168.23.212 2024-06-20 14:55:00")
        elif userInput.lower() == "-list":
            list_devices()
        elif userInput.lower().startswith("-restart "):
            ip = userInput.split(" ")[1]
            restart_device(ip)
        elif userInput.lower().startswith("-userlist "):
            ip = userInput.split(" ")[1]
            list_users(ip)
        elif userInput.lower().startswith("-info "):
            ip = userInput.split(" ")[1]
            info(ip)
        elif userInput.lower().startswith("-setTime "):
            ip = userInput.split(" ")[1]
            timeDate = userInput.split(" ")[2]
            setTimeDate(ip, timeDate)
        elif userInput.lower() == "exit":
            break

if __name__ == "__main__":
    main()
