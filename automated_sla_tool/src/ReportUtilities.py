from datetime import datetime, date, time
from dateutil.parser import parse
from pyexcel import Book, Sheet, get_sheet, get_book
from subprocess import Popen
from re import split
from glob import glob
from os.path import join

from automated_sla_tool.src.UtilityObject import UtilityObject


class UniqueDict(dict):
    def __setitem__(self, key, value):
        if key not in self:
            super().__setitem__(key, value)


class BoundSettings(object):

    def __init__(self):
        self._bound_settings = []
        self._cwd = None

    @property
    def current_binding(self):
        return self._bound_settings

    @current_binding.setter
    def current_binding(self, new_binding):
        self._bound_settings = new_binding

    @property
    def cwd(self):
        return self._cwd

    @cwd.setter
    def cwd(self, new_dir):
        self._cwd = new_dir


class ReportUtilities(UtilityObject):

    def __init__(self):
        super().__init__()
        self._bound_settings = BoundSettings()

    @property
    def cwd(self):
        return self._bound_settings.cwd

    @cwd.setter
    def cwd(self, new_wd):
        self._bound_settings.cwd = new_wd

    @property
    def bound_settings(self):
        return tuple(self._bound_settings.current_binding)

    @bound_settings.setter
    def bound_settings(self, new_bindings):
        self._bound_settings.current_binding = new_bindings

    @staticmethod
    def is_weekday(raw_date):
        try:
            return ReportUtilities.day_of_week(raw_date) not in (5, 6)
        except AttributeError:
            print('{date} is invalid to get day of the week.'.format(date=raw_date))

    @staticmethod
    def day_of_week(raw_date):
        return raw_date.weekday() if isinstance(raw_date, datetime) else 'Unknown Date'

    @staticmethod
    def name_of_day(raw_date):
        return raw_date.strftime('%A') if isinstance(raw_date, datetime) else 'Unknown Date'

    @staticmethod
    def date_to_dt(raw_date):
        return datetime.combine(raw_date, time()) if isinstance(raw_date, date) else raw_date

    @staticmethod
    def phone_number(raw_number):
        rtn_val = [ch for ch in str(raw_number) if ch.isdigit()]
        return rtn_val[1:] if len(rtn_val) > 7 and rtn_val[0] == 1 else rtn_val

    @staticmethod
    def find_non_distinct(sheet=None, event_col=None):
        i_count = {}
        for row_name in reversed(sheet.rownames):
            dup_event = sheet[row_name, event_col]
            dup_info = i_count.get(dup_event, {'count': 0,
                                               'rows': []})
            dup_info['count'] += 1
            dup_info['rows'].append(row_name)
            i_count[dup_event] = dup_info
        return i_count

    @staticmethod
    def apply_format_to_wb(wb, filters=(), one_filter=None):
        for sheet in wb:
            ReportUtilities.apply_format_to_sheet(sheet, filters, one_filter)

    @staticmethod
    def apply_format_to_sheet(sheet, filters=(), one_filter=None):
        for a_filter in filters:
            del sheet.row[a_filter]
        if one_filter:
            del sheet.row[one_filter]

    @staticmethod
    def collate_wb_to_sheet(wb=()):
        headers = ['row_names'] + wb[0].colnames
        sheet_to_replace_wb = Sheet(colnames=headers)
        unique_records = UniqueDict()
        for sheet in wb:
            for i, name in enumerate(sheet.rownames):
                unique_records[name] = sheet.row_at(i)
        for rec in sorted(unique_records.keys()):
            sheet_to_replace_wb.row += [rec] + unique_records[rec]
        sheet_to_replace_wb.name_rows_by_column(0)
        return sheet_to_replace_wb

    @staticmethod
    def shortest_longest(*args):
        return (args[0], args[1]) if args[0] is min(*args, key=len) else (args[1], args[0])

    @staticmethod
    def return_selection(input_opt):
        selection = list(input_opt.values())
        return selection[
            int(
                input(
                    ''.join(['{k}: {i}\n'.format(k=k, i=i) for i, k in enumerate(input_opt)])
                )
            )
        ]

    @staticmethod
    def find(lst, a):
        return [i for i, x in enumerate(lst) if x == a]

    @staticmethod
    def is_empty_wb(book):
        if isinstance(book, Book):
            return book.number_of_sheets() is 0

    @staticmethod
    def make_summary(headers):
        todays_summary = Sheet()
        todays_summary.row += headers
        todays_summary.name_columns_by_row(0)
        return todays_summary

    # TODO consider methods like this to move into UtilityObject
    @staticmethod
    def add_time(dt_t, add_time=None):
        return (datetime.combine(datetime.today(), dt_t) + add_time).time()

    @staticmethod
    def safe_parse(dt=None):
        try:
            return parse(dt)
        except ValueError:
            print('Could not parse date_time: {dt}'.format(dt=dt))

    @staticmethod
    def apply_header_filters(work_sheet):
        del work_sheet.row[ReportUtilities.header_filter]
        work_sheet.name_rows_by_column(0)
        work_sheet.name_columns_by_row(0)

    @staticmethod
    def apply_body_filters(work_sheet):
        # Remove summary page
        # workbook.remove_sheet('Summary') -> map this to settings
        # try:
        #     self.chck_rpt_dates(sheet)
        # except ValueError:
        #     workbook.remove_sheet(sheet_name)
        pass

    @staticmethod
    def remove_sheets_per_settings(workbook):
        workbook.remove_sheet('Summary')
        # for sheet_to_remove in 'Summary':
        #     try:
        #         workbook.remove_sheet(sheet_to_remove)
        #     except KeyError:
        #         pass

    # TODO this need to be able to handle more data types than excel
    @staticmethod
    def load_data(report):
        print('testing load_data')

        unloaded_files = list(report.req_src_files)
        ReportUtilities.cwd = str(report.src_doc_path)
        ReportUtilities._bound_settings = report.settings['Header Formats']

        for f_name, path in ReportUtilities.loader(unloaded_files):
            file = ReportUtilities.open_excel(path)
            ReportUtilities.remove_sheets_per_settings(file)
            for sheet_name in reversed(file.sheet_names()):
                # Modify with mapped header stuff
                ReportUtilities.apply_header_filters(file.sheet_by_name(sheet_name))
                # Modify with mapped other stuff
                ReportUtilities.apply_body_filters(file.sheet_by_name(sheet_name))
                # yield book with basic modifications
            print(file)
        ReportUtilities._bound_settings = []
        ReportUtilities.cwd = None
        print('test complete')

    # TODO push this into ReportUtilities
    @staticmethod
    def loader(unloaded_files):
        for f_name in reversed(unloaded_files):
            src_f = glob(r'{f_path}*.*'.format(f_path=join(ReportUtilities.cwd, f_name)))
            if len(src_f) is 1:
                unloaded_files.remove(f_name)
            yield f_name, src_f[0]

    # TODO build out ReportUtility to open pe files for sheets/books
    @staticmethod
    def open_excel(f_name):
        try:
            return get_book(file_name=f_name)
        except OSError:
            print('OSError ->'
                  'cannot open {}'.format(f_name))

    @staticmethod
    def safe_div(num, denom):
        rtn_val = 0
        try:
            rtn_val = num / denom
        except ZeroDivisionError:
            pass
        return rtn_val

    # Generator Section
    @staticmethod
    def common_keys(*dcts):
        for i in set(dcts[0]).intersection(*dcts[1:]):
            yield (i,) + tuple(d[i] for d in dcts)

    @staticmethod
    def return_matches(*args, match_val=None):
        if len(args) == 2:
            shortest_list, longest_list = ReportUtilities.shortest_longest(*args)
            longest_list_indexed = {}
            for item in longest_list:
                longest_list_indexed[item[match_val]] = item
            for item in shortest_list:
                if item[match_val] in longest_list_indexed:
                    yield item, longest_list_indexed[item[match_val]]

    # Filter Section
    @staticmethod
    def header_filter(row_index, row):
        corner_case = split('\(| - ', row[0])
        bad_word = corner_case[0].split(' ')[0] not in ('Feature', 'Call', 'Event')
        # bad_word = corner_case[0].split(' ')[0] not in tuple(ReportUtilities.bound_settings)
        # bad_words = ReportUtilities.bound_settings
        return True if len(corner_case) > 1 else bad_word

    @staticmethod
    def blank_row_filter(row_index, row):
        result = [element for element in str(row[3]) if element != '']
        return len(result) == 0

    @staticmethod
    def answered_filter(row_index, row):
        try:
            answered = row[-5]
        except ValueError:
            answered = False
        return answered

    @staticmethod
    def inbound_call_filter(row_index, row):
        return row[0] not in ('Inbound', 'Call Direction')

    @staticmethod
    def zero_duration_filter(row_index, row):
        result = [element for element in row[-1] if element != '']
        return len(result) == 0

    @staticmethod
    def remove_internal_inbound_filter(row_index, row):
        return row[-2] == row[-3]

    @staticmethod
    def open_directory(tgt_dir):
        Popen('explorer "{0}"'.format(tgt_dir))
        input('Any key to continue.')
