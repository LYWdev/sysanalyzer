# sysanalyzer
Nginx 성능 테스트 스크립트 설명 (bench.sh)
이 스크립트는 다양한 요청 유형 및 동시성 수준을 이용하여 Nginx 서버의 성능을 측정하는 도구입니다. Apache Benchmark (ab) 및 curl을 사용하여 HTTP 요청을 보내며, 결과에 따라 성공 여부를 확인하는 방식으로 동작합니다.

테스트 목록
1. 기본 성능 테스트 (1000개의 요청, 동시성 100)
기본적인 성능 테스트로 1000개의 요청을 100개의 동시 연결로 서버에 보내어 처리 속도를 측정합니다.

bash
코드 복사
ab -n 1000 -c 100 http://localhost:8080/
2. 동시성 감소 테스트 (1000개의 요청, 동시성 10)
동시성을 줄여 10개의 연결로 1000개의 요청을 처리하는 테스트입니다.

bash
코드 복사
ab -n 1000 -c 10 http://localhost:8080/
3. 요청 수 증가 테스트 (10000개의 요청, 동시성 100)
요청 수를 증가시켜 10000개의 요청을 100개의 동시 연결로 서버에 보내는 성능 테스트입니다.

bash
코드 복사
ab -n 10000 -c 100 http://localhost:8080/
4. Keep-Alive 활성화 테스트 (1000개의 요청, 동시성 100)
Keep-Alive를 활성화한 상태에서 1000개의 요청을 100개의 동시 연결로 처리합니다. Keep-Alive는 연결을 유지하여 성능을 향상시킵니다.

bash
코드 복사
ab -n 1000 -c 100 -k http://localhost:8080/
5. 대용량 파일 응답 테스트 (1000개의 요청, 동시성 50)
대용량 파일을 요청하는 시나리오로, 50개의 동시 연결로 1000개의 요청을 보냅니다.

bash
코드 복사
ab -n 1000 -c 50 http://localhost:8080/largefile
6. POST 요청 테스트 (1000개의 요청, 동시성 100)
POST 요청을 보내는 테스트로, 100개의 동시 연결로 1000개의 요청을 처리합니다.

bash
코드 복사
ab -n 1000 -c 100 -p post_data.txt -T 'application/x-www-form-urlencoded' http://localhost:8080/api/post
7. HTTPS 요청 테스트 (1000개의 요청, 동시성 100)
HTTPS를 사용하여 100개의 동시 연결로 1000개의 요청을 처리하는 테스트입니다.

bash
코드 복사
ab -n 1000 -c 100 https://localhost:8443/
8. 타임아웃 테스트 (1000개의 요청, 동시성 100, 5초 타임아웃)
요청 처리 시간에 5초의 타임아웃을 설정하여 100개의 동시 연결로 1000개의 요청을 보냅니다.

bash
코드 복사
ab -n 1000 -c 100 -s 5 http://localhost:8080/
9. 커스텀 헤더 테스트 (1000개의 요청, 동시성 100, 커스텀 헤더 사용)
Authorization 헤더를 사용하여 100개의 동시 연결로 1000개의 요청을 보내는 테스트입니다.

bash
코드 복사
ab -n 1000 -c 100 -H "Authorization: Bearer your_token" http://localhost:8080/
10. 세션 쿠키 테스트 (1000개의 요청, 동시성 100, 세션 쿠키 사용)
세션 쿠키를 포함하여 100개의 동시 연결로 1000개의 요청을 처리하는 테스트입니다.

bash
코드 복사
ab -n 1000 -c 100 -C "sessionid=abcd1234" http://localhost:8080/
11. PUT 요청 테스트 (1000개의 요청, 동시성 100)
PUT 요청을 보내는 테스트로, JSON 데이터를 포함하여 100개의 동시 연결로 1000개의 요청을 처리합니다.

bash
코드 복사
ab -n 1000 -c 100 -u -p put_data.txt -T 'application/json' http://localhost:8080/api/resource
12. DELETE 요청 테스트 (1000개의 요청, curl로 동시 처리)
curl을 이용하여 1000개의 DELETE 요청을 병렬로 처리하는 테스트입니다.

bash
코드 복사
for i in $(seq 1 1000); do
    curl -X DELETE http://localhost:8080/api/resource &
done
wait
13. PATCH 요청 테스트 (1000개의 요청, 동시성 100)
PATCH 요청을 JSON 데이터와 함께 보내는 테스트입니다. 100개의 동시 연결로 1000개의 요청을 처리합니다.

bash
코드 복사
ab -n 1000 -c 100 -X PATCH -p patch_data.txt -T 'application/json' http://localhost:8080/api/resource
