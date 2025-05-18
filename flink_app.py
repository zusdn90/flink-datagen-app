from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment

# 환경 설정
env = StreamExecutionEnvironment.get_execution_environment()
settings = EnvironmentSettings.in_streaming_mode()
table_env = StreamTableEnvironment.create(env, environment_settings=settings)

# DataGen 소스 테이블 생성
table_env.execute_sql("""
    CREATE TABLE datagen_source (
        user_id INT,
        user_name STRING,
        score DOUBLE,
        event_time TIMESTAMP(3),
        WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
    ) WITH (
        'connector' = 'datagen',
        'rows-per-second' = '5',
        'fields.user_id.kind' = 'random',
        'fields.user_id.min' = '1',
        'fields.user_id.max' = '1000',
        'fields.user_name.length' = '8',
        'fields.score.min' = '0',
        'fields.score.max' = '100'
    )
""")

# Print 싱크 테이블 생성
table_env.execute_sql("""
    CREATE TABLE print_sink (
        user_id INT,
        user_name STRING,
        score DOUBLE,
        event_time TIMESTAMP(3)
    ) WITH (
        'connector' = 'print'
    )
""")

# 전처리 및 삽입 로직 (필터 조건 포함)
table_env.execute_sql("""
    INSERT INTO print_sink
    SELECT
        user_id,
        UPPER(user_name) AS user_name,
        ROUND(score, 2) AS score,
        event_time
    FROM datagen_source
    WHERE score > 50
""")