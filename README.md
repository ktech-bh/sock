# Socket_Server by python

***1. Server_ping.ui 파일과 같은 경로에서 server_g.exe 실행***  
***2. Port 번호 입력 후 Open 클릭***  
***3. Ping 버튼은 테스트 할 ip를 선택 후 클릭***  

## 개발 환경
- python==3.9
- PyQt5==5.15.6
- PyQt5==5.15.2
- PyQt5-sip==12.10.1

## 사용 모듈
```
import sys
import socket
import os
import threading import Thread
from PyQt5.Qtwidgets import *
from PyQt5 import uic
from datetime import datetime
```

## 주요 기능
- Server 자동 IP 입력  
- ~~비어있는 Port 자동 입력~~
- 메세지 송수신 시간 표시
- 메세지 보낸 사람 IP 표시
- 참여 IP, PORT, PING 표시
- PING 수동 확인

***
Server_ping.ui : PyQt로 만든 ui 파일  
server_g.py : Server_ping.ui 파일과 연동된 소스코드 파일  
server_s2.py : 소켓통신이 이루어지는 소스코드 파일  
***
