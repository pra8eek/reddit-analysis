#!/usr/bin/env python
# coding: utf-8

# In[64]:


import bz2
import json
import time
import os.path


# In[65]:


submissions = bz2.open('RS_2017-01.bz2')
comments = bz2.open('RC_2017-01.bz2')


# In[66]:


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


# In[67]:


def JSONtoDict(x) :
    x = '{'+str(x)[3:-4]+'}'
    x = x.replace('\\\\"','').replace('\\','')
    try :
        y = json.loads(x, strict = False)
    except Exception as e :
        y = correction(e, x)
    return y


# In[68]:


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


# In[69]:


def writeComment(f, comment, instance_id):
    f.write('\t\t<Instance Id= "'+str(instance_id)+'" InstanceType= "Comment">'+"\n")
    f.write("\t\t\t<TimeStamp>"+"\n")
    f.write("\t\t\t\t<CreationUTC>"+str(comment["created_utc"])+"</CreationUTC> "+"\n")
    f.write("\t\t\t</TimeStamp>"+"\n")
    f.write("\t\t\t<Contributors>"+"\n")
    f.write("\t\t\t\t<OwnerUserId>"+comment["author"]+"</OwnerUserId>"+"\n")
    f.write("\t\t\t</Contributors>"+"\n")
    f.write("\t\t\t<Body>"+"\n")
    f.write("\t\t\t\t<Text>"+"\n")
    f.write("\t\t\t\t\t"+comment["body"]+"\n")
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
        filename = './ABC/'+submission['id'] + '.xml'
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
t1 = time.time()

for comment in comments :
    i += 1    
    comment = JSONtoDict(comment)
    
    if i%100000 == 0 :
        print(i," comments processed in ", int(time.time() - t1),"seconds. || ",j," failed")
        print("Conversion ratio = ",100*(i-j)/i,"%\n--------------------------------------------------------------------------")
    
    try :
        submissionID = comment['link_id'][3:]
        filename = './ABC/' + str(submissionID) + '.xml'
        if os.path.isfile(filename) :
            file = open(filename,"a")
        else :
            j += 1
            continue
            
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
    
t2 = time.time()
print("Phase 2 done in ",t2-t1,"seconds")


# In[61]:


i = 0
j = 0
t2 = time.time()

for submission in submissions :
    i += 1
    if i%100000 == 0 :
        print(str(i).format(7.0)," posts closed in ", int(time.time() - t2),"seconds\n--------------------------------------------------------------------------")
    
    try :  
        submission = JSONtoDict(submission)
        filename = './ABC/'+submission['id'] + '.xml'
    except :    
        j += 1
        continue
        
    if os.path.isfile(filename) :
        file = open(filename,"a")
    else :
        j += 1
        continue
    
    file.write('\t</KnowledgeData>'+"\n")
    file.write('</KnolML>')
    file.close()
    
t3 = time.time()    
print("Phase 3 done in ",t3-t2,"seconds")


# In[82]:


i = 1
for submission in submissions :
    submission = JSONtoDict(submission)
    filename = './ABC/'+submission['id'] + '.xml'
    if i == 0:
        break
    i -= 1
    with open(filename, "r") as f:
            searchlines = f.readlines()
            for x in searchlines :
                print(x)
    
    print("-------------------------------------")       

