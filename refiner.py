# 파일 경로 설정
input_file = "mongo_docker.log"
output_file = "refined_mongo_docker.log"

# 파일 읽기 및 처리
with open(input_file, "r") as file:
    lines = file.readlines()

# 특정 문자열을 포함하는 행을 제외하고 저장
with open(output_file, "w") as file:
    for line in lines:
        if "<unfinished ...>" not in line and "resumed" not in line:
            file.write(line)

print(f"Filtered log has been saved to {output_file}")
