# -*- coding: utf-8 -*-
'''
created by David Cho(csi00700@gmail.com)
'''
import requests

import ast
import gspread
import json
from oauth2client.client import AccessTokenCredentials
'''
# 도움말 https://github.com/burnash/gspread
'''


def getAuth(fn):
    with open(fn, 'r') as fp:
        authobj = json.load(fp)
    return authobj


def authenticate_google_docs_from_file(fn='token.json'):
    with open(fn, 'r') as fp:
        token_info = fp.read()
    return authenticate_google_docs(token_info)


def authenticate_google_docs(token_info):
    '''
    :params str token_info - json_string
    '''
    authobj = json.loads(token_info)
    data = {
        'refresh_token': authobj['refresh_token'],
        'client_id': authobj['client_id'],
        'client_secret': authobj['client_secret'],
        'grant_type': 'refresh_token',
    }
    r = requests.post('https://accounts.google.com/o/oauth2/token', data=data)
    gc = gspread.authorize(AccessTokenCredentials(
        ast.literal_eval(r.text)['access_token'], 'Test'))
    return gc


class GSWorker:
    # https://docs.google.com/spreadsheets/d/1PouSRYV6NpTalJeHK9W7bXolw7mfEQ_AyXSKZmrgLUc/edit?usp=sharing

    def __init__(self, filekey="1lxXZoMbNE7RA9fRhtYU-SuxMv-wAkL2k2KfpYHFXAGg", token_fn=None, token_string=None):
        if token_fn is not None:
            gc = authenticate_google_docs_from_file(fn=token_fn)
        elif token_string is not None:
            gc = authenticate_google_docs(token_string)

        self.document = gc.open_by_key(filekey)

    def addWorkSheet(self, title):
        self.document.add_worksheet(title, 200, 150)

    def get_row(self, row):
        '''row에 해당하는 데이타를 모두 불러옴
        :param int to_col 몇번 째 컬럼 까지 불러올지2
        '''
        sheet = self.document.worksheet("Sheet1")
        return sheet.row_values(row)

    def get_all_values(self):
        return self.document.sheet1.get_all_values()

    def insert_row(self, row_data_json):
        row_data = json.loads(row_data_json)
        print("-->", row_data)

        try:
            sheet = self.document.worksheet("Sheet1")
            keyList = sheet.row_values(1)
            print("keyList:", keyList)

            # for key, value in row_data.items():
            ordered_values = list()
            for key in keyList:
                if key in row_data:
                    ordered_values.append(row_data[key])
                else:
                    ordered_values.append("")
            sheet.append_row(ordered_values)
            return True
        except Exception as err:
            print(err)
            return False
