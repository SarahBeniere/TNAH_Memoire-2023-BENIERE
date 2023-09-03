"""
PREAMBLE
--------
    - Description: Parses the given corpus searching for specific information.
    - Author: Sarah Bénière
    - Date: June 2023
    - Running instructions:
        ======
        python script.py arg1
        arg1: absolute path for the corpus
        ======
"""


import os  # Allows interaction with the computer, regardless of its operating system.
import sys  # Allows for the argument to be called directly from the command line.
from bs4 import BeautifulSoup



def parse(corpus):
    """ Parses the given corpus.

    Parameter
    ---------
    corpus
       Absolute path for the corpus.
       Corresponds to "arg1" in the command line.
    """

    for root, dirs, files in os.walk(corpus):
        for filename in files:
            with open(os.path.join(root, filename), 'r', encoding='UTF-8') as xml_file:
            # Opens the files in 'read' mode and stores the opened file in a variable called 'xml_file'.
                xml_content = xml_file.read()
                # The 'xml_content' variable stores the content of the file opened in 'xml_file' with the '.read()' method.
                soup = BeautifulSoup(xml_content, 'xml')
                # Creates a 'soup' object, which parses 'xml_content' with the XML parser included in the BeautifulSoup library.
                yield filename, soup
                # The 'yield' statement suspends the execution of the function to return a result, and then resumes execution instead of starting over every time.



def tag_finder(element_name):
    """ Finds the files in which the element appears.
    
    Parameter
    ---------
    element_name : str
        Name of the researched element, between quotation marks.
    
    Returns
    -------
    set()
        Set containing the names of the files in which the given element appears.
    """

    files_containing_tag = set()
    for filename, soup in parse(sys.argv[1]):
        # Uses the 'parse' function to parse the corpus provided by 'arg1' in the command line.
        for tag in soup.find_all():
            if tag.name == element_name:
                files_containing_tag.add(filename)
                # Adds the name of the file to the set if any tag name matches the value of the 'element_name' variable.
                print(filename)

# Example --> tag_finder("biblScope")



def missing_tag(tag):
    """ Finds the files from which the element is missing.

    Parameter
    ---------
    tag : str
        Name of the researched element, between quotation marks.
    
    Returns
    -------
    set()
        Set containing the names of the files from which the given element is missing.
    """

    files_missing_tag = set()
    for filename, soup in parse(sys.argv[1]):
        # Uses the 'parse' function to parse the corpus provided by 'arg1' in the command line.
        if not soup.find_all(tag):
            files_missing_tag.add(filename)
            # Adds the name of the file to the set if the '.find_all()' method does not find any occurrence.
            print(filename)

# Example --> missing_tag("catRef")



def duplicates_finder(element_name):
    """ Finds the files containg at least two occurrences of the element.

    Parameter
    ---------
    element_name : str
        Name of the researched element, between quotation marks.
    
    Returns
    -------
    list
        List of the files containing two or more occurrences of the given element.
    """

    for filename, soup in parse(sys.argv[1]):
        # Uses the 'parse' function to parse the corpus provided by 'arg1' in the command line.
        occurrences = 0
        # Creates an 'occurrences' variable with an initial value of '0' (int).
        for tag in soup.find_all(element_name):
            if tag.name == element_name:
                occurrences += 1
                # Adds '1' (int) to 'occurrences' whenever a tag name matches the value of the 'element_name' variable.
        if occurrences > 1:
            print(filename)
            # Returns the names of the files only if the number of occurrences of the given element is strictly superior to 1.

# Example --> duplicates_finder("creation")



def attribute_finder(attrs):
    """ Finds the files in which the attribute appears.

    Parameter
    ---------
    attrs : str
        Name of the researched attribute, between quotation marks.
    
    Returns
    -------
    list
        List of the files in which the attribute appears at least once.
    """

    for filename, soup in parse(sys.argv[1]):
        # Uses the 'parse' function to parse the corpus provided by 'arg1' in the command line.
        files_with_attribute = soup.find_all(attrs)
        # Creates a 'files_with_attributes' variable containing all the occurrences of the researched attribute.
        if len(files_with_attribute) > 0:
            print(filename)
            #Returns the names of the files in which the researched attribute appears at least once.

# Example --> attribute_finder("target")



def attlist(element_name):
    """ Finds the attributes associated with an element in the given corpus.
    
    Parameter
    ---------
    element_name : str
        Name of the researched element, between quotation marks.

    Returns
    -------
    set()
        Set containing the list of attributes used with the researched element in the given corpus.
    """
    
    attributes_list = set()
    # Creates an 'attributes_list' set that will store the name of the attribute(s).
    for soup in parse(sys.argv[1]):
        # Uses the 'parse' function to parse the corpus provided by 'arg1' in the command line.
        for tag in soup.find_all():
            if tag.name == element_name:
                for attribute in tag.attrs:
                    attributes_list.add(attribute)
                    # Adds the name of every attribute appearing in the corpus whenever the name of the tag matches the value of the 'element_name' variable.
    print(attributes_list)

# Example --> attlist("date")