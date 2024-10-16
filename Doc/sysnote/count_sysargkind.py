import csv
from collections import Counter, defaultdict

def analyze_syscall_args(csv_file):
    # 각 인자(arg)의 종류별로 시스템 콜 개수를 카운트하기 위한 사전 생성
    arg_counters = defaultdict(Counter)

    # CSV 파일 읽기
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)

        # 각 시스템 콜의 인자를 분석
        for row in reader:
            for i in range(1, 7):  # arg1부터 arg6까지
                arg_key = f'arg{i}'
                arg_value = row[arg_key].strip()
                if arg_value:  # 인자가 비어있지 않으면 처리
                    arg_counters[arg_key][arg_value] += 1

    # 분석 결과 출력
    for arg_key, counter in arg_counters.items():
        print(f"\n{arg_key}에는 총 {len(counter)}가지의 종류가 있습니다:")
        for arg_type, count in counter.items():
            print(f"  '{arg_type}': {count}개의 시스템 콜에서 사용됨")

# 파일 경로
csv_file = 'syscall_data.csv'

# 함수 호출
analyze_syscall_args(csv_file)

