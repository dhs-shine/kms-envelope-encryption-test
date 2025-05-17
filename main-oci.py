import oci
import os
import asyncio
import base64
from dotenv import load_dotenv
from common import KMSClient, main

class OCIKMSClient(KMSClient):
    def __init__(self, config, service_endpoint):
        self.config = config
        self.service_endpoint = service_endpoint
        self.crypto_client = oci.key_management.KmsCryptoClient(
            config,
            service_endpoint=service_endpoint
        )

    async def generate_dek(self, key_id: str):
        """OCI KMS를 사용하여 DEK 생성 및 암호화"""
        generate_dek_details = oci.key_management.models.GenerateKeyDetails(
            key_id=key_id,
            key_shape=oci.key_management.models.KeyShape(
                algorithm="AES",
                length=32  # 32 bytes = 256 bits
            ),
            include_plaintext_key=True
        )
        generate_dek_response = await asyncio.to_thread(
            self.crypto_client.generate_data_encryption_key,
            generate_dek_details
        )
        # ciphertext를 bytes로 변환
        return base64.b64decode(generate_dek_response.data.ciphertext), base64.b64decode(generate_dek_response.data.plaintext)

    async def decrypt(self, ciphertext: str, key_id: str):
        """OCI KMS를 사용하여 DEK 복호화"""
        decrypt_details = oci.key_management.models.DecryptDataDetails(
            ciphertext=ciphertext,
            key_id=key_id
        )
        decrypt_response = await asyncio.to_thread(
            self.crypto_client.decrypt,
            decrypt_details
        )
        return base64.b64decode(decrypt_response.data.plaintext)

async def amain():
    load_dotenv()
    
    # OCI 설정 로드
    config = oci.config.from_file()
    
    # KMS 서비스 엔드포인트와 키 ID
    service_endpoint = os.environ.get('OCI_KMS_CRYPTO_ENDPOINT')
    if not service_endpoint:
        raise ValueError("OCI_KMS_CRYPTO_ENDPOINT 환경변수가 설정되지 않았습니다.")
    
    key_id = os.environ.get('OCI_KMS_KEY_ID')
    if not key_id:
        raise ValueError("OCI_KMS_KEY_ID 환경변수가 설정되지 않았습니다.")
    
    # KMS 클라이언트 생성
    kms_client = OCIKMSClient(config, service_endpoint)
    
    await main(kms_client, lambda: key_id)

if __name__ == "__main__":
    asyncio.run(amain())
