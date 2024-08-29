sudo apt update
sudo apt -y install build-essential
sudo apt -y install git

cd ../
wget https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-x86_64.sh
    
sh Anaconda3-2024.06-1-Linux-x86_64.sh -b -u

cd anaconda3/bin/
echo 'export PATH=$PATH:$(pwd)' >> ~/.bashrc

source ~/.bashrc

conda install -y pytorch torchvision torchaudio cpuonly -c pytorch

pip install -q flwr[simulation] flwr-datasets[vision] torch torchvision


