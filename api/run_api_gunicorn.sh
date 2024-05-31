export DIFY_HOME="/home/ykuang/dify_exp"
source "$DIFY_HOME/api/env_act.sh"
cd "$DIFY_HOME/api"
gunicorn -w 4 'app:app' -b:5001

