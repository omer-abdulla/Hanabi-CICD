ARCHITECTURE DIAGRAM 

          +------------------+
          |                  |
          |   Docker Host    |
          |                  |
          +--------|---------+
                   |
                   |
                   v
          +------------------+
          |                  |
          |    Docker        |
          |    Container     |
          |                  |
          +--------|---------+
                   |
                   |  Exposes port 80
                   |
                   v
          +------------------+
          |                  |
          |   Hello World    |
          |   Web Application|
          |                  |
          +------------------+


          1 .Basic directory structure



           |----.github/workflows
           |----Dockerfile
           |----app.py
           |----requirements.txt

           2 .requirements.txt  consists of

           FLASK 


           

