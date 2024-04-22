import os
from pathlib import Path

def process_file_name(name):
    # 파일 또는 폴더 이름에서 랜덤 글자를 제거하는 로직
    if len(name) > 36 and name[-36:].isalnum():  # 이름이 36글자 이상이고, 마지막 36글자가 알파벳과 숫자로만 구성된 경우
        return name[:-36]  # 마지막 36글자를 제거
    elif len(name) > 32 and name[-32:].isalnum():  # 이름이 32글자 이상이고, 마지막 32글자가 알파벳과 숫자로만 구성된 경우
        return name[:-32]  # 마지막 32글자를 제거
    return name  # 변경이 필요 없는 경우 원래 이름 반환

def rename_files_in_directory(directory_path):
    for item in directory_path.iterdir():
        if item.is_file() or item.is_dir():  # 파일 또는 디렉토리인 경우
            name, extension = os.path.splitext(item.name) if item.is_file() else (item.name, '')
            new_name = process_file_name(name) + extension
            new_file_path = item.with_name(new_name)

            # 중복된 파일 또는 폴더 이름을 처리합니다.
            counter = 1
            while new_file_path.exists():  # 새 이름이 이미 존재하는 경우
                # 이름에 숫자를 추가하여 고유한 이름을 생성합니다.
                new_name = f"{process_file_name(name)}_{counter}"
                if extension:  # 파일인 경우 확장자 추가
                    new_name += extension
                new_file_path = item.with_name(new_name)
                counter += 1
            
            os.rename(item, new_file_path)
            if item.is_dir():  # 디렉토리인 경우, 재귀적으로 함수를 호출합니다.
                rename_files_in_directory(item)

# 사용 예시
base_path = Path('D:/다운로드/개인 노션 저장/Export-81def9fc-5a3a-43e1-865e-575589bfac08-Part-1/testFolder')
rename_files_in_directory(base_path)
