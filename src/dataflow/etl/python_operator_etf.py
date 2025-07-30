# 匯入 Airflow 所需元件
import sys
from airflow.operators.python import PythonOperator

# 將專案路徑加入 sys.path
sys.path.append('/opt/projects/web_crawler_etf')

# 匯入兩個 main 函式
from crawler.producer_main_tw import main as run_producer_tw
from crawler.producer_main_us import main as run_producer_us


# 回傳 TW 的 PythonOperator 任務
def create_producer_task_tw() -> PythonOperator:
    return PythonOperator(
        task_id="producer_main_tw",
        python_callable=run_producer_tw,
        queue="twse",  # 可加上 queue，如果使用 CeleryExecutor 等
    )


# 回傳 US 的 PythonOperator 任務
def create_producer_task_us() -> PythonOperator:
    return PythonOperator(
        task_id="producer_main_us",
        python_callable=run_producer_us,
        queue="tpex",
    )
