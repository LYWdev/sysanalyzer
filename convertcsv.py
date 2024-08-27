import re
import csv

def parse_log_line(line):
    # 정규 표현식을 사용해 로그 라인에서 필요한 정보를 추출합니다.
    pattern = r'^(\d+)\s+([\d:.]+)\s+(\w+)\((.*?)\)\s+=\s+(.*)$'
    match = re.match(pattern, line)
    if match:
        pid = match.group(1)
        time = match.group(2)
        syscall = match.group(3)
        args = match.group(4)
        result = match.group(5)

        # 인자들을 쉼표로 분리하여 리스트로 변환
        args_list = split_args(args)

        return [pid, time, syscall] + args_list + [result]
    else:
        return None

def split_args(args):
    args = args.strip()
    result = []
    current = ''
    bracket_level = 0
    in_quote = False
    i = 0
    while i < len(args):
        char = args[i]
        if char == '"':
            in_quote = not in_quote
            current += char
        elif char == '[' and not in_quote:
            bracket_level += 1
            current += char
        elif char == ']' and not in_quote:
            bracket_level -= 1
            current += char
        elif char == ',' and not in_quote and bracket_level == 0:
            result.append(current.strip())
            current = ''
        else:
            current += char
        i += 1
    if current:
        result.append(current.strip())
    return result

def main():
    log_file = 'pgbench.log'
    csv_file = 'pgbench.csv'

    max_args = 0

    # 파일을 한 줄씩 읽어가며 처리
    with open(log_file, 'r') as log_f, open(csv_file, 'w', newline='') as csv_f:
        writer = csv.writer(csv_f)

        for line in log_f:
            parsed_line = parse_log_line(line)
            if parsed_line:
                args_count = len(parsed_line) - 4  # PID, 시간, 시스템 콜, 결과 제외
                if args_count > max_args:
                    max_args = args_count

        # 헤더 생성
        headers = ['PID', 'Time', 'System Call']
        for i in range(1, max_args + 1):
            headers.append(f'Arg{i}')
        headers.append('Result')

        # 헤더 작성
        writer.writerow(headers)

        # 다시 파일을 읽으면서 파싱한 데이터를 CSV에 기록
        log_f.seek(0)
        for line in log_f:
            parsed_line = parse_log_line(line)
            if parsed_line:
                # 부족한 인자는 빈 문자열로 채움
                row = parsed_line[:3] + parsed_line[3:-1] + [''] * (max_args - (len(parsed_line) - 4)) + [parsed_line[-1]]
                writer.writerow(row)

if __name__ == "__main__":
    main()

