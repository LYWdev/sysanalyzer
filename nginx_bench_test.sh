syz@benctest:~/nginxlog$ cat bench.sh 
#!/bin/bash

# Define the base URL
URL="http://localhost:8080/"

# Function to check if the previous command was successful
check_success() {
  if [ $? -ne 0 ]; then
    echo "Test failed: $1"
  else
    echo "Test succeeded: $1"
  fi
}

# Test 1: ???? ?????? (1000 requests, 100 concurrency)
echo "Running basic test with 1000 requests and 100 concurrency..."
ab -n 1000 -c 100 $URL
check_success "Basic test"

# Test 2: ???? ???? ???? 10???? ???? ?????? (1000 requests, 10 concurrency)
echo "Running test with 1000 requests and 10 concurrency..."
ab -n 1000 -c 10 $URL
check_success "Reduced concurrency test"

# Test 3: ???? ???? 10,000???? ???? ?????? (10000 requests, 100 concurrency)
echo "Running test with 10000 requests and 100 concurrency..."
ab -n 10000 -c 100 $URL
check_success "Increased requests test"

# Test 4: Keep-Alive ?????? ?????? (1000 requests, 100 concurrency, Keep-Alive)
echo "Running test with Keep-Alive enabled (1000 requests and 100 concurrency)..."
ab -n 1000 -c 100 -k $URL
check_success "Keep-Alive test"

# Test 5: ?? ???? ???? ?????? (1000 requests, 50 concurrency)
echo "Running large file test with 1000 requests and 50 concurrency..."
ab -n 1000 -c 50 ${URL}largefile
check_success "Large file response test"

# Test 6: POST ???? ?????? (1000 requests, 100 concurrency)
echo "Running POST request test with 1000 requests and 100 concurrency..."
ab -n 1000 -c 100 -p post_data.txt -T 'application/x-www-form-urlencoded' ${URL}api/post
check_success "POST request test"

# Test 7: HTTPS ???? ?????? (1000 requests, 100 concurrency)
echo "Running HTTPS test with 1000 requests and 100 concurrency..."
ab -n 1000 -c 100 https://localhost:8443/
check_success "HTTPS request test"

# Test 8: ???????? ?????? (1000 requests, 100 concurrency, 5?? ????????)
echo "Running test with 5 second timeout (1000 requests and 100 concurrency)..."
ab -n 1000 -c 100 -s 5 $URL
check_success "Timeout test"

# Test 9: ???? ?????? ???? ?????? (1000 requests, 100 concurrency, with custom headers)
echo "Running test with custom headers (1000 requests and 100 concurrency)..."
ab -n 1000 -c 100 -H "Authorization: Bearer your_token" $URL
check_success "Custom headers test"

# Test 10: ???? ?????? ?????? ???? ?????? (1000 requests, 100 concurrency, with session cookie)
echo "Running test with session cookie (1000 requests and 100 concurrency)..."
ab -n 1000 -c 100 -C "sessionid=abcd1234" $URL
check_success "Session cookie test"

# Test 11: PUT ???? ?????? (1000 requests, 100 concurrency)
echo "Running PUT request test with 1000 requests and 100 concurrency..."
ab -n 1000 -c 100 -u -p put_data.txt -T 'application/json' ${URL}api/resource
check_success "PUT request test"

# Test 12: DELETE ???? ?????? (1000 requests, ???? ????)
echo "Running DELETE request test with 1000 requests (parallel with curl)..."
for i in $(seq 1 1000); do
    curl -X DELETE ${URL}api/resource &  # curl?? ???????????? ???????? ???? ????
done
wait  # ???? ???? ?????? ???? ?????? ????
check_success "DELETE request test with curl"

# Test 13: PATCH ???? ?????? (1000 requests, 100 concurrency)
echo "Running PATCH request test with 1000 requests and 100 concurrency..."
ab -n 1000 -c 100 -X PATCH -p patch_data.txt -T 'application/json' ${URL}api/resource
check_success "PATCH request test"

echo "All tests completed."

