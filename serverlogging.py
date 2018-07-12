import datetime
import functools
import inspect


def logline(message, req_id = ['0', 'Init', None]):
    """
Log line header with timestamp and request ID

Parameters
----------

Returns
-------

Raises:
-------

"""
    if len(req_id[0]) < 12:
        req_id[0]= '0'*(12 - len(req_id[0])) + req_id[0]
    caller = inspect.getouterframes(inspect.currentframe())[1][-3]
    if caller != '<module>' and caller != 'wrapper':
        req_id[-1] = caller
    #req_id[0] = req_id[0][-12:-8] + '_' + req_id[0][-8:-4] + '_' + req_id[0][-4:]     
    tstamp = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f')[:-3]
    logheader = '[%s] %s' % (tstamp, req_id)
    print(logheader.replace("'",""), message)




def print_kwargs(**kwargs):
    kwargs.pop('req_id')
    if 'passwd' in kwargs:
        kwargs['passwd'] = '<password>'
    return kwargs

def log_func(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            kwargs['req_id'][2] = func.__name__
        except KeyError:
            pass
        return func(*args, **kwargs)
    return wrapper
