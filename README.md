# URL 단축 서비스 구현 - 옥주원

### 1️⃣ 개요

사용자가 구현된 API 서버에 인터넷 주소와 만료 시간(초)를 Request body에 포함하여 요청을 보내면, 그에 맞게 단축된 주소를 받아 접속할 수 있는 FastAPI 기반 서비스입니다.

### 2️⃣ 접속 방법

> ⭐️ API Swagger 문서는 프로젝트에 종속하여 작성했습니다.

1. `git clone https://github.com/OckJuWon0831/url-shortener` 으로 프로젝트를 로컬환경으로 불러옵니다.
2. `sh init.sh`로 설정값들과 이용할 도커 컨테이너들을 초기화합니다.
3. `http://localhost:8000/` 로 접속합니다.

- API 서버에 Request를 보내고 Response를 받은 일련의 과정들은 Postman을 사용하여 수행했습니다.

### 3️⃣ 프로젝트 설명

1. 데이터베이스로는 PostgreSQL과 Redis를 사용하였습니다. Redis를 통해, 단축 URL의 접속 기록을 cache값에 저장하도록 하였고, 이를 통해, 좀 더 효율적이고 빠른 시간 내에 유저의 리다이렉션 횟수를 구할 수 있게 하였습니다. RDBMS에 계속하여 쿼리를 날리는 것은 지금 당장 서비스를 이용하는 사용자들이 적을때에는 큰 문제가 되지 못한다고 생각했으나, 회원수가 많을때를 염두하여 이렇게 설계하였습니다.

2. 사용자가 단축한 주소와 함께 보낸 만료 시간이 지나면, DB에 삭제하는 쿼리를 보내도록 하여, 접속하지 못하게 했습니다.

3. 단축키를 만들기 위한 알고리즘은 파이썬의 빌트인 함수인 secret을 사용하였습니다. 데이터베이스에 생성된 키와 똑같은 값이 있는지 확인하는 로직을 넣어 중복되는 경우를 피하도록 하였습니다.

4. 통계 엔드포인트에 접속하면, 단축 URL에 접속한 통계값을 확인할 수 있게 했습니다.

5. 본 프로젝트를 수행하며, MySQL을 사용하려고 했습니다. 하지만, 개발도중
   cryptography 패키지 오류가 발생하였고, MySQL 서버가 기본적으로 사용하는 인증 방법 때문이라는 것을 알게되었습니다. MySQL 8.0 이상에서는 caching_sha2_password 인증 방법이 기본적으로 사용되며, 이 방법은 안전하지만, 클라이언트 측에서 이를 지원하려면 cryptography 패키지가 필요합니다. 반면에, PostgreSQL을 사용하면 이와 같은 오류가 발생하지 않았습니다. PostgreSQL의 기본 인증 방법은 MD5이므로 Python 클라이언트에서 추가적인 패키지를 설치할 필요가 없습니다. 따라서, PostgreSQL을 사용하면 이러한 종류의 인증 문제를 피할 수 있었습니다.

   서비스의 규모 혹은 종류에 따라 보안에 대하여 어떤 해싱 알고리즘이 적합한지 고민할 필요가 있다고 생각하지만, MD5나 SHA2 모두, 본 프로젝트에서는 안전하다 느껴 개발환경 설정이 수월한 PostgreSQL를 이용하기로 결정했습니다.

### 🚀 개발 기한

> 과제 README.md에 명시된 제출 기한에 맞게 6월 17일부터 6월 22일까지 개발 후 이메일을 통해 제출하였습니다.
