from zk import ZK, const
from datetime import datetime

################################################################################## Config

##### Devices List
zkDevicesList = [
    {
        "deviceName": "DMM - Ladies",
        "ip": "192.168.23.13",
        "port": "4370"
    }
]

##### 

Default_Port     = 4370
Default_Password = 0
###############################################################################

def welcome():
    print("***** ZK CLI APP")
    print("***** Created By Ali Alhashim")
    print("***** to view help menu enter -h")

def list_devices():
    print("***** List of Devices *****")
    for device in zkDevicesList:
        print(f"Device Name: {device['deviceName']}, IP: {device['ip']}, Port: {device['port']}")

def restart_device(ip):
    try: 
        zk = ZK(ip, port=Default_Port, password=Default_Password, force_udp=False, ommit_ping=False, timeout=5)
        conn = zk.connect()
        conn.restart()
        conn.disconnect()
        print(f"Device at IP {ip} has been restarted.")
    except Exception as e:
        print(f"Error restarting device at IP {ip}: {e}")

def set_time_date(ip, time_date):
    try:
        zk = ZK(ip, port=Default_Port, password=Default_Password, force_udp=False, ommit_ping=False, timeout=5)
        conn = zk.connect()
        date_format = "%Y-%m-%d %H:%M:%S"
        ctime_date = datetime.strptime(time_date, date_format)
        conn.set_time(ctime_date)
        print(f"...set TimeDate: {ip} {time_date} Done.")
        conn.disconnect()
    except Exception as e:
        print("Example: -settime 192.168.23.212 2024-06-20 14:55:00")
        print(f"Error setting time and date for device at IP {ip}: {e}")

def info(ip):
    try:
        zk = ZK(ip, port=Default_Port, password=Default_Password, force_udp=False, ommit_ping=False, timeout=5)
        conn = zk.connect()
        conn.disable_device()
        serial_number = conn.get_serialnumber()
        machine_name = conn.get_device_name()
        print(f"            IP   : {ip}")
        print(f" Serial Number   : {serial_number}")
        print(f"  Machine Name   : {machine_name}")
        print(f"Firmware Version : {conn.get_firmware_version()}")
        print(f"MAC Address      : {conn.get_mac()}")
        print(f"The memory usage : {conn.read_sizes()}")
        print(f"Machine's time   : {conn.get_time()}")
        conn.enable_device()
        conn.disconnect()
    except Exception as e:
        print(f"Error retrieving info for device at IP {ip}: {e}")

def list_users(ip):
    try:
        zk = ZK(ip, port=Default_Port, password=Default_Password, force_udp=False, ommit_ping=False, timeout=5)
        conn = zk.connect()
        conn.test_voice()  # Say Thank you
        conn.disable_device()
        users = conn.get_users()
        print(f"Users for device at IP {ip}:")
        for user in users:
            print(f"UID: {user.uid} - ID: {user.user_id} - Name: {user.name} - Privilege: {user.privilege} - Password: {user.password} - Group ID: {user.group_id} - Card: {user.card}")
        print("#################################")
        print(f"Total users: {len(users)}")
        conn.enable_device()
        conn.disconnect()
    except Exception as e:
        print(f"Error listing users for device at IP {ip}: {e}")

def get_time_sheet(badge_id, start_date, end_date):
    print(f"Get timesheet for {badge_id} from {start_date} to {end_date}")
    # Convert start_date and end_date to datetime objects
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError as e:
        print(f"Error parsing dates: {e}")
        return

    timeSheet = []
    for device in zkDevicesList:
        try:
            zk = ZK(device['ip'], port=Default_Port, password=Default_Password, force_udp=False, ommit_ping=False, timeout=5)
            conn = zk.connect()
            print(f'Connected to device {device["ip"]}')
            attendance = conn.get_attendance()

            user_attendance = [
                record for record in attendance 
                if record.user_id == badge_id and start_date <= record.timestamp <= end_date
            ]
            
            for record in user_attendance:
                timeSheet.append({
                    'user_id': record.user_id,
                    'timestamp': record.timestamp,
                    'status': record.status,
                    'punch': record.punch
                })
            conn.disconnect()
        except Exception as e:
            print(f"Error retrieving timesheet for device at IP {device['ip']}: {e}")

    # Print the timesheet
    for entry in timeSheet:
        print(entry)

def main():
    welcome()
    while True:
        user_input = input()
        if user_input.lower() == "-h":
            print("***** List all devices                               -list")
            print("***** Restart device: restart IP address example,    -restart 192.168.23.212")
            print("***** List all users in device -userlist IP example, -userlist 192.168.23.212")
            print("***** Device info                                    -info 192.168.23.212")
            print("***** Set Time %Y-%m-%d %H:%M:%S                     -settime 192.168.23.212 2024-06-20 14:55:00")
            print("***** Get Timesheet for user by range of date        -gettimesheet 1111 2024-05-16 2024-06-15")
        elif user_input.lower() == "-list":
            list_devices()
        elif user_input.lower().startswith("-restart "):
            ip = user_input.split(" ")[1]
            restart_device(ip)
        elif user_input.lower().startswith("-userlist "):
            ip = user_input.split(" ")[1]
            list_users(ip)
        elif user_input.lower().startswith("-info "):
            ip = user_input.split(" ")[1]
            info(ip)
        elif user_input.lower().startswith("-settime "):
            parts = user_input.split(" ")
            if len(parts) == 3:
                ip = parts[1]
                time_date = parts[2]
                set_time_date(ip, time_date)
            else:
                print("Invalid input for -settime. Example: -settime 192.168.23.212 2024-06-20 14:55:00")
        elif user_input.lower().startswith("-gettimesheet "):
            parts = user_input.split(" ")
            if len(parts) == 4:
                badge_id = parts[1]
                start_date = parts[2]
                end_date = parts[3]
                get_time_sheet(badge_id, start_date, end_date)
            else:
                print("Invalid input for -gettimesheet. Example: -gettimesheet 1111 2024-05-16 2024-06-15")
        elif user_input.lower() in ["exit", "q"]:
            break
        else:
            print("Invalid entry. For help enter -h")

if __name__ == "__main__":
    main()
