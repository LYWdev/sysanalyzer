# sysanalyzer


## Nginx 성능 테스트 스크립트 설명 (bench.sh)
이 스크립트는 다양한 요청 유형 및 동시성 수준을 이용하여 Nginx 서버의 성능을 측정하는 도구입니다. Apache Benchmark (ab) 및 curl을 사용하여 HTTP 요청을 보내며, 결과에 따라 성공 여부를 확인하는 방식으로 동작합니다.
이 스크립트는 ApacheBench(ab)와 curl을 사용하여 웹 서버의 성능을 다양한 시나리오에서 테스트합니다. 총 13개의 테스트로 구성되어 있으며, 각 테스트는 다른 요청 수, 동시 연결 수, HTTP 메서드 및 기타 옵션을 사용합니다.

스크립트 내용 요약

이 코드의 동작은 다음과 같다:

기본 설정을 한다:

URL 변수에 기본 URL인 http://localhost:8080/를 설정한다.

이전 명령의 성공 여부를 확인하는 함수 check_success를 정의한다.

테스트를 수행한다:

테스트 1: 1000개의 요청과 100개의 동시 연결로 기본 성능 테스트를 수행한다.

테스트 2: 동시 연결 수를 10으로 줄여 1000개의 요청을 테스트한다.

테스트 3: 요청 수를 10,000개로 늘려 100개의 동시 연결로 테스트한다.

테스트 4: Keep-Alive 옵션을 사용하여 1000개의 요청과 100개의 동시 연결로 테스트한다.

테스트 5: 대용량 파일에 대해 1000개의 요청과 50개의 동시 연결로 테스트한다.

테스트 6: post_data.txt를 사용하여 POST 요청을 1000개, 100개의 동시 연결로 테스트한다.

테스트 7: HTTPS 프로토콜로 1000개의 요청과 100개의 동시 연결로 테스트한다.

테스트 8: 타임아웃을 5초로 설정하여 1000개의 요청과 100개의 동시 연결로 테스트한다.

테스트 9: 커스텀 헤더(Authorization: Bearer your_token)를 포함하여 1000개의 요청과 100개의 동시 연결로 테스트한다.

테스트 10: 세션 쿠키(sessionid=abcd1234)를 사용하여 1000개의 요청과 100개의 동시 연결로 테스트한다.

테스트 11: put_data.txt를 사용하여 PUT 요청을 1000개, 100개의 동시 연결로 테스트한다.

테스트 12: curl로 DELETE 요청을 병렬 실행하여 1000개의 요청을 수행한다.

테스트 13: patch_data.txt를 사용하여 PATCH 요청을 1000개, 100개의 동시 연결로 테스트한다.

결과를 확인한다:

각 테스트 후 check_success 함수를 호출하여 테스트의 성공 여부를 출력한다.

마무리한다:

모든 테스트가 완료되면 "All tests completed."를 출력한다.

이 스크립트는 ApacheBench(ab)와 curl을 사용하여 다양한 시나리오에서 웹 서버의 성능과 안정성을 테스트한다.
