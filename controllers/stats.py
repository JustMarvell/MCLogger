import settings
import paramiko

def get_ssh():
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(
        settings.SERVER_HOST,
        port=int(settings.SERVER_SFTP_PORT),
        username=settings.SERVER_SFTP_USER,
        password=settings.SERVER_SFTP_PASSWORD,
    )
    return c

def ssh_run(client, cmd):
    _, stdout, _ = client.exec_command(cmd)
    return stdout.read().decode().strip()