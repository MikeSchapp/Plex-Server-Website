# Plex Server Website

This repo creates a frontend hosted on a raspberry pi with gunicorn to create a website that allows a user to remotely
turn on and off a server and launch plex. Currently the docker commands are in the works, however the functionality for 
interacting with a Dell server through its IDRAC is currently working.

## Needs to be implemented

* Launching Docker containers via the website
* Ability to sign up and add users to the website. (Currently only one master user)
* Add on functionality to the jquery components of the website.
* Add a better way to store the password and query it.
