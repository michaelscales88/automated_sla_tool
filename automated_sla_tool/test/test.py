from datetime import datetime, date, time, timedelta
from dateutil.parser import parse
from automated_sla_tool.src.BucketDict import BucketDict
from automated_sla_tool.src.UtilityObject import UtilityObject
import pyexcel as pe
from automated_sla_tool.src.FinalReport import FinalReport
from automated_sla_tool.src.TupleKeyDict import TupleKeyDict
import os
import re
from glob import glob as glob
from socket import *
import multiprocessing
from dateutil.parser import parse
import time
import sys
from queue import Queue
import sqlite3
import logging
import logging.config
import iso8601
from os import path
from os.path import basename
from automated_sla_tool.src.AppSettings import AppSettings
from automated_sla_tool.src.factory import get_email_data
from automated_sla_tool.src.InternalDb import InternalDb
from time import sleep
from collections import defaultdict, OrderedDict
from automated_sla_tool.src.utilities import valid_dt
import speech_recognition as sr
from pyexcel import Sheet

# Settings path
_settings = r'C:\Users\mscales\Desktop\Development\automated_sla_tool\automated_sla_tool\settings\SlaReport.ini'
# GOOGLE_CLOUD_SPEECH_CREDENTIALS = r""""installed":{"client_id":"766872889458-u869th48ktiifumrk5ek2a7lp36tb04r.apps.googleusercontent.com","project_id":"encoded-vista-156916","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://accounts.google.com/o/oauth2/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"bTvPefgEbqvc5k11JcoeAhSJ","redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}"""
# GOOGLE_CLOUD_SPEECH_CREDENTIALS = path.join(
#     r'C:\Users\mscales\Desktop\Development\automated_sla_tool\automated_sla_tool\settings',
#     'client_secret_766872889458-u869th48ktiifumrk5ek2a7lp36tb04r.apps.googleusercontent.com.json')
# def get_config(config_path, name):
#     logging.config.dictConfig(config_path)
#     return logging.getLogger(name)
#
#
# class Test:
#     def __init__(self):
#         self._finished = False
#
#     @property
#     def finished(self):
#         return self._finished
#
#     def set_finished(self):
#         self._finished = True
#
#     def run(self):
#         print('running..')
#
#
# def test_fn(stuff):
#     for thing in stuff:
#         print(thing)
#     print('something')
#
# class Point(object):
#     def __init__(self, x, y):
#         self.x, self.y = x, y
#
#     def __conform__(self, protocol):
#         if protocol is sqlite3.PrepareProtocol:
#             return "%f;%f" % (self.x, self.y)
#
#
# def worker():
#     p = multiprocessing.current_process()
#     print('worker {0} {1}'.format(p.name, datetime.now().time()))
#     sys.stdout.flush()
#     time.sleep(2)
#     print('worker {0} {1}'.format(p.name, datetime.now().time()))
#     sys.stdout.flush()
#
#
# class SqlCommand(object):
#     def __init__(self):
#         super().__init__()
#         self._name = None
#         self._cmd = None
#
#     def __repr__(self):
#         return self._cmd
#
#     @property
#     def cmd(self):
#         return self._cmd
#
#     @cmd.setter
#     def cmd(self, cmd):
#         self._cmd = cmd
#
#     @property
#     def name(self):
#         return self._name
#
#     @name.setter
#     def name(self, name):
#         self._name = name
# AUDIO_FILE = path.join(r'C:\Users\mscales\Downloads', "man1_nb.wav")
AUDIO_FILE = path.join(r'C:\Users\mscales\Downloads', "MSG00053.wav")


def filter_row(row_index, row):
    result = [element for element in row if element != '']
    return len(result) == 0


def test():
    # from os import getcwd
    # wav_f = path.join(getcwd(), 'MSG00053.wav')
    # with open(wav_f) as f:
    #     print(type(f))
    # email = get_email_data(settings=AppSettings(settings_file=_settings))
    # print(email)
    # for k, v in email.items():
    #     print(k)
    #     print(v)
    # conn = InternalDb()
    # print(conn.get_tables())
    # r = sr.Recognizer()
    # with sr.AudioFile(AUDIO_FILE) as source:
    #     audio = r.record(source)  # read the entire audio file
    #
    # # recognize speech using Google Cloud Speech
    #     try:
    #         print("Google Cloud Speech thinks you said {speech}".format(speech=r.recognize_google_cloud(audio)))
    #     except sr.UnknownValueError:
    #         print("Google Cloud Speech could not understand audio")
    #     except sr.RequestError as e:
    #         print("Could not request results from Google Cloud Speech service; {0}".format(e))

    # string_test = 'Voicemail Message (8472243850 > Danaher) From:8472243850Fri, 13 Jan 2017 07:08:43 -0600'
    # # print(iso8601.parse_date(string_test))
    # dt = valid_dt(string_test.split(',')[1])
    # print(dt)
    # print(type(dt))
    # str1 = ''
    # str2 = 'stuff'
    # print(str1.isalpha())
    # print(str2.isalpha())
    # from os import makedirs
    # from os.path import isfile
    # f_path1 = 'C:/Users/Mscales/Desktop/test_file'
    # f_path = 'C:/Users/Mscales/Desktop/test_file.txt'
    # print(isfile(f_path))
    # makedirs(f_path1, exist_ok=True)
    # print(isfile(f_path))
    # print(not True)
    # print(not False)
    # test_list= []
    # print(test_list.__sizeof__())
    # test_list.append(0)
    # test_list.append(0)
    # test_list.append(0)
    # print(test_list.__sizeof__())
    # import re
    # s = "alpha.Customer[cus_Y4o9qMEZAugtnW] ..."
    # m = re.search(r"\[([A-Za-z0-9_]+)\]", s)
    # print(m.group(1))
    # s = 'stuff stuff (1235) stuff'
    # matches = re.search(r"([0-9]+)", s)
    # print(matches.group(0))
    sheet = pe.Sheet(colnames=['', 'stuff'])
    rows = [
        ['row_name1', 'stuff_value3'],
        ['', ''],
        ['row_name2', 'stuff_value1'],
        ['row_name3', 'stuff_value3'],
        ['', ''],
        ['row_name4', 'stuff_value'],
        ['row_name5', 'stuff_value2'],
        ['row_name6', 'stuff_value'],
        ['row_name7', 'stuff_value2'],
        ['', ''],
        ['row_name8', 'stuff_value']
    ]
    for row in rows:
        sheet.row += row
    sheet.name_rows_by_column(0)
    print(sheet)
    del sheet.row[filter_row]
    print(sheet)
    # # for row_name in sheet.rownames:
    # #     if sheet[row_name, 'stuff'] == 'stuff_value1':
    # #         sheet.delete_named_row_at(row_name)
    # # print(sheet)
    # i_count = {}
    # for row_name in reversed(sheet.rownames):
    #     caller = sheet[row_name, 'stuff']
    #     # i_count[caller] = {
    #     #     'count': i_count.get(caller, 0).get('count', 0) + 1,
    #     #     ''
    #     # }
    #     dup_info = i_count.get(caller, {'count': 0,
    #                                     'call_ids': []})
    #     dup_info['count'] += 1
    #     dup_info['call_ids'].append(caller)
    #     i_count[caller] = dup_info
    # print(i_count)
    # string1 = 'string'
    # string2 = '123'
    # print(string1.isdigit())
    # print(string2.isdigit())
    # _log_path = path.join(path.dirname(path.dirname(path.abspath(__file__))), r'settings\logging2.conf')
    # print(_log_path)
    # log = SysLog(__file__, file_path=_log_path)
    # print(log)
    # test_sheet = pe.Sheet()
    # test_sheet.row += [['', 'A', 'B', 'C', 'D'],
    #                    [1, 2, 3, 4, 5],
    #                    [6, 7, 8, 9, 10]]
    # test_sheet.name_columns_by_row(0)
    # test_sheet.name_rows_by_column(0)
    # print(test_sheet)
    # for i, column in enumerate(test_sheet.columns()):
    #     print(test_sheet.colnames[i])
    #     print(column)
    # im_a_dict = {
    #     'value': 0
    # }
    # if im_a_dict['value']:
    #     print('i evaluated to true')
    # print(im_a_dict['value'] is False)
    # sheet = pe.Sheet(colnames=['', 'a', 'b', 'c', 'd'])
    # tuple_ex = (test_fn, 'stuff', 'stuff2')
    # fn = tuple_ex[:1]
    # other_stuff = tuple_ex[1:]
    # print(fn)
    # print(other_stuff)
    # tuple_ex[:1](other_stuff)
    # key = 'stuff'
    # thing1 = key[0]
    # thing2 = key[2]
    # print(thing1)
    # print(thing2)
    # sheet = pe.Sheet(colnames=['', 'a', 'b', 'c', 'd'])
    # rownames = ['a', 'b', 'c', 'd']
    # print(['row'] + [0 for x in range(len(sheet.colnames)-1)])
    # for row in rownames:
    #     sheet.row += [row] + [0 for x in range(len(sheet.colnames)-1)]
    # sheet.name_rows_by_column(0)
    # print(sheet)
    # rows = [
    #     ['{i}'.format(i=chr(i * (x+1) + 97)) for x in reversed(range(5))] for i in range(5)
    # ]
    # for row in rows:
    #     sheet.row += row
    # for x in range(3):
    #     sheet.row += [x, '0', '0', '0', '0']
    # sheet.name_rows_by_column(0)
    # print(sheet)
    # for i, row in enumerate(sheet.rownames):
    #     sheet.set_row_at(i, ['a', 'b', 'c', 'd'])
    # print(sheet)
    # print(sheet.rownames)
    # print(sheet.colnames)
    # print(sheet)
    # sheet.colnames += ['e', 'f']
    # print(sheet.colnames)
    # new_rows = [
    #     ['e', 'f'],
    #     ['1', '2'],
    #     ['2', '2'],
    #     ['3', '3'],
    #     ['4', '4'],
    #     ['5', '5']
    #     # ['', 'e', 'f'],
    #     # ['a', '1', '2'],
    #     # ['f', '2', '2'],
    #     # ['k', '3', '3'],
    #     # ['p', '4', '4'],
    #     # ['u', '5', '5']
    # ]
    # new_sheet = pe.Sheet(new_rows)
    # new_sheet.name_rows_by_column(0)
    # new_rows = OrderedDict(
    #     [
    #         ('e', ['1', '2', '3', '4', '5']),
    #         ('f', ['1', '2', '3', '4', '5'])
    #     ]
    # )
    # print(new_rows)
    # new_sheet.name_rows_by_column(0)
    # sheet.column['e'] += new_sheet.column['e']
    # sheet.column['f'] += new_sheet.column['f']
    # sheet.extend_columns(new_rows)
    # print(sheet)
    # print(sheet.column['e'])
    # sheet.column += new_sheet
    # print(sheet)
    # conn_string = {
    #     'DATABASE': 'chronicall',
    #     'UID': 'Chronicall',
    #     'PWD': 'ChR0n1c@ll1337',
    #     'SERVER': '10.1.3.17',
    #     'PORT': '9086'
    # }
    # tables = ['c_call', 'c_event', 'c_feature']
    # commands = []
    # raw_commands = {
    #     k: datetime.today().date() for k in tables
    # }
    # for k, v in raw_commands.items():
    #     cmd = SqlCommand()
    #     cmd.name = k
    #     cmd.cmd = (
    #         '''
    #         SELECT *
    #         FROM {t}
    #         WHERE to_char({t}.start_time, 'YYYY-MM-DD') = '{v}'
    #         '''.format(t=cmd.name, v=v.strftime('%Y-%m-%d'))
    #     )
    #     commands.append(cmd)
    # from automated_sla_tool.src.SqlWriter import SqlWriter as ps_write
    # from automated_sla_tool.src.SqliteWriter import SqliteWriter as sq_lite
    # conn = ps_write(**conn_string)
    # conn.replicate_to(dest_conn=sq_lite(), sql_commands=commands)
    # new_conn = sq_lite()
    # print(new_conn.query('c_call'))
    # print(new_conn.query('c_event'))
    # print(new_conn.query('c_feature'))
    # string = 'Call ID - 12312412'
    # import re
    # string = 'Cradle to, Grave - stuff'
    # corner_case = re.split(', | - ', string)
    # print(corner_case)
    # first_split = string.split(' - ')
    # second_split = first_split[0].split(' ')
    # print(second_split)
    # check_one = second_split[0] not in ('Feature', 'Call', 'Event')  # False
    # print(len(first_split))
    # print(True if len(first_split) > 1 else check_one)
    # input_opt = OrderedDict(
    #     [('Today', 0),
    #      ('Tomorrow', 1),
    #      ('Yesterday', -1)]
    # )
    # input_opt2 = ['Today', ]
    # selection = list(input_opt.values())
    # chc = selection[
    #         int(
    #             input(
    #                 ''.join(['{k}: {i}\n'.format(k=k, i=i) for i, k in enumerate(input_opt)])
    #             )
    #         )
    #     ]
    # print(
    #     date.today() + timedelta(days=chc)
    # )
    # from automated_sla_tool.src.FinalReport import FinalReport
    # rpt = FinalReport(report_date=date.today(), report_type='sla_report')
    # print(rpt.name)
    # rpt.name = 'something else'
    # print(rpt.name)
    # rpt.save_as('C:/Users/mscales/desktop/test.xlsx')
    # print(
    #     [0 for x in range(10)]
    # )


    print('Complete')


if __name__ == "__main__":
    test()
