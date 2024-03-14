# Automated Price Drop Notification for iPad on Amazon.com

A simple amazon scraper to extract prices from Amazon.com and notify
using email

## How it works

The program starts a website on a local server in which parameters can
be configured for a scrape. Once the scrape frequency parameter is
configured a scrape a scrape of the website is scheduled to start
repeatedly after that time period. If the price has dropped a
notification is sent using the Resend API. Logs are logged to
`logs.log`.

## Usage

From a terminal

1. Clone this project `git clone
   https://github.com/mkornreich/amazon-scraper.git` and cd into it
   `cd amazon-scraper`
2. Install Requirements `pip3 install -r requirements.txt`
3. Run the server `python3 main.py`
4. Open the link generated after the program starts. Should be
   something like http://127.0.0.1:5000
5. Configure the parameters on the website. Once the scrape frequency
   parameter is configured a scrape is be scheduled to start
6. Leave the server running and wait until the price changes

## Challenges faced

It was difficult to implement scheduling a scrape of the website while
also running the website for the configurable parameters. It was also
diffcult to make sure that only one scheduled scrape is running when
the parameter for the frequency of the scrapes are changed. I ended up
solving both of those problems by using multithreading and by giving
each thread a unique identifier. When the parameter for the frequency
of the scrapes is changed the new unique identifier is added to the
database and the old scheduled scrape only runs when the unique
idenitifier for that thread is found in the database.

## Additional features added

Configurable parameters were added via a website using the Flask
Python framework. The parameter are saved in a SQLite database so when
the script is restarted it automatically checks for a price.

## Testing

Manual testing was done in order to make sure the project works. Each
of the components were tested indivdually and functionality was also
verified in the logs.
