from pathlib import Path
import os

basePath = 'D:\다운로드'
path = Path(basePath + '\개인 노션 저장\Export-81def9fc-5a3a-43e1-865e-575589bfac08-Part-1/herenshii')

#! 파일 뒤에 붙는 랜덤글은 32 혹은 36글자가 전부이다.
#* 파일인지 폴더인지 확인하는 함수
def dirOrFile (path):
  result = None
  if path.is_dir():
    print(f"{path}는 디렉토리입니다.")
    result = 'dir'
  elif path.is_file():
    result = 'file'
    print(f"{path}는 파일입니다.")
  else:
    print("파일이나 폴더가 아닙니다.")
  return result

#* 하위 폴더 및 파일의 이름을 찾음
def directoryInName(path):
  arr = []
  try:
    for entry in path.iterdir():
      arr.append(entry.name)
  except FileNotFoundError:
    print('지정된 경로를 찾을 수 없습니다.')
  return arr

#* 파일의 이름 일부를 삭제하는 로직
def fileReMakeName(path):
  extension = path.suffix
  fileName = path.name[:-extension.__len__()].split()
  if(fileName.__len__() > 1):
    fileLen = fileName[-1].__len__()
    if(fileLen == 32 or fileLen == 36):
      fileName.pop()
  innerPath = ' '.join(map(str, fileName)) + extension
  newFileName = path.parent / innerPath
  os.rename(path, newFileName)

#! 파일 이름 변경까지 완료
def fileTest(path):
  innerFileName = []
  innerPath = path
  if dirOrFile(path) == 'dir':
    innerFileName = directoryInName(path)
  elif dirOrFile(path) == 'file':
    fileReMakeName(path)
    return


# dirOrFile(path)
# fileReMakeName(path)
# print(directoryInName(path))
# print(path)

test = '에펙 쇼츠 12편, 13편 edc064b23e074680945996779302447c.md'

# print(test.replace(' ','.').split('.')[-2].__len__())

