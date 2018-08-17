#-*- coding: utf-8 -*-
import sqlite3
from prettytable import from_db_cursor

# 각 문제에 작성한 SQL 질의문을 아래의 변수들 안에 복사 붙여 넣기 하기 바랍니다.
# note: 변수 이름들을 바꾸지 맙시다.

Q1 = '''
#이 줄을 삭제하고 HW1.ipynb에서 작성한 SQL 질의문을 여기에 붙여 넣기 바랍니다.
'''

Q2 = '''

'''

Q3 = '''

'''

Q4 = '''

'''

Q5 = '''

'''

Q6 = '''

'''

Q7 = '''

'''

Q8 = '''

'''

Q9 = '''

'''

Q10 = '''

'''

#################################
#      이 이하는 수정하지 말 것       #
#################################

# 항공 운항 기록 데이터베이스 연결
def connect_database(database_path):
    global conn
    conn = sqlite3.connect(database_path)

def get_all_query_results(debug_print = True):
    all_results = []
    for q, idx in zip([Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10], range(1, 11)):
        result_strings = ("The result for Q%d was:\n%s\n\n" % (idx, from_db_cursor(conn.execute(q)))).splitlines()
        all_results.append(result_strings)
        if debug_print:
            for string in result_strings:
                print string
    return all_results

if __name__ == "__main__":
    connect_database('flights.db')
    query_results = get_all_query_results()