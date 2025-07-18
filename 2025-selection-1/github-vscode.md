# 패키지 목록을 최신화하고, gh를 설치합니다.
flatpak-spawn --host bashsudo apt update

sudo apt install gh -y

gh auth login

https://github.com/login/device

# 홈 디렉토리(~) 아래에 dev 폴더를 만들고 이동합니다.
mkdir -p ~/dev/codyssey
cd ~/dev/codyssey

git clone https://github.com/shannonlee-dev/ia-codyssey.git


### push 하는 법

git config --global user.name "shannonlee-dev"

git config --global user.email "님의 GitHub 이메일 주소"
