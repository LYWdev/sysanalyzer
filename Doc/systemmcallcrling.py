import csv
import requests
from bs4 import BeautifulSoup

# 기본 URL 설정
base_url = "https://www.man7.org/linux/man-pages/man2/"

# CSV 파일에서 시스템 콜 이름 읽기
def read_syscall_names(csv_file):
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 헤더 건너뛰기
        return [row[0] for row in reader]  # 시스템 콜 이름만 리스트로 반환

# 각 시스템 콜 페이지에서 시놉시스 파싱
def parse_syscall_synopsis(syscall_name):
    url = f"{base_url}{syscall_name}.2.html"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to access {url}")
        return None

    # HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # SYNOPSIS 섹션 찾기
    pre_tag = soup.find('pre')
    if pre_tag:
        return pre_tag.get_text().strip()  # <pre> 태그 안의 텍스트 추출
    return None

# 시놉시스에서 시스템 콜 인자 추출
def extract_syscall_args(synopsis):
    # 시놉시스에서 함수 프로토타입과 인자를 추출
    lines = synopsis.splitlines()
    for line in lines:
        if '(' in line and ')' in line:  # 함수 선언을 포함하는 줄 찾기
            args_start = line.find('(')
            args_end = line.find(')')
            args_str = line[args_start + 1:args_end]
            args = [arg.strip() for arg in args_str.split(',')]
            return args
    return []

# 시스템 콜 시놉시스 및 인자를 CSV 파일로 저장
def save_syscall_summaries(syscall_summaries, output_csv='syscall_summaries.csv'):
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Syscall Name', 'Arg1', 'Arg2', 'Arg3', 'Arg4', 'Arg5', 'Arg6', 'Arg7', 'Arg8', 'Arg9', 'Arg10'])  # 헤더 작성

        # 각 시스템 콜의 인자를 CSV 파일에 저장
        for syscall_name, args in syscall_summaries.items():
            row = [syscall_name] + args + [''] * (10 - len(args))  # 최대 10개의 인자 저장, 부족하면 빈칸으로 채움
            writer.writerow(row)

# 실패한 시스템 콜을 CSV 파일로 저장
def save_failed_syscalls(failed_syscalls, failed_csv='failed_systemcall.csv'):
    with open(failed_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Syscall Name', 'Error Message'])  # 헤더 작성
        for syscall_name, error in failed_syscalls.items():
            writer.writerow([syscall_name, error])

# 메인 실행 함수
if __name__ == "__main__":
    # 시스템 콜 이름 CSV 파일 읽기
    syscall_names = read_syscall_names('syscall_names.csv')

    syscall_summaries = {}
    failed_syscalls = {}

    # 각 시스템 콜에 대해 시놉시스를 파싱하고 인자를 추출
    for syscall_name in syscall_names:
        print(f"Parsing {syscall_name}...")
        synopsis = parse_syscall_synopsis(syscall_name)
        if synopsis:
            args = extract_syscall_args(synopsis)
            syscall_summaries[syscall_name] = args
        else:
            failed_syscalls[syscall_name] = "Failed to parse synopsis or page not found"  # 실패한 경우

    # 파싱한 시스템 콜 정보를 CSV로 저장
    save_syscall_summaries(syscall_summaries)
    print("시스템 콜 요약이 syscall_summaries.csv에 저장되었습니다.")

    # 실패한 시스템 콜 정보를 CSV로 저장
    save_failed_syscalls(failed_syscalls)
    print("실패한 시스템 콜 정보가 failed_systemcall.csv에 저장되었습니다.")
