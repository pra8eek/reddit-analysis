import bs4 as bs
import urllib.request
import bz2
import json

file = bz2.open('RS_2017-01.bz2')

def correction(e, x, y):
    try :
        e = str(e)[::-1]
        e = int(e[1:e.index(' ')][::-1])
        x = x[:e-3]+'"'+x[e-2:]
        y = json.loads(x, strict = False)
        return y
    except Exception as e :
        y = correction(e, x, y)        

def writeStart(f, submission, instance_id) :
    f.write("<?xml version='1.0' encoding='utf-8'?>"+"\n")
    f.write("<KnolML>"+"\n")
    f.write('\t<KnowledgeData Type="Submision" Id= "'+str(submission['id'])+'">'+"\n")
    f.write('\t\t<Title>'+submission['title']+'</Title>'+"\n")
    f.write('\t\t<Instance Id= "'+str(instance_id)+'" InstanceType= "Description">'+"\n")
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

for line in file :
    instance_id = 1
    x = '{'+str(line)[3:-4]+'}'
    x = x.replace('\\\\"','').replace('\\','')
    try :
        submission = json.loads(x, strict = False)
    except Exception as e :
        submission = correction(e, x, y)
    
    filename = submission['id'] + '.xml'
    f = open(filename,"w+")
    writeStart(f, submission, instance_id)
    
    submission_id = submission['id']
    url = 'https://api.pushshift.io/reddit/submission/comment_ids/' + submission_id
    sauce = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')
    
    comment_ids = json.loads(soup.p.string)['data']
    
    for comment_id in comment_ids :
        url = 'http://api.pushshift.io/reddit/search/comment/?ids=' + comment_id
        saucee = urllib.request.urlopen(url).read()
        soupp = bs.BeautifulSoup(saucee, 'lxml')
    
        comment_description = json.loads(soupp.p.string)['data']
        
        for comment in comment_description :
            instance_id += 1
            writeComment(f, comment, instance_id)
    
    f.write('\t</KnowledgeData>'+"\n")
    f.write('</KnolML>')
