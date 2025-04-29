#### on your HOST
lima nerdctl run --rm -it -p 8000:8000 -v $(pwd):/html --entrypoint bash python

#### INSIDE the container:
cd /html/
 python -m http.server 8000


# on YOUR host visit  
https://localhost:8000

