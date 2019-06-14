'''
提供文件相关的处理
如返回yaml文件信息，返回图片base64编码数据
'''
import base64
import yaml
import os


class FileOperation:
    def load_conf(self, path):
        '''
        加载path所指定的yaml文件并返回
        '''
        conf_info = {}
        with open(path, 'r') as f:
            conf_info = yaml.load(f.read())
        return conf_info

    def read_image(self, path):
        '''
        返回path所指定文件的base64数据
        '''
        with open(path, "rb") as fh:
            return str(base64.b64encode(fh.read()),
                       encoding='utf-8')

    def write_image(self, base64_data, path):
        '''
        写一张base64数据的图片到path
        '''
        with open(path, "wb") as fh:
            fh.write(base64.b64decode(base64_data))

    def init_base64_data(self, path):
        '''
        读取路径下的所有文件并返回其base64编码数据的数组
        '''
        files = os.listdir(path)
        imglist = []
        for fh in files:
            filename = path+'/'+fh
            if not(os.path.isdir(filename)):
                imglist.append(self.read_image(filename))
        return imglist
