
# Ramiz_branch
# khatai branch
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from datetime import datetime, timedelta
# no conflict khatai
###############################################
# Parameters
###############################################
spark_master = "spark://172.18.0.5:7077"
spark_app_name = "SparkHelloWorld"
file_path = "/opt/airflow/airflow.cfg"
#no conflict Ramiz
###############################################
# DAG Definition
###############################################
now = datetime.now()

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(now.year, now.month, now.day),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}

dag = DAG(
        dag_id="spark-test",
        description="This DAG runs a simple Pyspark app.",
        default_args=default_args,
        schedule_interval=timedelta(1))

start = DummyOperator(task_id="start", dag=dag)

# spark_job = DummyOperator(task_id="spark_job", dag=dag)

spark_job = SparkSubmitOperator(
    task_id="spark_job",
    #  Spark application path created in airflow and spark cluster
    application="/opt/airflow/spark_apps/hello-world.py", 
    name=spark_app_name,
    conn_id="spark_default",
    verbose=False,
    # conf={"spark.master":spark_master},
    application_args=[file_path],
    dag=dag)

end = DummyOperator(task_id="end", dag=dag)

start >> spark_job >> end
