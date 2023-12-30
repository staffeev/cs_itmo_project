from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum
from datetime import timedelta, datetime



dag = DAG(
    dag_id="purchases_profit",
    start_date=datetime(year=2023, month=12, day=29),   
    schedule=timedelta(minutes=20),
    catchup=False,
    tags=["business"],
    params={"LAB_PATH": "/home/hadoop_user/lab", "INPUT_PATH": "hdfs:///user/student/input/data.tsv"}
)

task_run_dfs = BashOperator(
    task_id="task_run_dfs",
    dag=dag,
    bash_command="if [[ $(jps | wc -l) -eq 1 ]]; then start-dfs.sh && start-yarn.sh; fi"
)

task_get_currencies = BashOperator(
    task_id="task_get_currencies",
    dag=dag,
    bash_command='curl https://open.er-api.com/v6/latest/RUB | jq -r ".rates" > {{params.LAB_PATH}}/currencies.json'
)

task_run_mapreduce = BashOperator(
    task_id="task_run_mapreduce",
    dag=dag,
    bash_command="python3 {{params.LAB_PATH}}/mapred_script.py --currencies {{params.LAB_PATH}}/currencies.json -r hadoop {{params.INPUT_PATH}} > {{params.LAB_PATH}}/output.tsv "
)

task_visualize = BashOperator(
    task_id="task_visualize_proits",
    dag=dag,
    bash_command="python3 {{params.LAB_PATH}}/visualizer.py"
)

task_get_currencies >> task_run_dfs
task_run_dfs >> task_run_mapreduce
task_run_mapreduce >> task_visualize
