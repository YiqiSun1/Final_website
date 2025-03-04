## Mini Instagram web application

This is a tutorial project https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/. The essential idea is to create a web application deployed by docker. The web application / app is runned by Gunicorn server. The app includes postgres databases, and nginx for the dealing of static and media files. 

## Result: (uploading page)
![Alt text](picture2.png)

## After uploading, users can view the image being uploaded
![Alt text](picture1.png)


## implementation steps
1. fork this repo and cd into it. 
2. follow the tutorial and create the .env.dev file
3. run 
```
docker-compose -f docker-compose.prod.yml up -d --build
```
to bring out the container with docker images, environment variables specified in the docker-compose.pro.yml file

4. run 

```
docker-compose -f docker-compose.prod.yml exec web python manage.py create_db
``` 
to initialize postgres database 

5. perform appropraite port forwarding into port 1064

6. You should be able to upload the image through (http://localhost:8080/upload)

7. You should be able to view your image through (http://localhost:1337/media/IMAGE_FILE_NAME)




