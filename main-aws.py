import boto3
import base64
import os
import json
import asyncio
import time
from dotenv import load_dotenv
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

# 암호화할 긴 텍스트 생성
def generate_long_text():
    text = """인공지능과 머신러닝의 발전은 현대 사회에 큰 변화를 가져왔습니다. 
딥러닝 기술의 발전으로 이미지 인식, 자연어 처리, 음성 인식 등 다양한 분야에서 혁신적인 성과를 이루고 있습니다.
이러한 기술 발전은 우리의 일상생활에도 큰 영향을 미치고 있으며, 앞으로도 계속해서 발전할 것으로 예상됩니다.

클라우드 컴퓨팅의 발전은 기업들의 IT 인프라 구축 방식을 완전히 바꾸어 놓았습니다.
서버리스 아키텍처, 컨테이너 기술, 마이크로서비스 등 새로운 기술들이 등장하면서 
시스템 구축과 운영 방식이 더욱 효율적이고 유연해졌습니다.

보안 기술의 발전은 디지털 전환 시대에 필수적인 요소가 되었습니다.
암호화 기술, 블록체인, 양자 암호화 등 새로운 보안 기술들이 등장하면서 
데이터 보호와 개인정보 보호의 중요성이 더욱 커지고 있습니다.

빅데이터 분석 기술의 발전은 의사결정 과정을 데이터 기반으로 변화시켰습니다.
실시간 데이터 처리, 예측 분석, 머신러닝 기반 의사결정 등이 
기업의 경쟁력을 결정하는 중요한 요소가 되었습니다.

사물인터넷(IoT) 기술의 발전은 우리 주변의 모든 사물을 연결하고 있습니다.
스마트 홈, 스마트 시티, 산업용 IoT 등 다양한 분야에서 
연결성과 자동화가 확대되고 있습니다.

5G와 6G 통신 기술의 발전은 초고속, 초저지연, 초연결을 실현하고 있습니다.
증강현실(AR), 가상현실(VR), 메타버스 등 새로운 서비스들이 
이러한 통신 기술을 기반으로 발전하고 있습니다.

블록체인 기술은 분산 원장 기술로서 신뢰성 있는 거래를 가능하게 합니다.
암호화폐, 스마트 컨트랙트, 분산 금융(DeFi) 등이 
블록체인 기술을 기반으로 발전하고 있습니다.

양자 컴퓨팅 기술의 발전은 컴퓨팅의 패러다임을 바꿀 것으로 예상됩니다.
양자 암호화, 양자 시뮬레이션, 양자 머신러닝 등이 
새로운 컴퓨팅 시대를 열어갈 것입니다.

로봇공학의 발전은 자동화와 지능화를 더욱 가속화하고 있습니다.
산업용 로봇, 서비스 로봇, 협동 로봇 등이 
다양한 분야에서 활용되고 있습니다.

바이오테크놀로지의 발전은 의료와 건강 분야에 혁신을 가져오고 있습니다.
유전자 편집, 맞춤형 의료, 디지털 헬스케어 등이 
인간의 건강과 수명 연장에 기여하고 있습니다.

이러한 기술들의 발전은 서로 융합되면서 더욱 혁신적인 변화를 만들어내고 있습니다.
인공지능과 빅데이터의 결합, IoT와 5G의 결합, 
블록체인과 양자 컴퓨팅의 결합 등이 새로운 가능성을 만들어내고 있습니다.

기업들은 이러한 기술 변화에 대응하기 위해 디지털 전환을 가속화하고 있습니다.
클라우드 마이그레이션, 데이터 기반 의사결정, 
자동화와 지능화를 통한 효율성 향상 등이 진행되고 있습니다.

정부와 공공기관도 디지털 전환을 통해 서비스 혁신을 추진하고 있습니다.
스마트 시티, 디지털 정부, 공공 데이터 활용 등이 
시민들의 삶의 질 향상에 기여하고 있습니다.

교육 분야에서도 디지털 전환이 활발하게 진행되고 있습니다.
온라인 교육, AI 기반 맞춤형 학습, 
가상현실 기반 교육 등이 새로운 교육 방식을 만들어내고 있습니다.

의료 분야에서는 디지털 헬스케어가 빠르게 발전하고 있습니다.
원격 진료, AI 기반 진단, 
개인 맞춤형 의료 등이 의료 서비스의 혁신을 이끌고 있습니다.

금융 분야에서는 핀테크가 금융 서비스의 혁신을 주도하고 있습니다.
모바일 뱅킹, 암호화폐, 분산 금융 등이 
새로운 금융 서비스의 형태를 만들어내고 있습니다.

제조업 분야에서는 스마트 팩토리가 산업 혁신을 이끌고 있습니다.
자동화, IoT, AI 등이 결합된 스마트 제조 시스템이 
생산성과 효율성을 크게 향상시키고 있습니다.

유통 분야에서는 전자상거래가 새로운 형태로 발전하고 있습니다.
모바일 커머스, 소셜 커머스, 라이브 커머스 등이 
소비자들의 쇼핑 경험을 변화시키고 있습니다.

엔터테인먼트 분야에서는 메타버스가 새로운 가능성을 열고 있습니다.
가상현실, 증강현실, 블록체인 등이 결합된 
새로운 형태의 엔터테인먼트가 등장하고 있습니다.

이러한 기술 발전과 디지털 전환은 우리의 삶을 크게 변화시키고 있습니다.
더욱 편리하고 효율적인 생활, 
새로운 형태의 일과 여가, 
더 나은 의료와 교육 서비스 등이 
디지털 기술을 통해 실현되고 있습니다.

앞으로도 기술 발전은 계속될 것이며, 
이에 따른 사회 변화도 더욱 가속화될 것입니다.
우리는 이러한 변화에 능동적으로 대응하고, 
기회를 포착하여 새로운 가치를 창출해야 합니다.

디지털 전환 시대에 필요한 역량을 갖추고, 
지속적인 학습과 혁신을 통해 
미래를 준비해야 합니다.

기술 발전이 가져오는 변화를 두려워하지 말고, 
이를 기회로 삼아 
새로운 가능성을 탐색해야 합니다.

우리 모두가 디지털 전환의 주체가 되어 
더 나은 미래를 만들어가야 합니다.""".encode('utf-8')
    return text

# 암호화 함수
async def encryption(data_to_encrypt_bytes: bytes, key_id: str):
    start_time = time.time()

    # DEK 생성
    encrypted_dek, plaintext_dek = await generate_dek(key_id)

    # DEK를 사용하여 데이터 암호화 (GCM 모드)
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(plaintext_dek), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data_to_encrypt_bytes) + encryptor.finalize()
    tag = encryptor.tag

    # 암호화된 데이터, 암호화된 DEK 및 GCM 태그를 JSON으로 구조화
    envelope = {
        "encrypted_data": base64.b64encode(ciphertext).decode('utf-8'),
        "encrypted_dek": base64.b64encode(encrypted_dek).decode('utf-8'),
        "iv": base64.b64encode(iv).decode('utf-8'),
        "tag": base64.b64encode(tag).decode('utf-8'),
        "key_id": key_id
    }

    end_time = time.time()
    encryption_time = end_time - start_time

    return json.dumps(envelope), encryption_time

# DEK 생성 함수
async def generate_dek(key_id: str):
    # AWS KMS 클라이언트 생성
    region_name = os.environ.get("AWS_REGION")
    kms_client = boto3.client('kms', region_name=region_name)

    # KMS를 사용하여 DEK 생성
    response = kms_client.generate_data_key(
        KeyId=key_id,
        KeySpec='AES_256'
    )

    return response['CiphertextBlob'], response['Plaintext']

# 복호화 함수
async def decryption(envelope_json: str):
    start_time = time.time()

    # JSON 파싱
    envelope = json.loads(envelope_json)
    encrypted_data_b64 = envelope["encrypted_data"]
    encrypted_dek_b64 = envelope["encrypted_dek"]
    iv_b64 = envelope["iv"]
    key_id = envelope["key_id"]

    ciphertext = base64.b64decode(encrypted_data_b64)
    encrypted_dek = base64.b64decode(encrypted_dek_b64)
    iv = base64.b64decode(iv_b64)

    # AWS KMS 클라이언트 생성
    region_name = os.environ.get("AWS_REGION")
    kms_client = boto3.client('kms', region_name=region_name)

    # KMS를 사용하여 DEK 복호화
    response = kms_client.decrypt(
        CiphertextBlob=encrypted_dek,
        KeyId=key_id
    )

    plaintext_dek = response['Plaintext']

    # GCM 태그 가져오기
    tag = base64.b64decode(envelope["tag"])

    # DEK를 사용하여 데이터 복호화 (GCM 모드)
    cipher = Cipher(algorithms.AES(plaintext_dek), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    end_time = time.time()
    decryption_time = end_time - start_time

    return decrypted_data, decryption_time

async def main():
    load_dotenv()
    key_id = os.environ.get("AWS_KMS_KEY_ID")
    region_name = os.environ.get("AWS_REGION")

    # 긴 텍스트 생성
    data_to_encrypt_bytes = generate_long_text()
    print(f"원본 텍스트 크기: {len(data_to_encrypt_bytes)} bytes")
    print("\n=== 원본 텍스트 ===")
    print(data_to_encrypt_bytes.decode('utf-8'))

    # 암호화
    envelope_json, encryption_time = await encryption(data_to_encrypt_bytes, key_id)
    print(f"\n암호화 소요시간: {encryption_time:.3f}초")
    print(f"암호화된 데이터 크기: {len(envelope_json)} bytes")

    # 복호화
    decrypted_data, decryption_time = await decryption(envelope_json)
    print(f"\n복호화 소요시간: {decryption_time:.3f}초")
    print(f"복호화된 데이터 크기: {len(decrypted_data)} bytes")

    # 복호화된 데이터가 원본과 동일한지 확인
    print("\n복호화된 텍스트가 원본과 동일한지 확인:", data_to_encrypt_bytes == decrypted_data)

    # 복호화된 텍스트 출력
    print("\n=== 복호화된 텍스트 ===")
    print(decrypted_data.decode('utf-8'))

if __name__ == "__main__":
    asyncio.run(main())