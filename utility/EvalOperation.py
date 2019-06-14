'''
提供eval相关的处理
如将命令行的输入进行eval处理
'''
import logging


class EvalOperation:
    scope = {}

    def add_to_scope(self, key, value):
        '''
        将键值对加入到scope中
        如果为函数，key不要加参数和括号
        '''
        self.scope[key] = value

    def execute_eval(self, string):
        '''
        执行string所代表的命令
        '''
        try:
            return eval(string, self.scope)
        except Exception as e:
            logging.exception(e)
