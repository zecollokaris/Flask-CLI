"""
thermos

Usage:
  thermos create app <appname>
  thermos create blueprint <blueprintname>
  thermos create template <templatename>
  thermos -h | --help
  thermos -v | --version

Options:
  create                         generate new app,blueprint or template      
  -h --help                         Show this screen for available options.
  -v --version                         Show the version.
Examples:
  thermos create app nameofapp
  cd nameofapp
  thermos create blueprint nameofblueprint
Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/zecollokaris/Thermos-cli
"""

from inspect import getmembers, isclass

from docopt import docopt

import sys

from . import __version__ as VERSION

from colorama import init
init(strip=not sys.stdout.isatty())

from termcolor import cprint
import curses, random
import time
import sys


def main():
    """The main CLI entry-point."""

    import thermos.commands
    import os,pip

    options = docopt(__doc__, version=VERSION)

    def create_structure():
        app_name = options['<appname>']

        if not os.path.exists(app_name):
            os.makedirs(app_name)

            os.chdir(os.getcwd()+"/"+app_name)

            os.system('git init')
            os.system("touch .gitignore")
            os.system("touch README.md")

            with open('.gitignore','w+') as gitignore:
                gitignore.write('virtual/ \n *.pyc \n start.sh')
                gitignore.close()

            if not os.path.exists('tests'):
                os.makedirs('tests')

            config_file = 'class Config:\n\tpass \n class ProdConfig(Config):\n\tpass\
            \nclass DevConfig(Config): \n\tDEBUG = True\n\n\
            config_options={"production":ProdConfig,"default":DevConfig}'

            manage_file = "from flask_script import Manager,Server\n\
            from app import create_app,db\n\n\
            app = create_app('default')\n\n\
            manager = Manager(app)\n\n\
            manager.add_command('server', Server)\n\n\
            if __name__ == '__main__':\n\
            \tmanager.run()'\
            "

            with open('config.py','w+') as config:
                config.write(config_file)
                config.close()


            with open('manage.py','w+') as manage:
                manage.write(manage_file)
                manage.close()


            if not os.path.exists('app'):
                os.makedirs('app')

            os.chdir('app')

            folders = ['static','templates','static/css','static/js','static/images']

            base_html = "{% extends  'bootstrap/base.html' %}\n<!doctype html>\n<html><head>{% block head %}\
                <link rel='stylesheet' href=\"{{ url_for('static', filename='style.css') }}\">\
                <title>{% block title %}{% endblock %} - My Webpage</title>\
                {% endblock %} </head> <body> <div id='content'>{% block content %}{% endblock %}</div><div id='footer'>\
                {% block footer %}\
                &copy; Copyright 2010 by <a href='http://domain.invalid/'>you</a>.\
                {% endblock %} </div> </body></html>"

            for folder in folders:
                if not os.path.exists(folder):
                    os.makedirs(folder)

                if folder=='templates':
                    with open('templates/base.html','w+') as base_tem:
                        base_tem.write(base_html)
                        base_tem.close()


            init_file =  "from flask import Flask\nfrom config import config_options\nfrom flask_bootstrap import Bootstrap\nfrom flask_sqlalchemy import SQLAlchemy\n\n\nbootstrap = Bootstrap()\ndb = SQLAlchemy()\ndef create_app(config_state):\n\tapp = Flask(__name__)\n\tapp.config.from_object(config_options[config_state])\n\n\n\tbootstrap.init_app(app)\n\tdb.init_app(app)\n\tfrom .main import main as main_blueprint\n\tapp.register_blueprint(main_blueprint)\n\treturn app"

            with open('__init__.py','w+') as init:
                init.write(init_file)
                init.close()

            with open('models.py','w+') as models:
                models.write("#models")
                models.close()

            if not os.path.exists('main'):
                os.makedirs('main')

            os.chdir('main')

            main_init_file = "from flask import Blueprint\nmain = Blueprint('main',__name__)\n\nfrom . import views,error"
            view_file="from . import main\n\n@main.route('/')\ndef index():\n\treturn '<h1> Hello World </h1>'"
            error_file="from flask import render_template\nfrom . import main\n\n@main.app_errorhandler(404)\ndef for_Ow_four(error):\n\t'''\n\tFunction to render the 404 error page\n\t'''\n\treturn render_template('fourOwfour.html'),404"

            blueprint_files = ['__init__.py' ,'views.py' ,'error.py']

            for blueprint_file in blueprint_files:
                if blueprint_file == '__init__.py':
                    with open(blueprint_file,'w+') as m_init:
                        m_init.write(main_init_file)
                        m_init.close()

                elif blueprint_file == 'views.py':
                    with open(blueprint_file,'w+') as vw:
                        vw.write(view_file)
                        vw.close()

                else:
                    with open(blueprint_file,'w+') as er:
                        er.write(error_file)
                        er.close()


            os.chdir('..')
            os.chdir('..')

            with open('tests/__init__.py','a') as test_init:
                test_init.close()

            with open('start.sh','w+') as start:
                start.write('python3.6 manage.py server')
                start.close()

            os.system('chmod a+x start.sh')

            from platform  import python_version

            version= str(python_version())[:3]

            virtual="python%s -m venv virtual"%(version)


            os.system(virtual)

            os.system('. virtual/bin/activate')

            dependencies = ['flask','flask-script', 'flask-bootstrap','gunicorn','flask-wtf','flask-sqlalchemy']


            for dependency in dependencies:
                pip.main(['install',dependency])

            os.system('pip freeze > requirements.txt')


            with open('Procfile','w+') as proc:
                proc.write('web: gunicorn manage:app')
                proc.close()





                #ANIMATION CODE!

                screen  = curses.initscr()
                width   = screen.getmaxyx()[1]
                height  = screen.getmaxyx()[0]
                size    = width*height
                char    = [" ", ".", ":", "^", "*", "x", "s", "S", "#", "$"]
                b       = []

                curses.curs_set(0)
                curses.start_color()
                curses.init_pair(1,0,0)
                curses.init_pair(2,1,0)
                curses.init_pair(3,3,0)
                curses.init_pair(4,4,0)
                screen.clear
                for i in range(size+width+1): b.append(0)

                for i in range(100):
                        for i in range(int(width/9)): b[int((random.random()*width)+width*(height-1))]=65
                        for i in range(size):
                                b[i]=int((b[i]+b[i+1]+b[i+width]+b[i+width+1])/4)
                                color=(4 if b[i]>15 else (3 if b[i]>9 else (2 if b[i]>4 else 1)))
                                if(i<size-1):   screen.addstr(  int(i/width),
                                                                i%width,
                                                                char[(9 if b[i]>9 else b[i])],
                                                                curses.color_pair(color) | curses.A_BOLD )

                        screen.refresh()
                        screen.timeout(30)
                        if (screen.getch()!=-1): break

                curses.endwin()
                animation = "|/-\\"

                for i in range(20):
                    time.sleep(0.1)
                    sys.stdout.write("\r" + animation[i % len(animation)])
                    sys.stdout.flush()
                    #do something
                print("End!")

                


















            
            
            cprint("\nCREATED APPLICATION FOLDER STRUCTURE\n HAPPY flasking :)\n","green")
            BASE_FOLDER=os.getcwd()
            app_folder = 'cd {}'.format(BASE_FOLDER)
            os.system(app_folder)
        else:
            cprint("\nAnother folder with same name already exists\nPlease try with another name\n","red")

    def check_app_is_flask():
        existing_file_folders = ['app','virtual','config.py','manage.py','Procfile','README.md','requirements.txt','start.sh']

        if all(os.path.exists(fl) for fl in existing_file_folders):
            return True
        else:
            cprint("\nPlease navigate into the flask folder\n","red")
            return False

    def create_blueprint(blueprint_name):
        os.makedirs(blueprint_name)

        os.chdir(blueprint_name)

        blueprint_name_init_file = "from flask import Blueprint\n{} = Blueprint('{}',__name__)\n\nfrom . import views,error".format(blueprint_name,blueprint_name)

        view_file="from . import {}\n\n@{}.route('/')\ndef index():\n\treturn '<h1> Hello world </h1>'".format(blueprint_name,blueprint_name)

        error_file="from flask import render_template\nfrom . import {}\n\n@{}.app_errorhandler(404)\ndef four_Ow_four(error):\n\t'''\n\tFunction to render the 404 error page\n\t'''\n\treturn render_template('fourOwfour.html'),404".format(blueprint_name,blueprint_name)

        blueprint_files = ['__init__.py', 'views.py', 'error.py']


        for blueprint_file in blueprint_files:
            if blueprint_file == '__init__.py':
                with open(blueprint_file,'w+') as b_init:

                    b_init.write(blueprint_name_init_file)

                    b_init.close()

            elif blueprint_file == 'views.py':

                with open(blueprint_file,'w+') as v:

                    v.write(view_file)

                    v.close()

            else:

                with open(blueprint_file,'w+') as err:

                    err.write(error_file)

                    err.close()

    def create_template(template_name):
        with open(template_name+'.html','w+') as template:
            template.write("{% extends 'base.html' %}")
            template.close()


    def add_blueprint():
        if check_app_is_flask():
            os.chdir('app')

            blueprint_name = options['<blueprintname>']
            if not os.path.exists(blueprint_name):
                create_blueprint(blueprint_name)
                temp_message = "Blueprint {} created!".format(blueprint_name)
            else:
                temp_message = "Blueprint {} already exists!".format(blueprint_name)

            cprint(temp_message,"magenta")

    def add_template():
        if check_app_is_flask():
            os.chdir('app')
            os.chdir('templates')

            template_name = options['<templatename>']
            if not os.path.exists(template_name+'.html'):
                create_template(template_name)
                temp_message = "Template {} created!".format(template_name)
            else:
                temp_message = "Template {} already exists!".format(template_name)

            cprint(temp_message,"magenta")


    if options['create']:
        try:
            if options['app'] and options['<appname>']:
                create_structure()

            if options['blueprint'] and options['<blueprintname>']:
                add_blueprint()

            if options['template'] and options['<templatename>']:
                add_template()
        except:
            cprint("\nOops!An error occured\nPlease try again\n","red")
