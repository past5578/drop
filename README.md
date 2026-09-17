# drop

## Usage

In progress.

## Overview

This is an image host that I wrote to personally use and also to get a better understanding of image processing, using SQL databases (Postgresql for this project specifically), workers + jobs, and REST API designing.

The main endpoints to worry about are `/i/v?id={image_id}`, `/i/r?id={image_id}`, and `/i/u` which provide the pretty HTML page for an image, and provide the raw image respectively. Eventually, I would like to turn this into a full on website with users and everything of the sort, but that will be in the future.

A ShareX configuration will be provided when this project is in that stage.

## To do

This list is not in order of priority.

- Set up CI for automatically building a Docker image.
- Create a worker for image processing, like generating thumbnails and any other jobs that will be useful for this.
- Design a user system (will likely be invite only on my personal deployment) and integrate user data with the database schema.
- Design the pretty HTML page for images