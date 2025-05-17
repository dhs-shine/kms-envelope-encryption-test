import os
import asyncio
import boto3
from dotenv import load_dotenv
from common import KMSClient, main
import base64

class AWSKMSClient(KMSClient):
    def __init__(self):
        self.kms_client = boto3.client('kms')

    async def generate_dek(self, key_id: str):
        """AWS KMS를 사용하여 DEK 생성 및 암호화"""
        generate_dek_response = await asyncio.to_thread(
            self.kms_client.generate_data_key,
            KeyId=key_id,
            KeySpec='AES_256'
        )
        return generate_dek_response['CiphertextBlob'], generate_dek_response['Plaintext']

    async def decrypt(self, ciphertext: str, key_id: str):
        """AWS KMS를 사용하여 DEK 복호화"""
        decrypt_response = await asyncio.to_thread(
            self.kms_client.decrypt,
            CiphertextBlob=base64.b64decode(ciphertext)
        )
        return decrypt_response['Plaintext']

async def amain():
    load_dotenv()
    
    # AWS KMS 클라이언트 생성
    kms_client = AWSKMSClient()
    
    # KMS 키 ID
    key_id = os.environ.get('AWS_KMS_KEY_ID')
    if not key_id:
        raise ValueError("AWS_KMS_KEY_ID 환경변수가 설정되지 않았습니다.")
    
    await main(kms_client, lambda: key_id)

if __name__ == "__main__":
    asyncio.run(amain())