import requests
import re
import time
from fn import _
import random

class download():

    def __init__(self):

        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

        ipHtml = requests.get('http://haoip.cc/tiqu.htm')
        m = re.findall(r'r/>\S*(.*?)<br/>', ipHtml.text, re.S)
        self.ipList = list(map(lambda s: re.sub('\n', '', s).strip(), m))



    def get(self, url, timeout=3, proxy=None, num_retries=6):
        headers = {'User-Agent': random.choice(self.user_agent_list)}

        print('get url', url)
        try:
            if proxy == None:

                res = requests.get(url, headers=headers, timeout=timeout)
                if res.ok:
                    return res
                else:
                    return self.retrieGet(url, timeout=timeout, num_retries=num_retries)
            else:
                    print(u'当前代理', proxy)
                    res = requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
                    if res.ok:
                        return res
                    else:
                        return self.retrieGet(url, timeout=timeout, proxy=proxy, num_retries=num_retries)
        except:
            return self.retrieGet(url, timeout=timeout, proxy=proxy, num_retries=num_retries)

    def retrieGet(self, url, timeout, proxy=None, num_retries=6):

        print('开始重试 ', num_retries)
        time.sleep(10)

        if proxy == None:
            if num_retries > 0:
                print(u'重试：', url, 'num_retries:', num_retries)
                return self.get(url, timeout=timeout, num_retries=num_retries-1)
            else:
                ip = str(random.choice(self.ipList))
                proxy = {'http': ip}
                return self.get(url, timeout=timeout, proxy=proxy)
        else:
            if num_retries > 0:
                self.get(url, timeout=timeout, proxy=proxy, num_retries=num_retries-1)
            else:
                ip = random.choice(self.ipList)
                proxy = {'http': ip}
                return self.get(url, timeout=timeout, proxy=proxy)


request = download()
