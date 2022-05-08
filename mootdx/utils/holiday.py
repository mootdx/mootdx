# @Author  : BoPo
# @Time    : 2021/10/9 10:56
# @Function:
import datetime
import re
import time
from pathlib import Path

import httpx
import pandas as pd
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_fixed

from mootdx import get_config_path
from mootdx.logger import logger
# from py_mini_racer import py_mini_racer
# from mootdx.consts import return_last_value

# hk_js_decode = """
# function d(t) {
#     var e, i, n, r, a, o, s, l = (arguments,
#             864e5), u = 7657, c = [], h = [], d = ~(3 << 30), f = 1 << 30,
#         p = [0, 3, 5, 6, 9, 10, 12, 15, 17, 18, 20, 23, 24, 27, 29, 30], m = Math, g = function () {
#             var l, u;
#             for (l = 0; 64 > l; l++)
#                 h[l] = m.pow(2, l),
#                 26 > l && (c[l] = v(l + 65),
#                     c[l + 26] = v(l + 97),
#                 10 > l && (c[l + 52] = v(l + 48)));
#             for (c.push("+", "/"),
#                      c = c.join(""),
#                      i = t.split(""),
#                      n = i.length,
#                      l = 0; n > l; l++)
#                 i[l] = c.indexOf(i[l]);
#             return r = {},
#                 e = o = 0,
#                 a = {},
#                 u = w([12, 6]),
#                 s = 63 ^ u[1],
#             {
#                 _1479: T,
#                 _136: _,
#                 _200: S,
#                 _139: k,
#                 _197: _mi_run
#             }["_" + u[0]] || function () {
#                 return []
#             }
#         }, v = String.fromCharCode, b = function (t) {
#             return t === {}._
#         }, N = function () {
#             var t, e;
#             for (t = y(),
#                      e = 1; ;) {
#                 if (!y())
#                     return e * (2 * t - 1);
#                 e++
#             }
#         }, y = function () {
#             var t;
#             return e >= n ? 0 : (t = i[e] & 1 << o,
#                 o++,
#             o >= 6 && (o -= 6,
#                 e++),
#                 !!t)
#         }, w = function (t, r, a) {
#             var s, l, u, c, d;
#             for (l = [],
#                      u = 0,
#                  r || (r = []),
#                  a || (a = []),
#                      s = 0; s < t.length; s++)
#                 if (c = t[s],
#                     u = 0,
#                     c) {
#                     if (e >= n)
#                         return l;
#                     if (t[s] <= 0)
#                         u = 0;
#                     else if (t[s] <= 30) {
#                         for (; d = 6 - o,
#                                    d = c > d ? d : c,
#                                    u |= (i[e] >> o & (1 << d) - 1) << t[s] - c,
#                                    o += d,
#                                o >= 6 && (o -= 6,
#                                    e++),
#                                    c -= d,
#                                    !(0 >= c);)
#                             ;
#                         r[s] && u >= h[t[s] - 1] && (u -= h[t[s]])
#                     } else
#                         u = w([30, t[s] - 30], [0, r[s]]),
#                         a[s] || (u = u[0] + u[1] * h[30]);
#                     l[s] = u
#                 } else
#                     l[s] = 0;
#             return l
#         }, x = function (t) {
#             var e, i, n;
#             for (t > 1 && (e = 0),
#                      e = 0; t > e; e++)
#                 r.d++,
#                     n = r.d % 7,
#                 (3 == n || 4 == n) && (r.d += 5 - n);
#             return i = new Date,
#                 i.setTime((u + r.d) * l),
#                 i
#         }, S = function () {
#             var t, i, a, o, l;
#             if (s >= 1)
#                 return [];
#             for (r.d = w([18], [1])[0] - 1,
#                      a = w([3, 3, 30, 6]),
#                      r.p = a[0],
#                      r.ld = a[1],
#                      r.cd = a[2],
#                      r.c = a[3],
#                      r.m = m.pow(10, r.p),
#                      r.pc = r.cd / r.m,
#                      i = [],
#                      t = 0; o = {
#                 d: 1
#             },
#                  y() && (a = w([3])[0],
#                      0 == a ? o.d = w([6])[0] : 1 == a ? (r.d = w([18])[0],
#                          o.d = 0) : o.d = a),
#                      l = {
#                          day: x(o.d)
#                      },
#                  y() && (r.ld += N()),
#                      a = w([3 * r.ld], [1]),
#                      r.cd += a[0],
#                      l.close = r.cd / r.m,
#                      i.push(l),
#                  !(e >= n) && (e != n - 1 || 63 & (r.c ^ t + 1)); t++)
#                 ;
#             return i[0].prevclose = r.pc,
#                 i
#         }, _ = function () {
#             var t, i, a, o, l, u, c, h, d, f, p;
#             if (s > 2)
#                 return [];
#             for (c = [],
#                      d = {
#                          v: "volume",
#                          p: "price",
#                          a: "avg_price"
#                      },
#                      r.d = w([18], [1])[0] - 1,
#                      h = {
#                          day: x(1)
#                      },
#                      a = w(1 > s ? [3, 3, 4, 1, 1, 1, 5] : [4, 4, 4, 1, 1, 1, 3]),
#                      t = 0; 7 > t; t++)
#                 r[["la", "lp", "lv", "tv", "rv", "zv", "pp"][t]] = a[t];
#             for (r.m = m.pow(10, r.pp),
#                      s >= 1 ? (a = w([3, 3]),
#                          r.c = a[0],
#                          a = a[1]) : (a = 5,
#                          r.c = 2),
#                      r.pc = w([6 * a])[0],
#                      h.pc = r.pc / r.m,
#                      r.cp = r.pc,
#                      r.da = 0,
#                      r.sa = r.sv = 0,
#                      t = 0; !(e >= n) && (e != n - 1 || 7 & (r.c ^ t)); t++) {
#                 for (l = {},
#                          o = {},
#                          f = r.tv ? y() : 1,
#                          i = 0; 3 > i; i++)
#                     if (p = ["v", "p", "a"][i],
#                     (f ? y() : 0) && (a = N(),
#                         r["l" + p] += a),
#                         u = "v" == p && r.rv ? y() : 1,
#                         a = w([3 * r["l" + p] + ("v" == p ? 7 * u : 0)], [!!i])[0] * (u ? 1 : 100),
#                         o[p] = a,
#                     "v" == p) {
#                         if (!(l[d[p]] = a) && (s > 1 || 241 > t) && (r.zv ? !y() : 1)) {
#                             o.p = 0;
#                             break
#                         }
#                     } else
#                         "a" == p && (r.da = (1 > s ? 0 : r.da) + o.a);
#                 r.sv += o.v,
#                     l[d.p] = (r.cp += o.p) / r.m,
#                     r.sa += o.v * r.cp,
#                     l[d.a] = b(o.a) ? t ? c[t - 1][d.a] : l[d.p] : r.sv ? ((m.floor((r.sa * (2e3 / r.m) + r.sv) / r.sv) >> 1) + r.da) / 1e3 : l[d.p] + r.da / 1e3,
#                     c.push(l)
#             }
#             return c[0].date = h.day,
#                 c[0].prevclose = h.pc,
#                 c
#         }, T = function () {
#             var t, e, i, n, a, o, l;
#             if (s >= 1)
#                 return [];
#             for (r.lv = 0,
#                      r.ld = 0,
#                      r.cd = 0,
#                      r.cv = [0, 0],
#                      r.p = w([6])[0],
#                      r.d = w([18], [1])[0] - 1,
#                      r.m = m.pow(10, r.p),
#                      a = w([3, 3]),
#                      r.md = a[0],
#                      r.mv = a[1],
#                      t = []; a = w([6]),
#                      a.length;) {
#                 if (i = {
#                     c: a[0]
#                 },
#                     n = {},
#                     i.d = 1,
#                 32 & i.c)
#                     for (; ;) {
#                         if (a = w([6])[0],
#                         63 == (16 | a)) {
#                             l = 16 & a ? "x" : "u",
#                                 a = w([3, 3]),
#                                 i[l + "_d"] = a[0] + r.md,
#                                 i[l + "_v"] = a[1] + r.mv;
#                             break
#                         }
#                         if (32 & a) {
#                             o = 8 & a ? "d" : "v",
#                                 l = 16 & a ? "x" : "u",
#                                 i[l + "_" + o] = (7 & a) + r["m" + o];
#                             break
#                         }
#                         if (o = 15 & a,
#                             0 == o ? i.d = w([6])[0] : 1 == o ? (r.d = o = w([18])[0],
#                                 i.d = 0) : i.d = o,
#                             !(16 & a))
#                             break
#                     }
#                 n.date = x(i.d);
#                 for (o in {
#                     v: 0,
#                     d: 0
#                 })
#                     b(i["x_" + o]) || (r["l" + o] = i["x_" + o]),
#                     b(i["u_" + o]) && (i["u_" + o] = r["l" + o]);
#                 for (i.l_l = [i.u_d, i.u_d, i.u_d, i.u_d, i.u_v],
#                          l = p[15 & i.c],
#                      1 & i.u_v && (l = 31 - l),
#                      16 & i.c && (i.l_l[4] += 2),
#                          e = 0; 5 > e; e++)
#                     l & 1 << 4 - e && i.l_l[e]++,
#                         i.l_l[e] *= 3;
#                 i.d_v = w(i.l_l, [1, 0, 0, 1, 1], [0, 0, 0, 0, 1]),
#                     o = r.cd + i.d_v[0],
#                     n.open = o / r.m,
#                     n.high = (o + i.d_v[1]) / r.m,
#                     n.low = (o - i.d_v[2]) / r.m,
#                     n.close = (o + i.d_v[3]) / r.m,
#                     a = i.d_v[4],
#                 "number" == typeof a && (a = [a, a >= 0 ? 0 : -1]),
#                     r.cd = o + i.d_v[3],
#                     l = r.cv[0] + a[0],
#                     r.cv = [l & d, r.cv[1] + a[1] + !!((r.cv[0] & d) + (a[0] & d) & f)],
#                     n.volume = (r.cv[0] & f - 1) + r.cv[1] * f,
#                     t.push(n)
#             }
#             return t
#         }, k = function () {
#             var t, e, i, n;
#             if (s > 1)
#                 return [];
#             for (r.l = 0,
#                      n = -1,
#                      r.d = w([18])[0] - 1,
#                      i = w([18])[0]; r.d < i;)
#                 e = x(1),
#                     0 >= n ? (y() && (r.l += N()),
#                         n = w([3 * r.l], [0])[0] + 1,
#                     t || (t = [e],
#                         n--)) : t.push(e),
#                     n--;
#             return t
#         };
#     return _mi_run = function () {
#         var t, i, a, o;
#         if (s >= 1)
#             return [];
#         for (r.f = w([6])[0],
#                  r.c = w([6])[0],
#                  a = [],
#                  r.dv = [],
#                  r.dl = [],
#                  t = 0; t < r.f; t++)
#             r.dv[t] = 0,
#                 r.dl[t] = 0;
#         for (t = 0; !(e >= n) && (e != n - 1 || 7 & (r.c ^ t)); t++) {
#             for (o = [],
#                      i = 0; i < r.f; i++)
#                 y() && (r.dl[i] += N()),
#                     r.dv[i] += w([3 * r.dl[i]], [1])[0],
#                     o[i] = r.dv[i];
#             a.push(o)
#         }
#         return a
#     }
#         ,
#         g()()
# }
# """
#
#
# @retry(wait=wait_fixed(2), retry_error_callback=return_last_value, stop=stop_after_attempt(5))
# def holiday2(date=False, save=True) -> pd.DataFrame:
#     """ 交易日历-历史数据
#     :return: 交易日历
#     :rtype: pandas.DataFrame
#     """
#     cache_file = get_config_path('holiday.csv')
#     temp_df = None
#
#     if Path(cache_file).exists():
#         df = pd.read_csv(cache_file)
#         if not df.loc[df['year'] == datetime.datetime.now().year].empty:
#             temp_df = df
#
#     if type(temp_df) is not pd.DataFrame:
#         client = httpx.Client(verify=False)
#
#         url = "https://finance.sina.com.cn/realstock/company/klc_td_sh.txt"
#         res = client.get(url)
#
#         js_code = py_mini_racer.MiniRacer()
#         js_code.eval(hk_js_decode)
#
#         # 执行js解密代码
#         dict_list = js_code.call("d", res.text.split("=")[1].split(";")[0].replace('"', ""))
#
#         temp_df = pd.DataFrame(dict_list)
#         temp_df.columns = ["date"]
#         temp_df["date"] = pd.to_datetime(temp_df["date"]).dt.date
#
#         temp_list = temp_df["date"].to_list()
#         temp_list.append(datetime.date(1992, 5, 4))  # 是交易日但是交易日历缺失该日期
#         temp_list.sort()
#
#         temp_df = pd.DataFrame(temp_list, columns=['date'])
#         temp_df['year'] = pd.DatetimeIndex(temp_df['date']).year
#
#         # 保存缓存
#         save and temp_df.to_csv(cache_file)
#
#     if date:
#
#         try:
#             date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
#         except ValueError:
#             date = datetime.datetime.now().date()
#
#         return temp_df.loc[temp_df['date'] == date].all().any()
#
#     return temp_df


def holiday(date=None, format_=None, country=None):
    cache_file = get_config_path('holiday.plk')

    format_ = format_ if format_ else '%Y-%m-%d'
    country = country if country else '中国'

    try:
        if date:
            date = datetime.datetime.strptime(date, format_).date()
        else:
            date = datetime.datetime.now().date()
    except ValueError as ex:
        logger.exception('日期或者日期格式错误!')
        raise ex

    if date.weekday() >= 5:
        return True

    if Path(cache_file).exists() and time.localtime(Path(cache_file).stat().st_mtime).tm_year == time.localtime(time.time()).tm_year:
        df = pd.read_pickle(cache_file)
    else:
        res = httpx.get('https://www.tdx.com.cn/url/holiday/')
        ret = re.findall(r'<textarea id="data" style="display:none;">([\s\w\d\W]+)</textarea>', res.text, re.M)[0].strip()
        day = [d.split('|')[:4] for d in ret.split('\n')]

        df = pd.DataFrame(day, columns=['日期', '节日', '国家', '交易所'], dtype=str)
        df.index = pd.to_datetime(df['日期'].astype('str'), format='%Y%m%d')
        df.to_pickle(cache_file)

    if country not in list(set(df['国家'].values)):
        raise ValueError(f'没有该国家`{country}`的交易日数据')

    df = df[df['国家'] == country]
    return not df[df.index.isin([date])].empty
