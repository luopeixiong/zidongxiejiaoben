self.zhaozhong_biao(response, items)|
    def zhaozhong_biao(self, response, items):
        biaoshi = response.url.split('/')[-2]  # ※注意这个-2
        if biaoshi in ['hw_14209', 'gc_14212', 'fw_14213', 'zfjzcgl']:
            items['channel_id'] = 15  # 中标15  招标16
        else:
            items['channel_id'] = 16  # 中标15  招标16