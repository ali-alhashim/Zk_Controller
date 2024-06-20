from zk import ZK, const

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
        zk = ZK(ip, port=4370, password=0, force_udp=False, ommit_ping=False)
        conn = zk.connect()
        conn.restart()
        conn.disconnect()
        print(f"Device at IP {ip} has been restarted.")
    except Exception as e:
        print(e)
       

def list_users(ip):
    try:
        zk = ZK(ip, port=4370, password=0, force_udp=False, ommit_ping=False)
        conn = zk.connect()
        users = conn.get_users()
        print(f"Users for device at IP {ip}:")
        for user in users:
            print(f"ID: {user.user_id}, Name: {user.name}, Privilege: {user.privilege}, Password: {user.password}, Group ID: {user.group_id}, Card: {user.card}")
        conn.disconnect()
    except Exception as e:
        print(e)

def main():
    welcome()
    while True:
        userInput = input()
        if userInput.lower() == "-h":
            print("***** list all devices                               -list")
            print("***** restart device: restart IP address example,    -restart 192.168.23.212")
            print("***** list all users in device -userlist IP example, -userlist 192.168.23.212")
        elif userInput.lower() == "-list":
            list_devices()
        elif userInput.lower().startswith("-restart "):
            ip = userInput.split(" ")[1]
            restart_device(ip)
        elif userInput.lower().startswith("-userlist "):
            ip = userInput.split(" ")[1]
            list_users(ip)
        elif userInput.lower() == "exit":
            break

if __name__ == "__main__":
    main()
