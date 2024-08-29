sudo apt update
sudo apt -y install build-essential
sudo apt -y install git

cd /home/tejas

wget https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-x86_64.sh
    
sh Anaconda3-2024.06-1-Linux-x86_64.sh -b -u -p /home/tejas/anaconda3

export PATH=$PATH:/home/tejas/anaconda3/bin/

conda install -y pytorch torchvision torchaudio cpuonly -c pytorch

pip install -q flwr[simulation] flwr-datasets[vision] torch torchvision


