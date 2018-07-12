import sys
import os
import ssl

from getpass import getpass
from suds.client import Client
from suds.xsd.doctor import Import
from suds.xsd.doctor import ImportDoctor
from serverlogging import logline

VER = '10.5'
WSDL_RELPATH = '/axltoolkit/schema/%s/AXLAPI.wsdl' % VER
DUMPS_RELPATH = 'static' + os.path.sep + 'dumps'
TNS = 'http://schemas.cisco.com/ast/soap/'

if 'win' in sys.platform.lower():
    WSDL_CURPATH = os.path.abspath(os.path.curdir).replace('\\', '/')
    WSDL_PATH = 'file:///' + WSDL_CURPATH + WSDL_RELPATH
else:
    WSDL_CURPATH = os.path.abspath(os.path.curdir)
    WSDL_PATH = 'file://' + WSDL_CURPATH + WSDL_RELPATH


CUCMRO = {'server': False,
          'username': False,
          'password': False,
          'readonly': True,
          }

CUCMRW = {'server': False,
          'username': False,
          'password': False,
          'readonly': False,
          }


class AXLError(Exception):
    pass


class AxlConn:
    """AXL Connection to CUCM Object"""

    def __init__(self, **kwargs):
        kwargs['_'] = None
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        self.server = kwargs.get('server', False
                                 ) or (input('CUCM address: '))
        self.location = 'https://' + self.server + ':8443/axl/'
        self.username = kwargs.get('username', False) or \
                        input('AXL Username: ')
        self.password = kwargs.get('password', False) or \
                        getpass('Password for %s: ' % self.username)
        self.imp = Import('http://schemas.xmlsoap.org/soap/encoding/',
                          'http://schemas.xmlsoap.org/soap/encoding/')
        self.imp.filter.add(TNS)
        self.readonly = kwargs.get('readonly', True)
        self.client = Client(WSDL_PATH, location=self.location,
                             faults=False,
                             plugins=[ImportDoctor(self.imp)],
                             username=self.username,
                             password=self.password)
        # Test Connection
        try:
            response = self.client.service.getCCMVersion()
            validate_axlresp(response)
            if VER not in str(response[1]['return'].componentVersion.version):
                logline('WARNING: CUCM version is ' +
                        '%s, this script is using %s AXL schema.' %
                        (response[1]['return'].componentVersion.version, VER))
        except Exception as e:
            logline('%s: %s' % (type(e).__name__, e))
            raise

    def __repr__(self):
        return 'AXLConn(CUCM: %s, AXLUser: %s, %s)' % \
               (self.server, self.username, (self.readonly and 'RO') or 'RW')

    def axl_query(self, query):
        if self.readonly:
            if not query.lower().startswith('get') \
                    and not query.startswith('list'):
                raise PermissionError('ReadOnly Mode')
        query = 'self.client.service.' + query
        try:
            response = eval(query)
            validate_axlresp(response)
        except Exception as e:
            logline('%s: %s' % (type(e).__name__, e))
            raise

        return response

    def sql_query(self, query):
        if self.readonly:
            if not query.lower().startswith('select'):
                raise PermissionError('ReadOnly Mode')
        try:
            response = self.client.service.executeSQLQuery("%s" % query)
            validate_axlresp(response)
        except Exception as e:
            logline('%s: %s' % (type(e).__name__, e))
            raise

        if query.lower().startswith('select'):
            result = []
            if response[1]['return']:
                for item in response[1]['return'][0]:
                    result.append(dict(item))
            return result

        return response[1]['return']


def validate_axlresp(response):
    if not hasattr(response[0], 'value'):
        raise AXLError(response)
    if response[0].value != 200:
        raise AXLError('%s:%s' %
                       (response[1].detail.axlError.axlcode,
                        response[1].faultstring)
                       )
