# Source for the Lost and Found Website

This is the source code for the BIS Lost and Found IA. You are allowed to do whatever you like outside the context of the IB as long as you attribute me. This means that you are not allowed to use this code, partially or in full in any formal submissions to the IB. I am not responsible for any consequences that may arise from the use of this code. Incase of any dispute, I withold all the rights to this codebase. This code is provided as is and is not guaranteed to work in all environments. If you have any questions, feel free to reach out at hi[at]aryanmukherjee.com. 

## Installation and Setup

### Windows

1. **Install Python 3.11**: Download and install from the [official website](https://python.org/).

> [!CAUTION]
> Python 3.12 is NOT supported. Please ensure you install Python 3.11+.

2. **Install Git**: Download and install from the [official website](https://git-scm.com/).

> [!TIP]
> You can also install Python and Git through package manager like Chocolatey in Admin Powershell. <br> Run these commands, one by one.

```powershell
PS C:\> Set-ExecutionPolicy Bypass -Scope Process -Force # Allow installation, only for this process
PS C:\> [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072 
PS C:\> iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1')) # Install Chocolatey
PS C:\> choco upgrade git --params "/GitOnlyOnPath /WindowsTerminal" -y # Install Git 
PS C:\> choco upgrade python311 -y # Install Python
```

> [!NOTE]
> win-get has NOT been tested. You may use it if you know what you're doing.

> [!TIP]
> At this point, if you have an NVIDIA GPU, you could also install [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit) and [cuDNN](https://developer.nvidia.com/cudnn) if you want to leverage GPU acceleration. This is only leveraged during training and workloads that benefit from high parallelization. For normal classification workloads (like in production), this step is optional if a more lightweight installation is desired.

3. **Clone the repository**: Use the command `git clone https://github.com/Bavarian-International-School/BIS-Lost-and-Found-Website`.

4. **Create a virtual environment**: Using windows command prompt in the directory of the project and run the following commands to install and activate a venv
```shell
C:\> cd Codebase
C:\> py -3.11 -m venv "venv"
C:\> "venv\Scripts\activate.bat"
```

>[!CAUTION]
> Do not run this in powershell and do not start the project with admin rights. It may lead to privilage escalation vurnerabilities.

5. **Install the requirements**: To install the requirements, make sure the virtual environment is active. It is usually shown as with the `(venv)` text before the directory.

```shell
(venv) C:\> pip install -r requirements.txt # Grab a coffee, this takes a bit
```

> [!NOTE]  
> This will take about 300MB of storage on the disk.

6. **Set credentials**: All the credentials are stored in a `.env` file. Copy the existing `.env.example` file, and rename it to `.env`. <br>
For [Mailjet Credentials](https://app.mailjet.com/dashboard), generate a new secret-key pair. Also make sure the `MAILJET_EMAIL` value corresponds to the email that was used to signup for the service. <br>
To generate a new django secret, execute the `bis/utils.py` file. <br>
For [Google's API Credentials](https://console.cloud.google.com/apis/credentials), create a new resource, and generate an OAUTH2.0 key and secret. Make sure the Authorized JavaScript origins consits of the root url of the website and Authorized redirect URIs are set to `http://domain.com:8000/accounts/google/complete/google-oauth2/`. While it is possible to request authorisation, it is easier to set the app to `INTERNAL` and `USER TYPE` to internal to allow any student with a school domain to login.
For the Django secret key, run `bis/utils.py` to generate a random secret key. This key is used to encrypt session data and prevent [CSRF](https://en.wikipedia.org/wiki/Cross-site_request_forgery)

7. **Set a superuser**: To create a superuser, run the following commands and follow along the prompts that Django gives.
```shell
(venv) C:\> python manage.py createsuperuser
```

> [!CAUTION]
> DO NOT USE BASIC / REUSE PASSWORDS

8. **Run the server**: Run the command and the server should be online on the provided url.

```shell
(venv) C:\> python manage.py runserver <domainip>:<port>
```

> [!IMPORTANT]
> You will need to re-activate the venv after closing the process.

### MacOS

1. **Install Python 3.11**: Download and install from the [official website](https://python.org/).

> [!CAUTION]
> Python 3.12 is NOT supported. Please ensure you install Python 3.11+.

2. **Install Git**: Download and install from the [official website](https://git-scm.com/).

> [!TIP]
> To install the dependencies through a package manager like brew, run these commands, one by one to install brew and download the dependencies.

```bash
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
$ brew install python@3.11
$ brew install git
$ export PATH="$(brew --prefix)/opt/python@3.11/bin:$PATH"
```

> [!TIP]
> On Apple ARM Silicon Macs, install [Tensorflow Metal](https://developer.apple.com/metal/tensorflow-plugin/) to unlock better performance with **HIGH BATCH RATE TRAINING**. For normal classification workloads (like in production), this step is optional if a more lightweight installation is desired.

3. **Clone the repository**: Use the command `git clone https://github.com/Bavarian-International-School/BIS-Lost-and-Found-Website`.

4. **Create a virtual environment**: Using windows command prompt in the directory of the project and run the following commands to install and activate a venv
```bash
$ cd Codebase
$ python3.11 -m venv "venv"
$ source venv/bin/activate
```

5. **Install the requirements**: To install the requirements, make sure the virtual environment is active. It is usually shown as with the `(venv)` text before the directory.

```shell
(venv) $ pip install -r requirements.txt # Grab a coffee, this takes a bit
```

> [!NOTE]  
> This will take about 300MB of storage on the disk.

6. **Set credentials**: All the credentials are stored in a `.env` file. Copy the existing `.env.example` file, and rename it to `.env`. <br>
For [Mailjet Credentials](https://app.mailjet.com/dashboard), generate a new secret-key pair. Also make sure the `MAILJET_EMAIL` value corresponds to the email that was used to signup for the service. <br>
To generate a new django secret, execute the `bis/utils.py` file. <br>
For [Google's API Credentials](https://console.cloud.google.com/apis/credentials), create a new resource, and generate an OAUTH2.0 key and secret. Make sure the Authorized JavaScript origins consits of the root url of the website and Authorized redirect URIs are set to `http://domain.com:8000/accounts/google/complete/google-oauth2/`. While it is possible to request authorisation, it is easier to set the app to `INTERNAL` and `USER TYPE` to internal to allow any student with a school domain to login.
For the Django secret key, run `bis/utils.py` to generate a random secret key. This key is used to encrypt session data and prevent [CSRF](https://en.wikipedia.org/wiki/Cross-site_request_forgery)

7. **Set a superuser**: To create a superuser, run the following commands and follow along the prompts that Django gives.

```shell
(venv) $ python manage.py createsuperuser
```

> [!CAUTION]
> DO NOT USE BASIC / REUSE PASSWORDS

8. **Run the server**: Run the command and the server should be online on the provided url.

```shell
(venv) $ python manage.py runserver <domainip>:<port>
```

> [!IMPORTANT]
> You will need to re-activate the venv after closing the process.

### Ubuntu 22.04.4 LTS / Debian 11 Bullseye / Rasberry PiOS 11 Bullseye

> [!IMPORTANT]
> While it is likely that these steps may work for other Linux distributions, they have not been tested and your milage may vary.

1. **Install Software**: Install Python3.11 and Git using `apt-get`.

```bash
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt update
$ sudo apt -y install python3.11 git
```

3. **Clone the repository**: Use the command `git clone https://github.com/Bavarian-International-School/BIS-Lost-and-Found-Website`.

4. **Create a virtual environment**: Using windows command prompt in the directory of the project and run the following commands to install and activate a venv.

```bash
$ cd Codebase
$ python3.11 -m venv "venv"
$ source venv/bin/activate
```

5. **Install the requirements**: To install the requirements, make sure the virtual environment is active. It is usually shown as with the `(venv)` text before the directory.

```shell
(venv) $ pip install -r requirements.txt # Grab a coffee, this takes a bit
```

> [!NOTE]  
> This will take about 300MB of storage on the disk.

6. **Set credentials**: All the credentials are stored in a `.env` file. Copy the existing `.env.example` file, and rename it to `.env`. <br>
For [Mailjet Credentials](https://app.mailjet.com/dashboard), generate a new secret-key pair. Also make sure the `MAILJET_EMAIL` value corresponds to the email that was used to signup for the service. <br>
To generate a new django secret, execute the `bis/utils.py` file. <br>
For [Google's API Credentials](https://console.cloud.google.com/apis/credentials), create a new resource, and generate an OAUTH2.0 key and secret. Make sure the Authorized JavaScript origins consits of the root url of the website and Authorized redirect URIs are set to `http://domain.com:8000/accounts/google/complete/google-oauth2/`. While it is possible to request authorisation, it is easier to set the app to `INTERNAL` and `USER TYPE` to internal to allow any student with a school domain to login.
For the Django secret key, run `bis/utils.py` to generate a random secret key. This key is used to encrypt session data and prevent [CSRF](https://en.wikipedia.org/wiki/Cross-site_request_forgery)

7. **Set a superuser**: To create a superuser, run the following commands and follow along the prompts that Django gives.
```shell
(venv) $ python manage.py createsuperuser
```

> [!CAUTION]
> DO NOT USE BASIC / REUSE PASSWORDS

8. **Run the server**: Run the command and the server should be online on the provided url.

```shell
(venv) $ python manage.py runserver <domainip>:<port>
```

> [!IMPORTANT]
> You will need to re-activate the venv after closing the process.

## First Installation and Maintaining the Website

Run these commands after the first installation or if any changes to the models have been made, run the following commands:

```bash
(venv) $ python manage.py makemigrations
(venv) $ python manage.py migrate
(venv) $ python manage.py runserver <domainip>:<port>
```

## Usage

### URLS
    home/
    search/
    item-detail/
    claim/
    claims/
    profile/
    newsletter/
    hawkeye/
    login/
    accounts/
        login/
        logout/
        google/
    registration/
    admin/
