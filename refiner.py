import os

input_file = "strace_gvisor"
output_file = "strace_gvisor_refined"
chunk_size = 1024 * 1024 * 50000  #50000 *1MB 청크 단위

# 청크 단위로 파일을 처리
with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
    while True:
        # 청크 단위로 읽어들임
        lines = f_in.readlines(chunk_size)
        if not lines:
            break

        # 조건에 맞는 라인만 출력
        for line in lines:
            if "<unfinished ...>" not in line and "resumed" not in line:
                f_out.write(line)

print(f"Filtered log has been saved to {output_file}")

