import time
import datetime
import logging
import pymysql.cursors
import json
import requests
import paramiko
def gets(ip, user,  private, port=22):
    pkey = paramiko.RSAKey.from_private_key_file(private)
    transport = paramiko.Transport((ip, port))
    transport.connect(username=user, pkey=pkey)
    try:
        client = paramiko.SSHClient()
        client._transport = transport
        client.exec_command(command='bash /tmp/monitor.sh')
        time.sleep(5)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(remotepath='/var/log/monitor/monitor.log', localpath='./monitor.log')
    finally:
        transport.close()





def analysis(cpu=0, memory=2, disk=5, logpath='./monitor.log'):
    logging.basicConfig(level=logging.WARNING,
                        filename='./warning.log',
                        filemode='a',
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    with open(file=logpath, mode='r') as file:
            log = file.readlines()[0].split('-')[-1]
            logs = json.loads(log)
            for items in logs.items():
                if items[0] == 'cpu':
                    if items[1]['user'] + items[1]['system'] > cpu:
                        logging.warning('cpu usage rate: {}'.format(items[1]['user'] + items[1]['system']))
                elif items[0] == 'memory':
                    if int(items[1]['percent']) > memory:
                        logging.warning('memory usage rate: {}'.format(items[1]['percent']))
                elif items[0] == 'disk':
                    if int(items[1]['percent'].strip('%')) > disk:
                        logging.warning('disk usage rate: {}'.format(items[1]['percent']))


def dingtalk(token,schedule, logpath='./monitor.log'):
    token =token
    api = 'https://oapi.dingtalk.com/robot/send?access_token={}'.format(token)
    header = {'Content-Type': 'application/json'}

    def info(messages, phone):
        data = {"msgtype": "text",
                "text": {"content": "{}".format(messages)},
                'at': {'atMobiles': ["{}".format(phone)]},
                'isAtAll': 'false'}
        sendData = json.dumps(data).encode('utf-8')
        return sendData
    # dictA={20190830:17770718040,20190809:17770718041}
    with open(file=logpath, mode='r') as file:
            log = file.readlines()[0].split('-')[-1]
            logs = json.loads(log)
            now_time = datetime.datetime.now().strftime('%Y%m%d')
            for items in logs.items():
                if items[0] == 'cpu':
                    if (items[1]['user'] + items[1]['system']) > 50:

                       if int(now_time)in schedule:
                        requests.post(url=api, headers=header, data=info(
                            messages='[warning]: cpu rate: {}'.format(items[1]['user'] + items[1]['system']),
                            phone=schedule[int(now_time)]     # 写一个读取排班表格的函数获取返回值
                        ))
                if items[0] == 'memory':
                    if items[1]['percent'] > 50:
                        requests.post(url=api, headers=header, data=info(
                            messages='[warning]: memory rate: {}'.format(items[1]['percent']),
                            phone=schedule[int(now_time)]
                        ))
                if items[0] == 'disk':
                    if int(items[1]['percent'].strip('%')) > 5:
                        requests.post(url=api, headers=header, data=info(
                            messages='[warning]: disk rate: {}'.format(items[1]['percent']),
                            phone=schedule[int(now_time)]
                        ))



def record(serverIP, dbUser, dbPasswd, port=3306, db='systeminformations', logpath='./monitor.log'):
    """
    {
        "cpu": {"user": 1, "system": 0, "idle": 99},
        "memory": {"total": 972, "free": 177, "percent": 80.0},
        "disk": {"percent": "13%"}
    }
    """
    client = pymysql.connect(host=serverIP, user=dbUser, password=dbPasswd, db=db, port=3306)
    try:
        with client.cursor() as cursors:
            with open(file='monitor.log', mode='r') as file:
                    lines=file.readlines()

                    log = lines[0].split('-')[-1]

                    logs = json.loads(log)
                    hostname = lines[0].split('-')[-2]
                    times = lines[0].split('-')[0]

                    for items in logs.items():
                        if items[0] == 'cpu':
                            sql = "insert into cpu values ('{}', '{}', {}, {}, {});"
                            cursors.execute(sql.format(times, hostname, items[1]['user'], items[1]['system'], items[1]['idle']))
                        elif items[0] == 'memory':
                            sql = "insert into mem values ({}, '{}',{}, {}, {});"
                            cursors.execute(sql.format(times, hostname,items[1]['total'], items[1]['free'], items[1]['percent']))
                        elif items[0] == 'disk':
                            sql = "insert into disk values ({}, '{}', '{}');"
                            cursors.execute(sql.format(times, hostname, items[1]['percent']))
    finally:
        client.commit()
        client.close()
