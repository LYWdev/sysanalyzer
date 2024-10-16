import csv
import re

# 키워드 리스트 정의
keywords = ['flag', 'op', 'mode', 'opt', 'prot', 'option', 'which', 'who', 'whence','how']

def check_keywords_in_args(args):
    """
    주어진 인자 리스트에서 키워드가 있는지 확인하여 있으면 '있음', 없으면 '없음'을 반환
    """
    # 각 인자에서 키워드 검색을 위한 루프
    for arg in args:
        if arg:  # 빈 문자열이 아니면
            cleaned_arg = re.sub(r'[^\w\s]', '', arg)  # 특수 문자 제거 (ex: '...' 제거)
            for keyword in keywords:
                if keyword in cleaned_arg.lower():  # 대소문자 구분 없이 검색
                    return '있음'
    return '없음'

def analyze_syscall_data(input_file, output_file):
    """
    CSV 파일을 읽어서 각 syscall의 인자들을 분석하고 'flag유무' 열을 추가하여 결과를 저장
    """
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # 첫 줄(헤더)을 읽어서 'flag유무' 열 추가
        header = next(reader)
        header.append('flag유무')
        writer.writerow(header)

        # 각 행을 분석
        for row in reader:
            args = row[3:9]  # 인자들이 있는 열을 추출 (arg1 ~ arg6)
            flag_status = check_keywords_in_args(args)  # 인자들을 분석하여 flag 유무 확인
            row.append(flag_status)  # flag유무 결과 추가
            writer.writerow(row)  # 결과를 새로운 CSV 파일에 저장

# 파일 경로 설정
input_file = 'sysarg.csv'
output_file = 'syscall_arg_flag.csv'

# 함수 실행
analyze_syscall_data(input_file, output_file)

print(f"{output_file} 파일이 생성되었습니다.")
