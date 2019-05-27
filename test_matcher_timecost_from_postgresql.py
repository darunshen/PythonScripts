'''
测试基于postgresql的cube的特征比对
'''
import threading
from utility import PostgreSqlOperation

db_env = {
    'postgresql_info': {
        'db_name': 'bigrain',
        'username': 'postgres',
        'password': 'root',
        'host_ip': '172.17.0.2',
        'host_port': 5432,
    }
}


def test_time_cost(target_table_name, source_table_name,
                   begin_time_list, begin_time_mutex,
                   end_time_list, end_time_mutex, thread_num):

    threads = []
    postgresql_op = []
    for i in range(0, thread_num, 1):
        postgresql_op.append(PostgreSqlOperation.PostgreSqlOperation())
        postgresql_op[i].ConnectDB(db_env['postgresql_info']['username'],
                                   db_env['postgresql_info']['password'],
                                   db_env['postgresql_info']['db_name'],
                                   db_env['postgresql_info']['host_ip'],
                                   db_env['postgresql_info']['host_port']
                                   )
    for i in range(0, thread_num, 1):

        thread = threading.Thread(target=postgresql_op[i].GetFeatureCompareResult,
                                  args=(target_table_name+str(i),
                                        source_table_name, begin_time_list,
                                        begin_time_mutex,
                                        end_time_list, end_time_mutex))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    begin_time_mutex = threading.Lock()
    end_time_mutex = threading.Lock()
    begin_time_list = []
    end_time_list = []
    thread_num = 1
    target_table_name = 'image_2_target_'
    source_table_name = 'image_5w'
    test_time_cost(target_table_name, source_table_name,
                   begin_time_list, begin_time_mutex,
                   end_time_list, end_time_mutex, thread_num)
    print(begin_time_list)
    print(end_time_list)
    print('major time cost = ', str(max(end_time_list)-min(begin_time_list)))
