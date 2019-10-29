# Full-Download-Format-Setup
Used to set up Druid data.

You have to change the upSpec field baseDir to your local instance. I'll probably fix that though. 
Create and run the script in a folder called 'formatdata' under your druid incubating root otherwise it won't work.

ONLY RUN THIS ONCE. If you run it twice without deleting your old data you WILL GET UPWARDS OF 100,000 DUPLICATE ROWS. 

I'll update this to make it a bit better in the future. Needs to be combined with auto ingestion. Perhaps a makefile. 
