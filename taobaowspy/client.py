# coding: utf-8

from hashlib import md5
from datetime import datetime
import urllib2
import urllib
import sys
from json import loads


class Client(object):
    def __init__(self, **kwargs):
        self.last_body = None
        self.last_code = None
        self.last_data = None
        self.last_headers = None
        self.last_url = None
        self.timeout = kwargs.pop('timeout', 30)

    def execute(self, url, method, params=None, headers=None):
        headers = headers if headers is not None else {}

        str_params = urllib.urlencode(params if params is not None else {})

        req = urllib2.Request(url, str_params)

        for header, val in headers.iteritems():
            req.add_header(header, val)

        req.get_method = lambda: method.upper()

        self.last_url = url

        try:
            resp = urllib2.urlopen(req, timeout=self.timeout)
            self.last_code = resp.code
            self.last_headers = self.fetch_header(str(resp.headers))
            self.last_body = resp.read()
        except urllib2.HTTPError, e:
            self.last_code = e.code
            self._show_request_error(e.reason)
        except Exception, e:
            self._show_request_error(e)
        finally:
            self.last_data = params

        return self.last_body

    def _show_request_error(self, e):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sys.stderr.write("[%s] request error: %s %s \n" % (timestamp, self.last_url, str(e)))

    def get(self, url, params, headers=None):

        if len(params) > 0:
            url_params = urllib.urlencode(params)
            if url.find('?') == -1:
                url = '%s?%s' % (url, url_params)
            else:
                url = '%s&%s' % (url, url_params)

        return self.execute(url, 'GET', headers)

    @staticmethod
    def fetch_header(headers_str):
        ret = {}

        for line in headers_str.split("\r\n"):

            try:
                key, val = line.split(':', 1)
                ret[key] = val
            except:
                continue

        return ret


class TaobaoClient(Client):
    default_url = 'http://gw.api.taobao.com/router/rest'

    def __init__(self, **kwargs):
        super(TaobaoClient, self).__init__(**kwargs)

        self.url = kwargs.pop('api', TaobaoClient.default_url)
        self.appkey = kwargs.pop('appkey', '')
        self.secret = kwargs.pop('secret', '')
        self.format = 'json'
        self.sign_method = "md5"
        self.timeout = kwargs.pop('timeout', 180)

        self.session = kwargs.pop('session', '')

        self.sys_params = {
            'format': self.format,
            'app_key': self.appkey,
            'sign_method': self.sign_method,
            'v': '2.0',
            'timestamp': None,
            'method': None
        }

    def create_sign(self, params):
        """ 创建访问令牌 """

        if self.session is not None:
            params['session'] = self.session

        keys = params.keys()
        keys.sort()
        query = "%s%s%s" % (self.secret,
                            ''.join('%s%s' % (key, params[key]) for key in keys if params[key] is not None),
                            self.secret)

        return md5(query).hexdigest().upper()

    def request(self, api, params=None):
        params = params if params is not None else {}

        params = params.copy()
        params.update(self.sys_params)
        params.update({
            'method': api,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        params['sign'] = self.create_sign(params)

        return loads(self.get(self.url, params))

    def tmc_group_get(self, group_names=None):
        """ 获取自定义用户分组列表  """

        params = {}

        if group_names is not None:
            if isinstance(group_names, str):
                group_names = [group_names]
            params['group_names'] = ','.join(group_names)

        page_no = 1

        groups = []

        while True:
            params['page_no'] = page_no

            response = self.request(
                api='taobao.tmc.groups.get',
                params=params
            )

            if response is None or 'error_response' in response:
                break

            response = response['tmc_groups_get_response']

            total = response['total_results']
            _groups = response.get('groups', {'tmc_group': []}).get('tmc_group', [])

            if len(_groups) < 1 or total == len(groups):
                break
            else:
                groups.extend(_groups)

            page_no += 1

        return groups

    def tmc_group_add(self, group_name, nicks):
        if isinstance(nicks, str):
            nicks = [nicks]

        response = self.request(
            api='taobao.tmc.group.add',
            params={
                'group_name': group_name,
                'nicks': ','.join(nicks)
            }
        )

        print response

        if response is None or 'error_response' in response:
            return False

        return 'tmc_group_add_response' in response

    def del_all_tmc_group(self):
        """ 删除所有的分组, 返回空数组表示删除完毕"""

        groups = self.tmc_group_get()

        for group in groups:
            self.request(
                api='taobao.tmc.group.delete',
                params={
                    'group_name': group['name']
                }
            )

        return self.tmc_group_get()


if __name__ == '__main__':
    client = TaobaoClient(appkey='1021737885', secret='sandboxbbf5579605d7936422c11af0e',
                          api='http://gw.api.tbsandbox.com/router/rest',
                          session='6100f11de277a4d7dd6153772368fafd0993294f50fa1e02074082786')

    # client.tmc_group_add('test_1', 'sandbox_c_1')

    print client.del_all_tmc_group()
    print client.tmc_group_get()






        



        



