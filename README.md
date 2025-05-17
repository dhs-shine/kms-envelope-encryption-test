# KMS 봉투암호화(Envelope Encryption) 예제

## OCI KMS 봉투암호화(Envelope Encryption) 예제

이 프로젝트는 Oracle Cloud Infrastructure(OCI)의 Key Management Service(KMS)를 사용하여 봉투암호화를 구현한 예제입니다.

## 사전 요구사항

- OCI 계정 및 KMS 서비스 접근 권한
- OCI CLI가 설치되어 있어야 함

## 설치

1. 필요한 패키지 설치:
```bash
pip install oci python-dotenv cryptography
```

2. OCI 설정:
   - OCI CLI를 사용하여 config 파일 생성:
   ```bash
   oci setup config
   ```
   - 또는 수동으로 `~/.oci/config` 파일 생성:
   ```ini
   [DEFAULT]
   user=ocid1.user.oc1..aaaaaaaae3hml2bvw3rdapg7fwthakthywvzbr3xpken73fjkfo52bhfktoa
   fingerprint=70:93:99:8e:54:86:c4:7f:e1:dc:bc:bc:68:ac:dc:80
   tenancy=ocid1.tenancy.oc1..aaaaaaaaxkrxm2yiwzstzjxhakolvxblsd4nud5czmhnhmaw2yep4f6nx7oq
   region=ap-seoul-1
   key_file=/home/ubuntu/.oci/private.pem
   ```

3. 환경 변수 설정:
   - `.env` 파일 생성:
   ```
   OCI_KMS_KEY_ID=<your_key_id>
   OCI_KMS_CRYPTO_ENDPOINT=<your_kms_endpoint>
   ```
   - `OCI_KMS_KEY_ID`: OCI KMS에서 생성한 마스터 키의 ID (예: ocid1.key.oc1.ap-seoul-1.aaaaaaaaxxxxxx)
   - `OCI_KMS_CRYPTO_ENDPOINT`: OCI KMS의 암호화 서비스 엔드포인트 URL (예: https://<vault_id>-crypto.kms.<region>.oci.oraclecloud.com)

## 사용 방법

1. 스크립트 실행:
```bash
python main-oci.py
```

2. 출력 결과:
   - 원본 텍스트 크기
   - 암호화 소요 시간
   - 암호화된 데이터 크기
   - 복호화 소요 시간
   - 복호화된 데이터 크기
   - 원본과 복호화된 텍스트 비교 결과

## 주요 기능

- DEK(Data Encryption Key) 생성
- AES-256-GCM을 사용한 데이터 암호화
- 봉투암호화 구현 (암호화된 데이터 + 암호화된 DEK)
- 비동기 처리로 성능 최적화

## 보안 참고사항

- 마스터 키는 OCI KMS에서 안전하게 관리
- DEK는 메모리에서만 사용되고 암호화된 형태로만 저장
- 모든 암호화 작업은 AES-256-GCM으로 수행되어 인증된 암호화 제공

## AWS

AWS KMS를 사용한 봉투 암호화 예제는 다음과 같습니다.

## 사전 요구사항 (AWS)

- AWS 계정 및 KMS 서비스 접근 권한
- AWS CLI가 설치되어 있어야 함

## 설치 (AWS)

1. 필요한 패키지 설치:
```bash
pip install boto3 python-dotenv cryptography
```

2. AWS 설정:
   - AWS CLI를 사용하여 config 파일 생성:
   ```bash
   aws configure
   ```
   - 또는 수동으로 `~/.aws/config` 파일 생성:
   ```ini
   [default]
   region = ap-northeast-2
   output = json
   ```

3. 환경 변수 설정:
   - `.env` 파일 생성:
   ```
   AWS_KMS_KEY_ID=<your_kms_key_id>
   ```
   - `AWS_KMS_KEY_ID`: AWS KMS에서 생성한 키의 ID (예: arn:aws:kms:ap-northeast-2:xxxxxxxxxxxx:key/xxxxxxxxxxxxxxxxxxxxxxxxxxxxx)

## 사용 방법 (AWS)

1. 스크립트 실행:
```bash
python main-aws.py
```

2. 출력 결과:
   - 원본 텍스트 크기
   - 암호화 소요 시간
   - 암호화된 데이터 크기
   - 복호화 소요 시간
   - 복호화된 데이터 크기
   - 원본과 복호화된 텍스트 비교 결과

## 주요 기능 (AWS)

- DEK(Data Encryption Key) 생성
- AES-256-GCM을 사용한 데이터 암호화
- 봉투암호화 구현 (암호화된 데이터 + 암호화된 DEK)
- 비동기 처리로 성능 최적화

## 보안 참고사항 (AWS)

- 마스터 키는 AWS KMS에서 안전하게 관리
- DEK는 메모리에서만 사용되고 암호화된 형태로만 저장
- 모든 암호화 작업은 AES-256-GCM으로 수행되어 인증된 암호화 제공