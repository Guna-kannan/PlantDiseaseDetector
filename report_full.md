**PLANT DISEASE DETECTOR**

*CNN-Based Leaf Disease Classification with FastAPI and Docker*

*Submitted by*

**Satya Sriram Prakash P \[RA2411026010501\]**

**Guna K \[RA2411026010476\]**

**Shahma Saidali Thoppasheri \[RA2411026010434\]**

*Under the Guidance of*

**Dr. Prabakaran J**

**Assistant Professor**

**Department of Networking And Communications**

*in partial fulfillment of the requirements for the degree of*

**BACHELOR OF TECHNOLOGY**

**in**

**COMPUTER SCIENCE AND ENGINEERING**

**With specialization in AIML**

![SRM logo](media/image1.jpg "SRM"){width="2.4583333333333335in"
height="1.1296292650918636in"}

**DEPARTMENT OF COMPUTATIONAL INTELLIGENCE**

**COLLEGE OF ENGINEERING AND TECHNOLOGY**

**SRM INSTITUTE OF SCIENCE AND TECHNOLOGY**

**KATTANKULATHUR-- 603 203**

**NOV 2026**

+----------------------------------+----------------------------------+
| ![SRM                            | SRM INSTITUTE OF SCIENCE &       |
| logo](media/image2.jpg "SR       | TECHNOLOGY                       |
| M"){width="1.7708333333333333in" |                                  |
| height="0.6354166666666666in"}   | COLLEGE OF ENGINEERING &         |
|                                  | TECHNOLOGY                       |
|                                  |                                  |
|                                  | S.R.M. NAGAR, KATTANKULATHUR --  |
|                                  | 603 203                          |
+----------------------------------+----------------------------------+

**BONAFIDE CERTIFICATE**

Certified that this project report **Plant Disease Detector** is the
bonafide work of **Satya Sriram Prakash P \[RA2411026010501\]**, **Guna
K** **\[RA2411026010501\], Shahma Saidali Thoppasheri**
**\[RA2411026010501\]** of \[III Year/V Sem\] B.Tech. (CSE) who carried
out the capstone project work under my supervision for the course
\[21CSE216P - Linux and Container Technologies\] in SRM Institute of
Science and Technology during the academic year \[2026-2027 (ODD SEM)\].

**Date:**

+--------------------------+------------------------------------------+
| **Faculty in Charge**    | **Head of the Department**               |
|                          |                                          |
| Dr. Prabakaran J         | Dr. Annie Uthra R                        |
|                          |                                          |
| Assistant Professor      | Head & Professor                         |
|                          |                                          |
| Department of Networking | Department of Computational Intelligence |
|                          |                                          |
| And Communications       | SRMIST - KTR                             |
|                          |                                          |
| SRMIST - KTR             |                                          |
+--------------------------+------------------------------------------+

**ABSTRACT**

**TABLE OF CONTENTS**

  ----------------- ---------------------------------------- --------------
  **Chapter No.**   **Title**                                **Page No.**
  1                 **ABSTRACT**                             3
                    TABLE OF CONTENTS                        4
                    LIST OF FIGURES                          5
                    ABBREVIATIONS                            6
  2                 **INTRODUCTION**                         **7**
                    1.1 Introduction                         7
                    1.2 Problem Statement                    8
                    1.3 Objectives                           8
                    1.4 Scope and Applications               9
                    1.5 Tools Used                           10
  3                 **APPLICATION DESIGN**                   **11**
                    2.1 Architecture                         11
                    2.2 Module Design                        17
  4                 **CONTAINERIZING THE APPLICATION**       **20**
                    3.1 Container File                       20
                    3.2 Build and Test the Container         21
                    3.3 Run and Manage Containers            24
                    3.4 Use Container Lifecycle Operations   25
                    3.5 Upload in GitHub Repository          26
                    3.6 Push the Container in Registry       27
  5                 **CHALLENGES FACED AND SOLUTIONS**       **29**
  6                 **CONCLUSION**                           **31**
  7                 **REFERENCES**                           **33**
                                                             
  ----------------- ---------------------------------------- --------------

**LIST OF FIGURES**

  ------------- ---------------------------------------------------- --------------
  **Fig No.**   **Figure Name**                                      **Page No.**
  2.1           Working Flow Diagram of the Plant Disease Detector   11
  2.1.1.1       Front end user interface                             12
  2.1.1.2       Front end output demonstration                       12
  2.1.2.1       Working code of backend layer (app.py)               14
  2.1.3.1       CNN architecture of the model layer                  16
  2.1.4.1       Containerization layer and port/volume mapping       17
  3.1.1         Dockerfile of the application                        20
  3.1.2         Python dependencies (requirements.txt)               21
  3.2.1         Building the container image                         22
  3.2.2         Testing the running container                        23
  3.3.1         docker-compose.yml configuration                     24
  3.3.2         Starting the service with Docker Compose             25
  3.4.1         Checking container lifecycle operations              26
  3.5.1         Using git commands to push the repository            27
  3.5.2         Verifying the upload on GitHub                       27
  3.6.1         Pushing the container image to the registry          28
  3.6.2         Verifying the completion of upload                   28
  2.1.3.2       Confusion matrix of the trained model                16
  ------------- ---------------------------------------------------- --------------

**ABBREVIATIONS**

  ----------- ------------------------------------------------
  **API**     Application Programming Interface
  **ASGI**    Asynchronous Server Gateway Interface
  **CI/CD**   Continuous Integration / Continuous Deployment
  **CNN**     Convolutional Neural Network
  **CPU**     Central Processing Unit
  **CSS**     Cascading Style Sheets
  **DL**      Deep Learning
  **GPU**     Graphics Processing Unit
  **HTML**    Hypertext Markup Language
  **HTTP**    Hypertext Transfer Protocol
  **IDE**     Integrated Development Environment
  **JSON**    JavaScript Object Notation
  **ML**      Machine Learning
  **OCI**     Open Container Initiative
  **OS**      Operating System
  **REST**    Representational State Transfer
  **RGB**     Red, Green, Blue
  **UI**      User Interface
  **URL**     Uniform Resource Locator
  **VM**      Virtual Machine
  **YAML**    YAML Ain't Markup Language
  ----------- ------------------------------------------------

**CHAPTER 1**

INTRODUCTION
============

1.1 Introduction
----------------

Agriculture remains the backbone of food production worldwide, yet crop
diseases continue to cause significant losses every season. Fungal,
bacterial and viral infections spread quickly through a field, and the
symptoms that appear on leaves -- spots, lesions, mould, curling or
discolouration -- are often the first and only warning a farmer
receives. Identifying the exact disease normally requires an
agricultural expert or a laboratory test, which may be slow, costly or
simply unavailable in remote areas. A delayed or incorrect diagnosis
leads to unnecessary pesticide use, reduced yield and higher cost of
cultivation.

Advances in **deep learning** have made it possible to recognise such
visual symptoms automatically. A **Convolutional Neural Network (CNN)**
learns hierarchical visual features directly from labelled images,
starting from simple edges and textures and moving up to complex lesion
patterns. Public datasets such as **PlantVillage**, which contains
thousands of labelled photographs of healthy and diseased leaves, have
made it practical to train classifiers that identify crop diseases from
a single leaf image.

This project, **Plant Disease Detector**, builds a complete and
deployable application around such a classifier. A custom CNN trained
with **TensorFlow/Keras** recognises **15 classes** spanning **Tomato,
Potato and Bell Pepper** leaves. For every uploaded image the system
reports the predicted class, a confidence score, a severity level (None,
Moderate or High), a short description of the disease, a recommended
treatment and the three most likely candidate classes. The model is
served through a **FastAPI** application that offers both a browser
interface and a REST API.

A trained model is only useful when it can be run reliably by someone
else on another machine. The project therefore encapsulates the web
service and all of its dependencies inside a **Docker container**.
Containerization removes the "works on my machine" problem: the same
image runs identically on a developer laptop, a lab server or a cloud
virtual machine. The project documents the full workflow -- designing
the application, writing the Dockerfile, building and testing the image,
running it with Docker Compose, managing the container lifecycle,
publishing the source code to GitHub and distributing the image through
a registry -- making it a practical demonstration of **Linux container
technology applied to machine-learning inference**.

1.2 Problem Statement
---------------------

Early and accurate identification of leaf diseases is difficult for
growers who lack expert support. At the same time, machine-learning
applications that do exist are hard to deploy consistently. Python
projects that depend on TensorFlow, specific NumPy versions and
image-processing libraries frequently fail when moved between machines.
The main problems addressed are:

-   Manual diagnosis of leaf diseases is slow, subjective and dependent
    on scarce expertise.

-   Users receive a label but no practical guidance such as severity or
    treatment advice.

-   Dependency conflicts and version mismatches make ML applications
    difficult to reproduce on a new system.

-   Trained model files, uploaded images and application code are
    tightly coupled, which complicates updates and redeployment.

The central question answered by this project is:

*How can a lightweight, accurate and portable plant-disease detection
service be built so that it can be deployed identically on any
Linux-capable host?*

The proposed solution combines a **CNN classifier** with a **FastAPI**
service and packages everything as a **Docker image**. Model artefacts
and uploaded images are kept outside the image through mounted volumes,
which gives:

-   Environment consistency and portability across heterogeneous
    systems.

-   One-command deployment on any host that supports Docker.

-   The ability to retrain and replace the model without rebuilding the
    image.

-   A clean path towards scaling with orchestration platforms such as
    Kubernetes.

1.3 Objectives
--------------

The objectives of the project are both technical and educational: to
build a working disease-detection system and to apply the container
workflow end to end.

1.  **Train a CNN classifier** on the PlantVillage dataset to recognise
    15 classes of Tomato, Potato and Bell Pepper leaves.

2.  **Provide actionable output** for each prediction -- confidence,
    severity, description, treatment and the top three candidate
    classes.

3.  **Develop a REST API** with FastAPI exposing endpoints for
    prediction, health checking and class listing.

4.  **Build a web interface** that lets a user upload a leaf image and
    view the diagnosis in a browser.

5.  **Containerize the application** with a Dockerfile to achieve
    isolation, reproducibility and portability.

6.  **Use Docker Compose** to define port mapping, volumes and restart
    policy declaratively.

7.  **Demonstrate container lifecycle operations** such as build, run,
    stop, restart, inspect and remove.

8.  **Publish the project to GitHub** and push the image to a container
    registry to show how it can be distributed.

9.  **Document the complete workflow** following academic and industrial
    documentation standards.

1.4 Scope and Applications
--------------------------

The scope of the project covers the complete life cycle of a small
machine-learning service: data preparation, model training, inference
through an API, a browser front end, containerization and distribution.
It focuses on three areas:

-   **Model Development:** training and evaluating a CNN for 15
    leaf-health classes using an 80/10/10 train-validation-test split
    and data augmentation.

-   **Service Design:** exposing the model through a FastAPI application
    with input validation, structured JSON responses and clear error
    handling.

-   **Containerization and DevOps:** packaging, running and distributing
    the service using Docker, Docker Compose, Git and GitHub.

**Limitations.** The classifier supports only the 15 classes listed in
this report; images of other crops or diseases will be assigned to the
closest supported class. The PlantVillage images are captured under
controlled conditions, so accuracy on photographs taken in the field
with cluttered backgrounds may be lower. The treatment text is advisory
and does not replace the advice of an agronomist.

**Applications of the Project:**

1.  **Farm-level screening:** growers can photograph a suspicious leaf
    and obtain a quick first diagnosis with guidance on next steps.

2.  **Agricultural extension services:** field officers can use the
    service as a decision-support aid when advising farmers.

3.  **Education:** a teaching example that combines computer vision, web
    APIs and container technology in a single project.

4.  **Research and prototyping:** a baseline that can be extended with
    new crops, transfer learning or mobile applications.

5.  **DevOps demonstration:** a realistic example of packaging a
    TensorFlow application for repeatable deployment.

1.5 Tools Used
--------------

The following tools and technologies were used to build, containerize
and distribute the application:

  ---------------------- ------------------------------- ---------------------------------------------------------
  **Category**           **Tool / Technology**           **Purpose / Description**
  Programming Language   **Python 3.10**                 Model training, backend logic and scripting
  Deep Learning          **TensorFlow / Keras 2.15**     Building, training and running the CNN
  Numerical / Imaging    **NumPy, Pillow, Matplotlib**   Array handling, image decoding and training-curve plots
  Web Framework          **FastAPI 0.111**               REST API, request validation and routing
  ASGI Server            **Uvicorn**                     Serving the FastAPI application inside the container
  Templating             **Jinja2**                      Rendering the HTML upload page
  Dataset                **PlantVillage (Kaggle)**       Labelled leaf images for training and evaluation
  Container Engine       **Docker**                      Building images and running containers
  Orchestration          **Docker Compose**              Declarative port, volume and restart configuration
  Version Control        **Git and GitHub**              Source-code management and sharing
  Operating System       **Linux (Ubuntu)**              Host platform for development and containers
  Editor / IDE           **Visual Studio Code**          Code development and debugging
  ---------------------- ------------------------------- ---------------------------------------------------------

**CHAPTER 2**

APPLICATION DESIGN
==================

2.1 Architecture
----------------

The architecture is designed for simplicity, maintainability and ease of
containerization. It follows a layered structure in which the front end,
the backend API, the model layer and the container layer each have a
single responsibility. The request flow begins when a user uploads a
leaf image through the browser. The backend verifies that the upload is
an image and that the trained model has been loaded, preprocesses the
image, runs the CNN, looks up the description, treatment and severity of
the winning class, and returns a JSON response that the interface
displays. The complete flow is shown in Figure 2.1.

![Figure](media/image3.png "Figure"){width="4.697916666666667in"
height="5.314815179352581in"}

**Fig 2.1 Working Flow Diagram of the Plant Disease Detector**

### 2.1.1 Frontend Layer

The **Frontend Layer** is a lightweight HTML page (templates/index.html)
rendered by FastAPI through **Jinja2** and served at the root route /.
Static assets and uploaded images are served from the static/ directory.
The page requires no separate front-end build and runs in any modern
desktop or mobile browser, which keeps the container small and simple.

**Key Functionalities:**

-   Selecting or uploading a leaf image from the user's device.

-   Sending the image to the backend /predict endpoint using an HTTP
    POST request.

-   Displaying the predicted disease, confidence score, severity level,
    description and recommended treatment.

-   Listing the top three candidate classes so the user can see how
    certain the model is.

-   Showing a clear error message when the upload is invalid or the
    model is not available.

  --------------------------------------------------------------------
  ![](media/image4.png){width="6.75in" height="3.220833333333333in"}
  --------------------------------------------------------------------

**Fig 2.1.1.1 Front end user interface**

**Fig 2.1.1.2 Front end output demonstration**

### 2.1.2 Backend Layer

The **Backend Layer** is implemented with **FastAPI**, a modern Python
framework that provides automatic request validation, asynchronous
handling and built-in API documentation. The application (app.py) is
served by **Uvicorn**, an ASGI server, and is the only component that
communicates with both the browser and the model. FastAPI was chosen for
its performance, clean type-annotated code and ease of containerization.

**API Endpoints:**

  ----------- ------------ ------------------------------------------------------------
  **Route**   **Method**   **Description**
  /           GET          Returns the web upload interface
  /predict    POST         Accepts an image upload and returns the prediction as JSON
  /health     GET          Returns service status and whether the model is loaded
  /classes    GET          Returns all supported class names and their total count
  ----------- ------------ ------------------------------------------------------------

**Key Functionalities:**

1.  **Model loading at start-up:** when the application starts it checks
    for models/plant\_disease\_model.keras and loads it; if the file is
    missing, a warning explaining how to train the model is logged.

2.  **Validation:** the /predict route rejects any upload whose content
    type does not start with image/ with HTTP 400.

3.  **Model availability check:** if no model is loaded the route
    returns HTTP 503 with a message to train the model first.

4.  **Error handling:** invalid images raise HTTP 400, unexpected
    failures raise HTTP 500, and a custom handler returns every error as
    {\"error\": \...}.

5.  **Logging:** start-up status and prediction failures are recorded
    through Python's logging module.

![](media/image5.png){width="6.75in" height="3.775in"}

![](media/image6.png){width="6.75in" height="3.6798611111111112in"}

**Fig 2.1.2.1 Working code of backend layer (app.py)**

A successful call to /predict returns a structured JSON document. The
top3 list gives the three most probable classes with their confidence
values, and is\_healthy lets client applications distinguish healthy
leaves from diseased ones without parsing the class name.

### 2.1.3 Model Layer

The **Model Layer** is the core of the system. It defines the CNN,
trains it on the PlantVillage dataset, stores the trained network as
models/plant\_disease\_model.keras, and provides the predictor that the
API uses at run time. The code is organised in the src/ package:
model.py holds the class list and training logic, and predictor.py loads
the saved model and converts an uploaded image into a prediction.

**A. Supported Classes**

The model recognises 15 classes. Each class carries a crop name and a
severity level used by the application when producing its
recommendation.

  --------------------------------------------------- ------------- ----------- --------------
  **Class name**                                      **Crop**      **Cause**   **Severity**
  Pepper\_\_bell\_\_\_Bacterial\_spot                 Bell Pepper   Bacterial   Moderate
  Pepper\_\_bell\_\_\_healthy                         Bell Pepper   Healthy     None
  Potato\_\_\_Early\_blight                           Potato        Fungal      Moderate
  Potato\_\_\_Late\_blight                            Potato        Oomycete    High
  Potato\_\_\_healthy                                 Potato        Healthy     None
  Tomato\_Bacterial\_spot                             Tomato        Bacterial   Moderate
  Tomato\_Early\_blight                               Tomato        Fungal      Moderate
  Tomato\_Late\_blight                                Tomato        Oomycete    High
  Tomato\_Leaf\_Mold                                  Tomato        Fungal      Moderate
  Tomato\_Septoria\_leaf\_spot                        Tomato        Fungal      Moderate
  Tomato\_Spider\_mites\_Two\_spotted\_spider\_mite   Tomato        Pest        Moderate
  Tomato\_\_Target\_Spot                              Tomato        Fungal      Moderate
  Tomato\_\_Tomato\_YellowLeaf\_\_Curl\_Virus         Tomato        Viral       High
  Tomato\_\_Tomato\_mosaic\_virus                     Tomato        Viral       High
  Tomato\_healthy                                     Tomato        Healthy     None
  --------------------------------------------------- ------------- ----------- --------------

The "Cause" column is added here for explanation; the class names, crops
and severity levels follow the project documentation. Of the 15 classes,
3 are healthy, 8 are rated Moderate and 4 are rated High (Potato and
Tomato Late blight, Tomato Yellow Leaf Curl Virus and Tomato mosaic
virus).

**B. Network Architecture**

Input images are resized to **256 × 256** pixels and processed in
batches of 32. The network stacks six convolution--pooling stages whose
filter counts increase from 32 to 256, so that early layers capture
edges and colour patches while deeper layers capture lesion shapes and
leaf-level patterns. The resulting feature maps are flattened and passed
through a fully connected layer of 256 units with a **Dropout of 0.4**
to reduce over-fitting, followed by a 15-unit **softmax** output layer
that produces one probability per class.

![Figure](media/image7.png "Figure"){width="6.39375in" height="3.0in"}

**Fig 2.1.3.1 CNN architecture of the model layer**

**Fig 2.1.3.2 Confusion matrix of the trained model**

![](media/image20.png){width="5.0in" height="4.166666666666667in"}

**C. Training Configuration**

  ------------------------- ------------------------------------------------------------------------------------------------
  **Parameter**             **Value**
  Dataset                   PlantVillage (Kaggle), one sub-folder per class
  Data loading              tf.keras.preprocessing.image\_dataset\_from\_directory
  Input size / batch size   256 × 256 pixels / 32
  Data split                80% training, 10% validation, 10% testing
  Data augmentation         RandomFlip, RandomRotation(0.2), RandomZoom(0.1)
  Optimizer                 Adam
  Loss function             sparse\_categorical\_crossentropy
  Epochs / callbacks        11 epochs completed (early stopping, patience=5); ModelCheckpoint
  Training command          python -m src.model data/PlantVillage
  Outputs                   models/plant\_disease\_model.keras, models/training\_history.png, models/confusion\_matrix.png
  ------------------------- ------------------------------------------------------------------------------------------------

### 2.1.4 Containerization Layer

The **Containerization Layer** packages the FastAPI service, the
predictor and all Python dependencies into a portable, isolated unit
called a **container**. Unlike a virtual machine, a container shares the
host operating-system kernel and isolates the application using Linux
**namespaces** and **control groups (cgroups)**. It therefore starts in
seconds and uses far fewer resources, while still guaranteeing that the
application sees exactly the same libraries and configuration
everywhere.

The image is built from a lightweight **python:3.10-slim** base image.
The trained model and the uploaded images are deliberately **not** baked
into the image; they live on the host and are mounted into the container
at /app/models and /app/static/uploads. This separation lets a user
retrain the model, replace the file and restart the container without
rebuilding the image. The container listens on port 8000, which Docker
Compose publishes on host port 8001, as shown in Figure 2.1.4.1.

![Figure](media/image8.png "Figure"){width="6.302083333333333in"
height="4.1875in"}

**Fig 2.1.4.1 Containerization layer and port/volume mapping**

The containerization process follows a structured sequence:

1.  Describe the environment and dependencies in a **Dockerfile**.

2.  Build an image that contains the application code and all libraries.

3.  Run the image as a container using Docker or Docker Compose.

4.  Manage the lifecycle of the container: start, stop, restart, inspect
    and remove.

5.  Optionally push the image to a **container registry** for
    distribution.

2.2 Module Design
-----------------

The application is divided into five modules. Each module has a clearly
defined purpose, which keeps the code easy to test, extend and
containerize.

### 2.2.1 Model Module

The **Model Module** (src/model.py) defines the list of supported
classes (CLASS\_NAMES), builds the CNN, loads the dataset and trains the
network. When executed with python -m src.model data/PlantVillage it
splits the data, applies augmentation, trains with early stopping,
evaluates the network on the held-out test split, and saves both the
trained model and a plot of the accuracy and loss curves.

**Purpose**

-   Define the 15-class label set shared by training, inference and the
    API.

-   Build and train the CNN architecture described in Section 2.1.3.

-   Evaluate the trained network on unseen test images.

-   Persist the model and training history for later use by the
    predictor.

### 2.2.2 Predictor Module

The **Predictor Module** (src/predictor.py) exposes a single shared
predictor object. It loads the saved Keras model once at start-up,
converts uploaded image bytes into the tensor shape expected by the
network, performs inference and assembles the response. Because the
model is loaded once and reused for every request, individual
predictions are fast and memory use stays predictable.

**Purpose**

-   Load the trained model when the service starts (predictor.load()).

-   Preprocess image bytes and run inference
    (predictor.predict(image\_bytes)).

-   Return the predicted class, confidence, severity, description,
    treatment, top three classes and the healthy flag.

-   Raise a ValueError for unreadable images so that the API can answer
    with HTTP 400.

### 2.2.3 API Module

The **API Module** (app.py) is the communication layer between the
browser, external clients and the predictor. It follows REST principles:
each endpoint has a single purpose, uses the appropriate HTTP method and
returns JSON. The module is **stateless** -- every request is
independent -- which makes it straightforward to run several containers
behind a load balancer in future.

**Key Characteristics:**

-   **Stateless Communication:** no session data is kept between
    requests.

-   **Uniform Interface:** four well-defined routes (/, /predict,
    /health, /classes).

-   **Operational Visibility:** the /health route allows monitoring
    tools and Docker health checks to confirm that the model is loaded.

-   **Consistent Errors:** every failure is returned as a JSON object
    with an error field.

### 2.2.4 Frontend Module

The **Frontend Module** (templates/index.html) is the visual layer of
the system. It hides the technical details of image preprocessing and
inference from the user, who only needs to choose a leaf photograph and
read the result. Because it is served by the same container as the API,
no cross-origin configuration or separate web server is needed.

**Design Features:**

-   **Minimal Layout:** a single upload form and a result area.

-   **Informative Output:** disease name, confidence, severity,
    description, treatment and alternatives.

-   **Clear Feedback:** meaningful messages when the upload or the
    service fails.

### 2.2.5 Deployment Module

The **Deployment Module** consists of the Dockerfile, docker-compose.yml
and requirements.txt. Together they describe how to assemble, configure
and run the service. By keeping the deployment description in version
control, any collaborator can reproduce the exact runtime with a single
command.

**Purpose**

-   Package the application and its pinned dependencies into a
    self-contained image.

-   Provide the same runtime across development, testing and production.

-   Define the port mapping, volumes, environment variables and restart
    policy.

-   Support future scaling and orchestration with minimal changes.

**CHAPTER 3**

CONTAINERIZING THE APPLICATION
==============================

3.1 Container File
------------------

The **Dockerfile** is the blueprint for building the
PlantDiseaseDetector image. It lists, step by step, the base image,
system libraries, Python dependencies, source files, exposed port and
start-up command. Because the file is plain text and stored in the
repository, the build is repeatable on any machine -- following the
principle "**Build Once, Run Anywhere**."

**Purpose of the Dockerfile**

-   Automate the creation of the application image.

-   Install exact versions of all required libraries.

-   Guarantee identical behaviour on every Linux host.

-   Simplify deployment, sharing and future orchestration.

![](media/image9.png){width="6.75in" height="5.082638888888889in"}

**Fig 3.1.1 Dockerfile of the application**

**Components of the Dockerfile**

1.  **Base Image (FROM python:3.10-slim):** supplies Python 3.10 on a
    minimal Debian system, keeping the image small compared with the
    full Python image.

2.  **System Libraries (RUN apt-get install):** installs libgl1 and
    libglib2.0-0, shared libraries commonly required by TensorFlow and
    image-processing packages. The package index is deleted afterwards
    to reduce the image size.

3.  **Working Directory (WORKDIR /app):** all following commands run
    inside /app, which is also where the application is placed.

4.  **Dependency Installation:** requirements.txt is copied and
    installed **before** the rest of the source code. Docker caches each
    layer, so the long TensorFlow installation is repeated only when the
    dependency list changes, not on every code edit. \--no-cache-dir
    prevents pip from keeping downloaded archives in the image.

5.  **Source Code Copy (COPY . .):** copies app.py, the src/ package and
    the templates/ and static/ folders into the image.

6.  **Runtime Directories (mkdir -p models static/uploads):** guarantees
    that the mount points for the model and the uploads exist even when
    no volume is attached.

7.  **Port Exposure (EXPOSE 8000):** documents that the service listens
    on port 8000 inside the container.

8.  **Start-up Command (CMD):** launches the FastAPI application with
    Uvicorn on all interfaces (0.0.0.0) so that it is reachable from
    outside the container.

The Python dependencies are pinned to exact versions so that every build
installs the same libraries:

![](media/image10.png){width="3.141938976377953in"
height="1.8918307086614172in"}

**Fig 3.1.2 Python dependencies (requirements.txt)**

python-multipart is required by FastAPI to receive file uploads, and
jinja2 is required for template rendering.

3.2 Build and Test the Container
--------------------------------

After the Dockerfile is written, the next step is to **build** the image
and **test** that the containerized service behaves correctly. The build
converts the Dockerfile instructions into a series of immutable layers;
the test phase confirms that the application starts, loads the model and
answers requests.

**Purpose**

-   Verify that the Dockerfile is correct and all dependencies install
    successfully.

-   Confirm that the application starts inside the container and loads
    the trained model.

-   Check that the API endpoints respond as designed, including error
    cases.

-   Validate that the behaviour is identical to running the application
    directly on the host.

**Building the Image**

The image is built from the project directory with a meaningful name and
version tag. The model must be trained on the host first so that
models/plant\_disease\_model.keras exists before the container is
started.

**Testing the Container**

The container is started with the host port mapped to the container port
and the model directory mounted. The three simple requests below check
the service, the model and the prediction path.

  -------------------------- ------------------------------------ ----------------------------------------------------------------------
  **Test**                   **Request**                          **Expected result**
  Service and model status   GET /health                          {\"status\": \"ok\", \"model\_loaded\": true, \...}
  Class listing              GET /classes                         List of the 15 class names with \"total\": 15
  Valid prediction           POST /predict with a leaf image      JSON with predicted class, confidence, severity, treatment and top 3
  Non-image upload           POST /predict with a text file       HTTP 400 -- Upload must be an image file.
  Model missing              POST /predict without a model file   HTTP 503 -- model is not loaded
  -------------------------- ------------------------------------ ----------------------------------------------------------------------

![](media/image11.jpeg){width="6.75in" height="3.7222222222222223in"}

**Fig 3.2.2 Testing the running container**

**Model Evaluation Results**

After training, the test accuracy and test loss are printed in the
terminal and the accuracy and loss curves are saved to
models/training\_history.png. The values obtained on the 10% hold-out
test split should be entered in the table below.

![](media/image19.png){width="5.0in" height="2.0833333333333335in"}

  **Metric**                                   **Value**
  -------------------------------------------- -------------------------------------------
  Training epochs completed (early stopping)   11 (out of 50; early stopping patience=5)
  Final training accuracy                      78.74%
  Final validation accuracy                    81.69%
  Test accuracy                                81.28%
  Test loss                                    0.7025

![](media/image12.jpeg){width="6.75in" height="2.7930555555555556in"}

3.3 Run and Manage Containers
-----------------------------

Running a container with a long docker run command works for a quick
test but is difficult to repeat exactly. **Docker Compose** solves this
by describing the service in a YAML file. The docker-compose.yml of this
project builds the image from the local Dockerfile, publishes the port,
mounts the model and upload folders and keeps the service running.

![](media/image13.png){width="6.75in" height="3.466666666666667in"}

![](media/image14.png){width="6.75in" height="3.8618055555555557in"}

**Fig 3.3.1 docker-compose.yml configuration**

**Meaning of the Configuration**

-   **build: .** -- builds the image from the Dockerfile in the project
    directory.

-   **ports: \"8001:8000\"** -- publishes container port 8000 on host
    port 8001, so the application is opened at http://localhost:8001.

-   **volumes** -- mounts the host models and static/uploads folders so
    that the trained model is supplied from outside and uploaded images
    survive container removal.

-   **PYTHONUNBUFFERED=1** -- sends Python log output to the container
    log immediately, which makes docker compose logs useful for
    debugging.

-   **restart: unless-stopped** -- restarts the container automatically
    after a crash or a Docker daemon restart, unless it was stopped on
    purpose.The whole service is started with a single command and then
    reached from the browser:

![](media/image15.jpeg){width="6.75in" height="4.689583333333333in"}

**Fig 3.3.2 Starting the service with Docker Compose**

3.4 Use Container Lifecycle Operations
--------------------------------------

A container passes through a series of states -- **created, running,
paused, stopped and removed**. Managing these states correctly keeps the
system stable, avoids resource leaks and makes updates predictable. The
most commonly used operations for this project are summarised below.

  ----------------- ------------------------------------------------- --------------------------------------------------------
  **Operation**     **Docker Compose command**                        **Purpose**
  Build and start   docker compose up \--build -d                     Create the image and run the service in the background
  List containers   docker compose ps                                 Show running services and their port mappings
  View logs         docker compose logs -f                            Follow application and Uvicorn logs in real time
  Stop              docker compose stop                               Stop the container without deleting it
  Start             docker compose start                              Start a stopped container again
  Restart           docker compose restart                            Restart after replacing the model file
  Open a shell      docker compose exec plant-disease-detector bash   Inspect files inside the running container
  Remove            docker compose down                               Stop and delete the container and its network
  Remove image      docker rmi plant-disease-detector:1.0             Delete the local image to free disk space
  ----------------- ------------------------------------------------- --------------------------------------------------------

Because the model is mounted from the host, a retrained model can be
deployed by copying the new .keras file into models/ and running docker
compose restart; the image itself does not need to be rebuilt.

![](media/image16.jpeg){width="6.75in" height="4.366666666666666in"}

**Fig 3.4.1 Checking container lifecycle operations**

3.5 Upload in GitHub Repository
-------------------------------

The project is hosted on **GitHub** at
https://github.com/Guna-kannan/PlantDiseaseDetector under the **MIT
License**. Hosting the source on GitHub provides version control, a
complete history of changes, simple collaboration and an off-site
backup. The repository contains everything needed to rebuild the service
-- the Dockerfile, the Compose file, the dependency list and the source
code -- while generated artefacts such as the dataset and trained model
are kept out of version control.

![](media/image17.png){width="5.975517279090114in"
height="6.22553915135608in"}

**Fig 3.5.1 Using git commands to push the repository**

Benefits obtained from using GitHub include **version management** with
easy rollback, **collaboration** among team members, **accessibility**
from any system, and the possibility of later adding **CI/CD** workflows
that build and test the image automatically on every commit.

3.6 Push the Container in Registry
----------------------------------

A **container registry** is a central store from which images can be
pulled by any machine. Pushing the PlantDiseaseDetector image to a
registry such as **Docker Hub** or **GitHub Container Registry** means
that anyone can run the service without cloning the source code or
rebuilding the image. The process has three steps: tag the image with
the registry path, log in with secure credentials, and push.

![](media/image18.jpeg){width="6.75in" height="3.5375in"}

**Fig 3.6.1 Pushing the container image to the registry**

Because the trained model is supplied through a volume, a user who pulls
the image must also place plant\_disease\_model.keras in the mounted
models/ folder before starting the container. Registry hosting provides
**centralised access, secure storage, version tags and easy
distribution** of the service across environments.

**CHAPTER 4**

CHALLENGES FACED AND SOLUTIONS
==============================

Packaging a TensorFlow-based inference service into a container raised
several practical and conceptual challenges. They concerned dependency
management, image size, model management, networking and the reliability
of the model itself. Each challenge and the approach adopted is
described below.

### 1. Dependency Compatibility

TensorFlow places strict requirements on the NumPy version and the
Python interpreter, and a mismatch causes import errors that appear only
at run time. This was solved by pinning every library in
requirements.txt (TensorFlow 2.15.0, NumPy 1.26.4, FastAPI 0.111.0 and
so on) and fixing the interpreter to Python 3.10 through the base image,
so that every build produces an identical environment.

### 2. System Libraries in a Slim Image

The python:3.10-slim image omits many operating-system libraries that
image and numerical packages expect. Missing shared libraries cause the
container to fail while importing a package even though the build
succeeds. The Dockerfile therefore installs libgl1 and libglib2.0-0
explicitly and deletes the apt package lists afterwards to keep the
image small.

### 3. Image Size and Build Time

TensorFlow is a large package, so builds can be slow and images heavy.
Build time was reduced by ordering the Dockerfile so that
requirements.txt is copied and installed before the source code; Docker
reuses the cached dependency layer when only the code changes. pip
\--no-cache-dir and the slim base image further reduce size. A
multi-stage build or a CPU-only TensorFlow package can be adopted in
future for smaller images.

### 4. Managing the Trained Model

The trained model is a large binary file that changes whenever the
network is retrained. Baking it into the image would force a rebuild
after each training run. Instead the model is mounted into /app/models.
The application checks for the file at start-up, logs a clear warning if
it is absent, and answers prediction requests with HTTP 503 until a
model is available.

### 5. Port Mapping and Access

Inside the container the application listens on port 8000, but Docker
Compose publishes it on host port 8001 to avoid clashing with other
local services. Using the wrong port causes a "connection refused"
error. The correct URL when running through Compose is
http://localhost:8001, while a direct uvicorn run during development
uses the port given on the command line; documenting both avoids
confusion.

### 6. Persistence of Uploaded Images

Files written inside a container are lost when the container is removed.
Mounting ./static/uploads from the host keeps uploaded images across
restarts and rebuilds, and keeps the image itself stateless.

### 7. Dataset Layout and Class Consistency

The model assigns labels from the alphabetical order of the class
folders, and the API reports names from CLASS\_NAMES. If folder names
differ from the expected names, predictions would be mapped to the wrong
labels. The dataset folder is therefore required to contain exactly one
sub-folder per supported class using the exact class names.

### 8. Over-fitting and Generalisation

A CNN trained on a few thousand images can memorise the training set.
This was addressed with data augmentation (random flip, rotation and
zoom), a Dropout of 0.4 before the output layer, an 80/10/10 split that
keeps a test set untouched, and early stopping with patience 5. Because
PlantVillage photographs are taken under controlled conditions, accuracy
on field photographs can still be lower, which is noted as a limitation.

### 9. Input Validation and Error Handling

Users may upload files that are not images or request a prediction
before a model exists. The API validates the content type, checks that
the model is loaded, converts unreadable images into HTTP 400 and
unexpected failures into HTTP 500, and returns every error in the same
JSON structure so the front end can display it.

### 10. Version Control and Reproducibility

Large generated files such as datasets and trained models should not be
committed to Git. A .gitignore keeps them out of the repository, while
the Dockerfile, Compose file and pinned dependency list are committed so
that any collaborator can reproduce the environment. The MIT licence
clarifies how the code may be reused.

**CHAPTER 5**

CONCLUSION
==========

The PlantDiseaseDetector project successfully combined deep learning,
web-service design and Linux container technology into a single
deployable application. A custom CNN trained on the PlantVillage dataset
classifies Tomato, Potato and Bell Pepper leaves into 15 classes and,
for every image, returns a confidence score, severity level, description
and treatment recommendation together with the three most likely
alternatives. The result is more than a bare label: it is practical
guidance that a grower can act on. The trained CNN achieved 81.28% test
accuracy on the 10% hold-out test split (78.74% training accuracy,
81.69% validation accuracy) after 11 epochs with early stopping, and a
confusion matrix was generated to evaluate per-class performance.

The model is served through a FastAPI backend with clear validation,
structured JSON output and consistent error handling, and a lightweight
browser interface makes it accessible to non-technical users. Separating
the model layer, predictor, API and front end into distinct modules kept
the code organised and easy to extend.

From the deployment perspective, the project demonstrated the strengths
of containerization. A short Dockerfile based on python:3.10-slim,
together with pinned dependencies, produces an image that behaves
identically on any host. Docker Compose captures the port mapping,
volumes and restart policy in a single file, so the complete service
starts with one command. Keeping the trained model and uploaded images
outside the image through volumes allows the model to be retrained and
replaced without rebuilding, which is an important property for
machine-learning systems whose models change over time. Publishing the
source code to GitHub and the image to a registry completed a workflow
that mirrors real DevOps practice.

The theoretical and practical outcomes illustrate the main benefits of
containerization:

-   **Portability:** the same image runs on any Linux, Windows or macOS
    host with Docker.

-   **Reproducibility:** pinned dependencies and a declarative
    Dockerfile remove environment mismatches.

-   **Isolation:** the application runs in its own namespace without
    affecting the host.

-   **Efficiency:** containers share the host kernel and start much
    faster than virtual machines.

-   **Maintainability:** model, uploads and code are separated, so each
    can be updated independently.

**Future Enhancements**

-   Extend the dataset to more crops and diseases and add field-captured
    images to improve robustness.

-   Apply transfer learning with pre-trained architectures such as
    MobileNet or EfficientNet to improve accuracy and reduce training
    time.

-   Add a Docker health check based on the /health endpoint and
    automated tests for the API.

-   Create CI/CD workflows with GitHub Actions to build, test and push
    the image automatically.

-   Provide a mobile application or offline model (TensorFlow Lite) for
    use in areas with poor connectivity.

-   Deploy the service on Kubernetes for scaling, rolling updates and
    load balancing.

-   Store prediction history and add a dashboard for disease trends and
    monitoring.

**CHAPTER 6**

REFERENCES
==========

1.  PlantDiseaseDetector source code, GitHub repository --
    https://github.com/Guna-kannan/PlantDiseaseDetector

2.  PlantVillage Dataset, Kaggle --
    https://www.kaggle.com/datasets/arjuntejaswi/plant-village

3.  D. P. Hughes and M. Salathé, "An open access repository of images on
    plant health to enable the development of mobile disease
    diagnostics," arXiv:1511.08060, 2015.

4.  TensorFlow and Keras Documentation --
    https://www.tensorflow.org/api\_docs

5.  FastAPI Documentation -- https://fastapi.tiangolo.com

6.  Uvicorn Documentation -- https://www.uvicorn.org

7.  Docker Documentation -- https://docs.docker.com

8.  Docker Compose Documentation -- https://docs.docker.com/compose

9.  Docker Hub Documentation -- https://docs.docker.com/docker-hub

10. Pro Git Book -- https://git-scm.com/book
