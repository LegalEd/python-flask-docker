# python-flask-docker
Basic Python Flask app in Docker which prints the hostname and IP of the container

### Build application
Build the Docker image manually by cloning the Git repo.
```
$ git clone git@github.com:LegalEd/python-flask-docker.git
$ docker build -t python-flask-docker .
```

### Run the container
Create a container from the image.
```
$ docker run --name my-container -d -p 8080:8080 python-flask-docker
```

Now visit http://localhost:8080
```
 The hostname of the container is 982aa7321adc and its IP is 172.17.0.2. 
```

### Verify the running container
Verify by checking the container ip and hostname (ID):
```
$ docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' my-container
172.17.0.2
$ docker inspect -f '{{ .Config.Hostname }}' my-container
982aa7321adc
```


