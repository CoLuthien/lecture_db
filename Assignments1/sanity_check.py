#-*-coding: utf-8 -*-
#!/usr/bin/env python

import sys
import os
import imp
import difflib
import itertools

DEFAULT_PATH = 'submit.py'
CORRECT_OUTPUT_PATH = 'correct_output.txt'
DATABASE_PATH = 'flights.db'

def main(argv):
    print "작성된 결과를 검사하는 스크립트입니다."
    print " 질의문을 실행하고 그 결과를 해답과 비교할 것입니다."
    print "SQL에 숫자를 삽입하여 답을 얻는 경우를 방지하기 위해"
    print "최종 결과물은 다른 데이터로 평가합니다."

    # 검사 스크립트의 경로를 확인 
    # 해답 파일도 같은 위치에 있을 것이라 가정함
    sanity_check_folder = os.path.dirname(os.path.realpath(__file__))

    # 제출한 파일의 경로를 확인
    submission = argv[1] if len(argv) > 1 else DEFAULT_PATH
    submissionPath = os.path.join(os.getcwdu(), submission)

    # 제시된 경로가 존재하고 파일인지 검사
    print("검사 중 '{}'...".format(submissionPath))
    if not os.path.isfile(submissionPath):
        print("ERROR: 파일 '{}'가 존재하지 않음.".format(submissionPath))
        return 1
    # 스크립트 형식으로 파일 불러오기.
    foo = imp.load_source('submit', submissionPath)

    # 데이터베이스 연결
    foo.connect_database(os.path.join(sanity_check_folder, DATABASE_PATH))
    results = foo.get_all_query_results(debug_print=False)

    # 문자열리스트의 리스트를 문자열 리스트로 변환
    # https://stackoverflow.com/questions/716477/join-list-of-lists-in-python
    listStrings = list(itertools.chain.from_iterable(results))

    # 해답 파일 읽기
    correctOutputStrings = None
    with open(os.path.join(sanity_check_folder, CORRECT_OUTPUT_PATH)) as f:
        correctOutputStrings = f.readlines()
    correctOutputStrings = [s.strip() for s in correctOutputStrings]

    # 두 파일 비교
    diff = difflib.ndiff(listStrings, correctOutputStrings)
    diffPrinted = False
    for s in diff:
        if s[0] == '-' or s[0] == '+':
            diffPrinted = True
        print s

    qwer =  foo.conn.execute(foo.Q7)
    for i in qwer:
        print i[0]


    # Q7의 예외, 이 부분은 자동은 안되고 위치를 검색하여 그 결과를 계산해보는 것으로 차이를 비교합니다.
    print "Q7의 답으로 %.2 내의 오차만 인정합니다. Q7의 답을 계산합니다..."
    q7correctAnswerIndex = correctOutputStrings.index("Q7의 결과는:")
    q7correctAnswer = float(correctOutputStrings[q7correctAnswerIndex+4][1:-1])
    q7query =  foo.conn.execute(foo.Q7)
    q7answer = q7query.fetchone()
    relativeDifference = abs(q7correctAnswer-q7answer[0])/q7correctAnswer
    print "Q7의 답이 %.8f 입니다. 해답은 %.8f. 입니다. 상대적 차이는 %f 입니다." % (q7answer[0], q7correctAnswer, relativeDifference)
    if relativeDifference < .002:
        print "Q7의 답이 오차 범위 내입니다. 에러 메시지는 무시하기 바랍니다."
    else:
        print "Q7의 답이 오차 범위 밖입니다. 다시 한 번 확인하기 바랍니다."


    # 에러 메시지 출력
    if diffPrinted:
        print "해답과 다름. 위의 비교 결과를 확인하여 옳은 질의문을 다시 작성하기 바랍니다."
        return 1
    else:
        print "결과가 좋습니다. 제출하기 바랍니다."

if __name__ == '__main__':
    sys.exit(main(sys.argv))
