import bz2
import json

submissions = bz2.open('RS_2017-01.bz2')
comments = bz2.open('RC_2017-01.bz2')

def correction(e, x):
    e = ""
    while True :
        try :
            e = str(e)[::-1]
            e = int(e[1:e.index(' ')][::-1])
            x = x[:e-3]+'"'+x[e-2:]
            y = json.loads(x, strict = False)
            return y
        except Exception as e :
            continue

def JSONtoDict(x) :
    x = '{'+str(x)[3:-4]+'}'
    x = x.replace('\\\\"','').replace('\\','')
    try :
        y = json.loads(x, strict = False)
    except Exception as e :
        y = correction(e, x)
    return y

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

for submission in submissions :
    submission = JSONtoDict(submission)
    filename = './KnolML/'+submission['id'] + '.xml'
    file = open(filename,"w+")
    writeStart(file, submission)

for comment in comments :
    comment = JSONtoDict(comment)
    submissionID = comment['link_id'][3:]
    filename = './KnolML/' + submissionID + '.xml'
    try :
        file = open(filename,"a")
    except :
        continue
    writeComment(file, comment, 0)

for submission in submissions :
    submission = JSONtoDict(submission)
    filename = './KnolML/'+submission['id'] + '.xml'
    file = open(filename,"w+")
    writeStart(file, submission)
    file.write('\t</KnowledgeData>'+"\n")
    file.write('</KnolML>')