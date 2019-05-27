'''
此用例功能：
将sqlite数据库转换为postgresql数据库
'''
from utility import SqliteOperation
from utility import PostgreSqlOperation
from utility import DataOperation
data_op = DataOperation.DataOperation()
sqlite_op = SqliteOperation.SqliteOperation()
postgresql_op = PostgreSqlOperation.PostgreSqlOperation()
db_env = {
    'postgresql_info': {
        'db_name': 'bigrain',
        'username': 'postgres',
        'password': 'root',
        'host_ip': '172.17.0.2',
        'host_port': 5432,
    },
    'sqlite_info': {
        'db_path': '/home/bigrain/Documents/data/db/50wdb/test_4.db',
    },
    'table_info': {
        'sqlite_table_name': 'image',
        'postgresql_table_name': 'image_target_5',
        'table_columns': {
            'id': 'integer PRIMARY KEY NOT NULL',
            'image': 'bytea',
            'feature': 'float[]',
            'image_name': 'text'},
        'change_rules': {
            'feature': data_op.BytesToFloat8List
        }
    },
    'end_execute_sqls': []
}


def change_begin(db_env):
    sqlite_op.ConnectDB(db_env['sqlite_info']['db_path'])
    postgresql_op.ConnectDB(db_env['postgresql_info']['username'],
                            db_env['postgresql_info']['password'],
                            db_env['postgresql_info']['db_name'],
                            db_env['postgresql_info']['host_ip'],
                            db_env['postgresql_info']['host_port']
                            )
    postgresql_op.CreateTable(db_env['table_info'])
    table_rows = sqlite_op.GetRows(db_env['table_info']['sqlite_table_name'])
    table_rows = 500
    limit = 1000
    for offset in range(0, table_rows, limit):
        results = sqlite_op.SelectValues(db_env['table_info'], limit, offset)
        for result in results:
            postgresql_op.InsertValues(result)

    for statement in db_env['end_execute_sqls']:
        postgresql_op.ExecuteCustomSql(statement)
    postgresql_op.ReleaseResource()


def mutitables_change_begin(db_env, table_num):
    for i in range(0, table_num, 1):
        db_env['table_info']['postgresql_table_name'] = \
            db_env['table_info']['sqlite_table_name'] +\
            '_2_target_' + str(i)
        db_env['end_execute_sqls'].clear()
        db_env['end_execute_sqls']\
            .append('delete from ' +
                    db_env['table_info']['postgresql_table_name'] +
                    ' where id != '+str(i+1))
        change_begin(db_env)


if __name__ == '__main__':
    # change_begin(db_env)
    mutitables_change_begin(db_env, 100)
