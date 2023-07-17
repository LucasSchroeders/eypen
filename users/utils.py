import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pytz import timezone


def string_to_date(str_date):

    if isinstance(str_date, str):
        # %d/%m/%Y
        validate_a = (
            r"^((0[1-9])|(1\d)|(2\d)|(3[0-1]))\/(|(0[1-9])|(1[0-2]))\/((\d{4}))$"
        )
        # %d-%m-%Y
        validate_b = (
            r"^((0[1-9])|(1\d)|(2\d)|(3[0-1]))\-(|(0[1-9])|(1[0-2]))\-((\d{4}))$"
        )
        # %d%m%Y
        validate_c = r"^((0[1-9])|(1\d)|(2\d)|(3[0-1]))(|(0[1-9])|(1[0-2]))((\d{4}))$"
        # %m/%d/%Y
        validate_d = (
            r"^(|(0[1-9])|(1[0-2]))\/((0[1-9])|(1\d)|(2\d)|(3[0-1]))\/((\d{4}))$"
        )
        # %m-%d-%Y
        validate_e = (
            r"^(|(0[1-9])|(1[0-2]))\-((0[1-9])|(1\d)|(2\d)|(3[0-1]))\-((\d{4}))$"
        )
        # %m%d%Y
        validate_f = r"^(|(0[1-9])|(1[0-2]))((0[1-9])|(1\d)|(2\d)|(3[0-1]))((\d{4}))$"
        # %Y/%m/%d
        validate_g = r"^\d{4}[\/s]((((0[13578])|(1[02]))[\/s](([0-2][0-9])|(3[01])))|(((0[469])|(11))[\/s](([0-2][0-9])|(30)))|(02[\/s]?[0-2][0-9]))$"
        # %Y-%m-%d
        validate_h = r"^\d{4}[\-s]((((0[13578])|(1[02]))[\-s](([0-2][0-9])|(3[01])))|(((0[469])|(11))[\-s](([0-2][0-9])|(30)))|(02[\-s]?[0-2][0-9]))$"
        # %Y%m%d
        validate_i = r"^\d{4}((((0[13578])|(1[02]))(([0-2][0-9])|(3[01])))|(((0[469])|(11))(([0-2][0-9])|(30)))|(02[0-2][0-9]))$"
        # %d/%m/%y
        validate_l = r"^(((0[1-9]|[12]\d|3[01])\/(0[13578]|1[02])\/(\d{2}))|((0[1-9]|[12]\d|30)\/(0[13456789]|1[012])\/(\d{2}))|((0[1-9]|1\d|2[0-8])\/02\/(\d{2}))|(29\/02\/((0[48]|[2468][048]|[13579][26])|(00))))$"

        if bool(re.match(validate_a, str_date)):
            ret_date = datetime.strptime(str_date, '%d/%m/%Y')
        elif bool(re.match(validate_b, str_date)):
            ret_date = datetime.strptime(str_date, '%d-%m-%Y')
        elif bool(re.match(validate_c, str_date)):
            ret_date = datetime.strptime(str_date, '%d%m%Y')
        elif bool(re.match(validate_d, str_date)):
            ret_date = datetime.strptime(str_date, '%m/%d/%Y')
        elif bool(re.match(validate_e, str_date)):
            ret_date = datetime.strptime(str_date, '%m-%d-%Y')
        elif bool(re.match(validate_f, str_date)):
            ret_date = datetime.strptime(str_date, '%m%d%Y')
        elif bool(re.match(validate_g, str_date)):
            ret_date = datetime.strptime(str_date, '%Y/%m/%d')
        elif bool(re.match(validate_h, str_date)):
            ret_date = datetime.strptime(str_date, '%Y-%m-%d')
        elif bool(re.match(validate_i, str_date)):
            ret_date = datetime.strptime(str_date, '%Y%m%d')
        elif bool(re.match(validate_l, str_date)):
            ret_date = datetime.strptime(str_date, '%d/%m/%y')
            if ret_date.year > datetime.now(timezone('America/Sao_Paulo')).year:
                # fix para nao exceder o ano atual
                ret_date = ret_date - relativedelta(years=100)
        else:
            raise Exception('formato invalido')
    else:
        raise Exception('tipo da variavel tem que ser string')

    return ret_date
