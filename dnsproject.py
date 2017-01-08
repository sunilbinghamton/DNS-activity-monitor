from collections import OrderedDict

DEBUG = False
NEW_DNS_REQ_THRES = 3.0

timestamp =[]
dns_name =[]
dif_more_thres =[]
time_more_thres =[]
dns_more_thres = []
date_time = []
dns_address = []


TXT_FILE = 'set1.log'
REPORT = 'report.txt'
dns_txt = open(TXT_FILE, 'rb')
report_txt = open(REPORT,'wb')

def hms_to_secs(hms):
  hms_split = hms.split(':')
  return  float(hms_split[0]) * 3600 + int(hms_split[1]) * 60 + float(hms_split[2])

# Read queries and extract necessary information
for line in dns_txt.readlines():
  try:
    line = line.split(" ")
    date_time.append(line[0]+ "  " +line[1])
    timestamp.append(line[1])
    dns_name.append(line[6])
  except(IndexError):
    print "oops!! Index error detected.. continuing with next line"
    pass
if DEBUG : print 'Timestamp & dnsname contents : \n', timestamp, dns_name

# Convert time in hms format to seconds
secs =[hms_to_secs(hms) for hms in timestamp]
if DEBUG : print 'Time in sec : \n', secs

# Evaluate incremental time difference in secs for the queries
secs_diff = [0]
[secs_diff.append( secs[index+1] - secs[index]) for index in range(0,len(secs)-1)]
if DEBUG : print 'Diff in secs : \n', sorted(set(secs_diff)), len(secs_diff), len(timestamp)

# Merge time and dns_name
diff_query_dns = zip(secs_diff,dns_name)
if DEBUG :
  for tqd in diff_query_dns:
    print tqd

# Find possible new dns queries:
dns_requests = [diff_query_dns[0]]
dns_group = [diff_query_dns[0][1]]
dns_groups = []
existing_dns_queries =[]

for index in range(len(diff_query_dns) -1):

  diff2 = diff_query_dns[index+1][0]
  dns2 = diff_query_dns[index+1][1]

  if diff2 > NEW_DNS_REQ_THRES and dns2 not in dns_group and dns2.count('.') == 1:
    dns_requests.append(diff_query_dns[index+1])
    dns_groups.append(dns_group)
    dns_group = []

  else:
    dns_group.append(dns2)
dns_groups.append(dns_group)

# Print in format

for dns_group in dns_groups:
  count = 1
  index =  dns_name.index(dns_group[0])
  p = str(dns_group[0])+ ": "  + str(len(set(dns_group))) + " Time : " + date_time[index] + "\n"
  report_txt.write(p)

  for dns in list(OrderedDict.fromkeys(dns_group)):
    p = str(count) + ". " + dns + "\n"
    report_txt.write( p)
    count+=1
  report_txt.write( "\n\n")

dns_txt.close()


