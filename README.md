# RSEProject - Smart Door Unlock


## To Get Started
### Generate SSH key
```
cd ~/
cd .ssh
cat id_rsa.pub
```
Copy the entire string after ssh-rsa and send it to James so he can add you to the aws server. Once you have been given access to the server,
```
ssh ec2-user@3.19.39.220
sudo python cloud.py
```
This will run the cloud.py file. Copy and past the IP address into preferred browser and the results will be shown there.

