"""
micromamba deactivate
micromamba remove -n csv-tool --all
micromamba create --yes --file environment.yml
micromamba activate csv-tool

python3 -m uvicorn main:app --reload --host 0.0.0.0

"""

import os
import re
import sys
from dotenv import load_dotenv

from collections.abc import Iterable
import datetime

import chardet    

import secrets
from fastapi import FastAPI, Body, HTTPException, File, Form, UploadFile
from fastapi.responses import PlainTextResponse
from fastapi.responses import StreamingResponse, FileResponse, Response
from fastapi import Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
import json

### type-related
import typing


from logging.config import dictConfig
import logging

dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s | %(asctime)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "csv-tool-logger": {"handlers": ["default"], "level": "DEBUG"},
    }
})
logger = logging.getLogger("csv-tool-logger")


###############################################################################
##
##       
##       SETTINGS / ENV
##
##
###############################################################################

# Env
basedir = os.path.abspath(os.path.dirname(__file__))
parentdir = os.path.dirname( basedir )
filepath_basedir = os.path.join(basedir,'.env')
filepath_parent = os.path.join(parentdir,'.env')
ENV_FILE_PATH = ""
if os.path.isfile(filepath_basedir):
    load_dotenv(filepath_basedir)
    ENV_FILE_PATH = filepath_basedir
elif os.path.isfile(filepath_parent):
    load_dotenv(filepath_parent)
    ENV_FILE_PATH = filepath_parent

logger.info("BASE DIR: "+basedir)
logger.info("ENV FILE PATH: "+ENV_FILE_PATH)

NECESSARY_ENV_KEYS = [] # ["API_USER", "API_PW"]

for k in NECESSARY_ENV_KEYS:
    if not os.environ.get(k):
        if ENV_FILE_PATH:
            raise Exception( "ERROR: Env var '{}' not set (loaded .env from {})".format(k, ENV_FILE_PATH) )
        else:
            raise Exception( "ERROR: Env var '{}' not set".format(k) )

API_USER = os.environ.get('API_USER')
API_PW = os.environ.get('API_PW')



###############################################################################
##
##       
##       FastAPI STARTUP
##
##
###############################################################################
tags_metadata = [
    {
        "name": "Upload",
        "description": "..."
    }
]

app = FastAPI(
    title="CSV-Tool",
    tags_metadata=tags_metadata
)

security = HTTPBasic()

def assertAuth(credentials):
    if not secrets.compare_digest(credentials.username, API_USER) or not secrets.compare_digest(credentials.password, API_PW):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/password",
            headers={"WWW-Authenticate": "Basic"},
        )

#@app.on_event("startup")
#async def startup_event():







###############################################################################
##
##
##       ENDPOINTS
##
##
###############################################################################

@app.get("/isalive")
def isalive():
    return {"isalive": True}

#(?P<name>...)
PATTERN_FROM = re.compile(r"(^(?:[^\t]+\t){15}(?:[0-9]{5,})),00(\t[^\n]+$)", flags=re.MULTILINE)

@app.post("/csvfiles")#, response_class=PlainTextResponse)
async def csvfiles( files: typing.List[UploadFile] = File(default=None) ): #= Field(default_factory=list)
    if not files or len(files) == 0:
        raise HTTPException(status_code=400, detail="Missing files")
    
    contents_new = ""
    result = []
    for f in files:
        rawdata = f.file.read()
        result = chardet.detect(rawdata)
        charenc = result['encoding']
        
        contents = rawdata.decode(charenc)
        contents_new += re.sub(PATTERN_FROM, r"\1\2", contents)+"\n"
        
        return Response(
            content=contents_new.strip().encode(charenc), 
            media_type="text/csv",
            headers={
                'Content-Disposition': 'attachment;filename='+f.filename+" (converted)",
                'Access-Control-Expose-Headers': 'Content-Disposition'
            }
        )

@app.get("/")
def root():
    content = """
        <body>
        <form action="/csvfiles/"  enctype="multipart/form-data"  method="post">
        <input type="file" name="files" style="background-color:yellow;padding:3em;">
        <input type="submit">
        </form>
        </body>
    """
    return HTMLResponse(content=content)
