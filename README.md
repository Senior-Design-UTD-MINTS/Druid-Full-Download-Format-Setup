# Full-Download-Format-Setup
Used to set up Druid data.

To run this code:
1) Install Druid https://druid.apache.org/docs/latest/tutorials/index.html (tutorial to install)
  - REQUIRES JAVA 8. You CANNOT use any java version greater than JDK 8. There are ways on linux to switch between java runtimes. https://askubuntu.com/questions/1133216/downgrading-java-11-to-java-8 and for Mac https://dzone.com/articles/switching-java-versions-on-mac-os (UNTESTED).
  
  2) Install Python 3 (minimum Python 3.6) --REQUIRED
  
  3) In your Druid root directory (incubating directory) create a directory called "formatdata" (spelled exactly like that, no caps or anything). 
  
  4) Place files 'formatCSV.py' and 'upSpec.json' in the 'formatdata' directory.
  
  5) Run Druid (in Druid root/incubating directory run './bin/start-micro-quickstart'). Default port is http://localhost:8888 , go to that URl to see Druid overlord interface. MUST BE RUNNING TO WORK. 
  
  6) Go into 'upSpec.json' and CHANGE 'baseDir' field in schema to the filepath for the formatdata directory you've created. (I will automate this later). Currently it is hardcoded to my (Ben's) machine. 
  
  7) run formatCSV.py in 'formatdata' directory. (cd to 'formatdata' and then run 'python3 formatCSV.py' on command line)
  
  8) You will be prompted if you want to upload to Druid. MAKE SURE DRUID IS RUNNING BEFORE SAYING YES. Any input besides 'y' will not execute. 
  
  9) Assuming Druid is running and you changed the baseDir field, it should perform a verbose download of all the data and then upload to druid. 
    -OPTIONAL: in 'formatdata' you can place the auto ingestion script and json and run those ('ingestion.py' and uploadspec.json found in repo. This is not a fleshed out feature but will work, just inefficiently. RUN AFTER 'formatCSV.py'. SEE SCRIPT COMMENTS FOR THIS TO WORK)
    
  10) If you want to redo this process simply delete the 'formatted.csv' file in 'formatdata' and DELETE DATASOURCE FROM LOCAL DRUID INSTANCE (use Druid overlord interface at port 8888). Then simply run 'formatCSV.py' again. 
  
  Notes: formatCSV.py gets all the latest data up to the point when you run the code, it DOES NOT acquire new data afterwards (that's what ingest.py is for). YOU MUST CHANGE 'upSpec.json' FOR THIS TO WORK (see step 6). If you choose NOT to run the auto-ingestion script, in order to get the latest data at that moment you will have to repeat this process (see step 10). ANY TASK YOU RUN TO DRUID CAN BE VERIFIED AS RUNNING AND WHETHER OR NOT IT WAS SUCCESSFUL IN THE OVERLORD INTERFACE AT PORT 8888 (navigate to 'tasks').
  
  
  
# RESYNCHRONIZING DATA

If for some reason the auto ingestion script missed a period of data that needs to be recovered, this can be done by utilizing the formatCSV.py script.

1. Navigate to Druid overlord url (should be http://imd.utdallas.edu:8888), go to data sources, and drop any databases with missing data.

2. Log onto imd, navigate to the formatdata directory inside of the Druid database

3. Format upSpec.json and formatCSV.py to be associated with the data source you want to restore

4. Run formatCSV.py and upload the CSV to Druid
    NOTE: make sure to remove the formatted.csv file before and/or after running the python script

5. Repeat for any other data sources you may need
