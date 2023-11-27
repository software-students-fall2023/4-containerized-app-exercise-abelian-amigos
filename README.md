# Sketchify

[![ML Client](https://github.com/software-students-fall2023/4-containerized-app-exercise-abelian-amigos/actions/workflows/test_ml.yml/badge.svg)](https://github.com/software-students-fall2023/4-containerized-app-exercise-abelian-amigos/actions/workflows/test_ml.yml) [![Web App](https://github.com/software-students-fall2023/4-containerized-app-exercise-abelian-amigos/actions/workflows/test_app.yml/badge.svg)](https://github.com/software-students-fall2023/4-containerized-app-exercise-abelian-amigos/actions/workflows/test_app.yml)

# Team Members

* [Aavishkar Gautam](https://github.com/aavishkar6)
* [Avaneesh Devkota](https://github.com/avaneeshdevkota)
* [Soyuj Jung Basnet](https://github.com/basnetsoyuj)

# Description

Sketchify is a web application that leverages the power of machine learning to transform your ordinary photos into 
captivating sketches. With just a few clicks, you can upload your favorite images or click a new picture entirely, 
and our intelligent system will create stunning sketches for you.

## Setup

### Prerequisites

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

### Running the application

1. Clone the repository
    ```shell
    git clone https://github.com/software-students-fall2023/4-containerized-app-exercise-abelian-amigos.git
    ```
2. Navigate to the project directory
    ```shell
    cd 4-containerized-app-exercise-abelian-amigos
    ```
3. Setup the environment variables
    ```shell
    cp .env.example .env
    ```
4. Build the images
    ```shell
    docker-compose build
    ```
5. Run the containers
    ```shell
    docker-compose up -d
    ```
6. Open the application in your browser
    ```shell
    http://localhost:8001
    ```
7. To stop the containers
    ```shell
    docker-compose stop
    ```
   
OR

### Accessing the deployed application

1. Open the application in your browser
    ```shell
    http://134.209.174.92
    ```
   
**Note:** You can provide camera access to the web app to take a picture directly from the browser or upload an image.


## Credits

The machine learning model used in this project is based on [AnimeGANv3 Portrait Sketch](https://github.com/TachibanaYoshino/AnimeGANv3).

## Notes and Links

* Link to the Task Board:
    * [Project Board](https://github.com/orgs/software-students-fall2023/projects/88/views/1)
* The code has been formatted in accordance with [PEP 8](https://www.python.org/dev/peps/pep-0008/) using the [black](https://black.readthedocs.io/en/stable/) formatter.
* The code has been linted using [pylint](https://www.pylint.org/).
* The Machine Learning Client and Web App are tested using Github Actions on every push to the main branch and approved pull requests.
* The coverage report for the tests can be found in the Github Actions logs. If the coverage is below 80%, the build will fail.
   ```
     Run cd machine-learning-client
     cd machine-learning-client
     pipenv run python -m coverage run -m pytest
     pipenv run python -m coverage report --include=src/**/*.py --fail-under=80
     shell: /usr/bin/bash -e {0}
     env:
       pythonLocation: /opt/hostedtoolcache/Python/3.11.6/x64
       PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.6/x64/lib/pkgconfig
       Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.6/x64
       Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.6/x64
       Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.6/x64
       LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.6/x64/lib
    ============================= test session starts ==============================
    platform linux -- Python 3.11.6, pytest-7.4.3, pluggy-1.3.0
    rootdir: /home/runner/work/4-containerized-app-exercise-abelian-amigos/4-containerized-app-exercise-abelian-amigos/machine-learning-client
    plugins: flask-1.3.0
    collected 4 items
      
    tests/test_ml.py ...                                                     [ 75%]
    tests/test_model.py .                                                    [100%]
      
    ============================== 4 passed in 4.55s ===============================
    Name                 Stmts   Miss  Cover
    ----------------------------------------
    src/__init__.py          0      0   100%
    src/main.py             40      1    98%
    src/ml_db.py             6      1    83%
    src/ml_defaults.py      14      0   100%
    src/model.py            64      4    94%
    ----------------------------------------
    TOTAL                  124      6    95%
  ```
