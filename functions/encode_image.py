# encode_image.py (functions 폴더 안에 생성)
import base64
import os

# 인코딩할 이미지 파일 이름 (위에서 준비한 이미지 파일 이름과 동일하게)
image_file_name = 'hello.png' # <- 여기를 당신의 이미지 파일 이름으로 바꿔주세요 (예: 'my_image.jpg')
output_b64_file_name = 'encoded_image.txt' # <- Base64 문자열을 저장할 파일 이름

image_path = os.path.join(os.path.dirname(__file__), image_file_name)
output_b64_path = os.path.join(os.path.dirname(__file__), output_b64_file_name)

try:
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        # Base64 문자열을 파일로 저장
        with open(output_b64_path, 'w') as f:
            f.write(encoded_string)

        print(f"Base64 데이터가 '{output_b64_file_name}' 파일에 성공적으로 저장되었습니다.")
        print("이제 이 파일을 열어 데이터를 복사하세요.")

except FileNotFoundError:
    print(f"오류: '{image_file_name}' 파일을 찾을 수 없습니다. 'functions' 폴더에 파일이 있는지 확인하세요.")
except Exception as e:
    print(f"오류 발생: {e}")