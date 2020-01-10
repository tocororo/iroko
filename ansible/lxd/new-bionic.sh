#bin/bash

echo container_name?

read container_name

lxc launch bionicbase $container_name

public_key=id_rsa.pub

lxc file push ~/.ssh/$public_key $container_name/root/$public_key
lxc exec $container_name  -- /bin/bash -c  "mkdir -p /root/.ssh"
lxc exec $container_name  -- /bin/bash -c "cat /root/$public_key >> /root/.ssh/authorized_keys"

echo create code disk
read code_disk

echo source_dir
read source_dir

echo dest_dir
read dest_dir

lxc config device add $container_name code disk source=$source_dir path=$dest_dir
