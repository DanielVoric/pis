## Warehouse managment

This project is a warehouse managment application used for adding, editing, deleting, filtering and sorting goods(merchandise). Table will be made out of id, name, type, quantity, entry date and exit date of goods. 

![image](https://github.com/DanielVoric/pis/assets/115411881/65bf83c6-80e2-4701-a360-b54342c33011)


## Features
-Add new goods
-Delete goods
-Update goods
-Filter goods by type
-Sort goods by entry date

## Running the Backend
Application is run by docker

#### Creating a docker image
```sh
cd pis
docker build -t warehousemanagment -f ./Dockerfile .
```

#### Running the docker image
```sh
docker run -p 5000:5000 warehousemanagment
```
