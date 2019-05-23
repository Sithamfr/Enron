#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 16:03:19 2019

@author: cordier
"""




import re
import email.parser as ep
import os
from django.core.exceptions import ObjectDoesNotExist
from app_enron.models import adresses, destinataires, mails, references






'''
EMPLOYES
''' 
def dico_employes():
    dico={}
    with open("/users/mmath/echange/enron/employes.csv") as f:
        F = f.readlines()
    F[0] = F[0].replace('\\N','"N/A"')   # correction erreur en première ligne
    K = 1
    for ligne in F:
        tmp = ligne[:-1].replace('"','').split(',')
        mails = tmp[2:6]
        for adr in mails:
            dico[adr]=K
        K+=1
    return dico # retourne les id






'''
EXTRACTION
'''

          
            
def extract_fichier(nom,discu,charset='utf-8'):
    
    doss = nom[34:]
    print(doss)
    
    try :
    
        with open(nom, encoding=charset) as f:
            c = f.read()
    
        found = re.compile(r'\n\n').search(c)
        entete = c[:found.span()[0]]
        contenu = c[found.span()[1]:]
            
        entete_sep = ep.Parser().parsestr(entete)
    
        mail_id = entete_sep.get('Message-ID')
        obj = entete_sep.get('Subject')
        exp = entete_sep.get('From')
        dest = entete_sep.get('To')
        cc = entete_sep.get('Cc')
        bcc = entete_sep.get('Bcc')
        
    
    
        # DATE HORAIRES GMT
        date = re.compile(r"Date:.* \(").search(entete).group()[11:].split(' ')
        date[4] = date[4][:3] + ":" + date[4][3:]
        date = f"{date[2]}-{mois[date[1]]}-{date[0]}T{date[3]}{date[4]}"
        
        sep = re.compile(r'\w[^\s,<>]*@[^\s,<>]+')
        if exp :
            exp = exp.replace("'","").replace('"','').replace(' ','')
            exp = sep.findall(exp)[0]
        if dest :
            dest = dest.replace("'","").replace('"','').replace(' ','')
            dest = sep.findall(dest)
        else : dest = [exp]
        if cc :
            cc = cc.replace("'","").replace('"','').replace(' ','')
            cc = sep.findall(cc)
        if bcc :
            bcc = bcc.replace("'","").replace('"','').replace(' ','')
            bcc = sep.findall(bcc)

                
            
    #         ADRESSE EXPEDITEUR
        

    
        try :
            expediteur = adresses.objects.get(adresse=exp)
        except ObjectDoesNotExist :
            if exp in d_emp.keys():
                emp = d_emp[exp]
            else:
                emp = 0
            expediteur = adresses(employe=emp,adresse=exp)
            expediteur.save()
                
        try :
            tabl_mail = mails.objects.get(date=date,expe=expediteur,objet=obj)
        except ObjectDoesNotExist :
                
        
    #             MAILS
        
            obj2 = obj.replace("Re: ","")
            if not obj2 in discu :
                discu.append(obj2)
            iddiscu = discu.index(obj2)
        
            tabl_mail = mails(date=date,expe=expediteur,objet=obj,corps=contenu,discu=iddiscu)
            tabl_mail.save()
    
            
        
    #           ADRESSES + DESTINATAIRES
        
            for adr in dest:
                try :
                    tabl_adr = adresses.objects.get(adresse=adr)
                except ObjectDoesNotExist :
                    if adr in d_emp.keys():
                        emp = d_emp[adr]
                    else:
                        emp = 0
                    tabl_adr = adresses(employe=emp,adresse=adr)
                    tabl_adr.save()
                relation = destinataires(mail=tabl_mail,desti=tabl_adr,en_tant_que="TO")
                relation.save()
            
            if cc:
                for adr in cc:
                    try :
                        tabl_adr = adresses.objects.get(adresse=adr)
                    except ObjectDoesNotExist :
                        if adr in d_emp.keys():
                            emp = d_emp[adr]
                        else:
                            emp = 0
                        tabl_adr = adresses(employe=emp,adresse=adr)
                        tabl_adr.save()
                    relation = destinataires(mail=tabl_mail,desti=tabl_adr,en_tant_que="CC")
                    relation.save()
              
            if bcc:
                for adr in bcc:
                    try :
                        tabl_adr = adresses.objects.get(adresse=adr)
                    except ObjectDoesNotExist :
                        if adr in d_emp.keys():
                            emp = d_emp[adr]
                        else:
                            emp = 0
                        tabl_adr = adresses(employe=emp,adresse=adr)
                        tabl_adr.save()
                    relation = destinataires(mail=tabl_mail,desti=tabl_adr,en_tant_que="BCC")
                    relation.save()
                
                            

#           REFERENCES
        ref = references(mail=tabl_mail,dossier=doss,id_original=mail_id)
        ref.save()
        
                
    except UnicodeError :
        discu = extract_fichier(nom,discu,'latin-1')
            
    return discu


        
''' essai avec dir : /users/mmath/echange/enron/maildir/brawner-s/contract '''


        
def extract(path1,discu):
    for i in os.listdir(path1):
        path2 = path1 + "/" + i
        if os.path.isdir(path2):
            extract(path2,discu)
        elif os.path.isfile(path2):
            try :
                discu = extract_fichier(path2,discu)
                print(f"{next(evol)/5174.01} %")
            except :
                trait.write(path2+"\n")
                print("Erreur")
    return




if __name__=='__main__':
    mois = {"Jan":"01", "Feb":"02", "Mar":"03", "Apr":"04", "May":"05", "Jun":"06", "Jul":"07",
            "Aug":"08", "Sep":"09", "Oct":"10", "Nov":"11", "Dec":"12"}
    discu = ["Liste des objets"]
    d_emp = dico_employes()
    evol = iter(range(517401))
    trait = open("trait.txt","w")
    trait.write("Fichier non ajouté à la base de données :\n\n")
    extract("/users/mmath/echange/enron/maildir",discu)
    trait.close()





