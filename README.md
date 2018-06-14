# hirebob
Opensource Job portal

# Configure application via Docker
1. Run Dockerfile 
# docker build -t hirebob .
2. Get newly created docker images id
# docker images
3. Run Docker image
# docker run -itd -p (localport)8000:8000 (image-id)
4. Open application web console on "<machine-ip:<localport>/portal>"

