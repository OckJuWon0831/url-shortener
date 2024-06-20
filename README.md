# URL Shortener - Ock Ju Won

## DB 선택 이유

1. PostgreSQL
   DB 서버로서 MySQL을 사용하려고 했으나,

MySQL을 본 때 cryptography 패키지 오류가 발생하는 이유는 MySQL 서버가 기본적으로 사용하는 인증 방법 때문입니다. MySQL 8.0 이상에서는 caching_sha2_password 인증 방법이 기본적으로 사용되며, 이 방법은 안전하지만, 클라이언트 측에서 이를 지원하려면 cryptography 패키지가 필요합니다. cryptography 패키지는 Python에서 안전한 해시 함수와 기타 암호화 기능을 제공하는 패키지입니다.

PostgreSQL을 사용하면 이와 같은 오류가 발생하지 않습니다. PostgreSQL의 기본 인증 방법은 MD5이므로 Python 클라이언트에서 추가적인 패키지를 설치할 필요가 없습니다. 따라서, PostgreSQL을 사용하면 이러한 종류의 인증 문제를 피할 수 있습니다.
