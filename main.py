import oci
import base64
import os
from dotenv import load_dotenv
from oci.key_management import KmsCryptoClient
from oci.key_management.models import EncryptDataDetails

def main():
  load_dotenv()

  # 사용자 환경에 맞게 수정
  key_id = os.environ.get("KEY_ID") # master_key_id와 동일
  data_to_encrypt_bytes = b"This is a secret message"

  # OCI 인증 정보 로드 (기본 config 파일 사용)
  config = oci.config.from_file()

  # KMS Crypto Client 생성
  # service_endpoint는 config 파일의 region 정보를 사용하여 자동 구성될 수 있습니다.
  # 명시적으로 지정하려면 vault의 crypto endpoint를 사용하세요.
  # 예: service_endpoint="https://<vault_id>-crypto.kms.<region>.oci.oraclecloud.com"
  service_endpoint = os.environ.get("SERVICE_ENDPOINT")
  crypto_client = KmsCryptoClient(config, service_endpoint=service_endpoint)

  # 암호화할 데이터를 base64로 인코딩
  data_to_encrypt_base64 = base64.b64encode(data_to_encrypt_bytes).decode('utf-8')

  # 암호화 요청 상세 정보 생성
  encrypt_details = EncryptDataDetails(
      key_id=key_id,
      plaintext=data_to_encrypt_base64
  )

  # 암호화 수행
  encrypt_response = crypto_client.encrypt(encrypt_details)

  # 암호화된 데이터는 encrypt_response.data.ciphertext에 저장됨
  print("Encrypted data (base64):", encrypt_response.data.ciphertext)

if __name__ == "__main__":
    main()
