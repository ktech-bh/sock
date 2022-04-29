# Socket_Server by python

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
