cd /home/ykuang/dify_exp/web
# source load_nvm.sh
export NVM_DIR="/home/ykuang/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
nvm use 18
npm run dev
