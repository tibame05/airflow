import os
from datetime import timedelta
# 從 Airflow 匯入 DockerOperator，用來在 DAG 中執行 Docker 容器任務
from airflow.providers.docker.operators.docker import DockerOperator

# Swarm secret 會掛在這個路徑
SECRET_ENV_PATH = "/run/secrets/web_crawler_env"


def _load_crawler_env(path: str = SECRET_ENV_PATH) -> dict:
    """
    從 /run/secrets/web_crawler_env 讀取 KEY=VALUE 形式的內容，
    轉成 dict，給 DockerOperator 的 environment 使用。
    """
    envs: dict[str, str] = {}
    if not os.path.exists(path):
        return envs

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            envs[key] = value
    return envs


def create_producer_task_tw() -> DockerOperator:
    crawler_env = _load_crawler_env()

    return DockerOperator(
        task_id="producer_main_tw",
        image="winston07291/web_crawler_etf:0.0.8.amd64",  # 換成你新 build 的 tag
        command="pipenv run python crawler/producer_main_tw.py",
        # 每次執行前都強制重新拉取最新的 image（確保使用最新版本）
        force_pull=True,
        # 容器執行完畢後自動刪除（避免堆積殘留容器）
        auto_remove=True,
        execution_timeout=timedelta(hours=1),
        # ✅ 指定容器要使用的 Docker network 名稱
        # 注意：這要是 Docker Engine 中已存在的 network 名稱
        network_mode="etf_lib_network",
        # 指定容器要使用的 queue 名稱
        queue="crawler_tw",
        environment=crawler_env,
    )


def create_producer_task_us() -> DockerOperator:
    crawler_env = _load_crawler_env()

    return DockerOperator(
        task_id="producer_main_us",
        image="winston07291/web_crawler_etf:0.0.8.amd64",  # 同上
        command="pipenv run python crawler/producer_main_us.py",
        # 每次執行前都強制重新拉取最新的 image（確保使用最新版本）
        force_pull=True,
        # 容器執行完畢後自動刪除（避免堆積殘留容器）
        auto_remove=True,
        execution_timeout=timedelta(hours=1),
        # ✅ 指定容器要使用的 Docker network 名稱
        # 注意：這要是 Docker Engine 中已存在的 network 名稱
        network_mode="etf_lib_network",
        # 指定容器要使用的 queue 名稱
        queue="crawler_us",
        environment=crawler_env,
    )