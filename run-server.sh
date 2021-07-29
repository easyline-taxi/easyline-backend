# configuração de bridge para rede local
# docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 mynet

# code to bulild aplication 
docker build -t backend_easyline .
# docker run -it --net=mynet -p 8000:8000 -e DJANGO_SUPERUSER_USERNAME=admin@admin.com -e DJANGO_SUPERUSER_PASSWORD=admin -e DJANGO_SUPERUSER_EMAIL=admin@admin.com --name=backend_node -t easyline:0
docker run -it -p 8000:8000 -e DJANGO_SUPERUSER_USERNAME=admin@admin.com -e DJANGO_SUPERUSER_PASSWORD=admin -e DJANGO_SUPERUSER_EMAIL=admin@admin.com --name=backend_node -t backend_easyline
# code to run aplication