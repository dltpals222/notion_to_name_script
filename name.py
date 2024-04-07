from pathlib import Path

basePath = 'D:\다운로드'
path = Path(basePath + '\개인 노션 저장\Export-81def9fc-5a3a-43e1-865e-575589bfac08-Part-1/herenshii')

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

#? 파일 이름을 구분짓기
def pathFile (path):
  root = dirOrFile(path)
  # if root == 'dir':

#* 하위 폴더 및 파일의 이름을 찾음
def directoryInName(path):
  arr = []
  try:
    for entry in path.iterdir():
      arr.append(entry.name)
  except FileNotFoundError:
    print('지정된 경로를 찾을 수 없습니다.')

  return arr

# dirOrFile(path)
# print(directoryInName(path))
# print(path)

test = '잡다한 기록 모음 dc2f363d82e043a0a7b0974c250f3761_all.csv'

print(test.replace(' ','.').split('.')[-1])