import re
import numpy as np
import ast
from datetime import datetime


def cnj_sanitization(cnj):
    '''
    Recebe o cnj como string e faz a validação do mesmo, retornando corrigido quando possível
    :param cnj:
    :return:
    TO DO: Put more cases, get from
    '''
    cnj_corrected = np.nan

    if re.match('.*[0-9]{7}[-][0-9]{2}[.][0-9]{4}[.][0-9][.][0-9]{2}[.][0-9]{4}.*', str(cnj).strip()):
        cnj_corrected = str(cnj)

    elif re.match('[0-9]{7}[.][0-9]{2}[.][0-9]{4}[.][0-9][.][0-9]{2}[.][0-9]{4}', str(cnj).strip()):
        cnj_aux = str(cnj).strip()
        cnj_aux = cnj_aux[:7] + '-' + cnj_aux[8:]
        cnj_corrected = str(cnj_aux)

    elif re.match('[0-9]{7}[-][0-9]{2}[.][0-9]{4}[.][0-9]{3}[.][0-9]{4}', str(cnj).strip()):
        cnj_aux = str(cnj).strip()
        cnj_aux = cnj_aux[:17] + '.' + cnj_aux[17:]
        cnj_corrected = str(cnj_aux)

    elif re.match('[0-9]{2,6}[-][0-9]{2}[.][0-9]{4}[.][0-9][.][0-9]{2}[.][0-9]{4}', str(cnj).strip()):

        cnj_aux = re.findall('[0-9]{2,6}[-][0-9]{2}[.][0-9]{4}[.][0-9][.][0-9]{2}[.][0-9]{4}', str(cnj).strip())[0]

        while len(str(cnj_aux).strip()) < 25:
            cnj_aux = '0' + str(cnj_aux).strip()

        cnj_corrected = str(cnj_aux)

    elif re.match('^[0-9]{15,20}$', str(re.sub('\.|-', '', str(cnj))).strip()) and \
            len(str(re.sub('\.|-', '', str(cnj))).strip()) <= 20:

        cnj_aux = re.sub('\.|-', '', str(cnj)).strip()

        if len(cnj_aux) < 20:
            while len(str(cnj_aux).strip()) <= 20:
                cnj_aux = '0' + str(cnj_aux).strip()

        cnj_aux = cnj_aux[0:7] + '-' + cnj_aux[7:9] + '.' + cnj_aux[9:13] + '.' + cnj_aux[13:14] + '.' + cnj_aux[
                                                                                                         14:16] + '.' + cnj_aux[
                                                                                                                        16:20]

        cnj_corrected = str(cnj_aux)

    if not str(cnj_corrected) == 'nan':
        return re.findall('[0-9]{7}[-][0-9]{2}[.][0-9]{4}[.][0-9][.][0-9]{2}[.][0-9]{4}', cnj_corrected)[0]

    else:
        return np.nan


def date_sanitization(date):
    date = str(date).strip()
    if re.match('([0-2]?\d|3[0-1])(/|-|\.)(0?\d|1[0-2])(/|-|\.)((\d\d)?\d\d)', date):
        date = re.sub('\.|-', '/', date)
        date = date.split('/')

        dd = date[0] if len(date[0]) == 2 else '0' + date[0]
        mm = date[1] if len(date[1]) == 2 else '0' + date[1]
        yyyy = date[2] if len(date[2]) == 4 else ('19' + date[2] if int(date[2]) >= 90 else '20' + date[2])

        try:
            date = dd + '/' + mm + '/' + yyyy
            datetime.strptime(date, '%d/%m/%Y')
        except:
            date = np.nan

        return date

    return np.nan


def num_sanitization(num):
    num = str(num).strip()
    if re.match('(\d*)(\.|,)?(\d*)', num):
        num = num.replace('.', ':')
        num = num.replace(',', '.')
        num = num.replace(':', '.') if '.' not in num else num.replace(':', '')

        try:
            return ast.literal_eval(num)
        except:
            return np.nan

    return np.nan


def filter_date(date, start, end):
    if np.nan in (date, start, end):
        return np.nan

    date_ = datetime.strptime(date, '%d/%m/%Y')
    start_ = datetime.strptime(start, '%d/%m/%Y')
    end_ = datetime.strptime(end, '%d/%m/%Y')

    if start_ <= date_ <= end_:
        return date

    return np.nan


def filter_num(num, start, end):
    if np.nan in (num, start, end):
        return np.nan

    if start <= num <= end:
        return num

    return np.nan
