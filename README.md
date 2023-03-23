## Prophet

### 목적
- META의 예언자(Prophet) 라이브러리를 사용하여 시계열 예측 학습


### 준비
- pyenv(파이썬 버전 관리자) 설치
  - https://github.com/pyenv-win/pyenv-win
  - `Windows` PowerShell 관리자 모드로 설치
    - `선행` -> 스크립트 보안 해제
      ```
      --PowerShell
      $ ExecutionPolicy
      > Restricted --> 라고 결과 나오면 아래의 명령어 중 하나 입력
      
      $ Set-ExecutionPolicy Unrestricted
      or
      $ Set-ExecutionPolicy RemoteSigned(추천)
      
      $ ExecutionPolicy
      > Unrestricted
      or
      > RemoteSigned
      
      ```
      - 정책
        - Restricted : 기본 실행 정책으로 개별 명령을 허용하지만 스크립트를 실행하지 않습니다.
        - Unrestricted : 서명되지 않은 스크립트를 실행할 수 있음, 악의적인 스크립트를 실행할 위험이 있음
        - RemoteSigned : 스크립트를 실행 가능, 이미 실행한 스크립트와 로컬 컴퓨터에 작성한 스크립트에는 디지털 서명이 필요 없음
    - pyenv 설치
      ```
      --PowerShell, 설치 후 터미널 재실행
      $ Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
      $ pyenv --version
      ```
    - pyenv python 설치
      ```
      $ pyenv install -l
      -> 버전 확인
      $ pyenv install 3.10.10
      -> 파이썬 설치
      $ pyenv global 3.10.10
      -> 환경변수 설정
      $ python --version
      > Python 3.10.10
      ```
- poetry(파이썬 의존성 관리) 설치
  - https://python-poetry.org/docs/
  - `Windows` PowerShell 관리자 모드로 설치
    ```
    --PowerShell, 설치 후 터미널 재실행
    -- windows install powershell
    $ (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
  
    -- windows uninstall powershell
    $ (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python - --uninstall
    
    -- windows add path poetry dir(유저명은 각자 환경에 맞춰서 변경)
    -- 환경변수 설정으로 굳이 여기서 하지 않아도 됩니다.
    -- 백업 후 'Machine', 'User' 환경 등록
    $ [System.Environment]::GetEnvironmentVariable('Path','User') > C:\backup-path-user.txt
    $ [System.Environment]::GetEnvironmentVariable('Path','Machine') > C:\backup-path-machine.txt
    
    -- check path
    $ ($env:Path).split(";")
    
    $ $INCLUDE = "C:\Users\유저명\AppData\Roaming\Python\Scripts"
    $ $OLDPATH = [System.Environment]::GetEnvironmentVariable('Path','Machine')
    $ $NEWPATH = "$OLDPATH;$INCLUDE"
    $ [Environment]::SetEnvironmentVariable("Path", "$NEWPATH", "Machine")
    
    $ $INCLUDE = "C:\Users\유저명\AppData\Roaming\Python\Scripts"
    $ $OLDPATH = [System.Environment]::GetEnvironmentVariable('Path','User')
    $ $NEWPATH = "$OLDPATH;$INCLUDE"
    $ [Environment]::SetEnvironmentVariable("Path", "$NEWPATH", "User")
    
    -- check path
    $ ($env:Path).split(";")
    
    $poetry --version
    > Poetry (version 1.4.0)
    ```
- poetry project get started
  ```
  --PowerShell or cmd or GitBash
  $ poetry new py_forecasting
  $ cd py_forecasting
  ```
- poetry add library
  ```
  -- install
  $ poetry add prophet
  
  -- remove
  $ poetry remove prophet
  
  -- update(toml file update)
  $ poetry update
  
  -- show 
  $ poetry show
  
  -- add virtualenv
  $ poetry env use python
  $ poetry env use {파이썬경로}
  
  -- info virtualenv
  $ poetry env info
  ```
- poetry install(Create a lock file)
  ```
  $ poetry install
  ```


## Reference
- https://itpro.tistory.com/100
- https://github.com/pyenv-win/pyenv-win
- https://python-poetry.org/
- https://techexpert.tips/ko/powershell-ko
- https://facebook.github.io/prophet/docs/quick_start.html
- https://machinelearningmastery.com/time-series-forecasting-with-prophet-in-python/