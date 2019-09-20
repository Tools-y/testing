import paramiko
def puts(ip, user, private, port):
    pkey = paramiko.RSAKey.from_private_key_file(private)
    transport = paramiko.Transport((ip, port))
    transport.connect(username=user, pkey=pkey)
    try:
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(remotepath='/tmp/monitor.sh', localpath='monitor.sh')
        sftp.put(remotepath='/tmp/deploy.sh', localpath='deployenv.sh')
        client = paramiko.SSHClient()
        client._transport = transport
        client.exec_command(command='bash /tmp/deploy.sh')
    finally:
        transport.close()

# translateAA.puts('192.168.52.133','root','C:/Users/THINK/.ssh/id_rsa',22)