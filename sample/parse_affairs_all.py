import logging
import os
from glob import glob

import pandas as pd

from mootdx.affair import Affair

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()

Affair.fetch(downdir='tmp')  # 下载全部

for x in glob('tmp/*.zip'):
    dist = os.path.basename(x).replace('.zip', '.csv')
    file = os.path.basename(x)

    if os.path.exists('tmp/{}'.format(dist)):
        logger.warning('文件已存在: {}'.format(dist))
        continue

    data = Affair.parse(downdir='tmp', filename=file)

    if data is not None:
        data.to_csv('tmp/{}'.format(dist))
        logger.info('文件已导出: {}'.format(dist))

for input_file in glob('tmp/*.csv'):
    df = pd.read_csv(input_file, header=None)
    df.to_csv('all.csv', mode='a', index=False, header=False)
