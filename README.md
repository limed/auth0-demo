Simple flask app to show auth0 authentication

#### To configure ####
```
cp config.py-dist config.py
<edit file with relevant information>
```

#### To run ####
You can run this with docker by running the following command

```
docker build -t auth0-demo .
docker run -p 8080:8080 auth0-demo
```

At this point just point your browser to port 8080
