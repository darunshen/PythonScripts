'''
提供sqlite操作相关的方法
'''
import sqlite3


class SqliteOperation:
    connect = {}
    cursor = {}

    def ConnectDB(self, db_path):
        self.connect = sqlite3.connect(db_path)
        self.cursor = self.connect.cursor()

    def GetRows(self, table_name):
        '''
        返回表的行数
        table_name:表名
        '''
        sql_statement = 'select count(*) from ' + table_name + ';'
        self.cursor.execute(sql_statement)
        rows = self.cursor.fetchall()
        return rows[0][0]

    def SelectValues(self, data_type, limit, offset):
        '''
        查找数据
        data_type样式参考db_env['table_info']
        limit: 返回数据大小
        offset: 返回数据对应数据集的起始位置
        返回的数据样式:
        [
            {
                'table_name':'image',
                'column_data':{
                    'column_name':'column_value',
                    .....
                }
            },
            .....
        ]
        '''
        sql_statement = 'SELECT '
        columns_statement = ''
        columns = []
        results = []
        for key, value in data_type['table_columns'].items():
            columns.append(key)
            columns_statement = columns_statement +\
                ' ' + key + ','
        columns_statement = columns_statement[:-1]
        columns_statement = columns_statement + \
            ' from '+data_type['sqlite_table_name'] + \
            ' limit ' + str(limit) + ' offset ' + str(offset)
        sql_statement = sql_statement + columns_statement
        print(sql_statement)
        try:
            self.cursor.execute(sql_statement)
            rows = self.cursor.fetchall()
        except sqlite3.DatabaseError as err:
            print('sqlite select error! error:', format(err))
            print('data_type : ', data_type)
            print('limit : ', limit)
            print('offset : ', offset)
            return results

        for row in rows:
            item = {'column_data': {}}
            item['table_name'] = data_type['postgresql_table_name']
            i = 0
            for column in columns:
                if column in data_type['change_rules']:
                    item['column_data'][column] = \
                        data_type['change_rules'][column](row[i])
                else:
                    item['column_data'][column] = row[i]
                i = i + 1
            results.append(item)

        return results
