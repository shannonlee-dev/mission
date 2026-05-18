# 실행 예시와 내부 동작 요약

## 공통 흐름

```bash
python3 submission/mini_redis.py
```

- [submission/mini_redis.py](submission/mini_redis.py)에서 `MiniRedisCLI().run()` 시작
- [submission/mini_redis/cli.py](submission/mini_redis/cli.py)에서 입력 한 줄을 읽고 `execute_line()` 호출
- `execute_line()`이 명령을 파싱하고 각 핸들러로 분기
- [submission/mini_redis/store.py](submission/mini_redis/store.py)에서 실제 상태 변경 및 결과 문자열 반환
- `MiniRedisCLI._write_result()`가 결과 출력

## 명령별 예시와 내부 흐름

### 명령 분기 요약 (execute_line)

- `EXIT`, `QUIT`
- `SET key value` 
- `GET key` 
- `DEL key` 
- `EXISTS key` 
- `DBSIZE`
- `KEYS` 
- `CONFIG SET maxmemory value`
- `INFO memory` 
- `EXPIRE key seconds`
- `TTL key`
- `PUBLISH channel message`
- `SUBSCRIBE channel`

### SET name sisi

```bash
printf 'SET name sisi\nquit\n' | python3 submission/mini_redis.py
```

- mini_redis.py → `MiniRedisCLI().run()`
- cli.py → 사용자 입력 읽기
- cli.py → `execute_line("SET name sisi")`
- cli.py → `parts = ["SET", "name", "sisi"]`
- cli.py → `_set(parts)`
- store.py → `set("name", "sisi")`
- store.py → `_data.put("name", StoreEntry("sisi"))`
- store.py → `_add_lru("name")`
- store.py → `_evict_if_needed()`
- store.py → "OK"
- cli.py → "OK" 출력

### GET name

```bash
printf 'SET name sisi\nGET name\nquit\n' | python3 submission/mini_redis.py
```

- cli.py → `execute_line("GET name")`
- cli.py → `_get(parts)`
- store.py → `get("name")`
- store.py → `_is_expired("name")` 확인
- store.py → `_data.get("name")`로 값 획득
- store.py → `_touch_lru("name")`
- cli.py → `"sisi"` 출력 (문자열은 따옴표 포함)

### DEL name

```bash
printf 'SET name sisi\nDEL name\nquit\n' | python3 submission/mini_redis.py
```

- cli.py → `execute_line("DEL name")`
- cli.py → `_del(parts)`
- store.py → `delete("name")`
- store.py → `_delete_expired()`
- store.py → `_delete_key("name")`
- store.py → `(_data.remove, _expires.remove, _remove_lru)`
- cli.py → `(integer) 1` 출력

### EXISTS name

```bash
printf 'SET name sisi\nEXISTS name\nquit\n' | python3 submission/mini_redis.py
```

- cli.py → `execute_line("EXISTS name")`
- cli.py → `_exists(parts)`
- store.py → `exists("name")`
- store.py → `_is_expired("name")` 확인
- store.py → `_data.contains("name")`
- cli.py → `(integer) 1` 출력

### DBSIZE

```bash
printf 'SET a 1\nSET b 2\nDBSIZE\nquit\n' | python3 submission/mini_redis.py
```

- cli.py → `execute_line("DBSIZE")`
- cli.py → `_dbsize(parts)`
- store.py → `dbsize()`
- store.py → `_delete_expired()`
- store.py → `_data.size()`
- cli.py → `(integer) N` 출력

### KEYS

```bash
printf 'SET a 1\nSET b 2\nKEYS\nquit\n' | python3 submission/mini_redis.py
```

- cli.py → `execute_line("KEYS")`
- cli.py → `_keys(parts)`
- store.py → `keys()`
- store.py → `_delete_expired()`
- store.py → `_data.keys()`
- hash_map.py → 버킷별 `iter_values()`로 키 수집
- cli.py → `1. "a"` 같은 형태로 출력

### CONFIG SET maxmemory 30

```bash
printf 'CONFIG SET maxmemory 30\nquit\n' | python3 submission/mini_redis.py
```

- cli.py → `execute_line("CONFIG SET maxmemory 30")`
- cli.py → `_config(parts)`
- store.py → `config_set_maxmemory("30")`
- store.py → `_parse_non_negative_integer()`
- store.py → `_maxmemory = 30`
- store.py → `_evict_if_needed()`
- cli.py → "OK" 출력

### INFO memory

```bash
printf 'INFO memory\nquit\n' | python3 submission/mini_redis.py
```

- cli.py → `execute_line("INFO memory")`
- cli.py → `_info(parts)`
- store.py → `info_memory()`
- store.py → `_delete_expired()`
- store.py → `used_memory/maxmemory/evicted_keys` 리스트 반환
- cli.py → 줄 단위로 출력

### EXPIRE name 5

```bash
printf 'SET name sisi\nEXPIRE name 5\nquit\n' | python3 submission/mini_redis.py
```

- cli.py → `execute_line("EXPIRE name 5")`
- cli.py → `_expire(parts)`
- store.py → `expire("name", "5")`
- store.py → `_parse_integer()`
- store.py → `_expires.put("name", expire_at)`
- store.py → `_expire_heap.push(HeapItem(expire_at, "name"))`
- cli.py → `(integer) 1` 출력

### TTL name

```bash
printf 'SET name sisi\nEXPIRE name 5\nTTL name\nquit\n' | python3 submission/mini_redis.py
```

- cli.py → `execute_line("TTL name")`
- cli.py → `_ttl(parts)`
- store.py → `ttl("name")`
- store.py → `_is_expired("name")` 확인
- store.py → `_expires.get("name")`에서 만료 시간 확인
- store.py → 남은 초 계산 후 반환
- cli.py → `(integer) N` 출력

### PUBLISH news hello

```bash
printf 'SUBSCRIBE news\nPUBLISH news hello\nquit\n' | python3 submission/mini_redis.py
```

- cli.py → `execute_line("PUBLISH news hello")`
- cli.py → `_publish(parts)`
- store.py → `publish("news", "hello")`
- store.py → 채널 상태가 있으면 `messages.insert_back("hello")`
- store.py → 구독자 수 반환
- cli.py → `(integer) N` 출력

### SUBSCRIBE news

```bash
printf 'SUBSCRIBE news\nquit\n' | python3 submission/mini_redis.py
```

- cli.py → `execute_line("SUBSCRIBE news")`
- cli.py → `_subscribe(parts)`
- store.py → `subscribe("news")`
- store.py → 채널 상태가 없으면 새로 생성
- store.py → `subscribers += 1`
- cli.py → `subscribed to "news" (1)` 출력

### QUIT / EXIT

```bash
printf 'quit\n' | python3 submission/mini_redis.py
```

- cli.py → `execute_line("quit")`
- cli.py → "__QUIT__" 반환
- cli.py → REPL 루프 종료

```bash
printf 'exit\n' | python3 submission/mini_redis.py
```

- cli.py → `execute_line("exit")`
- cli.py → "__QUIT__" 반환
- cli.py → REPL 루프 종료

## 참고: 내부 자료구조 연결

- HashMap 버킷은 [submission/mini_redis/linked_list.py](submission/mini_redis/linked_list.py)의 `DoublyLinkedList`로 체이닝
- TTL은 [submission/mini_redis/min_heap.py](submission/mini_redis/min_heap.py)의 최소 힙으로 만료 우선 처리
- LRU는 `DoublyLinkedList`에 키를 보관하고 `_lru_nodes` 해시로 위치를 추적

