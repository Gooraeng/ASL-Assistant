# ASL-Assistant

## 🚩 소개
- Asphalt 9을 즐기는 유저들이 자신이 찾고자 하는 차량의 정보를 디테일하게 제공하는 Discord Bot입니다.
- <a href="https://www.mei-a9.info/">MEI</a> / <a href="https://discord.gg/dVA7R9CXpB">A9-Database</a> 내 자료를 기반으로 하고 있습니다.



## 📅 개발 기간
* 23.9.14(목) ~ 23.9.21(목)



### 👩‍👧‍👦 참여 인원
* Gooraeng



### ⚙️ 개발 환경
- Python(3.10.10 / 64-bit)
- Discord.py (2.3.2)
- **IDE** : Microsoft Visual Studio Code



## 📍 메인 기능
- ASL Assistant는 아래 두 개의 메인 기능을 지원하며, 그 밖의 6개의 서브 기능을 지원합니다.
- 아래 메인 기능들의 조건을 만족하지 못하면 오류 메세지를 출력합니다.

#### 1. '/spec' 커맨드
- <a href="https://www.mei-a9.info/cars">MEI - Cars list</a>페이지에서 차량 리스트를 만들기 위한 소스 추출
- 불필요한 부분 제거 후 리스트로 제작
- 사용자가 찾고자 하는 차량 네임의 일부를 입력하면 조건에 맞는 차량(리스트) 나엻 및 자동 완성 가능 (/spec '찾고자 하는 차량')
- 입력 후 조건에 맞는 차량의 스펙 이미지를 봇이 답장으로 보여줌.

#### 2. '/clash' 커맨드
- 원본 : Club Clah reference by Sharp
- 맵과 클래스, 차량을 인스턴스로 가지며, 사용자가 입력하였거나 리스트에 있는 값을 터치/클릭하여 채팅에 전송하면 조건을 만족하는 레퍼런스를 검색할 수 있음.
