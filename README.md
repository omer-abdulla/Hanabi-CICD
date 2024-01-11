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

           2. requirements.txt  consists of

           FLASK 

           3. Make the flask application run locally using python app.py. Tested the root  from the browser and got the expected response

           ![requirement txt - PythonProgramming - Visual Studio Code  Administrator  11-01-2024 16_26_22](https://github.com/omer-abdulla/Hanabi-CICD/assets/98330268/f7fde2fb-4456-40a3-bccd-99ead1db2e25)  

           
           4. Dockerization: Dockerize the Python application

           
            FROM python:3.13-rc-slim

           WORKDIR /python-docker

          COPY requirements.txt requirements.txt
          RUN pip3 install -r requirements.txt

          COPY . .

         EXPOSE 8081
         
         CMD [ "python3","app.py"]


        The README provides clear steps on how to clone the repository, build the Docker image, run the Docker container, and access the application.
        It includes a section explaining the purpose of the Dockerfile and how to customize the application.
        There's a section on contributing, encouraging users to open issues or submit pull requests.
        The license information is included at the end (you may want to customize the license details as per your preferences).
        it is the executable or interpreter for the Python programming language. It tells Docker to use Python 3 to execute the script and "app.py" will be executed when the container starts. It is assumed to 
        be in the current working directory or specified path within the container.


        GIT-HUB ACTION WORKFLOW


        steps:
     - name: Checkout code
     uses: actions/checkout@v2

    - name: Set up Python
    uses: actions/setup-python@v2
    with:
      python-version: 3.8

    - name: Install Bandit
     run: pip install bandit

     - name: Run Bandit Scan
     run: bandit -ll -ii -r . -f json -o bandit-report.json -vv

    - name: Upload Artifact
     uses: actions/upload-artifact@v3
     if: always()
     with:
     name: bandit-findings
     path: bandit-report.json

    This GitHub Actions workflow checks Python code for security issues using Bandit, saving the results as an artifact. It helps ensure the project's security during development.

        
        
       image_scan:
  name: Build Image and Run Image Scan
  runs-on: ubuntu-latest

  steps:
  - name: Checkout code
    uses: actions/checkout@v2

  - name: Set up Docker
    uses: docker-practice/actions-setup-docker@v1
    with:
     docker_version: '20.10.7'

  - name: Build Docker Image
    run: docker build -f Dockerfile -t hameedakshal/hanabi-py:$GITHUB_RUN_NUMBER .

  - name: Docker Scout Scan
    run: |
      curl -fsSL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh -o install-scout.sh
      script -q -e -c "bash install-scout.sh" /dev/null

      echo ${{secrets.REPO_PASSWORD}} | docker login -u ${{secrets.REPO_USER}} --password-stdin

      docker scout quickview
       
      docker scout cves 2> error_list.txt

   - name: Upload Error List Artifact
     uses: actions/upload-artifact@v3
     with:
       name: error-list
       path: error_list.txt


  The above workflow performs a security scan using Docker Scout. Scans vulnerabilities of dockerfile layer by layer, saving the results as an artifact. It helps ensure the project's security during 
  development.

    push:
   name: Build Image and Push Image 
   runs-on: ubuntu-latest
   needs: image_scan
 
   steps:
    - name: Checkout code
      uses: actions/checkout@v2
 
    - name: Set up Docker
      uses: docker-practice/actions-setup-docker@v1
      with:
       docker_version: '20.10.7'
 
    - name: Build and Push Docker Image with build tag
      run: |
       docker build -f Dockerfile -t hameedakshal/hanabi-py:$GITHUB_RUN_NUMBER .
       echo ${{secrets.REPO_PASSWORD}} | docker login -u ${{secrets.REPO_USER}} --password-stdin
       docker push  hameedakshal/hanabi-py:$GITHUB_RUN_NUMBER
      
    - name: Tag and Push Docker Image with latest tag
      run: |
       echo ${{secrets.REPO_PASSWORD}} | docker login -u ${{secrets.REPO_USER}} --password-stdin
       docker tag  hameedakshal/hanabi-py:$GITHUB_RUN_NUMBER hameedakshal/hanabi-py:latest
       docker push hameedakshal/hanabi-py:latest

        
    The above GitHub workflow uses Docker to package and share code. It builds and pushes two versions – one with a specific tag and another with the latest tag   

           
            deploy:
         name: deploy to ebs
        runs-on: ubuntu-latest
        needs: push

     env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
         AWS_DEFAULT_REGION: ${{ secrets.AWS_DEFAULT_REGION }}
         steps:
         - uses: actions/checkout@v2
        - name: Install Python 3.9
         uses: actions/setup-python@v2
         with:
       python-version: 3.9
     - name: Install AWS CLI and Elastic Beanstalk CLI
       run: |
         sudo apt-get update
         sudo apt-get install -y awscli
         sudo apt-get install -y python3-pip
         python -m pip install --upgrade pip
         pip install awsebcli
     - name: Deploy to Elastic Beanstalk
       run: |
         eb init -r us-east-1 -p docker Hanabi-demo
         eb deploy Hanabi-demo-env 



         
