import dba_learn__get_order_info
import dba_learn__get_dg_promotion_data
import dba_learn__get_product
import dba_learn__get_user_info
import dba_learn__get_product_consume

import datetime,time
import random
@DFF.API('获取自动生成订单和订单产品映射信息')
def get_datetime():
    order_date = time.strftime('%Y%m%d', time.localtime(time.time()))
    return  order_date

def get_order_id():
    """
    获取订单信息
    """
    orders = dba_learn__get_order_info.get_order_info()
    orders_id = list(map(lambda x: x['order_id'], orders['msg']))
    orders_id1 = int(str(orders_id[0])[8:])+1
    order_id2 = str(orders_id1).zfill(4)
    order_id = (get_datetime() + order_id2)
    return order_id

def get_user_id():
    """
    获取选择用户ID
    """
    users = dba_learn__get_user_info.get_user_info()
    user_id = random.choice(list(map(lambda x:x["user_id"],users['msg'])))
    return user_id


def get_product_order_num():
    """
    获取随机产品和购买数量
    """
    products = random.sample(list(map(lambda x:[x['product_id'],x['price']],dba_learn__get_product.get_product()['msg'])),random.choice(range(1, len(dba_learn__get_product.get_product()["msg"]) + 1)))

    product_order_num = list(map(lambda x:[x, random.choice(range(1,10))],products))
    return product_order_num


def get_order_award_promotion_info():
    """
    获取奖励积分和打折信息
    """
    order_award = 1
    promotion_info = 1
    order_date = get_datetime()
    data = dba_learn__get_dg_promotion_data.get_dg_promotion_data()['msg']
    promotion_data= list(filter(lambda x:x['promotion_date'] == order_date, data))
    for i in promotion_data:
            if i["promotion_info"] == "双倍积分":
                order_award = 2
            if i["promotion_info"] == "打折8":
                promotion_info = 0.8
    data = [order_award, promotion_info]
    return data



def get_qinxi_random_order_info():
    """
    获取自动生成订单和订单产品映射信息
    """
    order_award = get_order_award_promotion_info()[0]
    promotion_info = get_order_award_promotion_info()[1]
    order_to_products = get_product_order_num()
    order_id = get_order_id()
    get_score = sum(list(map(lambda x:x[0][1]*x[1], order_to_products))) * order_award
    pay = sum(list(map(lambda x:x[0][1]*x[1], order_to_products))) * promotion_info
    data =     {"order_info":
                    {
                        'order_id':order_id,
                        'order_date':get_datetime(),
                        'user_id':get_user_id(),
                        'order_award':order_award,
                        'promotion_info':promotion_info,
                        'get_score': get_score,
                        'pay':pay
                    },
    "order_to_products": list(map(lambda x:{
                                                'product_id': x[0][0],
                                                'order_id': order_id,
                                                'order_num': x[1]
                                                }, order_to_products))
    }
    return data

@DFF.API('写入时间线(衾袭)')
def get_qinxi_insert_influxdb(points):
    helper = DFF.SRC('df_influxdb')
    db = DFF.ENV('it_database')
    try :
        series = helper.write_points(points,database=db)
    except Exception as e:
        DFF.log(str(e))

def get_qinxi_select_influxdb():
    #获取最新订单号
    conn_name = DFF.SRC('df_influxdb')
    db_name = DFF.ENV('it_database')
    select_sql = '''select order_id,pay,order_date,promotion_info,order_num from dba_hjt_qx order by time desc limit 1'''
    try :
        select_ret = conn_name.query(select_sql,database=db_name)
    except Exception as e:
        DFF.log(str(e))
    #return select_ret
    return select_ret

@DFF.API('采集订单数据(衾袭)')
def get_qinxi_order_data():
    """
    时序数据库模型
    measurement:
    dba_test
    tag:
    order_id,user_id,user_name,product_id,product_name,order_date
    filed:
     'order_id','get_score', 'pay','order_date','order_award','promotion_info','order_num','min_used_days','max_used_days','official_used_days'
    """
    order = get_qinxi_random_order_info()
    user_list = dba_learn__get_user_info.get_user_info()['msg']
    product_list = dba_learn__get_product.get_product()['msg']
    product_consume_list = dba_learn__get_product_consume.get_product_consume()['msg']
    points = []

    for i in order['order_to_products']:
        point = {
            "measurement": "dba_hjt_qx",
            "tags": {
                'order_id':order['order_info']['order_id'],
                'user_id':order['order_info']['user_id'],
                'user_name':list(filter(lambda x:x['user_id'] == order['order_info']['user_id'], user_list))[0]['name'],
                'product_id':i['product_id'],
                'product_name':list(filter(lambda x:x['product_id'] == i['product_id'], product_list))[0]['product_name'],
                'order_date':order['order_info']['order_date'],
            },
            "fields": {
                'order_id':order['order_info']['order_id'],
                'get_score':order['order_info']['get_score'],
                'pay':order['order_info']['pay'],
                'order_date':order['order_info']['order_date'],
                'order_award':order['order_info']['order_award'],
                'promotion_info':order['order_info']['promotion_info'],
                'order_num':i['order_num'],
                'min_used_days': list(filter(lambda x:x['product_id'] == i['product_id'], product_consume_list))[0]['min_used_days'],
                'max_used_days': list(filter(lambda x:x['product_id'] == i['product_id'], product_consume_list))[0]['max_used_days'],
                'official_used_days': list(filter(lambda x:x['product_id'] == i['product_id'], product_consume_list))[0]['official_used_days'],
            },
            }
        points.append(point)
    # print(points)
    get_qinxi_insert_influxdb(points)
    return ('插入时序数据成功')







