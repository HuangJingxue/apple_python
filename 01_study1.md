```python
@DFF.API('qinxi的函数')
def qinxi_func():
    helper = DFF.SRC("df_influxdb")
    # 空列表用于存放输出结果
    sql = "select last(ip) as ip ,last(ip_normal_req) as ip_normal_req from req_info_summary where time > now() -1h"
    
    db_res = helper.query(sql,database="biz_default")
    return db_res

#截取出IP和访问信息次数
series = qinxi_func()
list_ip = (series["series"][0]["values"][0][1]).split(',')
list_num =  (series["series"][0]["values"][0][2]).split(',')


#传统列表元素处理ip中有‘|上海’
# new_list_ip = []
# for new_ip in list_ip:
#     new_ip =  new_ip.split('|')[0]
#     new_list_ip.append(new_ip)
# print(new_list_ip)

#高级列表元素处理有‘|上海’
new_list_ip = list(map(lambda x:x.split('|')[0],list_ip))
# print(new_list_ip)

#传统列表转换为字典
# dic_test = dict(zip(new_list_ip,list_num))
# print(dic_test)


{'xxx': '80',
 '10.202.3.80': '2834',
 '10.202.68.181': '2693',
 '10.202.68.49': '3005',
 '10.202.73.119': '0',
 '10.202.73.147': '0',
 '10.203.3.207': '0',
 '10.203.98.123': '63667',
 '118.31.5.201': '0',
 'xxx': '3790'}

datav_keys=['name','value']


series = []
for i in  range(len(new_list_ip)):
    values = {'name':new_list_ip[i],
    'value':list_num[i]}
    series.append(values)

print(series)


 [{'name': 'xxx', 'value': '61946'},
 {'name': '42.245.252.50', 'value': '3636'},
 {'name': '10.202.68.49', 'value': '2905'},
 {'name': '10.202.3.80', 'value': '2760'},
 {'name': '10.202.68.181', 'value': '2618'},
 {'name': '10.188.30.100', 'value': '72'},
 {'name': '10.202.73.119', 'value': '0'},
 {'name': '118.31.5.201', 'value': '0'},
 {'name': '10.202.73.147', 'value': '0'},
 {'name': 'xxx', 'value': '0'}]
```
