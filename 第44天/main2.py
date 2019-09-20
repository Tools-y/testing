from library import analyseAA
# from library import analysis
# from library import record
# from library import dingtalk

analyseAA.gets('192.168.52.133','root','C:/Users/THINK/.ssh/id_rsa')

analyseAA.analysis()

schedule={20190831:17770718040,20190809:17770718041}
analyseAA.dingtalk('1fbb36af7526afead22497c49934bd225655be46f4da601c5ba06e26f28f5a7b',schedule)


analyseAA.record('192.168.52.134', 'tools', 'Yuan..1234', port=3306, db='systeminformations', logpath='./monitor.log')