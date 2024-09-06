

partition_id=$1

export PATH=$PATH:/home/tejas/anaconda3/bin/
nohup python client.py --partition-id "$partition_id" > nohup.out 2>&1 &
