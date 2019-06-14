#!/usr/bin/env python
# coding: utf-8

# In[2]:


import bz2
import json
import time

# In[3]:


submissions = bz2.open('RS_2017-01.bz2')
comments = bz2.open('RC_2017-01.bz2')


# In[4]:


def correction(e, x):
    i = 0
    if str(e).find("Expecting ',' delimiter:") != 0 :
        return e
    try :
        e = str(e)[::-1]
        e = int(e[1:e.index(' ')][::-1])
        x = x[:e-3]+'"'+x[e-2:]
        y = json.loads(x, strict = False)
        return y
    except Exception as e :
        y = correction(e, x)        


# In[5]:


def JSONtoDict(x) :
    x = '{'+str(x)[3:-4]+'}'
    x = x.replace('\\\\"','').replace('\\','')
    try :
        y = json.loads(x, strict = False)
    except Exception as e :
        y = correction(e, x)
    return y


# In[6]:


def writeStart(f, submission) :
    f.write("<?xml version='1.0' encoding='utf-8'?>"+"\n")
    f.write("<KnolML>"+"\n")
    f.write('\t<KnowledgeData Type="Submision" Id= "'+str(submission['id'])+'">'+"\n")
    f.write('\t\t<Title>'+submission['title']+'</Title>'+"\n")
    f.write('\t\t<Instance Id= "1" InstanceType= "Description">'+"\n")
    f.write("\t\t\t<TimeStamp>"+"\n")
    f.write("\t\t\t\t<CreationUTC>"+str(submission['created_utc'])+"</CreationUTC> "+"\n")
    f.write("\t\t\t</TimeStamp>"+"\n")
    f.write("\t\t\t<Contributors>"+"\n")
    f.write("\t\t\t\t<OwnerUserId>"+submission['author']+"</OwnerUserId> "+"\n")
    f.write("\t\t\t</Contributors>"+"\n")  
    f.write("\t\t\t<Body>"+"\n")
    f.write("\t\t\t\t<Text>"+"\n")
    f.write("\t\t\t\t\t"+submission['selftext']+"\n")
    f.write("\t\t\t\t</Text> "+"\n")
    f.write("\t\t\t</Body>"+"\n")  
    f.write("\t\t\t<Credit>"+"\n")
    f.write("\t\t\t\t<Score>"+str(submission['score'] if 'score' in submission else 0)+"</Score> "+"\n")
    f.write("\t\t\t</Credit>"+"\n")   
    f.write('\t\t</Instance>'+"\n")


# In[7]:


def writeComment(f, comment, instance_id):
    f.write('\t\t<Instance Id= "'+str(instance_id)+'" InstanceType= "Comment">'+"\n")
    f.write("\t\t\t<TimeStamp>"+"\n")
    f.write("\t\t\t\t<CreationUTC>"+str(comment["created_utc"])+"</CreationUTC> "+"\n")
    f.write("\t\t\t</TimeStamp>"+"\n")
    f.write("\t\t\t<Contributors>"+"\n")
    f.write("\t\t\t\t<OwnerUserId>"+str(comment["author"])+"</OwnerUserId>"+"\n")
    f.write("\t\t\t</Contributors>"+"\n")
    f.write("\t\t\t<Body>"+"\n")
    f.write("\t\t\t\t<Text>"+"\n")
    f.write("\t\t\t\t\t"+str(comment["body"])+"\n")
    f.write("\t\t\t\t</Text> "+"\n")
    f.write("\t\t\t</Body>"+"\n")
    f.write("\t\t\t<Credit>"+"\n")
    f.write("\t\t\t\t<Score>"+str(comment['score'] if 'score' in comment else 0)+"</Score> "+"\n")
    f.write("\t\t\t</Credit>"+"\n")
    f.write('\t\t</Instance>'+"\n")


# In[9]:


i = 0
j = 0
t0 = time.time()

for submission in submissions :
    i += 1
    if i%100000 == 0 :
        print(str(i).format(7.0)," posts opened in ", int(time.time() - t0),"seconds\n--------------------------------------------------------------------------")
    submission = JSONtoDict(submission)
    try :
        filename = './KnolML/'+submission['id'] + '.xml'
    except Exception as e:
        j += 1
        print("Accuracy = ",'{:f}'.format(100*(i-j)/i),"% \t",submission)
        continue
    file = open(filename,"w+")
    writeStart(file, submission)

t1 = time.time()
print("Phase 1 done in ",t1-t0,"seconds")


# In[10]:

 
i = 0
j = 0
for comment in comments :
    i += 1
    comment = JSONtoDict(comment)
    if i%100000 == 0 :
        print(i," comments processed in ", int(time.time() - t1),"seconds. || ",j," failed")
        print("Conversion ratio = ",100*(i-j)/i,"%\n--------------------------------------------------------------------------")
    try :
        submissionID = comment['link_id'][3:]
        filename = './KnolML/' + str(submissionID) + '.xml'
        file = open(filename,"a")
    except Exception as e:
        j += 1
        print(e)
        continue
    
    instance_id = 0
    with open(filename, "r") as f:
        searchlines = f.readlines()
        for _, line in enumerate(searchlines):
            if '\t\t<Instance Id= "' in line: 
                instance_id += 1
                
    writeComment(file, comment, instance_id+1)
    print(i, j)

t2 = time.time()
print("Phase 2 done in ",t2-t0,"seconds")


# In[11]:


i = 0
j = 0
for submission in submissions :
    i += 1
    if i%100000 == 0 :
        print(str(i).format(7.0)," posts closed in ", int(time.time() - t2),"seconds\n--------------------------------------------------------------------------")
    try :  
        submission = JSONtoDict(submission)
        filename = './KnolML/'+submission['id'] + '.xml'
    except :    
        i -= 1
        continue
    file = open(filename,"w+")
    writeStart(file, submission)
    file.write('\t</KnowledgeData>'+"\n")
    file.write('</KnolML>')
    
t3 = time.time()    
print("Phase 2 done in ",t3-t0,"seconds")
