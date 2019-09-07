#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import csv
import datetime
import logging
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--url", help = "Please enter a URL linking to a CSV file.")
args = parser.parse_args()

logging.basicConfig(filename='errors.log', level=logging.ERROR)
logger = logging.getLogger('assignment2')

    
def main():
    if not args.url:
        print 'No URL was entered. Kindly try again.'
        raise SystemExit
    try:
        csvData = downloadData(args.url)
    except urllib2.URLError:
        print 'The URL that was entered is invalid. Kindly confirm the address and try again.'
    else:
        personData = processData(csvData)
        chooseID = raw_input('Kindly enter the ID# of the person you wish to lookup:')
        print chooseID

        chooseID = int(chooseID)

        if chooseID <= 0:
            print 'A number less than or equal to zero has been entered. The program will exit. Good Bye!'
            raise SystemExit
        else:
            displayPerson(chooseID, personData)
            main()


def downloadData(url):
    """
    Downloads content from a supplied URL.
    
    Args:
        url (str): A string value for a URL.

    Returns:
        csv_file (various): A variable linked to content found at the supplied URL, if the URL is valid.

    Example:
        >>> downloadData('https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv')
    """
    
    content = urllib2.urlopen(url)
    return content


def processData(content):
    """
    Processes content within a .csv file.

    Args:
        content (file): A .csv file supplied by user or downloaded from a valid URL.

    Returns:
        Dictionary (dict): A dictionary containing keys and values.

    """

    csv_file = csv.DictReader(content)
    Dictionary = {}

    for num, line in enumerate(csv_file):
        try:
            born = datetime.datetime.strptime(line['birthday'], '%d/%m/%Y')
            Dictionary[line['id']] = (line['name'], born)
        except:
            logging.error('Error processing line #{} for ID# {}'.format(num, line['id']))

    return Dictionary


def displayPerson(id, personData):
    """
    This function prints the name and birthday of a given user identified by the input ​ID.

    Args:
        id(int): an integer that corresponds to a uniqye user ID.

        personData(dict): A dictionary containing a tuple of the username and birthday.
        
    Returns:
        A string displaying the ID, person and birthday which corresponds with the input ID number
        or a string indicating the ID is not valid.
    """

    uniqueID = str(id)
    if uniqueID in personData.keys():
        print 'The person with ID# {} is {} and their birthday is {}'.format(id, personData[uniqueID][0], datetime.datetime.strftime(personData[uniqueID][1], '%Y-%m-%d'))
    else:
        print 'No user was found matching that ID#. Kindly try again.'
        

if __name__ == '__main__':
    main()
