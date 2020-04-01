```python
#--*-- coding:utf-8 --*--
# 多线程备份所有SQL Server数据库（有多少服务器就开多少个线程）
# 周日全备份，其它时间差异备份，事务日志备份工作日每小时备份一次(日志备份独立脚本实现)
# 每月1日保留一份月备份，保留12个月
# 1月1日保留一份年备份，保留5年
 
import os,time,logging
import pymssql
import threading
from datetime import datetime
 
 
logpath='D:\\scripts\\backup\\logs\\'
# 日志目录是否存在
isExists = os.path.exists(logpath)
if not isExists:
    os.makedirs(logpath)
# 日志信息
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)-4s %(message)s',
                    filename=logpath + 'backup_db_' + time.strftime('%Y%m%d_%H%M%S', time.localtime()) + '.log',
                    filemode='w',
                    datefmt='%Y%m%d %X')
 
# 按照时间决定采用哪种备份类型
weekday = datetime.now().weekday()
 
class MSSQL:
 
    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
 
    def __GetConnect(self):
        # 创建连接
        if not self.db:
            raise(NameError,"Not set db info")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"Connect db Failed!")
        else:
            return cur
 
    def ExecQuery(self,sql):
        # 执行查询语句
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
 
        self.conn.close()
        return resList
 
    def ExecNonQuery(self,sql):
        # 执行非查询语句
 
        cur = self.__GetConnect()
        try:
            self.conn.autocommit(True)
            cur.execute(sql)
            self.conn.autocommit(False)
        except Exception as e:
            logging.info(e)
        self.conn.close()
 
class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name=name
        self.func=func
        self.args=args
    def run(self):
        apply(self.func,self.args)
 
def delbak(path,flag):
    f = list(os.listdir(path))
    #logging.info("Delete >31 days backup file %s" % path)
    for i in range(len(f)):
        filedate = os.path.getmtime(path + f[i])
        currdate = time.time()
        num = (currdate - filedate) / (60 * 60 * 24 * 31 )
        if flag == 'sunday':
            if num > 3:
                if os.path.isfile(path + f[i]):
                    try:
                        os.remove(path +   f[i])
                        #logging.info(u"Delete %s" % f[i])
                    except Exception as e:
                        logging.info(e)
        if flag == 'mon':
            if num > 12:
                if os.path.isfile(path + f[i]):
                    try:
                        os.remove(path + f[i])
                        #logging.info(u"Delete %s" % f[i])
                    except Exception as e:
                        logging.info(e)
        if flag == 'year':
            if num > 12 * 5:
                if os.path.isfile(path + f[i]):
                    try:
                        os.remove(path + f[i])
                        #logging.info(u"Delete %s" % f[i])
                    except Exception as e:
                        logging.info(e)
 
def backup(ip,mark):
    stip='\\\\10.110.0.1\\'
    ms = MSSQL(host=ip,user="dumper",pwd="123456",db="master")
    # 只备份所有业务数据库
    dblist = ms.ExecQuery("SELECT name FROM Master..SysDatabases Where dbid > 6")
 
    delpath = stip + '\\dbbackup\\' + ip + '\\'
    # 逐个库进行备份
    for db in dblist:
        # 备份的数据库名
        dbname = db[0]
        logging.info('Backup '+ ip + ' ' + dbname)
        ti = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        # 指定备份目录
        path = delpath  + dbname + "\\" 
        # 全量/差异备份标识
        flag = 1
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            flag = 0
        # 备份文件名
        fname = path + dbname + "_" + str(ti)
 
        # 年初 月初多保留一份
        dat = time.strftime('%Y%m%d', time.localtime())
        mon = '%d%02d01' % (time.localtime().tm_year, time.localtime().tm_mon)
        year = '%d0101' % (time.localtime().tm_year)
 
        if dat == mon:
            fname = path + dbname + "_" + str(ti) + "_full.bak"
            sql = "backup database [" + dbname + "] to disk='" + fname + "' with checksum,compression"
            print(sql)
            ms.ExecNonQuery(sql)
            # 月
            mpath = path + 'month\\'
            isExists = os.path.exists(mpath)
            if not isExists:
                os.makedirs(mpath)
            cmd = 'copy ' + fname + ' ' + mpath
            os.system(cmd)
            # 删除超过12月的备份文件
            delbak(mpath,'mon')
            if dat == year:
                # 年
                ypath = path + 'year\\'
                isExists = os.path.exists(ypath)
                if not isExists:
                    os.makedirs(ypath)
                cmd = 'copy ' + fname + ' ' + ypath
                os.system(cmd)
                # 删除超过5年的备份文件
                delbak(ypath,'year')
        elif weekday == 6:
            fname = path + dbname + "_" + str(ti) + "_full.bak"
            sql = "backup database [" + dbname + "] to disk='" + fname + "' with checksum,compression"
            print(sql)
            # 执行备份
            ms.ExecNonQuery(sql)
            # 删除超过30天的备份文件
            delbak(path,'sunday')
        else:
            if flag == 0:
                fname = path + dbname + "_" + str(ti) + "_full.bak"
                sql = "backup database [" + dbname + "] to disk='" + fname + "' with checksum,compression"
                logging.info(dbname + " is a new db, first backup must full backup.")
            else:
                fname = path + dbname + "_" + str(ti) + "_diff.bak"
                sql = "backup database [" + dbname + "] to disk='" + fname + "' with differential,checksum,compression"
            print(sql)
            # 执行备份
            ms.ExecNonQuery(sql)    
 
 
def main():
    # 所有需要备份的数据库IP
    pre = '192.'
    iplist = ('100.10.11','100.10.12','100.10.13','100.10.14','100.10.15','100.10.16','100.10.17','100.10.18','100.10.19',
              '100.10.220','100.10.200','100.10.180','100.10.181','100.65.150','100.65.151',
              '100.65.190','100.66.19','100.66.59',
              '11.12.81','11.12.11',
             )
 
    threads = []
    num = len(iplist)
    for i in iplist:
        ip = pre + i
        t = MyThread(backup,(ip,0),backup.__name__)
        threads.append(t)
 
    for i in xrange(num):
        threads[i].start() 
    for i in xrange(num):
        threads[i].join()
    logging.info(num)
        
if __name__ == '__main__':
    main()
```
