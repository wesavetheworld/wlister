try:
    import unittest2 as unittest
except ImportError:
    import unittest

import requests

class ProxyTest(unittest.TestCase):

    def test_flask_ok(self):
        r = requests.get('http://localhost:5000')
        self.assertEqual(r.status_code, 200,
                         'HTTP target service is not running')

    def test_proxy_ok(self):
        r = requests.get('http://localhost/')
        self.assertEqual(r.status_code, 200,
                         'Proxy service is not running properly')

    def test_dummy_uri(self):
        r = requests.get('http://localhost/abc')
        self.assertEqual(r.status_code, 404,
                         'Filtering service not working')


class ParametersTest(unittest.TestCase):

    def test_parameters_ok_same_order(self):
        r = requests.get('http://localhost/parameters?var1=val1&var2=val2')
        self.assertEqual(r.status_code, 200)

    def test_parameters_ok_different_order(self):
        r = requests.get('http://localhost/parameters?var2=val2&var1=val1')
        self.assertEqual(r.status_code, 200)

    def test_parameters_ko_wrong_value(self):
        r = requests.get('http://localhost/parameters' +
                         '?var1=ValueNotExpected&var2=val2')
        self.assertEqual(r.status_code, 404)

    def test_parameters_ko_less_parameter(self):
        r = requests.get('http://localhost/parameters?var2=val2')
        self.assertEqual(r.status_code, 404)

    def test_parameters_ko_more_parameter(self):
        r = requests.get('http://localhost/parameters' +
                         '?var1=val1&var2=val2&UnexpectedParameter=whatever')
        self.assertEqual(r.status_code, 404)

    def test_parameters_ko_duplicated(self):
        r = requests.get('http://localhost/parameters' +
                         '?var1=val1&var2=val2&var1=val1')
        self.assertEqual(r.status_code, 404)


class ContentUrlEncodedTest(unittest.TestCase):

    def test_content_url_encoded_ok_same_order(self):
        content = {"var1": "val1", "var2": "val2"}
        r = requests.post('http://localhost/post/', data=content)
        self.assertEqual(r.status_code, 200)

    def test_content_url_encoded_ok_different_order(self):
        content = {"var2": "val2", "var1": "val1"}
        r = requests.post('http://localhost/post/', data=content)
        self.assertEqual(r.status_code, 200)

    def test_content_url_encoded_ko_less_parameter(self):
        content = {"var1": "val1"}
        r = requests.post('http://localhost/post/', data=content)
        self.assertEqual(r.status_code, 404)

    def test_content_url_encoded_ko_more_parameter(self):
        content = {"var1": "val1", "var2": "val2",
                   "UnexpectedParamter": "whatever"}
        r = requests.post('http://localhost/post/', data=content)
        self.assertEqual(r.status_code, 404)

    def test_content_url_encoded_ko_wrong_value(self):
        content = {"var1": "UnexpectedValue", "var2": "val2"}
        r = requests.post('http://localhost/post/', data=content)
        self.assertEqual(r.status_code, 404)

    def test_content_url_encoded_ko_wrong_value_too_large(self):
        v = 'val1' * 10
        content = {"var1": v, "var2": "val2"}
        r = requests.post('http://localhost/post/', data=content)
        self.assertEqual(r.status_code, 404)

class HeadersTest(unittest.TestCase):

    def test_headers_ok(self):
        h = { 'header-test': 'test' }
        r = requests.get('http://localhost/headers/', headers=h)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.content, "OK", "Response is not OK")

    def test_headers_ko_wrong_value(self):
        h = { 'header-test': 'UnexpectedValue' }
        r = requests.get('http://localhost/headers/', headers=h)
        self.assertEqual(r.status_code, 404)

    def test_headers_ko_duplicated_header(self):
        import telnetlib
        t = telnetlib.Telnet('wlister.vm', 80)
        t.write('GET /headers/ HTTP/1/1\n')
        t.write('Host: localhost\n')
        t.write('Accept: */*\n')
        t.write('User-Agent: python-requests/2.2.0 CPython/2.7.3 Linux/3.8.0-29-generic\n')
        t.write('Accept-Encoding: gzip, deflate, compress\n')
        t.write('header-test: test\n')
        t.write('header-test: test\n\n')
        r = t.read_all()
        t.close()
        self.assertEqual(int(r[9:12]), 404)

    def test_headers_ko_less_header(self):
        import telnetlib
        t = telnetlib.Telnet('wlister.vm', 80)
        t.write('GET /headers/ HTTP/1/1\n')
        t.write('Host: localhost\n')
        #t.write('Accept: */*\n')
        t.write('User-Agent: python-requests/2.2.0 CPython/2.7.3 Linux/3.8.0-29-generic\n')
        t.write('Accept-Encoding: gzip, deflate, compress\n')
        t.write('header-test: test\n\n')
        r = t.read_all()
        t.close()
        self.assertEqual(int(r[9:12]), 404)

    def test_headers_ko_more_header(self):
        import telnetlib
        t = telnetlib.Telnet('wlister.vm', 80)
        t.write('GET /headers/ HTTP/1/1\n')
        t.write('Host: localhost\n')
        t.write('Accept: */*\n')
        t.write('Supernumerary: ouh yeah\n')
        t.write('User-Agent: python-requests/2.2.0 CPython/2.7.3 Linux/3.8.0-29-generic\n')
        t.write('Accept-Encoding: gzip, deflate, compress\n')
        t.write('header-test: test\n\n')
        r = t.read_all()
        t.close()
        self.assertEqual(int(r[9:12]), 404)