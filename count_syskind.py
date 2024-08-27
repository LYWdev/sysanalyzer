import re
import csv
from collections import defaultdict

# 시스템 호출 이름이 올바른지 확인하기 위한 정규 표현식
syscall_re = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

# 입력 파일 및 출력 파일 설정
input_file = "pgbench.log"
anomaly_log_file = "anomalylog.txt"
output_csv_file = "syskind_count.csv"

# 시스템 콜 이름별 카운트를 저장할 딕셔너리 초기화
syscall_counts = defaultdict(int)

# 로그 파일을 읽고 시스템 콜 이름별로 카운트를 계산 및 검증
with open(input_file, mode='r') as infile, open(anomaly_log_file, mode='w') as anomaly_file:
    for line_number, line in enumerate(infile, 1):  # line_number는 1부터 시작
        # 로그 형식에 따라 시스템 콜 이름을 추출
        parts = line.split()
        if len(parts) > 2:
            syscall_name = parts[2].split('(')[0]
            
            # 시스템 콜 이름이 유효한지 검증
            if syscall_re.match(syscall_name):
                syscall_counts[syscall_name] += 1
            else:
                anomaly_file.write(f"Invalid syscall name found: '{syscall_name}' on line {line_number}: {line}\n")
        else:
            # parts가 2개 이하인 경우, 잘못된 로그 행으로 간주하고 anomalylog에 기록
            anomaly_file.write(f"Malformed line on line {line_number}: {line}\n")

# syskind_count.csv 파일에 시스템 콜 별 사용 횟수를 저장
with open(output_csv_file, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Syscall Name', 'Count'])  # 헤더 작성
    for syscall_name, count in syscall_counts.items():
        writer.writerow([syscall_name, count])

print("Validation complete. Check the anomalylog.txt file for details.")
print(f"System call counts saved to {output_csv_file}.")

