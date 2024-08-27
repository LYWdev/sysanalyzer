import os
import csv
import re
from collections import defaultdict

# 입력 파일과 출력 디렉토리 설정
input_file = "pgbench.csv"
arg_dir = 'arg'
flag_dir = 'flag'

# 플래그 패턴을 찾기 위한 정규 표현식
reObj = re.compile(r'[A-Z]+_[A-Z]+')

# 출력 디렉토리 생성 (존재하지 않으면 생성)
os.makedirs(arg_dir, exist_ok=True)
os.makedirs(flag_dir, exist_ok=True)

# 파일을 시스템 콜별로 분리하여 저장
with open(input_file, mode='r') as infile:
    reader = csv.reader(infile)
    
    # 첫 번째 줄(헤더)을 저장
    header = next(reader)
    
    # 딕셔너리로 파일 포인터 및 통계 관리
    file_pointers = {}
    syscall_stats = defaultdict(lambda: {"flag_counts": defaultdict(int), "flag_combination_counts": defaultdict(int)})

    for row in reader:
        syscall_name = row[2]  # 세 번째 열에 시스템 콜 이름이 있음
        
        # 시스템 콜별 파일 생성 및 파일 포인터 관리
        if syscall_name not in file_pointers:
            # 파일 이름에 사용될 수 없는 문자를 제거
            clean_syscall_name = re.sub(r'[^\w]', '_', syscall_name)
            arg_output_file = os.path.join(arg_dir, f"pgbench_{clean_syscall_name}.csv")
            flag_output_file = os.path.join(flag_dir, f"pgbench_{clean_syscall_name}_flag.csv")
            
            # 아규먼트 파일
            arg_outfile = open(arg_output_file, mode='w', newline='')
            arg_writer = csv.writer(arg_outfile)
            arg_writer.writerow(header)  # 헤더 추가
            
            # 플래그 파일
            flag_outfile = open(flag_output_file, mode='w', newline='')
            flag_writer = csv.writer(flag_outfile)
            file_pointers[syscall_name] = (arg_outfile, arg_writer, flag_outfile, flag_writer)
        
        # 해당 시스템 콜에 해당하는 파일에 데이터 추가
        arg_outfile, arg_writer, flag_outfile, flag_writer = file_pointers[syscall_name]

        # 각 행을 시스템 콜별로 파일에 기록
        arg_writer.writerow(row)

        # 플래그 카운트를 저장할 딕셔너리 가져오기
        flag_counts = syscall_stats[syscall_name]["flag_counts"]
        flag_combination_counts = syscall_stats[syscall_name]["flag_combination_counts"]

        def new_split(s, sep_list):
            temp_list = [s]
            for sep in sep_list:
                new_temp_list = []
                for x in temp_list:
                    s_list = x.split(sep)
                    new_temp_list.extend(s_list)
                temp_list = new_temp_list
            return temp_list
                
        # 각 행의 데이터를 처리하여 플래그 통계를 기록
        for item in row:
            item = item.strip()
            items = new_split(item, ['|', '(', ')', '='])
            
            flags = []
            for x in items:
                if reObj.match(x):
                    flag_counts[x] += 1
                    flags.append(x)
            if len(flags) >= 2:   
                flag_combination = '|'.join(sorted(flags))
                flag_combination_counts[flag_combination] += 1
        
    # 모든 시스템 콜에 대해 플래그 총합을 한 번에 기록
    for syscall_name, stats in syscall_stats.items():
        _, _, flag_outfile, flag_writer = file_pointers[syscall_name]
        flag_counts = stats["flag_counts"]
        flag_combination_counts = stats["flag_combination_counts"]
        
        if flag_counts or flag_combination_counts:
            flag_writer.writerow(["System Call Flag", "Count"])
            for flag, count in flag_counts.items():
                flag_writer.writerow([flag, count])
            
            flag_writer.writerow([])  # 빈 줄로 구분
            
            if flag_combination_counts:
                flag_writer.writerow(["Flag Combination", "Count"])
                for flag_combination, count in flag_combination_counts.items():
                    flag_writer.writerow([flag_combination, count])
            
            flag_writer.writerow([])  # 마지막에 빈 줄 추가

# 모든 파일 포인터 닫기
for arg_outfile, _, flag_outfile, _ in file_pointers.values():
    arg_outfile.close()
    flag_outfile.close()

print("Processing complete. Argument and flag files have been saved in the respective directories.")

