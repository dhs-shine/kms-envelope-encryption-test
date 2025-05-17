import oci
import os
import asyncio
import base64
from dotenv import load_dotenv
from common import KMSClient, main, create_kms_client

class OCIKMSClient(KMSClient):
    def __init__(self):
        # OCI 설정 로드
        self.config = oci.config.from_file()
        
        # 환경 변수에서 필요한 설정 로드
        self._service_endpoint = os.environ.get('OCI_KMS_CRYPTO_ENDPOINT')
        if not self._service_endpoint:
            raise ValueError("OCI_KMS_CRYPTO_ENDPOINT 환경변수가 설정되지 않았습니다.")
            
        self._key_id = os.environ.get('OCI_KMS_KEY_ID')
        if not self._key_id:
            raise ValueError("OCI_KMS_KEY_ID 환경변수가 설정되지 않았습니다.")

        # KMS 클라이언트 초기화
        self.crypto_client = oci.key_management.KmsCryptoClient(
            self.config,
            service_endpoint=self._service_endpoint
        )

    def get_key_id(self) -> str:
        """OCI KMS 키 ID를 반환"""
        return self._key_id

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
    
    # KMS 클라이언트 생성
    kms_client = create_kms_client('oci')
    
    await main(kms_client)

if __name__ == "__main__":
    asyncio.run(amain())
