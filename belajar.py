import sshtunnel
import paramiko, os

current_directory = os.getcwd()
ppk_dir = current_directory + r'\settings\test3.pem'

if os.path.exists(ppk_dir):
    print(f"The file {ppk_dir} exists.")
else:
    print(f"The file {ppk_dir} does not exist.")
# --- Input Values (REPLACE THESE WITH YOUR ACTUAL VALUES) ---
REMOTE_SERVER_IP = "152.42.226.71"  # IP or hostname of your SSH jump host
SSH_USERNAME = "root"  # Your username on the jump host
SSH_PRIVATE_KEY = ppk_dir  # Path to your *OpenSSH* private key file (not .ppk)
SSH_PRIVATE_KEY_PASSWORD = "cfu800212"  # Passphrase for your private key (or "" if none)
PRIVATE_SERVER_IP = "localhost"  # IP of the server you want to reach *through* the tunnel
PRIVATE_SERVER_PORT = 443  # The port of the server you want to reach
LOCAL_BIND_PORT = 10022  # Local port for the tunnel (can usually be left as is)

try:
    with sshtunnel.open_tunnel(
        (REMOTE_SERVER_IP, 22),  # SSH server address and port (22 is the default SSH port)
        ssh_username=SSH_USERNAME,
        ssh_pkey=SSH_PRIVATE_KEY,
        ssh_private_key_password=SSH_PRIVATE_KEY_PASSWORD,
        remote_bind_address=(PRIVATE_SERVER_IP, PRIVATE_SERVER_PORT),  # Destination server and port
        local_bind_address=('0.0.0.0', LOCAL_BIND_PORT)) as tunnel:  # Local port to listen on

        # --- SSH Connection through the Tunnel ---
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Use with caution in production
        client.connect('127.0.0.1', LOCAL_BIND_PORT)  # Connect to the *local* end of the tunnel

        # --- Example Operations with the SSH Client ---
        # Get the RSA key fingerprint to check it.
        key = client.get_transport().getpeerkey()
        if key.get_name() == 'ssh-rsa':
            fingerprint = paramiko.util.format_fingerprint(key)
            print(f"RSA Fingerprint: {fingerprint}")
        else:
            print(f"Key type: {key.get_name()}")

        stdin, stdout, stderr = client.exec_command("ls -l")  # Example command: list files

        for line in stdout:  # Print the command's output
            print(line.strip())

        client.close()  # Close the SSH connection

    print('SSH Tunnel and Connection Successful!')

except Exception as e:
    print(f"An error occurred: {e}")