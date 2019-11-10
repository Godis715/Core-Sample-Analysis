# Core-Sample-Analysis
A web-based tool for geologists, which helps to analyse, keep and search core samples. The main feature is an auto marking of core sample via machine learning and data analysis. 

# About
This project is developing as a part of educational practice by students from AM-CP faculty of St. Petersburg State University.

# Run application
Currently, it is possible to run application in **development mode**.
Firstly, go to **mainService** and execute command `python manage.py migrate`
Secondly, run command `python manage.py createsuperuser` and follow the instructions.
Finally, run all batch files in the root director. Visit localhost:8080/ in your browser and log in, using credentials, which you had specified when create superuser.
