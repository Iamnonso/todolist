import os
from urllib import response
from myapp.app import mysql
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from ..myhelper import myhelper
from ..model import mymodel

blueprint = Blueprint('main', __name__)

#View routes
