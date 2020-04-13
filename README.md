# CS50W Project 1 By Mahdi Salem

## Web Programming with Python and JavaScript
### https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/

## Use the app on Heroku

### https://cs50-prj01.herokuapp.com/

Login
![](https://i.imgur.com/Ra2FRdh.png)

Register
![](https://i.imgur.com/FFjeDLH.png)

Home Page
![](https://i.imgur.com/cyIfrWm.png)

Book Page
![](https://i.imgur.com/pOoxC5o.png)

Search result
![](https://i.imgur.com/WTpz0YK.png)

Submit rate and Review
![](https://i.imgur.com/bMk5viY.png)

API call result
![](https://i.imgur.com/oJNK6Hv.png)

## Usage

* Register/ Login
* Search books by name, author or ISBN
* Get info about a book and submit your own review!

## :gear: Setup your own

```bash
# Clone repo
$ git clone https://github.com/mahhdy/cs50w-prj1.git

$ cd cs50w-prj1

# Create a virtualenv (Optional but reccomended)
$ python3 -m venv myenv

# Activate the virtualenv
$ source myenv/bin/activate (Linux or by bash in windows)

# Install all dependencies
$ pip install -r requirements.txt

# ENV Variables

Other requirements:
 setting DATABASE_URL=  #Your Heroku Postgres DB URI
 setting GOODREADS_KEY= # Goodreads API Key. # More info: https://www.goodreads.com/api

```