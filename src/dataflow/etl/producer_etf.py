# 從 Airflow 匯入 DockerOperator，用來在 DAG 中執行 Docker 容器任務
from airflow.operators.docker_operator import (
    DockerOperator,
)


# 建立一個 PythonOperator 任務，將上述 crawler 函式包裝成 DAG 中的一個任務
def create_producer_task_tw() -> DockerOperator:
    return DockerOperator(
        # 設定這個 task 在 DAG 中的名稱（唯一識別碼）
        task_id="producer_main_tw",
        image="peiyuji/tibame_crawler:0.0.7",
        command="pipenv run python crawler/producer_main_tw.py",
        # 每次執行前都強制重新拉取最新的 image（確保使用最新版本）
        force_pull=True,
        # 容器執行完畢後自動刪除（避免堆積殘留容器）
        auto_remove=True,
        # ✅ 指定容器要使用的 Docker network 名稱
        # 注意：這要是 Docker Engine 中已存在的 network 名稱
        network_mode="etf_lib_network",
    )

# 建立一個 DockerOperator 任務的函式，回傳一個 Airflow 的任務實例
def create_producer_task_us() -> DockerOperator:
    return DockerOperator(
        # 設定這個 task 在 DAG 中的名稱（唯一識別碼）
        task_id="producer_main_us",
        image="peiyuji/tibame_crawler:0.0.7",
        command="pipenv run python crawler/producer_main_us.py",
        # 每次執行前都強制重新拉取最新的 image（確保使用最新版本）
        force_pull=True,
        # 容器執行完畢後自動刪除（避免堆積殘留容器）
        auto_remove=True,
        # ✅ 指定容器要使用的 Docker network 名稱
        # 注意：這要是 Docker Engine 中已存在的 network 名稱
        network_mode="etf_lib_network",
    )