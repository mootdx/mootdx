import logging
import os
from glob import glob

from mootdx.affair import Affair

logging.basicConfig(level=logging.DEBUG)

Affair.fetch(downdir='tmp')  # 下载全部

for x in glob('tmp/*.zip'):
    dist = os.path.basename(x).replace('.zip', '.csv')
    file = os.path.basename(x)

    if not os.path.exists('tmp/{}'.format(dist)):
        print('文件已存在: {}'.format(dist))
        continue

    data = Affair.parse(downdir='tmp', filename=file)
    data.to_csv('csv/{}'.format(dist))
