from library import translateAA
# def puts(ip, user,  private, port):
# pkey = paramiko.RSAKey.from_private_key_file('C:/Users/THINK/.ssh/id_rsa')
# transport = paramiko.Transport(('192.168.52.133', 22))
# transport.connect(username='root', pkey=pkey)
    # try:
# sftp = paramiko.SFTPClient.from_transport(transport)
# sftp.put('monitor.sh','/tmp/monitor.sh')
# sftp.put('./deployenv.sh','/tmp/deploy.sh' )
# client = paramiko.SSHClient()
# client._transport = transport
# client.exec_command(command='bash /tmp/deploy.sh')
    # finally:
# transport.close()

translateAA.puts('192.168.52.133','root','C:/Users/THINK/.ssh/id_rsa',22)