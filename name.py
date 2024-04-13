from pathlib import Path

basePath = 'D:\다운로드'
path = Path(basePath + '\개인 노션 저장\Export-81def9fc-5a3a-43e1-865e-575589bfac08-Part-1\\testFolder')

#! 파일 뒤에 붙는 랜덤글은 32 혹은 36글자가 전부이다.
#todo 파일 뒤 붙는 notionId가 36글자일 경우 파일명 뒤에 _all이 붙는다.
#todo 이름이 중복이 될 경우 뒤에 (2)같이 괄호 숫자가 붙는다. 

#* 파일인지 폴더인지 확인하는 함수
def dirOrFile (paramPath):
  result = None
  if paramPath.is_dir():
    print(f"{paramPath}는 디렉토리입니다.")
    result = 'dir'
  elif paramPath.is_file():
    result = 'file'
    print(f"{paramPath}는 파일입니다.")
  else:
    print("파일이나 폴더가 아닙니다.")
  return result

#* 하위 폴더 및 파일의 이름을 찾음
def directoryInName(paramPath):
  arr = []
  try:
    for entry in paramPath.iterdir():
      arr.append(entry.name)
  except FileNotFoundError:
    print('지정된 경로를 찾을 수 없습니다.')
  return arr

#* 파일의 이름 일부를 삭제하는 로직
def fileReName(paramPath):
  extension = paramPath.suffix
  fileName = ''
  if(extension == ''): 
    fileName = paramPath.name.split()
  else: 
    fileName = paramPath.name[:-extension.__len__()].split()

  innerFileName = ''
  if(fileName.__len__() > 1):
    fileLen = fileName[-1].__len__()
    if(fileLen == 32):
      fileName.pop()
    elif(fileLen == 36):
      innerFileName = fileName.pop()
    innerFileName = ' '.join(map(str, fileName)) + '_all' + extension
  else:
    innerFileName = fileName[0]
  innerPath = paramPath.parent / innerFileName
  try:
    if(paramPath != innerPath):
      paramPath.rename(innerPath)
  except Exception as error:
    print('동일한 이름이 존재합니다.')
    print(error)
    fileReName(errorFileReName(paramPath))

#* 파일 이름 변경
def remake_file_and_dir(paramPath):
  innerFileName = [];
  innerPath = paramPath
  if dirOrFile(innerPath) == 'dir':
    innerFileName = directoryInName(innerPath)
    for i in innerFileName:
      remake_file_and_dir(innerPath / i)
    fileReName(innerPath)
  elif dirOrFile(innerPath) == 'file':
    fileReName(innerPath)
    return
  
#! 동일한 이름이 있을 경우의 함수(예외처리 함수)
reErrorPath = ''
def errorFileReName (paramPath):
  extension = paramPath.suffix
  nameSplit = paramPath.name.split()
  notionIds = ''
  dupliNumbering = ''
  if(extension):
    notionIds = nameSplit.pop()[:-extension.__len__()]
  else:
    notionIds = nameSplit.pop()

  if len(notionIds) in [32, 36]:
    if ('(' in nameSplit[-1] and ')' in nameSplit[-1]):
      dupliNumbering = nameSplit.pop()
      dupliNumbering = int(dupliNumbering.replace('(', "").replace(')',""))
      dupliNumbering += 1
      dupliNumbering = f'({dupliNumbering})'
      nameSplit.append(dupliNumbering)
      if(notionIds):
        nameSplit.append(notionIds)
    else:
      nameSplit.append('(2)')
      if(notionIds):
        nameSplit.append(notionIds)
  else:
    if ('(' in notionIds and ')' in notionIds):
      dupliNumbering = int(notionIds.replace('(', "").replace(')',""))
      dupliNumbering += 1
      dupliNumbering = f'({dupliNumbering})'
      nameSplit.append(dupliNumbering)
    else:
      if(notionIds):
        nameSplit.append(notionIds)
      nameSplit.append('(2)')
  
  result = paramPath.parent / f'{" ".join(nameSplit)}{extension}'
  try:
    if(paramPath.exists() == True and result.exists() == False):
      paramPath.rename(result)
    else:
      if paramPath.exists() == False :
        print('기존 파일경로의 파일이 존재하지 않습니다.')
      elif result.exists() == True:
        print('새 파일이름이 존재합니다.')
      else:
        raise ValueError("알수없는 에러가 발생했습니다.")
  except Exception as error:
    print('동일한 이름이 존재합니다.')
    print(error)

  return result

remake_file_and_dir(path)