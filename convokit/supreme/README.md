To run the code in a docker container,
* Make sure your 8000 port is not busy
* Build docker image 
  ` docker build -t supreme-modals:latest .`
  
* Run docker image `docker run -dit -p 8000:8000  --name supremedock supreme-modals:latest`

You're all set!

Execute plots inside the container by running the plot scripts and view them on the browser at http://localhost:8000/