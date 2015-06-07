import shutil

file1 = "/home/masdarcis/Documents/projects_amalfi/twitter_data/03-2014-dump/archiveteam-twitter-stream-2014-03.tar"
file1dest = "/home/masdarcis/Documents/projects_amalfi/twitter_data/collected/mar14.tar"

file2 = "/home/masdarcis/Documents/projects_amalfi/twitter_data/04-2014-dump/archiveteam-twitter-stream-2014-04.tar"
file2dest = "/home/masdarcis/Documents/projects_amalfi/twitter_data/collected/apr14.tar"

file3 = "/home/masdarcis/Documents/projects_amalfi/twitter_data/05-2014-dump/archiveteam-twitter-stream-2014-05.tar"
file3dest = "/home/masdarcis/Documents/projects_amalfi/twitter_data/collected/may14.tar"

file4 = "/home/masdarcis/Documents/projects_amalfi/twitter_data/02-2014-dump/archiveteam-twitter-stream-2014-02.tar"
file4dest = "/home/masdarcis/Documents/projects_amalfi/twitter_data/collected/feb14.tar"

# print "Processing file 1..."
# shutil.copy2(file1, file1dest)
# print "Processing file 2..."
# shutil.copy2(file2, file2dest)
# print "Processing file 3..."
# shutil.copy2(file3, file3dest)
print "Processing file 4..."
shutil.copy2(file4, file4dest)
print "Copying done!!!"