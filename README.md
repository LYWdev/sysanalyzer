# sysanalyzer


## Nginx 성능 테스트 스크립트 설명 (bench.sh)
이 스크립트는 다양한 요청 유형 및 동시성 수준을 이용하여 Nginx 서버의 성능을 측정하는 도구입니다. Apache Benchmark (ab) 및 curl을 사용하여 HTTP 요청을 보내며, 결과에 따라 성공 여부를 확인하는 방식으로 동작합니다.
이 스크립트는 ApacheBench(ab)와 curl을 사용하여 웹 서버의 성능을 다양한 시나리오에서 테스트합니다. 총 13개의 테스트로 구성되어 있으며, 각 테스트는 다른 요청 수, 동시 연결 수, HTTP 메서드 및 기타 옵션을 사용합니다.

스크립트 내용 요약
기본 설정
기본 URL 설정: URL="http://localhost:8080/"
함수 정의
check_success 함수: 이전 명령어의 성공 여부를 확인하여 테스트의 성공 또는 실패를 출력합니다.
테스트 목록
기본 테스트

설명: 1000개의 요청을 100개의 동시 연결로 전송합니다.
명령어:
bash
코드 복사
ab -n 1000 -c 100 $URL
동시성 감소 테스트

설명: 1000개의 요청을 10개의 동시 연결로 전송합니다.
명령어:
bash
코드 복사
ab -n 1000 -c 10 $URL
요청 수 증가 테스트

설명: 10000개의 요청을 100개의 동시 연결로 전송합니다.
명령어:
bash
코드 복사
ab -n 10000 -c 100 $URL
Keep-Alive 테스트

설명: Keep-Alive 옵션을 사용하여 1000개의 요청을 100개의 동시 연결로 전송합니다.
명령어:
bash
코드 복사
ab -n 1000 -c 100 -k $URL
대용량 파일 응답 테스트

설명: 대용량 파일에 대해 1000개의 요청을 50개의 동시 연결로 전송합니다.
명령어:
bash
코드 복사
ab -n 1000 -c 50 ${URL}largefile
POST 요청 테스트

설명: POST 데이터를 전송하여 1000개의 요청을 100개의 동시 연결로 전송합니다.
명령어:
bash
코드 복사
ab -n 1000 -c 100 -p post_data.txt -T 'application/x-www-form-urlencoded' ${URL}api/post
HTTPS 요청 테스트

설명: HTTPS 프로토콜을 사용하여 1000개의 요청을 100개의 동시 연결로 전송합니다.
명령어:
bash
코드 복사
ab -n 1000 -c 100 https://localhost:8443/
타임아웃 설정 테스트

설명: 타임아웃을 5초로 설정하여 1000개의 요청을 100개의 동시 연결로 전송합니다.
명령어:
bash
코드 복사
ab -n 1000 -c 100 -s 5 $URL
커스텀 헤더 테스트

설명: Authorization 헤더를 추가하여 1000개의 요청을 100개의 동시 연결로 전송합니다.
명령어:
bash
코드 복사
ab -n 1000 -c 100 -H "Authorization: Bearer your_token" $URL
세션 쿠키 테스트

설명: 세션 쿠키를 포함하여 1000개의 요청을 100개의 동시 연결로 전송합니다.
명령어:
bash
코드 복사
ab -n 1000 -c 100 -C "sessionid=abcd1234" $URL
PUT 요청 테스트

설명: PUT 메서드를 사용하여 1000개의 요청을 100개의 동시 연결로 전송합니다.
명령어:
bash
코드 복사
ab -n 1000 -c 100 -X PUT -p put_data.txt -T 'application/json' ${URL}api/resource
DELETE 요청 테스트 (curl 사용)

설명: curl을 사용하여 1000개의 DELETE 요청을 병렬로 전송합니다.
명령어:
bash
코드 복사
for i in $(seq 1 1000); do
    curl -X DELETE ${URL}api/resource &
done
wait
PATCH 요청 테스트

설명: PATCH 메서드를 사용하여 1000개의 요청을 100개의 동시 연결로 전송합니다.
명령어:
bash
코드 복사
ab -n 1000 -c 100 -X PATCH -p patch_data.txt -T 'application/json' ${URL}api/resource
테스트 결과
각 테스트 후에는 check_success 함수를 통해 해당 테스트의 성공 또는 실패 여부가 출력됩니다. 모든 테스트가 완료되면 "All tests completed."라는 메시지가 표시됩니다.

사용 방법
스크립트를 실행하기 전에 실행 권한을 부여합니다:
bash
코드 복사
chmod +x bench.sh
스크립트를 실행합니다:
bash
코드 복사
./bench.sh
각 테스트의 결과를 확인하고 필요한 경우 서버 설정을 조정합니다.
주의 사항
스크립트를 실행하기 전에 서버가 실행 중인지 확인하세요.
post_data.txt, put_data.txt, patch_data.txt와 같은 데이터 파일이 존재해야 합니다.
HTTPS 테스트를 위해서는 로컬 서버에 SSL 설정이 필요합니다.
과도한 요청은 서버에 부하를 줄 수 있으므로 테스트 환경에서 실행하시기 바랍니다.