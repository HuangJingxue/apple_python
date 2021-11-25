#!/usr/bin/env python3
# -*- coding: gbk -*- 


import psutil
import pymysql
import argparse
import json
import datetime


def get_cpu_info(verbose):
    cpu_info={}
    if verbose >0:
        print("[cpu]    start collect cpu info ...")
    data=psutil.cpu_times_percent(3)
    cpu_info['user']=data[0]
    cpu_info['system']=data[2]
    cpu_info['idle']=data[3]
    cpu_info['iowait']=data[4]
    cpu_info['hardirq']=data[5]
    cpu_info['softirq']=data[6]
    cpu_info['cpu_cores']=psutil.cpu_count()
    if verbose >0:
        print("{0}".format(json.dumps(cpu_info,ensure_ascii=False,indent=4)))
        print("[cpu]    collection compeleted ...")
    return cpu_info


def get_mem_info(verbose):
    mem_info={}
    if verbose >0:
        print("[mem]    start collect mem info ...")
    data=psutil.virtual_memory()
    mem_info['total']=data[0]/1024/1024/1024
    mem_info['avariable']=data[1]/1024/1024/1024
    if verbose>0:
        print("{0}".format(json.dumps(mem_info,ensure_ascii=False,indent=4)))
        print("[mem]    collection compeletd ...")
    return mem_info


def get_disk_info(verbose):
    disk_info={}
    if verbose >0:
        print("[disk]    start collect disk info ...")
    partitions=psutil.disk_partitions()
    partitions=[(partition[1],partition[2])for partition in partitions if partition[2]!='iso9660']
    disk_info={}
    for partition in partitions:
        disk_info[partition[0]]={}
        disk_info[partition[0]]['fstype']=partition[1]
    for mount_point in disk_info.keys():
        data=psutil.disk_usage(mount_point)
        disk_info[mount_point]['total']=data[0]/1024/1024/1024
        disk_info[mount_point]['used_percent']=data[3]
    if verbose >0:
        print("{0}".format(json.dumps(disk_info,ensure_ascii=False,indent=4)))
        print("[disk]    collection compeleted ....")
    return disk_info


def get_mysql_info(cnx_args,status_list):
    config={
        'user':cnx_args.user,
        'password':cnx_args.password,
        'host':cnx_args.host,
        'port':cnx_args.port}
    cnx=None
    cursor=None
    mysql_info={}
    try:
        cnx=pymysql.connect(**config)
        cursor=cnx.cursor()
        for index in range(len(status_list)):
            status_list[index].get_status(cursor)
            status=status_list[index]
            mysql_info[status.name]=status.value
        mysql_info['port']=config['port']
    except pymysql.connect.Error as err:
        print(err)
    finally:
        if cursor != None:
            cursor.close()
        if cnx != None:
            cnx.close()
    return mysql_info


class Status(object):
    def __init__(self,name):
        self.name=name
        self._value=None




    def get_status(self,cursor):
        stmt="show global status like '{0}';".format(self.name)
        cursor.execute(stmt)
        value=cursor.fetchone()[1]
        self._value=int(value)




    @property
    def value(self):
        if self._value==None:
            raise Exception("cant get value befor execute the get_status function")
        else:
            return self._value


IntStatus=Status




class diskResource(object):
    def __init__(self,mount_point,status):
        self.mount_point=mount_point
        self.status=status


    def __str__(self):
        result='''                <div class="stage-list">
                    <div class="stage-title"><span>{0}</span></div>
                    <div class="detail">
                        <p class="detail-list">
                            <span class="detail-title">range_format</span>
                            <span class="detail-describe">{1}</span>
                        </p>
                        <p class="detail-list">
                            <span class="detail-title">total_space</span>
                            <span class="detail-describe">{2:8.2f}G</span>
                        </p>
                        <p class="detail-list">
                            <span class="detail-title">used_space(%)</span>
                            <span class="detail-describe">{3:8.2f}</span>
                        </p>
                        <p class="detail-list">
                            
                        </p>
                    </div>
                </div>\n'''.format(self.mount_point,self.status['fstype'],self.status['total'],self.status['used_percent']
)
        return result


class diskResources(object):
    def __init__(self,status):
        self.disks=[]
        for mount_point in status.keys():
            self.disks.append(diskResource(mount_point,status[mount_point]))


    def __str__(self):
        result='''        <div class="list-item">
            <div class="category">
                <span>disk</span>
            </div>
            <div class="second-stage">\n'''
        for index in range(len(self.disks)):
            result=result+self.disks[index].__str__()
        result=result+'''            </div>
        </div>\n'''
        return result


class cpuResources(object):
    def __init__(self,status):
        self.status=status
    def __str__(self):
        result='''        <div class="list-item">
            <div class="category">
                <span>CPU</span>
            </div>
            <div class="second-stage">
                <div class="stage-list">
                    <div class="stage-title"><span>global</span></div>
                    <div class="detail">
                        <p class="detail-list">
                            <span class="detail-title">user_space(%)</span>
                            <span class="detail-describe">{0}</span>
                        </p>
                        <p class="detail-list">
                            <span class="detail-title">kernel_space(%)</span>
                            <span class="detail-describe">{1}</span>
                        </p>
                        <p class="detail-list">
                            <span class="detail-title">space(%)</span>
                            <span class="detail-describe">{2}</span>
                        </p>
                        <p class="detail-list">
                            <span class="detail-title">hard_cruppt(%)</span>
                            <span class="detail-describe">{3}</span>
                        </p>
                        <p class="detail-list">
                            <span class="detail-title">soft_cruppt(%)</span>
                            <span class="detail-describe">{4}</span>
                        </p>
                        <p class="detail-list">
                            <span class="detail-title">io_wait(%)</span>
                            <span class="detail-describe">{5}</span>
                        </p>
                        <p class="detail-list">


                        </p>
                    </div>
                </div>
            </div>
        </div>\n'''.format(self.status['user'],self.status['system'],self.status['idle'],self.status['hardirq'],self.status['softirq'],self.status['iowait'])
        return result


class memResources(object):
    def __init__(self,status):
        self.status=status


    def __str__(self):
        result='''        <div class="list-item">
            <div class="category">
                <span>MEM</span>
            </div>
            <div class="second-stage">
                <div class="stage-list">
                    <div class="stage-title"><span>global</span></div>
                    <div class="detail">
                        <p class="detail-list">
                            <span class="detail-title">total</span>
                            <span class="detail-describe">{0:8.2f}G</span>
                        </p>
                        <p class="detail-list">
                            <span class="detail-title">free</span>
                            <span class="detail-describe">{1:8.2f}G</span>
                        </p>
                        
                        <p class="detail-list">
                            
                        </p>
                    </div>
                </div>
            </div>
        </div>'''.format(self.status['total'],self.status['avariable'])
        return result




class mysqlResources(object):
    def __init__(self,status):
        self.status=status
    def __str__(self):
        result='''        <div class="list-item">
            <div class="category">
                <span>MYSQL</span>
            </div>
            <div class="second-stage">
                <div class="stage-list">
                    <div class="stage-title"><span>{0}</span></div>
                    <div class="detail">
                        <p class="detail-list">
                            <span class="detail-title">innodb_log_wait</span>
                            <span class="detail-describe">{1}</span>
                        </p>
                        <p class="detail-list">
                            <span class="detail-title">binlog_cache_use</span>
                            <span class="detail-describe">{2}</span>
                        </p>
                        <p class="detail-list">
                            <span class="detail-title">create_temp_disk_table</span>
                            <span class="detail-describe">{3}</span>
                        </p>
                        <p class="detail-list">
                            <span class="detail-title">Slow_querys</span>
                            <span class="detail-describe">{4}</span>
                        </p>
                        <p class="detail-list">
                            <span class="detail-title">Com_select</span>
                            <span class="detail-describe">{5}</span>
                        </p>



                        <p class="detail-list">
                            
                        </p>
                    </div>
                </div>
            </div>
        </div>'''.format(self.status['port'],self.status['Innodb_log_waits'],self.status['Binlog_cache_use'],
                          self.status['Created_tmp_disk_tables'],self.status['Slow_queries'],self.status['Com_select'])


        return result


class hostResources(object):
    def __init__(self,cpu_info,mem_info,disk_info,mysql_info,report_title='MySQL health check'):
        self.cpu=cpuResources(cpu_info)
        self.mem=memResources(mem_info)
        self.disk=diskResources(disk_info)
        self.mysql=mysqlResources(mysql_info)
        self.report_title=report_title
    def __str__(self):
        result='''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>health_check</title>
<style>
*{
    margin: 0;
    padding: 0;
}
    .content{
        width:1000px;
        height: auto;
        margin: 30px auto;
        border-bottom:1px solid #b2b2b2;
    }
    .list-item{
        border:1px solid #b2b2b2;
        border-bottom: none;
        transition: all .35s;
        overflow: hidden;
        display: flex;
    }
    .list-item:empty{
        display: none;
    }
    .top-title{
        line-height: 32px;
        font-size: 16px;
        color: #333;
        text-indent: 10px;
        font-weight: 600;
    }
    .category{
        width:97px;
        height: auto;
        border-right: 1px solid #b2b2b2;
        float: left;
        text-align: center;
        position: relative;
    }
    .stage-title>span,
    .category>span{
        display: block;
        height: 20px;
        width:100%;
        text-align: center;
        line-height: 20px;
        position: absolute;
        top: 50%;
        margin-top: -10px;left: 0;
    }
    .second-stage{
        width:900px;
        float: left;
    }
    .stage-list{
        border-bottom: 1px solid #b2b2b2;
        display: flex;
    }
    .stage-list:last-child{
        border-bottom: 0;
    }
    .stage-title{
        width:99px;
        border-right: 1px solid #b2b2b2;
        position: relative;
    }
    .detail{
        flex: 1;
    }
    .detail-list{
        border-bottom: 1px solid #b2b2b2;
        height: 40px;
        display: flex;
        transition: all .35s;
    }
    .detail-title{
        padding: 10px;
        height: 20px;
        line-height: 20px;
        border-right: 1px solid #b2b2b2;
        width:200px;
    }
    .detail-describe{
        flex: 1;
        padding: 10px;line-height: 20px;
    }
    .detail-list:last-child{
        border-bottom: 0;
    }
    .list-item:hover{
        background-color: #eee;
    }
    .detail-list:hover{
        background-color: #d1d1d1;
    }
</style>
</head>
<body>
    <div class="content">
                <div class="list-item">
                        <p class="top-title">report_title</p>
                </div>\n'''


        result=result.replace('report_title',self.report_title)
        result=result+self.cpu.__str__()
        result=result+self.mem.__str__()
        result=result+self.disk.__str__()
        result=result+self.mysql.__str__()
        result=result+'''    </div>
</body>
</html>'''
        return result




if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--verbose',type=int,default=1,help='verbose for output')
    parser.add_argument('--user',default='root',help='user name for connect to mysql')
    parser.add_argument('--password',default='roo123',help='user password for connect to mysql')
    parser.add_argument('--host',default='127.0.0.1',help='mysql host ip')
    parser.add_argument('--port',default=3306,type=int,help='mysql port')
    parser.add_argument('--int-status',default=('Com_select,Com_insert,Com_update,Com_delete,Innodb_log_waits,'
                                                'Binlog_cache_disk_use,Binlog_cache_use,Created_tmp_disk_tables,'
                                                'Slow_queries')
                       ,help='mysql status its value like int')
    parser.add_argument('--report-title',default='MySQL health check',help='report title')
    parser.add_argument('--output-dir',default='/tmp/',help='default report file output path')
    args=parser.parse_args()
    cpu_info=get_cpu_info(args.verbose)
    mem_info=get_mem_info(args.verbose)
    disk_info=get_disk_info(args.verbose)
    status_list=[ IntStatus(name=item) for item in args.int_status.split(',')]
    mysql_info=get_mysql_info(args,status_list)
    hr=hostResources(cpu_info,mem_info,disk_info,mysql_info,args.report_title)
    now1=str(datetime.datetime.now()).replace(' ','_')
    now2=now1.replace(':','')
    if args.output_dir.endswith('/') != True:
        args.output_dir=args.output_dir+'/'
    filename=args.output_dir+'mysql_inspection_{0}.html'.format(now2)
    with open(filename,'w') as output:
        output.write(hr.__str__())
    print('[report]    the report been saved to {0} ok.'.format(filename))
