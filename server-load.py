import psutil
import time
import paramiko

def check_system_usage():
    cpu_usage = psutil.cpu_percent(interval=1) 
    
    memory = psutil.virtual_memory()
    memory_usage = memory.percent 

    
    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_usage}%")

def run_ssh_command(host, username, password, command):
    
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        client.connect(host, username=username, password=password)
        
        stdin, stdout, stderr = client.exec_command(command)
        
        result = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if result:
            print(f"Output from {host}:\n{result}")
        if error:
            print(f"Error from {host}:\n{error}")
        
      
        client.close()
    except Exception as e:
        print(f"Failed to connect to {host}: {e}")

def monitor_cluster(ssh_hosts, interval=5, duration=60):
    start_time = time.time()
    while time.time() - start_time < duration:
        check_system_usage()

        for host in ssh_hosts:
            print(f"Checking {host}...")
            run_ssh_command(host['host'], host['username'], host['password'], 'top -b -n 1 | head -n 10') 

        time.sleep(interval)

if __name__ == "__main__":
    ssh_hosts = [
        {'host': '192.168.1.100', 'username': 'user1', 'password': 'password1'},
        {'host': '192.168.1.101', 'username': 'user2', 'password': 'password2'},
    ]

    monitor_cluster(ssh_hosts, interval=5, duration=60)  
