# webScraping

This project is constructed on Python and later uses PHP to visualize the web scraped data inside tables.
The purpose of this project is to scrape data for newly given construction permits in a specific county. As of now, the code is optimized
to work with the following cities: Sofia, Varna, and Burgas. 

Short Summary of Functionality:
Using beautifulsoup4, the code retrieves the provided web page as html code. Through determined patterns, the code then extracts the nescessary information
for the rows that match the pattern. Information is then sent to a host server, where it can be retrieved in a php page. 
