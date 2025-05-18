## 실시간 데이터 처리 흐름

이 애플리케이션은 Apache Flink와 DataGen 커넥터를 활용한 실시간 데이터 파이프라인 예제입니다.

1. **소스(DataGen)**
   - `user_id`, `user_name`, `score`, `event_time` 필드를 포함한 가상 데이터를 실시간으로 생성합니다.
   - 초당 5개의 행을 무작위 값으로 생성합니다.
2. **변환(Transformation)**
   - `score`가 50 이하인 레코드는 필터링합니다.
   - `user_name`을 대문자로 변환합니다.
   - `score`를 소수점 둘째 자리까지 반올림합니다.
3. **싱크(Print Connector)**
   - 처리된 결과를 Flink의 print 커넥터를 통해 콘솔(로그)로 출력합니다.

**SQL 처리 요약:**
- 파이프라인은 `datagen_source` 테이블에서 데이터를 읽고, 필터 및 변환을 적용한 뒤 결과를 `print_sink` 테이블에 기록합니다.
- `score > 50`인 데이터만 처리 및 출력됩니다.

이 흐름은 외부 데이터 소스 없이 실시간 스트림 처리 로직을 테스트하거나 프로토타이핑할 때 유용합니다.

## 실행 방법

1. Python 파일을 Flink JobManager 컨테이너로 복사합니다.
   ```bash
   docker cp flink_app.py jobmanager-1:/opt/flink/app/
   ```
2. 컨테이너에서 Python 작업을 실행합니다.
   ```bash
   docker exec -it jobmanager-1 flink run -py /opt/flink/app/flink_app.py
   ```