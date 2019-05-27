'''
存储postgresql的操作方法
'''
import psycopg2
import time


class PostgreSqlOperation:
    connect = {}
    cursor = {}

    def ConnectDB(self, username, password,
                  db_name, host_ip='127.0.0.1', host_port=5432):
        self.connect = psycopg2.connect(
            database=db_name, user=username,
            password=password, host=host_ip,
            port=host_port)
        self.cursor = self.connect.cursor()

    def CreateTable(self, data_type):
        '''
        创建数据表
        data_type样式参考db_env['table_info']
        '''
        sql_statement = 'DROP TABLE IF EXISTS '+data_type['postgresql_table_name'] + \
            '; CREATE TABLE '+data_type['postgresql_table_name']
        columns_statement = ' ('
        for key, value in data_type['table_columns'].items():
            columns_statement = columns_statement +\
                ' ' + key + ' ' + value + ','
        columns_statement = columns_statement[:-1]
        columns_statement = columns_statement + ');'
        sql_statement = sql_statement + columns_statement
        # print(sql_statement)
        self.cursor.execute(sql_statement)
        self.connect.commit()

    def InsertValues(self, data):
        '''
        插入数据
        data样式:{
            'table_name':'image',
            'column_data':{
                'column_name':'column_value',
                .....
            }
        }
        '''
        sql_statement = 'INSERT INTO '+data['table_name']
        columns_statement = ' ('
        value_statement = ' VALUES ('
        value_data = []
        for key, value in data['column_data'].items():
            columns_statement = columns_statement + key + ','
            value_statement = value_statement + '%s,'
            value_data.append(value)
        columns_statement = columns_statement[:-1]
        value_statement = value_statement[:-1]
        columns_statement = columns_statement + ')'
        value_statement = value_statement + ');'
        sql_statement = sql_statement+columns_statement+value_statement
        self.cursor.execute(sql_statement, tuple(value_data))
        self.connect.commit()

    def ExecuteCustomSql(self, sql_statement):
        '''
        执行自定义sql指令
        '''
        self.cursor.execute(sql_statement)
        self.connect.commit()

    def GetFeatureCompareResult(self, target_table_name,
                                source_table_name, begin_time_list,
                                begin_time_mutex,
                                end_time_list, end_time_mutex):
        '''
        执行特征比对的sql过程
        target_table_name:比对的表名
        source_table_name:被比对的表名
        '''
        sql_statement = 'SELECT public."GetFeatureCompareResult"(\''\
            + target_table_name+'\',\'' +\
            source_table_name+'\')'
        print(sql_statement)
        begin_time_mutex.acquire()
        begin_time_list.append(time.time())
        begin_time_mutex.release()
        self.cursor.execute(sql_statement)
        self.connect.commit()
        end_time_mutex.acquire()
        end_time_list.append(time.time())
        end_time_mutex.release()

    def ReleaseResource(self):
        self.cursor.close()
        self.connect.close()
