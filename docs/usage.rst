
使用方法
==============

To use mootdx in a project::

    from mootdx.reader import Reader, ExReader
    from mootdx.market import LiveBar, ExLiveBar

    # TDX 文件读取
    read = Reader(tdxdir='C:/new_tdx')
 
    data = read.daily(symbol='000001')
    data = read.index(symbol='000001')
    data = read.block(symbol='000001')

    data = read.fzline(symbol='000001')
    data = read.minute(symbol='000001')

    # TDX 实时数据读取
    live = LiveBar()
    data = live.minute(symbol='000001')
    data = live.block()
