cookies = {
        'hsite': '6',
        'currentRegionId': 'cn-zhangjiakou',
        '_umdata': 'G668FFC191D1149374B937E9485E343DC7B922A',
        'login_current_pk': '1031035430341318',
        'aliyun_lang': 'zh',
        'tfstk': 'dURJqM2hfmmlTiPJ7uHmYCOpKd0DwQLyl38_tMjudnKvvHLltLDypKKB09VlZHVpHHxXrzbk-KIpcnIWN_iF9wthDT0y-YrL9_RDEWjo46LBj6nijfcMzUWNOcmMwl8yz3-fsucisU8zragMlf0y0mndUInsYxE3GhRCPvDRrESgisQReGFhDWFK-aBRfUsxYDWamCATrWqGXw2SkqeULT_VY1z6y',
        '_samesite_flag_': 'true',
        'l': 'fBEB-4mIPs8s-6L_BOfwPurza77OSIRA_uPzaNbMi9fPOo1w5jWNW1F32DYeC3GVFsFyR3r0glSeBeYBqbh-nxvOEtGZ_fkmnmOk-Wf..',
        'hssid': 'CN-SPLIT-ARCEByIOc2Vzc2lvbl90aWNrZXQyAQE4hvSI6rsxQAFKELAIcgBVhmzBdIfV_CqMfEwTrDcMGQROJCyz8zNVqV9GxnB1hw',
        'aliyun_country': 'CN',
        'munb': '2212848404631',
        'cookie2': '1106be094b990f06f07eabbb817972a9',
        'aliyun_site': 'CN',
        'login_aliyunid_ticket': 'XZqg4XFWQfyKpeu*0vCmV8s*MT5tJl3_1$$wZC1f_am4p1v8C15cp7KIj0I6NNnjBrWGFOSIyXv2chf_INpoU_BOTwChTBoNM1ZJeedfK9zxYnbN5hossqIZCr6t7SGxRigm2Cb4fGaCdBZWIzmgdHs60',
        't': '1475f811478ee562bc47f15fa8443dc3',
        'csg': 'b2d24a33',
        'cna': 'hxnWHeYCewgCAXU9cW0SYeec',
        '_uab_collina': '169968732192257945518737',
        'isg': 'BEZGKoprXx6n-Qv6S1jB7dOklzzIp4phQsr3SDBvMmlEM-ZNmDfacSwCD2__nIJ5',
        'login_aliyunid_pk': '1031035430341318',
        'login_aliyunid_pks': 'BG+S0GDQHhuocCrFNey0BAJ27utf7Vnl53WYECoxueTD/M=',
        'login_aliyunid_csrf': '_csrf_tk_1795699687316330',
        'login_aliyunid': 'y130****24553',
        'login_disaster': 'master',
        '_tb_token_': 'eddb73bb3fab3',
    }

cookie_str_lst = []
for k, v in cookies.items():
    cookie_str_lst.append('{}={}'.format(k, v))

print('; '.join(cookie_str_lst))