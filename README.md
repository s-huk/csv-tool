# CSV Tool

# Setup

1. Install Micromamba

Windows
https://mamba.readthedocs.io/en/latest/installation.html#windows
```
Invoke-Webrequest -URI https://micro.mamba.pm/api/micromamba/win-64/latest -OutFile micromamba.tar.bz2
C:\PROGRA~1\7-Zip\7z.exe x micromamba.tar.bz2 -aoa
C:\PROGRA~1\7-Zip\7z.exe x micromamba.tar -ttar -aoa -r Library\bin\micromamba.exe

MOVE -Force Library\bin\micromamba.exe micromamba.exe
.\micromamba.exe --help

# You can use e.g. $HOME\micromambaenv as your base prefix
$Env:MAMBA_ROOT_PREFIX="C:\Your\Root\Prefix"

# Invoke the hook
.\micromamba.exe shell hook -s powershell | Out-String | Invoke-Expression

# ... or initialize the shell
.\micromamba.exe shell init -s powershell -p C:\Your\Root\Prefix
```

Linux:
```
wget -qO- https://micro.mamba.pm/api/micromamba/linux-64/latest | sudo tar -xvj -C /usr/local/bin bin/micromamba --strip-components=1
micromamba shell init -s bash -p ~/micromamba
source ~/.bashrc
```

2. Prepare conda environment `csv-tool` and its dependencies.

```
micromamba create --yes --file environment.yml
```


# Development

1. Ensure conda environment `csv-tool` is activated.

```
micromamba activate csv-tool
```

2. Then start development server.

```
uvicorn app.main:app --reload
```
oder
```
python3 -m uvicorn main:app --reload
```

3. Open in your browser:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc


## Keep packages up-to-date
In cases of new realeases/updates of used packages, consider to rebuild your local env like this:
```
micromamba deactivate
micromamba remove -n csv-tool --all
micromamba create --yes --file environment.yml
```

# Docker Build

```
docker login
docker build -t YourUsername/csv-tool -f ./Containerfile .
```
