
 INTRODUCTION
 ------------
This MotoGP project, as yet, only retrieves pdf files from the MotoGP website, processes
and cleans the data and saves it as csvs.  Goals moving forward are to create functions so
that pre-race analysis can be performed quickly the night before a race, and to use machine
learning in a predictive role.


  REQUIREMENTS
  ------------

This project *currently* requires the following modules:

 * requests
 * BeautifulSoup (bs4)
 * numpy
 * pandas
 * selenium
 * pdfplumber
 * fnmatch
 * re
 * csv
 * matplotlib
 * scipy.stats
 * warnings

This project has in the past, and may in the future implement the following modules:

 * time
 * collections
 * os
 * datetime
 * winsound
 * scipy.stats
 * tabula


  FILE STRUCTURE
  --------------
For simplicity's sake, all used main files, helper modules, and jupyter notebook files
are kept in a single directory.  There is also a nested directory of deprecated code that
anyone coming after me *might* find useful.  In all likelihood, all useful code from the
deprecated files has been re-used and can be found elsewhere in the implemented code.

In addition a file tree needs to be created for the web scraped pdf's, dirty csv's, and
cleaned csv's, to be saved to.  The tree used by this project is located on the desktop,
and can be found mapped out in the lists.py file.  If a user wants to modify where files
will be saved to and read from, all of the file locations can be viewed and edited there.


  MAINTAINER
  ----------

Current maintainers:
 * Neal Maze - nealwmaze@gmail.com


  PROJECT METHODOLOGY
  -------------------

In 0_autoRetrieve.py, A1_retrieveHelpers is imported, and process parameters are accepted
as user inputs.  Running this allows the user to set what years, and rounds of pdf files
should be retrieved from the MotoGP website, set what years and rounds of local pdf files
should be processed into csv files of relatively dirty data, and finally what years and
rounds of those dirty csv files should be cleaned and collected into two csv files for
each round, representing pre-race and post race data respectively.

In A1_retrieveHelpers the following helper modules are imported; A2_ScrappingHelpers,
B2_ConverterHelpers, D2_DataCleaningHelpers, and lists.  Each of the functions in this
module retrieve pdf files from the MotoGP website, convert those pdf files into csv files,
and clean and collate those csv files, respectively.  Each of these functions was at one
point it's own main file, but are here gathered so each can be called by 0_autoRetrieve
and the local data can be updated entirely in running one file.

In A2_ScrappingHelpers the following helper modules are imported; The helper methods
provided in A2_ScrappingHelpers facilitate reaching out to the MotoGP website and
retrieving the pdf files that contain the data this project is primarily concerned with.
These helpers also retrieve data available in the html code, that is related to the race,
including weather data, and rider teams and numbers.  At some point, I'd like to update
this module to also grab rider data like age, weight, height, and possibly prior racing
experience.























