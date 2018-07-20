#!/usr/bin/python3
import copy
import pymysql
from blockchain.config import *


class Mysql_service(object):
    db = pymysql.connect(host=DB_HOST, user=DB_ID, password=DB_PASSWORD, db=DB_DATABASE)
    cursor = db.cursor()
    def __init__(self):
        print("connection on")

    def register(self,username,password,email,role): #self,user,email,password,role
        sql='''insert into all_users (user_name,password,email,role,account,credit,user_port,user_host)\
               values("%s","%s","%s","%s",0.0,100,3036,"0000") ''' % (username, password,email,role)
        try:
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            print('register successful')
        except:
            # 如果发生错误则回滚
            self.db.rollback()
        # 关闭数据库连接

#####################修改个人信息#######################
    # def changeMyInfo(self,username,email,address):
    #     sql = "update all_users set email='%s',address='%s' where user_name=%s" % (email,address,username)
    #     self.db.rollback()
    #     print(sql)
    #     try:
    #         self.cursor.execute(sql)
    #     except:
    #         self.db.rollback()


    def getUserInfoByUsername(self,username):
        sql="select * from all_users where user_name='%s'" % (username)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            print(results)
            for row in results:
                name=row[0]
                password = row[1]
                role = row[2]
                email = row[3]
                address = row[4]
                account=row[5]
                credit=row[6]
            return name,password,role,email,address,account,credit
        except:
            self.db.rollback()









    def check(self,user):

        check_sql = "select * from all_users where user_name='%s'" % self.user
        cur=self.db.cursor()
        cur.execute(check_sql)
        if cur.rowcount==0:
            return True
        else:
            return False






###############################删
    #######删除某一商品"""

    def del_good(self, good_id: int):
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

        sql = '''DELETE FROM all_goods WHERE login_name="%d" ''' % good_id

        try:
            # 执行sql语句
            cursor.execute(sql)
            self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()

    ########删除某一用户"""

    def del_users(self, login_name: str):
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

        sql = '''DELETE FROM all_users WHERE login_name="%s" ''' % login_name

        try:
            # 执行sql语句
            cursor.execute(sql)
            self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()


###############################查

#############################################

    ##########获得小于60用户信誉值"""
    def search_for_credity_byusername(self):

        data_result = []
        data_total = 0
        # 存放结果的字典数组与数量
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

        sql = '''select * from all_users where credit<60 order by credit desc'''

        try:
            # 执行sql语句
            cursor.execute(sql)
            data = cursor.fetchall()

            # cursor.rowcount
            # 提交到数据库执行

            for row in data:
                data_result.append(row)
                data_total = data_total + 1
                # self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()

        return data_total, data_result



    ########查某一个用户的信誉值
    def search_for_credity_byusername(self, username):

        data_result = []
        data_total = 0
        # 存放结果的字典数组与数量
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

        sql = '''select * from all_users where user_name="%s"\
            and credit<60 order by credit desc''' % username

        try:
            # 执行sql语句
            cursor.execute(sql)
            data = cursor.fetchall()

            # cursor.rowcount
            # 提交到数据库执行

            for row in data:
                data_result.append(row)
                data_total = data_total + 1
                # self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()

        return data_total, data_result

    #######按名称查找某一商品
    def search_for_commodity_bygoods(self,goods_name):

        data_result=[]
        data_total=0
        #存放结果的字典数组与数量
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

        sql='''select * from all_goods where goods_name="%s" order by price_ava asc''' % goods_name

        try:
            # 执行sql语句
            cursor.execute(sql)
            data=cursor.fetchall()

            #cursor.rowcount
            # 提交到数据库执行

            for row in data:
                data_result.append(row)
                data_total=data_total+1
            #self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()

        return data_total,data_result



    ####按物流价格/时间排序  获取物流公司的信息
    ###return 记录数量 价格顺序推荐 时间顺序推荐
    def search_for_logistics(self, distance):

        data_result_priceorder = []

        data_total = 0
        # 存放结果的字典数组与数量
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

        sql = '''select * from all_logistics '''

        try:
            # 执行sql语句
            cursor.execute(sql)
            data = cursor.fetchall()
            # cursor.rowcount
            # 提交到数据库执行

        except:
            # 如果发生错误则回滚
            self.db.rollback()

        for row in data:
            data_result_priceorder.append(row)
            data_result_priceorder[data_total]["total_price"] = data_result_priceorder[data_total]["init_price"] + data_result_priceorder[data_total]["ava_price"] * distance
            data_result_priceorder[data_total]["total_time"] =  data_result_priceorder[data_total]["ava_time"] * distance
            data_total = data_total + 1
            # self.db.commit()


        sorted(data_result_priceorder, key=lambda price_order: price_order["total_price"])
        data_result_timeorder=copy.deepcopy(data_result_priceorder)

        sorted(data_result_timeorder, key=lambda price_order: price_order["total_time"])
        return data_total, data_result_priceorder,data_result_timeorder

    ########获得节点中的所有IP"""

    def get_all_ip(self):
        address = []
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        sql = '''select user_host,user_port from all_users'''
        try:
            # 执行sql语句
            cursor.execute(sql)
            data = cursor.fetchall()
            # cursor.rowcount
            # 提交到数据库执行
        except:
            # 如果发生错误则回滚
            self.db.rollback()

        for record in data:
            string = record['user_host'] + ":" + "%s" % record['user_port']
            address.append(string)

        return address

    ######获得指定用户地址"""

    def get_ip(self, login_name: str):
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        sql = '''select user_host,user_port from all_users where login_name = "%s" ''' % login_name
        try:
            # 执行sql语句
            cursor.execute(sql)
            data = cursor.fetchone()
            # cursor.rowcount
            # 提交到数据库执行
        except:
            # 如果发生错误则回滚
            self.db.rollback()

        temp = str(data['user_port'])
        string = data['user_host'] + ":" + temp

        return string

#############################################
    ####查某一名称的所有商品
    def search_for_commodity_bygoods(self,goods_name):

        data_result=[]
        data_total=0
        #存放结果的字典数组与数量
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

        sql='''select * from all_goods where goods_name="%s" \
            and goods_stat="for sale" order by price_ava asc''' % goods_name

        try:
            # 执行sql语句
            cursor.execute(sql)
            data=cursor.fetchall()

            #cursor.rowcount
            # 提交到数据库执行

            for row in data:
                data_result.append(row)
                data_total=data_total+1
            #self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()

        return data_total,data_result


    def get_block_tem(self):
        ####查所有的临时交易
        data_result = []
        data_total = 0
        # 存放结果的字典数组与数量
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

        sql = '''select * from block_tem '''
        try:
            # 执行sql语句
            cursor.execute(sql)
            data = cursor.fetchall()

            # cursor.rowcount
            # 提交到数据库执行

            for row in data:
                data_result.append(row)
                data_total = data_total + 1
                # self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()

        return data_total, data_result


    def search_for_commodity_byseller(self,seller_name):
####查商家的所有商品
        data_result=[]
        data_total=0
        #存放结果的字典数组与数量
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

        sql='''select * from all_goods where goods_seller="%s" \
            and goods_stat="for sale" order by price_ava asc''' % seller_name

        try:
            # 执行sql语句
            cursor.execute(sql)
            data=cursor.fetchall()

            #cursor.rowcount
            # 提交到数据库执行

            for row in data:
                data_result.append(row)
                data_total=data_total+1
            #self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()

        return data_total,data_result



###################################改
    def confirm_goods_arrival(self,goods_id):
        cursor = self.db.cursor()
        #改商品的销售状态
        sql = '''update all_goods set goods_stat="sold" where goods_id=%d''' % goods_id

        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()


    def modify_user_info(self,username,password=None,address=None,account=-1,email=None,host=None,port=-1):
        cursor1 = self.db.cursor(cursor=pymysql.cursors.DictCursor)

        sql = '''select * from all_users where user_name="%s" ''' % username

        try:
            # 执行sql语句
            cursor1.execute(sql)
            data = cursor1.fetchone()

            # 提交到数据库执行

            self.password = data["password"] if password is None else password
            self.address = data["address"] if address is None else address
            self.account = data["account"] if account ==-1 else account
            self.email = data["email"] if email is None else email
            self.user_host = data["user_host"] if host is None else host
            self.user_port = data["user_port"] if port == -1 else port

            #判断哪些有修改
        except:
            # 如果发生错误则回滚
            self.db.rollback()

        print(cursor1.rowcount)

        sql2 = '''update all_users set password="%s",address="%s",account=%lf,email="%s", user_port=%d, user_host="%s"\
                        where user_name="%s" ''' % (self.password, self.address, self.account,self.email,self.user_port,self.user_host, username)

        # cursor2 = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        # cursor1.scroll(0,mode='absolute')
        try:
            # 执行sql语句
            cursor1.execute(sql2)
            print(cursor1.rowcount)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()

######################################增
    #增加临时交易记录
    def add_tem_block(self):
        cursor = self.db.cursor()
        sql_create='''CREATE TABLE `block_tem` \
          (`sales_id` int(11) NOT NULL,\
          `seller_name` varchar(11) NOT NULL,\
          `buyer_name` varchar(11) NOT NULL,\
          `amount` float(10,2) NOT NULL,\
          `goods_name` varchar(45) NOT NULL,\
          `sales_time` float(10,0) NOT NULL,\
          `arrive_time` float(10,0) NOT NULL,\
          `sale_type` enum('log','sale') CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,\
          `sales_condition` enum('not_arrived','arrived') CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,\
          PRIMARY KEY (`sales_id`),\
          UNIQUE KEY `sales_id_UNIQUE` (`sales_id`),\
          UNIQUE KEY `seller_id_UNIQUE` (`seller_name`),\
          UNIQUE KEY `buyer_id_UNIQUE` (`buyer_name`),\
          CONSTRAINT `block_tem_ibfk_1` FOREIGN KEY (`buyer_name`) REFERENCES `all_users1` (`user_name`),\
          CONSTRAINT `block_tem_ibfk_2` FOREIGN KEY (`seller_name`) REFERENCES `all_users1` (`user_name`)\
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''

        # sql = '''insert into all_goods(goods_id,goods_name,goods_amount,goods_seller,goods_stripeID,goods_price,goods_stat,price_ava
        #         ,seller_host,seller_port)  values(%d,"%s",%d,"%s","%s","%f","for sale",%f,"%s",%d) ''' \
        #       % (goods_id, goods_name, goods_amount, goods_seller, goods_stripeID, goods_price, price_ava
        #          , seller_host, seller_port)
        # self,sales_id,seller_name,buyer_name,amount,goods_name,sales_time,arrive_time,sales_type,sales_condition
        try:
            # 执行sql语句
            cursor.execute(sql_create)
            #print(cursor.rowcount)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 如果发生错误则回滚
            print("operation failed")
            self.db.rollback()


    #在临时区块增加交易记录
    def add_sale_to_tem_block(self,sales_id,seller_name,buyer_name,amount,goods_name,sales_time,arrive_time,sales_type,sales_condition,seller_host,seller_port,price):

        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        sql_block_insert='''insert into block_tem(sales_id,seller_name,buyer_name,amount,goods_name,\
        sales_time,arrive_time,sales_type,sales_condition,seller_host,seller_port,price)  \
        values(%d,"%s","%s",%f,"%s",%lf,%lf,%d,%d,"%s",%d,%lf)'''% (sales_id,seller_name,buyer_name,amount,goods_name,sales_time,arrive_time,sales_type,sales_condition,seller_host,seller_port,price)

        try:
            # 执行sql语句
            cursor.execute(sql_block_insert)
            print(cursor.rowcount)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 如果发生错误则回滚
            print("insert failed")
            self.db.rollback()





    #增加物流公司的信息(计费标准和时间花费）
    def add_log_info(self,logger_name,init_price,ava_price,ava_time):
        data_total = 0
        # 存放结果的字典数组与数量
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

        sql = '''select * from all_users where user_name="%s" ''' % logger_name


        try:
            # 执行sql语句
            cursor.execute(sql)
            data = cursor.fetchone()
            logger_host=data["user_host"]
            logger_port=data["user_port"]
            # cursor.rowcount
            # 提交到数据库执行

        except:
            # 如果发生错误则回滚
            self.db.rollback()

        sql = '''insert into all_logger(init_price,ava_price,ava_time,logger_name,logger_host,logger_port)\
                   values(%f,%f,%d,"%s","%s",%d) ''' \
              % (init_price,ava_price,ava_time,logger_name,logger_host,logger_port)

        try:
            # 执行sql语句
            cursor.execute(sql)
            print(cursor.rowcount)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 如果发生错误则回滚
            print("insert failed")
            self.db.rollback()

            # 增加区块

    def add_block(self, index, previous_hash, timestamp, transaction, nonce):
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        sql_check_num = '''select * from block_header'''
        cursor.execute(sql_check_num)
        num = cursor.rowcount
        sql_add_header = '''insert into block_header(index,previous_hash,timestamp,transaction,nonce)\
                        values('''
        sql_add_block = '''alter table test rename test1;'''

    #增加商品
    def insert_commodity(self, goods_id,goods_name, goods_amount, goods_seller, goods_stripeID, goods_price, seller_host, seller_port):
        cursor = self.db.cursor()
        price_ava=goods_price / goods_amount
        sql = '''insert into all_goods(goods_id,goods_name,goods_amount,goods_seller,goods_stripeID,goods_price,goods_stat,price_ava
        ,seller_host,seller_port)  values(%d,"%s",%d,"%s","%s",%f,"for sale",%f,"%s",%d) ''' \
              % (goods_id,goods_name, goods_amount, goods_seller, goods_stripeID, goods_price,  price_ava
                 ,seller_host, seller_port)

        try:
            # 执行sql语句
            cursor.execute(sql)
            print(cursor.rowcount)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 如果发生错误则回滚
            print("insert failed")
            self.db.rollback()

####################区块链

    ########获取区块链长度"""

    def get_length(self):
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        sql = '''select * from block_header'''
        try:
            # 执行sql语句
            cursor.execute(sql)
            # cursor.rowcount
            # 提交到数据库执行
        except:
            # 如果发生错误则回滚
            self.db.rollback()
        return cursor.rowcount

    ########返回指定区块头的内容"""

    def get_block_header(self, index: int):
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        sql = '''SELECT * from block_header limit %d,1''' % index

        try:
            # 执行sql语句
            cursor.execute(sql)
            data = cursor.fetchall()
            # cursor.rowcount
            # 提交到数据库执行
        except:
            # 如果发生错误则回滚
            self.db.rollback()

        return data

    #########返回指定区块体的内容"""

    def get_block_body(self, index: int):
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        block_body = "block_body" + '%d' % index
        sql = '''select * from %s''' % block_body

        try:
            # 执行sql语句
            cursor.execute(sql)
            data = cursor.fetchall()
            # cursor.rowcount
            # 提交到数据库执行
        except:

            # 如果发生错误则回滚
            self.db.rollback()

        return data

    ##########找到某一用户所有订单"""

    def search_all_record(self, user_name: str):
        record_seller = []
        record_buyer = []
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        sql = '''select * from block_header'''
        try:
            # 执行sql语句
            cursor.execute(sql)
            # cursor.rowcount
            # 提交到数据库执行
        except:
            # 如果发生错误则回滚
            self.db.rollback()
        len = cursor.rowcount
        for i in range(len - 1):
            i += 1
            # 找到区块体
            block_body = "block_body" + '%d' % i
            # 买家
            sql = '''select * from %s where buyer_name = '%s' ''' % (block_body, user_name)
            cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
            try:
                self.db.commit()
                cursor.execute(sql)
                data = cursor.fetchall()
                if data != ():
                    record_seller.append(data)
            except:
                # 如果发生错误则回滚
                self.db.rollback()
            # 卖家情况
            sql = '''select * from %s where seller_name = '%s' ''' % (block_body, user_name)
            cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
            try:
                self.db.commit()
                cursor.execute(sql)
                data = cursor.fetchall()
                if data != ():
                    record_buyer.append(data)
            except:
                # 如果发生错误则回滚
                self.db.rollback()

        return record_buyer, record_seller

    ###########找到某一条特定记录"""

    def search_record(self, time, sales_id):
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        sql = '''select timestamp from block_header'''
        try:
            # 执行sql语句
            cursor.execute(sql)
            data = cursor.fetchall()
            # cursor.rowcount
            # 提交到数据库执行
        except:
            # 如果发生错误则回滚
            self.db.rollback()

        max = 0
        for row in data:
            if row['timestamp'] > time:
                break
            max += 1

        # 找到对应的区块体
        block_body = "block_body" + '%d' % max
        sql = '''select * from %s where sales_id = %d ''' % (block_body, sales_id)
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            self.db.commit()
            cursor.execute(sql)
            data = cursor.fetchall()
        except:
            # 如果发生错误则回滚
            self.db.rollback()

        return data


    def close_db(self):
        self.db.close()
# 关闭数据库连接
