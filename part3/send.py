import os
str0 = "POST /mcs/v2/devices/"
str1 = "/datapoints.csv HTTP/1.1\n"
str2 = "Host: api.mediatek.com\n"
str3 = "deviceKey: "
str4 = "\n"
str5 = "Cache-Control: no-cache\n"
str6 = "Content-Length: "

def send_data_point(devID, devKey, dataID, dataValue):
    f = open('asjflksajf',"w")
    f.write(str0 + devID + str1)
    f.write(str2)
    f.write(str3+devKey+str4)
    f.write(str5)
    contLen = len(dataID+",,"+dataValue)
    f.write(str6+str(contLen)+"\n")
    f.write("\n")
    f.write(dataID+",,"+dataValue);
    f.write("\n")
    f.write("\n")
    f.close()
    os.system("telnet api.mediatek.com 80 < asjflksajf")
    os.system("rm asjflksajf")

send_data_point("DnAi0j9n","es9mBYPEZ9hOW3c9","2","7122")


