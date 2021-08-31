def calc_fuquan_use_fenhong(df, df_fenhong):
    """获取复权后的历史数据, 用分红表来计算复权 , 前复权
    df: 日k线
    df_fenhong: 分红表
    return: df"""
    # 日期早的在前面
    df_fenhong = df_fenhong.sort_index(by=2)

    for i in range(len(df_fenhong)):
        gu, money, date = df_fenhong.irow(i)

        if len(df.ix[:date]) < 2:
            continue

    date = agl.df_get_pre_date(df, date)

    if money > 0:
        money = money * 0.1
        df["o"].ix[:date] -= money
        df["h"].ix[:date] -= money
        df["c"].ix[:date] -= money
        df["l"].ix[:date] -= money
    if gu > 0:
        # x = cur / (1+y/10)
        gu = 1 + gu / 10
        df["o"].ix[:date] /= gu
        df["h"].ix[:date] /= gu
        df["c"].ix[:date] /= gu
        df["l"].ix[:date] /= gu
    return df
