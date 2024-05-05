import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from hashlib import md5
from itertools import repeat
from mmap import ACCESS_READ
from mmap import mmap

import requests
from tqdm import tqdm


class DownloadTDXCaiWu(object):
    tdx_root_dir = 'new_tdx'
    tdx_cw_dir = tdx_root_dir + '/vipdoc/cw'
    tmp_cw_dir = 'cw_tmp'  # 所有的文件处理都在这个文件夹下，不修改tdx本地的财务文件，确认无误后再同步回tdx目录下

    hashlist_gpcw_url = 'https://data.tdx.com.cn/tdxfin/gpcw.txt'
    hashlist_gpsz_url = 'https://data.tdx.com.cn/tdxgp/gpszsh.txt'

    one_gpcw_url = 'https://data.tdx.com.cn/tdxfin/{file_name}'
    one_gpsz_url = 'https://data.tdx.com.cn/tdxgp/{file_name}'

    workerPool = None

    def __init__(self):
        self.workerPool = ThreadPoolExecutor(max_workers=10, thread_name_prefix='TDX_CW_')

    @staticmethod
    def download_file(url, save_dir, save_file_name):
        response = requests.get(url)

        if len(save_file_name) < 5:
            if 'content-disposition' in response.headers:
                content_disposition = response.headers['content-disposition']
                save_file_name = content_disposition.split('filename=')[1]
            else:
                save_file_name = url.split('/')[-1]

        file_loc = f'{save_dir}/{save_file_name}'

        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        with open(file_loc, mode='wb') as file:
            file.write(response.content)
            # print(f"已下载文件: {file_loc}")

    def download_cw_hashlist(self):
        urls = [
            self.hashlist_gpcw_url,
            self.hashlist_gpsz_url,
        ]
        files = [
            'gpcw.txt',
            'gpszsh.txt',
        ]

        for data in self.workerPool.map(self.download_file, urls, repeat(self.tmp_cw_dir), files):
            pass

    def download_cw_items(self, file_name_list):
        if len(file_name_list) == 0:
            return

        gpcw_urls = [self.one_gpcw_url.format(file_name=file_name) for file_name in file_name_list if 'gpcw' in file_name]
        gpsz_urls = [self.one_gpsz_url.format(file_name=file_name) for file_name in file_name_list if 'gpcw' not in file_name]

        # display(gpcw_urls)
        # display(gpsz_urls[0:5])

        gpcw_tasks = list(tqdm(
            self.workerPool.map(self.download_file, gpcw_urls, repeat(self.tmp_cw_dir), repeat('')),
            total=(len(gpcw_urls)),
            desc='下载财务数据包',
            unit=' 文件',
        ))
        print(f" {datetime.now().strftime('%X')} - 财务数据包[{len(gpcw_urls)}]条 下载完成! **")

        gpsz_tasks = list(tqdm(
            self.workerPool.map(self.download_file, gpsz_urls, repeat(self.tmp_cw_dir), repeat('')),
            total=(len(gpsz_urls)),
            desc='下载股票数据包',
            unit=' 文件',
        ))
        print(f" {datetime.now().strftime('%X')} - 股票数据包[{len(gpsz_urls)}]条 下载完成! **")

    @staticmethod
    def checksum(hash_expected, check_file_name, check_file_dir, is_eq):
        file_location = f'{check_file_dir}/{check_file_name}'

        if not os.path.exists(file_location):
            if is_eq == False:
                return check_file_name
            else:
                return None

        with open(file_location) as file, mmap(file.fileno(), 0, access=ACCESS_READ) as file:
            file_md5 = (md5(file).hexdigest())
            if is_eq == False and file_md5 != hash_expected:
                return check_file_name
            elif is_eq == True and file_md5 == hash_expected:
                return check_file_name
            else:
                return None

    # file_name_scope
    def check_hashlist(self, hash_file_name, check_file_dir, is_eq, file_name_scope=[]):
        file_hashmap = {}

        with open(f'{self.tmp_cw_dir}/{hash_file_name}', mode='r') as f:
            lines = f.readlines()
            count = 0

            # Strips the newline character
            for line in lines:
                count += 1
                line_contents = line.strip().split(',')
                file_name = line_contents[0]
                file_hash = line_contents[1]

                if len(file_name_scope) == 0 or (len(file_name_scope) > 0 and file_name in file_name_scope):
                    file_hashmap[file_name] = file_hash

        to_update_cw_files = []

        for file_name in self.workerPool.map(self.checksum, list(file_hashmap.values()), list(file_hashmap.keys()), repeat(check_file_dir), repeat(is_eq)):
            if file_name is not None and len(file_name) > 0:
                to_update_cw_files.append(file_name)

        return to_update_cw_files

    def download_due_cw(self, ):
        to_update_gpcw = self.check_hashlist('gpcw.txt', self.tdx_cw_dir, False)
        print(f" {datetime.now().strftime('%X')} - 需要更新财务数据包: {len(to_update_gpcw)}条 **")

        to_update_gpsz = self.check_hashlist('gpszsh.txt', self.tdx_cw_dir, False)
        print(f" {datetime.now().strftime('%X')} - 需要更新股票数据包: {len(to_update_gpsz)}条 **")

        to_update_cw_files = (to_update_gpcw + to_update_gpsz)

        if len(to_update_cw_files) > 0:
            print(f" {datetime.now().strftime('%X')} - TDX远程下载数据包到本地临时文件夹 {self.tmp_cw_dir} {len(to_update_cw_files)}条 完成！**")
        else:
            print(f'\n\n######################################################### ')
            print(f'!!!!!!!! TDX主目录已经是最新的财务数据，无需更新 !!!!!!!!')
            print(f'#########################################################\n\n')

        return to_update_cw_files

    def copy_right_cw_to_tdx(self, downloaded_files):
        to_copy_gpcw = self.check_hashlist('gpcw.txt', self.tmp_cw_dir, True, downloaded_files)
        print(f" {datetime.now().strftime('%X')} - 正确的财务数据包: {len(to_copy_gpcw)}条 **")
        to_copy_gpsz = self.check_hashlist('gpszsh.txt', self.tmp_cw_dir, True, downloaded_files)
        print(f" {datetime.now().strftime('%X')} - 正确的股票数据包: {len(to_copy_gpsz)}条 **")
        cw_file_to_copy = (to_copy_gpcw + to_copy_gpsz)
        print(f" {datetime.now().strftime('%X')} - 正确的数据包共 {len(cw_file_to_copy)} 个 **")
        if len(cw_file_to_copy) > 0:
            self.copy_cw_to_tdx(cw_file_to_copy, self.tmp_cw_dir, self.tdx_cw_dir)
            print(f" {datetime.now().strftime('%X')} - 复制正确的数据包到TDX主目录 {self.tdx_cw_dir} 完成！**")
        else:
            print(f" {datetime.now().strftime('%X')} - 没有正确的数据库包可以复制！**")

        return cw_file_to_copy

    @staticmethod
    def copy_cw_to_tdx(copy_files_list, src_dir, dst_dir):
        # shutil.copytree(self.tmp_cw_dir, self.tdx_cw_dir, dirs_exist_ok=True)
        if len(copy_files_list) == 0:
            return

        with tqdm(total=len(copy_files_list), desc='复制文件到TDX主目录', leave=True, ncols=100, unit=' 文件', unit_scale=True) as pbar:
            for copy_file_name in copy_files_list:
                shutil.copy2(os.path.join(src_dir, copy_file_name), dst_dir)
                pbar.update(1)

    def run(self, clear_temp_dir=False):

        if clear_temp_dir:
            shutil.rmtree(self.tmp_cw_dir, ignore_errors=True)
            print(f"** {datetime.now().strftime('%X')} - 0. 清空本地临时文件夹完成！ **")

        print(f"\n {datetime.now().strftime('%X')} - 1. 启动通达信财务数据下载脚本 **")
        self.download_cw_hashlist()

        print(f"\n {datetime.now().strftime('%X')} - 2. 财务HASH列表比对文件(gpcw.txt, gpszsh.txt)下载完成! **")

        print(f"\n {datetime.now().strftime('%X')} - 3. 下载过期的财务数据包...**")

        to_update_cw_files = self.download_due_cw()

        if len(to_update_cw_files) == 0:
            return

        self.download_cw_items(to_update_cw_files)

        print(f"\n {datetime.now().strftime('%X')} - 4. 将正确的财务数据包复制到TDX主目录...**")

        to_copy_cw_files = self.copy_right_cw_to_tdx(to_update_cw_files)

        if len(to_update_cw_files) == len(to_copy_cw_files):
            print(f'\n\n######################################################### ')
            print(f" {datetime.now().strftime('%X')} - WELL DONE！")
            print(f'#########################################################\n\n')
        else:
            print(f'\n\n######################################################### ')
            print(f" {datetime.now().strftime('%X')} - 下载的数据有异常！")
            print(f" {datetime.now().strftime('%X')} - {set(to_update_cw_files) - set(to_copy_cw_files)}！")
            print(f'#########################################################\n\n')


if __name__ == '__main__':
    tdxcw = DownloadTDXCaiWu()
    tdxcw.run()
