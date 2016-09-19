# Latitude
The lead aggregation tool with attitude.

## What is Latitude?

Lattitude is an AWS-based tool which scours the web for consulting leads. Driven by
a list of sources and parser functions stored in DynamoDB, a Lambda function is executed
on a regular basis to fetch data from these sources and store them in a database.

The React-based frontend then loads these leads from DynamoDB and displays them in an
easy-to-read format.

## Setup and Installation

## Next Steps

* Integrate Streak API to send leads to Streak
* Implement automated lead research, including:
  * Contact name(s)
  * Contact email addresses
  * LinkedIn
  * Twitter
  * Website
