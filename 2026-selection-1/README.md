# 개발 워크스테이션 구축 미션

## 1. 프로젝트 개요

터미널, Docker, Git/GitHub를 사용해 재현 가능한 개발 워크스테이션을 구축하고, 수행 과정과 검증 결과를 README에 기록한다.

### 1-1. 프로젝트 디렉토리 구조를 구성한 기준

이번 프로젝트는 **제출물 확인이 쉽고, 실행에 필요한 파일과 증거 자료를 분리**하는 기준으로 디렉토리를 구성했다.

- `README.md`
  - 과제 전체 설명, 수행 로그, 검증 결과, 트러블슈팅을 한곳에 모아 두는 문서
  - 평가자가 저장소를 열었을 때 가장 먼저 확인하는 파일이므로 루트에 배치했다

- `Dockerfile`
  - 커스텀 이미지를 빌드하는 핵심 파일
  - 보통 `docker build .`를 실행하는 위치가 프로젝트 루트이므로 루트에 두었다

- `app/`
  - 실제 웹 서버가 제공할 정적 파일(`index.html`)을 분리 보관하는 디렉토리
  - Dockerfile의 `COPY app/ /usr/share/nginx/html/`와 bind mount의 `-v $(pwd)/app:/usr/share/nginx/html`가 모두 이 디렉토리를 기준으로 동작하도록 맞췄다
  - 즉, **이미지 빌드용 소스와 실시간 수정 반영용 소스를 같은 기준 경로로 통일**하기 위해 `app/`를 사용했다

- `docs/screenshots/`
  - 브라우저 접속 증거, 바인드 마운트 전/후 비교, VSCode 연동 증거 등 스크린샷 자료를 별도로 관리하는 디렉토리
  - README 본문은 설명 중심으로 유지하고, 이미지 자료는 별도 폴더에 모아 **가독성과 관리 편의성**을 높였다

정리하면, 이번 디렉토리 구조는 **실행 파일, 문서, 증거 자료를 역할별로 분리**하고, Docker 빌드/실행/검증 명령이 모두 같은 기준 경로에서 재현 가능하도록 구성한 것이다.

---

## 2. 실행 환경

- OS: macOS (Darwin Kernel Version 24.6.0)
- Shell: `/bin/zsh`
- Docker 엔진 실행 환경: OrbStack
- Docker 버전: Docker version 28.5.2
- Git 버전: git version 2.53.0

---

## 3. 터미널 조작 로그

### 3-1. 현재 위치 및 파일 목록 확인

```zsh
$ pwd
/Users/shh921shh4393/dev
```

```zsh
$ ls -la
total 0
drwxr-xr-x   4 shh921shh4393  shh921shh4393  128 Mar 30 18:04 .
drwxr-x---+ 21 shh921shh4393  shh921shh4393  672 Mar 30 18:04 ..
```

### 3-2. 파일/디렉토리 생성, 복사, 이동, 삭제, 내용 확인

```zsh
$ mkdir -p practice/dir1
$ cd practice
$ touch empty.txt
$ echo "hello workstation" > note.txt
$ cat note.txt
hello workstation
$ cp note.txt note-copy.txt
$ mv note-copy.txt renamed.txt
$ mkdir archive
$ mv renamed.txt archive
$ ls -la
total 8
drwxr-xr-x  6 shh921shh4393  shh921shh4393  192 Mar 30 18:26 .
drwxr-xr-x  5 shh921shh4393  shh921shh4393  160 Mar 30 18:25 ..
drwxr-xr-x  3 shh921shh4393  shh921shh4393   96 Mar 30 18:26 archive
drwxr-xr-x  2 shh921shh4393  shh921shh4393   64 Mar 30 18:25 dir1
-rw-r--r--  1 shh921shh4393  shh921shh4393    0 Mar 30 18:25 empty.txt
-rw-r--r--  1 shh921shh4393  shh921shh4393   18 Mar 30 18:25 note.txt
$ rm empty.txt
```

터미널에서 현재 위치 확인, 숨김 파일 포함 목록 확인, 디렉토리 생성, 파일 생성, 내용 작성, 복사, 이름 변경, 이동, 삭제를 수행했다.

---

## 4. 파일 권한 실습

### 4-1. 권한 변경 전/후 비교

```zsh
# 권한 변경 전
$ ls -ld permission-file.txt permission-dir
d---------  2 shh921shh4393  shh921shh4393  64 Mar 30 18:32 permission-dir
----------  1 shh921shh4393  shh921shh4393   0 Mar 30 18:31 permission-file.txt

$ chmod 644 permission-file.txt
$ chmod 755 permission-dir

# 권한 변경 후
$ ls -ld permission-file.txt permission-dir
drwxr-xr-x  2 shh921shh4393  shh921shh4393  64 Mar 30 18:32 permission-dir
-rw-r--r--  1 shh921shh4393  shh921shh4393   0 Mar 30 18:31 permission-file.txt
```

### 4-2. 권한 설명

- `r` = read
- `w` = write
- `x` = execute
- `644` = 소유자 `rw-`, 그룹 `r--`, 기타 사용자 `r--`
- `755` = 소유자 `rwx`, 그룹 `r-x`, 기타 사용자 `r-x`

파일 권한 숫자는 `r`, `w`, `x`를 숫자로 치환한 뒤 더해서 만든다.

- `r` = 4
- `w` = 2
- `x` = 1

각 사용자 구간(소유자 / 그룹 / 기타 사용자)에 대해 이 값을 더해서 한 자리 숫자를 만든다.

- `644` = 소유자 `rw-` = 4 + 2 = 6, 그룹 `r--` = 4, 기타 사용자 `r--` = 4
- `755` = 소유자 `rwx` = 4 + 2 + 1 = 7, 그룹 `r-x` = 4 + 1 = 5, 기타 사용자 `r-x` = 4 + 1 = 5

즉, 숫자 권한은 외우는 것이 아니라 **4, 2, 1의 합산 규칙으로 계산**하는 구조다.

### 4-3. 경로 설명

- 절대 경로: `/Users/username/dev-workstation-mission/app/index.html`
- 상대 경로: `./app/index.html`

절대 경로와 상대 경로는 둘 다 파일 위치를 가리키지만, 사용하는 상황이 다르다.

- 절대 경로는 **현재 작업 위치와 상관없이 항상 같은 위치를 정확하게 가리켜야 할 때** 적합하다
- 상대 경로는 **프로젝트 내부에서 짧고 읽기 쉽게 경로를 표현할 때** 적합하다

이번 과제에서는 설명 문서에서는 **가독성** 때문에 상대 경로를 자주 사용했고, 실제 bind mount처럼 실행 환경과 직접 연결되는 부분에서는 **정확성** 때문에 절대 경로 또는 `$(pwd)` 기반 경로를 사용했다.

---

## 5. Docker 설치 및 점검

```zsh
$ docker --version
Docker version 28.5.2, build ecc6942

$ docker info

Client:
 Version:    28.5.2
 Context:    orbstack
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.29.1
    Path:     /Users/shh921shh4393/.docker/cli-plugins/docker-buildx
  compose: Docker Compose (Docker Inc.)
    Version:  v2.40.3
    Path:     /Users/shh921shh4393/.docker/cli-plugins/docker-compose

Server:
 Containers: 11
  Running: 5
  Paused: 0
  Stopped: 6
 Images: 4
 Server Version: 28.5.2
 Storage Driver: overlay2
  Backing Filesystem: btrfs
  Supports d_type: true
  Using metacopy: false
  Native Overlay Diff: true
  userxattr: false
 Logging Driver: json-file
 Cgroup Driver: cgroupfs
 Cgroup Version: 2
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local splunk syslog
 CDI spec directories:
  /etc/cdi
  /var/run/cdi
 Swarm: inactive
 Runtimes: io.containerd.runc.v2 runc
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: 1c4457e00facac03ce1d75f7b6777a7a851e5c41
 runc version: d842d7719497cc3b774fd71620278ac9e17710e0
 init version: de40ad0
 Security Options:
  seccomp
   Profile: builtin
  cgroupns
 Kernel Version: 6.17.8-orbstack-00308-g8f9c941121b1
 Operating System: OrbStack
 OSType: linux
 Architecture: x86_64
 CPUs: 6
 Total Memory: 15.67GiB
 Name: orbstack
 ID: 24cb8908-86a3-4b7a-b84f-7bfcc9f4c900
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
 Experimental: false
 Insecure Registries:
  ::1/128
  127.0.0.0/8
 Live Restore Enabled: false
 Product License: Community Engine
 Default Address Pools:
   Base: 192.168.97.0/24, Size: 24
   Base: 192.168.107.0/24, Size: 24
   Base: 192.168.117.0/24, Size: 24
   Base: 192.168.147.0/24, Size: 24
   Base: 192.168.148.0/24, Size: 24
   Base: 192.168.155.0/24, Size: 24
   Base: 192.168.156.0/24, Size: 24
   Base: 192.168.158.0/24, Size: 24
   Base: 192.168.163.0/24, Size: 24
   Base: 192.168.164.0/24, Size: 24
   Base: 192.168.165.0/24, Size: 24
   Base: 192.168.166.0/24, Size: 24
   Base: 192.168.167.0/24, Size: 24
   Base: 192.168.171.0/24, Size: 24
   Base: 192.168.172.0/24, Size: 24
   Base: 192.168.181.0/24, Size: 24
   Base: 192.168.183.0/24, Size: 24
   Base: 192.168.186.0/24, Size: 24
   Base: 192.168.207.0/24, Size: 24
   Base: 192.168.214.0/24, Size: 24
   Base: 192.168.215.0/24, Size: 24
   Base: 192.168.216.0/24, Size: 24
   Base: 192.168.223.0/24, Size: 24
   Base: 192.168.227.0/24, Size: 24
   Base: 192.168.228.0/24, Size: 24
   Base: 192.168.229.0/24, Size: 24
   Base: 192.168.237.0/24, Size: 24
   Base: 192.168.239.0/24, Size: 24
   Base: 192.168.242.0/24, Size: 24
   Base: 192.168.247.0/24, Size: 24
   Base: fd07:b51a:cc66:d000::/56, Size: 64

WARNING: DOCKER_INSECURE_NO_IPTABLES_RAW is set
```

- `docker --version`: Docker CLI 설치 여부 확인
- `docker info`: Docker daemon 및 엔진 동작 여부 확인

---

## 6. Docker 기본 운영 명령 및 컨테이너 실습

### 6-1. `hello-world` 실행

```zsh
$ docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
4f55086f7dd0: Pull complete
Digest: sha256:452a468a4bf985040037cb6d5392410206e47db9bf5b7278d281f94d1c2d0931
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.
```

`hello-world` 실행 결과를 통해 Docker가 이미지를 pull하고 컨테이너를 생성 및 실행할 수 있음을 확인했다.

### 6-2. 이미지 및 컨테이너 목록 확인

```zsh
$ docker images
REPOSITORY    TAG       IMAGE ID       CREATED          SIZE
my-web        1.0       bf77efb0c126   56 minutes ago   62.2MB
nginx         alpine    d5030d429039   5 days ago       62.2MB
hello-world   latest    e2ac70e7319a   6 days ago       10.1kB
ubuntu        latest    f794f40ddfff   4 weeks ago      78.1MB

$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

```zsh
$ docker ps -a
CONTAINER ID   IMAGE         COMMAND    CREATED              STATUS                          PORTS     NAMES
80bea571fafc   hello-world   "/hello"   About a minute ago   Exited (0) About a minute ago             quizzical_jang
```

`docker ps`에서는 실행 중인 컨테이너만 보이고, `docker ps -a`에서는 종료된 컨테이너까지 확인할 수 있다.

### 6-3. 로그 확인

```zsh
docker logs ubuntu-test
root@cfec90c65426:/# ls
bin   dev  home  lib64  mnt  proc  run   srv  tmp  var
boot  etc  lib   media  opt  root  sbin  sys  usr
root@cfec90c65426:/# echo "inside container"
inside container
root@cfec90c65426:/# exit
exit

```

### 6-4. Ubuntu 컨테이너 진입

```zsh
$ docker run -it --name ubuntu-test ubuntu bash
root@cfec90c65426:/# ls
bin   dev  home  lib64  mnt  proc  run   srv  tmp  var
boot  etc  lib   media  opt  root  sbin  sys  usr
root@cfec90c65426:/# echo "inside container"
inside container
root@cfec90c65426:/# exit
exit
```

Ubuntu 컨테이너 내부에 진입하여 `ls`, `echo` 명령을 수행하고 `exit`로 종료했다.

### 6-5. `attach` / `exec` 차이 관찰

- `attach`: 기존 메인 프로세스에 연결
- `exec`: 실행 중인 컨테이너 안에서 새 명령 실행

```zsh
$ docker run -dit --name ubuntu-bg ubuntu bash
$ docker exec -it ubuntu-bg bash
```

### 6-6. 리소스 사용량 확인

```zsh
$ docker stats --no-stream
CONTAINER ID   NAME              CPU %     MEM USAGE / LIMIT     MEM %     NET I/O         BLOCK I/O    PIDS
5d8ab63a14b6   optimistic_benz   0.00%     1.312MiB / 15.67GiB   0.01%     1.13kB / 126B   147kB / 0B   1
```

이미지와 컨테이너는 비슷해 보이지만 역할이 다르다.

- **이미지**: Dockerfile을 기반으로 `docker build` 명령으로 만들어지는 결과물
- **컨테이너**: 이미지를 실제로 실행했을 때 생성되는 실행 인스턴스

즉, **빌드 결과물은 이미지이고, 실행 결과물은 컨테이너**다. 이미지는 스스로 동작하지 않고, 컨테이너는 실제로 프로세스를 실행하며 동작한다. 또한 이미지는 한 번 빌드되면 고정된 결과물이지만, 컨테이너는 실행 중 로그가 쌓이거나 임시 파일이 생기는 등 상태가 변할 수 있다.

---

## 7. Dockerfile 기반 커스텀 이미지 제작

### 7-1. 베이스 이미지

- `nginx:alpine`

### 7-2. Dockerfile

```dockerfile
FROM nginx:alpine

LABEL org.opencontainers.image.title="my-custom-nginx"
ENV APP_ENV=dev

COPY app/ /usr/share/nginx/html/
```

### 7-3. `app/index.html`

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <title>My Docker Web</title>
</head>
<body>
  <h1>Hello from custom Docker image</h1>
  <p>이 페이지는 Dockerfile로 빌드된 웹 서버입니다.</p>
</body>
</html>
```

### 7-4. 빌드 및 실행

```zsh
$ docker build -t my-web:1.0 .
[+] Building 0.9s (7/7) FINISHED                                                                                                                                                   docker:orbstack
 => [internal] load build definition from Dockerfile                                                                                                                                          0.1s
 => => transferring dockerfile: 161B                                                                                                                                                          0.0s
 => [internal] load metadata for docker.io/library/nginx:alpine                                                                                                                               0.0s
 => [internal] load .dockerignore                                                                                                                                                             0.1s
 => => transferring context: 2B                                                                                                                                                               0.0s
 => [internal] load build context                                                                                                                                                             0.1s
 => => transferring context: 299B                                                                                                                                                             0.0s
 => CACHED [1/2] FROM docker.io/library/nginx:alpine                                                                                                                                          0.0s
 => [2/2] COPY app/ /usr/share/nginx/html/                                                                                                                                                    0.2s
 => exporting to image                                                                                                                                                                        0.2s
 => => exporting layers                                                                                                                                                                       0.1s
 => => writing image sha256:49d94329c75b5a741a60f8b877bd4367cb6b505c20b54ee8337da76f953e8cb6                                                                                                  0.0s
 => => naming to docker.io/library/my-web:1.0  

$ docker run -d --name my-web -p 8080:80 my-web:1.0
e43a3960e0a3f5aa737a97e1bb2171f9dd5b8c9a8fb2e5e1d2862aaa6255c4ba
```

### 7-5. 확인

```zsh
$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

$ docker logs my-web
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2026/03/30 11:27:58 [notice] 1#1: using the "epoll" event method
2026/03/30 11:27:58 [notice] 1#1: nginx/1.29.7
2026/03/30 11:27:58 [notice] 1#1: built by gcc 15.2.0 (Alpine 15.2.0) 
2026/03/30 11:27:58 [notice] 1#1: OS: Linux 6.17.8-orbstack-00308-g8f9c941121b1
2026/03/30 11:27:58 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 20480:1048576
2026/03/30 11:27:58 [notice] 1#1: start worker processes
2026/03/30 11:27:58 [notice] 1#1: start worker process 30
2026/03/30 11:27:58 [notice] 1#1: start worker process 31
2026/03/30 11:27:58 [notice] 1#1: start worker process 32
2026/03/30 11:27:58 [notice] 1#1: start worker process 33
2026/03/30 11:27:58 [notice] 1#1: start worker process 34
2026/03/30 11:27:58 [notice] 1#1: start worker process 35

$ curl http://localhost:8080
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <title>My Docker Web</title>
</head>
<body>
  <h1>Hello from custom Docker image</h1>
  <p>이 페이지는 Dockerfile로 빌드된 웹 서버입니다.</p>
</body>
</html>
```

![docker-web-success](docs/screenshots/docker-web-success.png)

---

## 8. 포트 매핑 검증

```zsh
$ docker run -d --name my-web-8080 -p 8080:80 my-web:1.0
1a5d55d9e4dd85d2355fe61364feedd7cda6a816747889d5164d3d9dea72223d
```

- `-p 8080:80` = 호스트 `8080` 포트를 컨테이너 `80` 포트에 연결
- 브라우저에서 `localhost:8080`으로 접속 가능

포트 매핑은 아래 형식으로 고정해서 기록했다.

```zsh
docker run -d --name my-web -p 8080:80 my-web:1.0
```

이 명령은 항상 다음 규칙으로 읽힌다.

- 호스트 포트: `8080`
- 컨테이너 포트: `80`
- 이미지: `my-web:1.0`
- 컨테이너 이름: `my-web`

즉, README에서 **호스트 포트:컨테이너 포트** 순서를 명확히 고정해서 설명했기 때문에, 다른 사람이 같은 포트 구조를 그대로 재현할 수 있다.

또한 컨테이너 내부에서 실행되는 웹 서버는 컨테이너 내부 네트워크의 포트를 사용하므로, 호스트 브라우저가 자동으로 접근할 수 없다. 그래서 `-p 8080:80`처럼 **호스트 포트와 컨테이너 포트를 연결하는 포트 매핑이 필요하다.**

---

## 9. 바인드 마운트 검증

```zsh
$ docker run -d --name bind-web -p 8081:80 \
  -v $(pwd)/app:/usr/share/nginx/html \
  nginx:alpine
Unable to find image 'nginx:alpine' locally
alpine: Pulling from library/nginx
589002ba0eae: Already exists
8892f80f46a0: Already exists
91d1c9c22f2c: Already exists
cf1159c696ee: Already exists
3f4ad4352d4f: Already exists
c2bd5ab17727: Already exists
4d9d41f3822d: Already exists
3370263bc02a: Already exists
Digest: sha256:e7257f1ef28ba17cf7c248cb8ccf6f0c6e0228ab9c315c152f9c203cd34cf6d1
Status: Downloaded newer image for nginx:alpine
48a5a7ae7ddeb9df2e4b78998c35579ccd7986e1617ec9d3ff9800c5b5aa9cf7
```


![docker-web-bind-before](docs/screenshots/docker-web-bind-before.png)
![docker-web-bind-after](docs/screenshots/docker-web-bind-after.png)

바인드 마운트를 사용하면 호스트의 `app` 디렉토리 변경 사항이 컨테이너 웹 루트에 즉시 반영된다.

bind mount 실습은 포트 충돌을 피하기 위해 별도 포트를 사용했다.

```zsh
docker run -d --name bind-web -p 8081:80 -v $(pwd)/app:/usr/share/nginx/html nginx:alpine
```

이렇게 하면 `8080`은 커스텀 이미지 검증용, `8081`은 bind mount 검증용으로 역할이 분리되어 실습 목적이 섞이지 않는다.

또한 bind mount는 호스트 디렉토리를 컨테이너에 직접 연결하는 방식이므로, 데이터가 실제로 호스트 파일시스템에 저장된다. 따라서 컨테이너가 삭제되어도 호스트 파일은 그대로 남고, 개발 중 실시간 반영에 유리하다.

---

## 10. Docker 볼륨 영속성 검증

```zsh
$ docker volume create mydata
mydata

$ docker volume ls
DRIVER    VOLUME NAME
local     mydata

$ docker run -d --name vol-test -v mydata:/data ubuntu sleep infinity
4029dc11552b7df0f9b1a28f2926079251b7a03368e0f9cfac1006f176243e12

$ docker exec -it vol-test bash -lc "echo hi > /data/hello.txt && cat /data/hello.txt"
hi

$ docker rm -f vol-test
vol-test

$ docker run -d --name vol-test2 -v mydata:/data ubuntu sleep infinity
339fd6efef405995e68c8f002d7e34acf849944b52ccbfd8ac1bc0b39e91482f

$ docker exec -it vol-test2 bash -lc "cat /data/hello.txt"
hi
```

동일한 볼륨을 새 컨테이너에 다시 연결했을 때 `hello.txt`가 유지되어 데이터 영속성을 확인했다.

볼륨은 아래 3단계 흐름으로 고정해서 정리했다.

1. 볼륨 생성
2. 첫 번째 컨테이너에 연결 후 데이터 생성
3. 첫 번째 컨테이너 삭제 후 새 컨테이너에 같은 볼륨 재연결

이 구조의 핵심은 **볼륨 이름(`mydata`)을 기준으로 데이터를 분리 저장**하고, 컨테이너 이름은 달라도 같은 볼륨을 붙이면 데이터가 유지된다는 점을 검증하는 것이다.

즉, 컨테이너 삭제 후 데이터가 사라지는 문제를 막으려면 컨테이너 내부에만 저장하지 말고, **Docker 볼륨 또는 bind mount로 외부 저장소를 연결해야 한다.** 이번 과제 기준으로는 데이터 소실 방지가 핵심이면 볼륨이 더 적절하다.

---

## 11. Git 설정 및 GitHub / VSCode 연동

### 11-1. Git 설정

```zsh
$ git config --global user.name "shannonlee-dev"
$ git config --global user.email "~~~~@~~.com"
$ git config --global init.defaultBranch main
$ git config --list
credential.helper=osxkeychain
user.name=shannonlee-dev
user.email=shannon.lee.dev@*****.com
init.defaultbranch=main
core.repositoryformatversion=0
core.filemode=true
core.bare=false
core.logallrefupdates=true
core.ignorecase=true
core.precomposeunicode=true
```

### 11-2. 저장소 초기화 및 push

```zsh
$ git init
Initialized empty Git repository in /Users/shh921shh4393/dev/dev-workstation-mission/.git/
$ git add .
$ git commit -m "개발환경 구축"
[main (root-commit) 16cdf58] 개발환경 구축
 4 files changed, 593 insertions(+)
 create mode 100644 Dockerfile
 create mode 100644 README.md
 create mode 100644 app/index.html
 create mode 100644 docs/screenshots/docker-web-success.png
$ git remote add origin https://github.com/shannonlee-dev/Codyssey2026.git
$ git push -u origin main 
Enumerating objects: 9, done.
Counting objects: 100% (9/9), done.
Delta compression using up to 6 threads
Compressing objects: 100% (6/6), done.
Writing objects: 100% (9/9), 7.18 KiB | 7.18 MiB/s, done.
Total 9 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To https://github.com/shannonlee-dev/Codyssey2026.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

### 11-3. VSCode / GitHub 연동

![vscode-github-login](docs/screenshots/vscode-github-login.png)

---

## 12. 검증 방법 및 결과 위치

| 항목 | 검증 방법 | 결과 위치 |
|---|---|---|
| 터미널 조작 | `pwd`, `ls -la`, `mkdir`, `touch`, `cp`, `mv`, `rm`, `cat` | 3장 |
| 파일 권한 | `ls -ld`, `chmod` | 4장 |
| Docker 설치/점검 | `docker --version`, `docker info` | 5장 |
| 컨테이너 기본 실행 | `docker run hello-world` | 6장 |
| Ubuntu 진입 | `docker run -it ubuntu bash` | 6장 |
| Docker 운영 명령 | `docker images`, `docker ps`, `docker ps -a`, `docker logs`, `docker stats` | 6장 |
| 커스텀 이미지 | `docker build`, `docker run`, `curl` | 7장 |
| 포트 매핑 | `-p 8080:80` + 브라우저 접속 | 8장 |
| 바인드 마운트 | `-v $(pwd)/app:/usr/share/nginx/html` | 9장 |
| 볼륨 영속성 | `docker volume create`, `docker exec`, 컨테이너 재생성 | 10장 |
| Git 설정 | `git config --list` | 11장 |
| GitHub/VSCode 연동 | 연동 화면 스크린샷 | 11장 |

---

## 13. 트러블슈팅

### 문제 1. `docker info` 실행 실패

- 문제: `Cannot connect to the Docker daemon`
- 원인 가설: Docker 엔진이 실행되지 않음
- 확인: OrbStack 앱이 꺼져 있었음
- 해결: OrbStack 실행 후 `docker info` 재시도

### 문제 2. 브라우저 접속 실패

- 문제: `localhost:8080` 접속 불가
- 원인 가설: 포트 매핑 누락 또는 잘못된 포트 지정
- 확인: `docker ps`에서 `PORTS` 항목 확인
- 해결: `-p 8080:80`으로 다시 실행

포트 매핑 실패는 보통 호스트 포트 충돌 때문에 발생한다. 이 경우 아래 순서로 진단하는 것이 합리적이다.

1. `docker run -p 8080:80 ...` 실행 시 출력되는 에러 메시지를 확인한다
2. `docker ps`로 현재 실행 중인 컨테이너가 같은 포트를 점유 중인지 확인한다
3. 필요하면 `lsof -i :8080` 또는 `sudo lsof -iTCP:8080 -sTCP:LISTEN`으로 호스트 프로세스를 확인한다
4. 원인에 따라 컨테이너를 중지/삭제하거나, 다른 호스트 포트를 사용한다
5. 다시 `docker ps`와 브라우저 접속으로 정상 매핑 여부를 검증한다

### 문제 3. Ubuntu 컨테이너 `zsh` 진입 실패

- 문제: `docker run -it ubuntu zsh` 동작 불가
- 원인 가설: 기본 `ubuntu` 이미지에 `zsh` 미설치
- 확인: `bash`로는 정상 진입 가능
- 해결: 실습을 `bash` 기준으로 통일

---

## 14. 수행 체크리스트

- [x] 프로젝트 개요가 있다
- [x] 실행 환경(OS/쉘/터미널/Docker/Git)이 있다
- [x] 터미널 조작 로그가 있다
- [x] 파일 권한 실습 전/후가 있다
- [x] docker --version, docker info 결과가 있다
- [x] docker images / ps / ps -a / logs / stats 결과가 있다
- [x] hello-world 실행 증거가 있다
- [x] ubuntu 컨테이너 진입 증거가 있다
- [x] Dockerfile, app 소스가 저장소에 있다
- [x] 커스텀 이미지 빌드/실행 로그가 있다
- [x] 포트 매핑 접속 증거가 있다
- [x] bind mount 전/후 비교가 있다
- [x] volume 영속성 검증이 있다
- [x] git config --list 결과가 있다
- [x] GitHub / VSCode 연동 증거가 있다
- [x] 트러블슈팅 2건 이상 있다
- [x] 민감정보가 가려져 있다
