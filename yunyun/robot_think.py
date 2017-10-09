#-*-coding:utf-8-*-
'''
Date:20170619
Author:linqingbin
Description:robot_think.py
'''
import time
import re
import os
import sys
import uuid
import ctypes
import numpy as np
import pdb
from io import StringIO

SAVE_DIR_PATH = os.path.join(os.path.expanduser(
    "~"), 'AppData\\Local\\robot_think\\datasets\\')

if not os.path.exists(SAVE_DIR_PATH):
    os.makedirs(SAVE_DIR_PATH)


def iscreatenew():
    '''用户判断是否新建数据'''
    flag_select = ctypes.windll.user32.MessageBoxW(
        0, '请问是否新建数据？\n确定点击是，自定义点击否，退出点击取消', '提示', 3)
    if flag_select == 7:
        os.startfile(SAVE_DIR_PATH)
        input_filename = input('请输入文件的名称：')
        filename = ''
        for x in os.listdir(SAVE_DIR_PATH):
            if input_filename in x:
                filename = x
                break
        if not filename:
            ctypes.windll.user32.MessageBoxW(0, '抱歉！未找到该文件', '提示', 1)
            sys.exit()

        file_save_path = os.path.join(SAVE_DIR_PATH, filename)
        with open(file_save_path, 'r') as f:
            stream = f.read()
        import pandas as pd
        df = pd.read_csv(StringIO(stream), index_col=0)
        return df
    elif flag_select == 2:
        sys.exit()


def humaninput():
    '''手工新建数据'''
    sample_names = []
    feature_names = []
    feature_weights = []
    score_list = []
    x = input('请输入本次思考的主题：')
    title = re.sub("[^\w]", '', x)
    # 加入对title的特殊字符替换
    x = input('请输入要对比的对象（中文或英文逗号分隔每个对象）：')
    sample_names = re.split(',|，', x.replace(' ', ''))
    x = input('请输入要比较的特征（中文或英文逗号分隔每个对象）：')
    feature_names = re.split(',|，', x.replace(' ', ''))

    for feature_name in feature_names:
        message = '对于{feature_name}，你觉得权重有多大，请在-2,-1,0，1，2中选择：'.format(
            feature_name=feature_name)
        x = input(message)
        feature_weights.append(int(x))

    for feature_name in feature_names:
        col_score = []
        for sample_name in sample_names:
            message = '对于{feature_name}，你觉得{sample_name}怎么样，请在0,1,2中选择：'.format(
                feature_name=feature_name, sample_name=sample_name)
            x = input(message)
            col_score.append(int(x))
        score_list.append(col_score)

    score_arr = np.array(score_list).T
    feature_weights = np.array(feature_weights)
    import pandas as pd
    df = pd.DataFrame(data=score_arr, index=sample_names,
                      columns=feature_names)
    df.index.name = 'sol'
    df.loc['weight'] = feature_weights
    save_file_path = os.path.join(
        SAVE_DIR_PATH, title + str(uuid.uuid4()) + '.csv')
    df.to_csv(save_file_path)
    # os.startfile(SAVE_DIR_PATH)
    return df


def cal_profit(score_arr, feature_weights):
    '''计算最后的利润'''
    return np.mat(score_arr) * np.mat(feature_weights).T


def splitdf(df):
    '''分割数据集为几个部分'''
    config = {}
    config['sample_names'] = np.array(df.index)[:-1]
    config['feature_names'] = np.array(df.columns)
    config['score_arr'] = df.values[:-1]
    config['feature_weights'] = df.values[-1]
    return config


def process(df):
    '''对输入的数据集进行处理'''
    config = splitdf(df)
    profit_arr = cal_profit(config['score_arr'], config['feature_weights'])
    profit_arr = profit_arr.A.flatten()
    best_sol = config['sample_names'][profit_arr.argmax()]
    import pandas as pd
    ser = pd.Series(profit_arr, index=config['sample_names'])
    ser.name = 'final_score'
    results = pd.concat([df, ser], axis=1)
    return results


def main():
    print('程序已启动。请根据提示输入。')
    df = iscreatenew()
    if df is None:
        df = humaninput()
    print('存储完毕。正在处理数据...')
    x = time.time()
    results = process(df)
    taketime = (time.time()-x)
    if taketime < 2:
        time.sleep(3 - taketime)
    print('处理结束。请查看结果。\n')
    time.sleep(1)
    print(results)
    return results

if __name__ == '__main__':
    main()
