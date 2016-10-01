# Latitude
The lead aggregation tool with attitude.

## What is Latitude?

Latitude is a tool which scours the web for consulting leads, driven by a list of lead sources
stored in AWS DynamoDB. There are three main components:

* Lambda Python function - executed on a regular basis to fetch data from the sources and store them in DynamoDB.
* Minimal Python/web.py backend - used for user authentication and some basic interactivity
* Grunt/ES6/Handlebars frontend - a custom Gruntfile built to support integration between Bower+ES6+Handlebars

## Setup and Installation

## Next Steps

* Integrate Streak API to send leads to Streak
* Implement automated lead research, including:
  * Contact name(s)
  * Contact email addresses
  * LinkedIn
  * Twitter
  * Website
