import csv
import re

def convert_log_to_csv(input_file, output_file):
    with open(input_file, 'r') as log_file, open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # 헤더 설정
        header = ["sysnumber", "rtnvalue", "sysname", "arg1", "arg2", "arg3", "arg4", "arg5", "arg6"]
        writer.writerow(header)

        # 로그 파일의 각 줄을 처리
        for line in log_file:
            # 정규식을 사용하여 각 요소를 추출
            # 반환값에 *이 포함된 경우와 함수명을 정확하게 분리
            # 인자에 특수 문자가 포함될 수 있도록 유연한 정규식 적용
            match = re.match(r'(\d+)\s+([a-zA-Z_]+(?:\s*\*?)?)\s+(\w+)\((.*)\);', line)
            if match:
                sysnumber = match.group(1)  # 시스템 호출 번호
                rtnvalue = match.group(2).strip()   # 반환값 (예: void *, int 등)
                sysname = match.group(3)    # 시스템 호출 이름
                arguments = match.group(4)  # 인자들

                # 괄호 안에 있는 인자들을 처리
                args = []
                current_arg = ""
                depth = 0  # 괄호 깊이 추적

                for char in arguments:
                    if char == ',' and depth == 0:  # 괄호 밖에서 ,는 인자 구분자로 처리
                        args.append(current_arg.strip())
                        current_arg = ""
                    else:
                        current_arg += char
                        if char == '(':
                            depth += 1
                        elif char == ')':
                            depth -= 1

                if current_arg:  # 마지막 인자 추가
                    args.append(current_arg.strip())

                # 출력할 행을 준비 (최대 6개의 인자만 기록)
                row = [sysnumber, rtnvalue, sysname] + args[:6]

                # 부족한 인자 자리를 None으로 채움
                while len(row) < 9:
                    row.append(None)

                # CSV 파일에 행 작성
                writer.writerow(row)

input_file = "tes.log"
output_file = "syscall_data.csv"
convert_log_to_csv(input_file, output_file)

print(f"CSV 파일 {output_file}가 생성되었습니다.")
