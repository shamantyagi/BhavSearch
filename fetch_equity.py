import urllib,zipfile,csv
import glob,os
import redis

#creating folder if not exist
if not os.path.exists('cache_files'):
    os.makedirs('cache_files')

#downloading zip file
testfile = urllib.URLopener()
testfile.retrieve("http://www.bseindia.com/download/BhavCopy/Equity/EQ010218_CSV.ZIP", "cache_files/equity.zip")

#unzipping downloaded file
zip_ref = zipfile.ZipFile("cache_files/equity.zip", 'r')
zip_ref.extractall('cache_files')
zip_ref.close()

#renaming extracted csv file to a standard name
prev_file_name=glob.glob('cache_files/*.CSV')
if os.path.exists(prev_file_name[0]):
	  os.rename(prev_file_name[0], 'cache_files/equity.csv')

#initiating redis 
r=redis.StrictRedis(host="localhost",port=6379,db=0)

#deleting previous data
r.flushall()

counter_insert = 0 
with open('cache_files/equity.csv') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
				key_var = row['SC_NAME']
				value_var = row['SC_CODE'] + ',' + row['OPEN'] + ',' + row['HIGH'] + ',' + row['LOW'] + ',' + row['CLOSE'] 
				r.set(key_var,value_var)							# entering data to redis
				counter_insert = counter_insert + 1

print '\n'+ ' values inserted : '
print counter_insert


