from pathlib import Path
import shutil
import sys

# exceptionPathName = '\\exception'
# basePath = 'C:\\Users\\lw\\Downloads'
basePath = 'D:\\다운로드'
# addPath = '/노션 아묻따'
# addPath = '\개인 노션 저장\\1\\testFolder'
addPath = '\\노션 자료\\Export'
path = Path(basePath + addPath)


#! 파일 뒤에 붙는 랜덤글은 32 혹은 36글자가 전부이다.
#todo 파일 뒤 붙는 notionId가 36글자일 경우 파일명 뒤에 _all이 붙는다.
#todo 이름이 중복이 될 경우 뒤에 (2)같이 괄호 숫자가 붙는다. 

is_renamed = False
# 최대 재귀 깊이를 10000으로 설정
sys.setrecursionlimit(10000)

#* 파일인지 폴더인지 확인하는 함수
def dirOrFile (paramPath):
  result = None
  if paramPath.is_dir():
    result = 'dir'
  elif paramPath.is_file():
    result = 'file'
  else:
    fileOrDirectoryElse(paramPath)
    # print(f"{paramPath}의 경로 및 파일의 글자 제한이 260이 넘습니다.")
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
  innerPath = ''
  if(extension == ''): 
    fileName = paramPath.name.split()
  else: 
    fileName = paramPath.name[:-extension.__len__()].split()

  innerFileName = ''
  innerAllStr = False
  booleanFileLength = False
  if(fileName.__len__() > 1):
    fileLen = fileName[-1].__len__()
    booleanFileLength = True
    if(fileLen == 32):
      fileName.pop()
    elif(fileLen == 36):
      innerFileName = fileName.pop()
      innerAllStr = True
    if(innerAllStr == True):
      innerFileName = ' '.join(map(str, fileName)) + '_all' + extension
    else:
      innerFileName = ' '.join(map(str, fileName)) + extension

  else:
    booleanFileLength = False
    innerFileName = fileName[0]
  if(paramPath.parent / innerFileName).suffix:
    innerPath = paramPath.parent / innerFileName
  elif not((paramPath.parent / innerFileName).suffix) and extension != '':
    innerPath = paramPath.parent / (innerFileName + extension)
  else: 
    innerPath = paramPath.parent / innerFileName
  try:
    if(paramPath.exists() == True and innerPath.exists() == False):
      paramPath.rename(innerPath)
      global is_renamed
      is_renamed = True
    elif((paramPath.exists() == True and innerPath.exists() == True) and (paramPath == innerPath)):
      return
    elif(booleanFileLength):
      errorFileReName(paramPath)
  except Exception as error:
    print('fileReName_동일한 이름이 존재합니다.')
    print(error)

#* 파일, 폴더 구분시켜서 이름 변경하는 함수로 보내기
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
  

def checkNumbering (paramPath):
  innerPath = paramPath
  while innerPath.exists():
    extension = innerPath.suffix
    nameSplit = innerPath.name.split()
    if(extension != ''):
      nameSplit[-1] = nameSplit[-1].split('.')[0]
      nameSplit[-1] = nameSplit[-1][0] + str(int(nameSplit[-1][1:-1]) +1) + nameSplit[-1][-1]
      checkName = ' '.join(nameSplit) + extension
      checkName = paramPath.parent / checkName
      if(checkName.exists()):
        checkNumbering(checkName)
      else:
        return checkName
  return innerPath


#! 동일한 이름이 있을 경우의 함수(예외처리 함수)
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
  result = checkNumbering(result);
    
  pathLength = len(str(result));
  try:
    if(pathLength <= 260):
      if(paramPath.exists() == True and result.exists() == False):
        paramPath.rename(result)
        global is_renamed
        is_renamed = True
      else:
        if paramPath.exists() == False :
          print(f'{paramPath}(은)는 기존 파일경로의 파일이 존재하지 않습니다.')
        elif result.exists() == True:
          print(f'{paramPath}의 새 파일이름이 존재합니다.')
        else:
          raise ValueError("알수없는 에러가 발생했습니다.")
    else:
      print('파일 경로가 260글자가 넘었습니다.', result)
      return;
  except Exception as error:
    print('errorFileReName_동일한 이름이 존재합니다.')
    print(error)

  return result

# 경로 및 파일의 길이가 윈도우 기본제한인 260글자가 넘을 경우 처리하는 함수
# 해당 함수는 다른곳으로 파일을 옮겨서 생성한 후 다시 옮기는 걸로 처리
def fileOrDirectoryElse (paramPath):
  innerParamPath = paramPath 
  try:
    
    innerParamPath 
  except Exception as error:
    print(error)
  if len(str(paramPath)) >= 260:
    # 사무실에서는 늘려놈
    print(f"{paramPath}의 경로 및 파일의 글자 제한이 260이 넘습니다.")
  else:
    print(f"{paramPath}가 디렉토리나 파일이 아닙니다.")

#! 윈도우 기본 경로 길이가 260글자가 한계이므로 재귀함수로 처리하여 해결
def start_rename_dir_file (paramPath):
  global is_renamed
  is_renamed = False
  try:
    remake_file_and_dir(paramPath)
    if(not is_renamed):
      print('작업이 완료되었습니다.')
      return;
    else:
      start_rename_dir_file(paramPath)
  except Exception as error:
    print(error)

start_rename_dir_file(path)