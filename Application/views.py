from django.shortcuts import render
from app_enron.models import employes, adresses, destinataires, mails, references
from django.db.models import Q
from itertools import chain


"""      MENU     """

def menu(request): #OK
    return render(request, 'menu.tmpl',{})

"""      TABLE DES EMPLOYÉS     """

def employ(request): #OK
    d = {}
    adr = adresses.objects.filter(employe__gte=1)
    emp = employes.objects.all().order_by('poste')
    for e in emp:
        res = []
        for a in adr.filter(employe=e.id):
            res.append(a.adresse)
        d[e] = res
    return render(request,'employes.tmpl',
            {"adr" : d,
             "nb" : len(emp)
             })
    
"""      CONTENU DE MAIL     """
    
def ref(request): #OK
    if not 'idmail' in request.GET.keys():
        return render(request,'search_error.tmpl',{})
    idmail = request.GET['idmail']
    try  :
        idmail = int(idmail)
    except :
        return render(request,'search_error.tmpl',{})
    email = mails.objects.get(id=idmail)
    ref = references.objects.filter(mail=email)
    dest = destinataires.objects.filter(mail=email)
    destto = dest.filter(en_tant_que='TO')
    destcc = dest.filter(en_tant_que='CC')
    destbcc = dest.filter(en_tant_que='BCC')
    return render(request,'references.tmpl',
                  {"email":email,
                   "ref":ref,
                   "desti":destto,
                   "cc":destcc,
                   "bcc":destbcc})
    
"""      CONTENU DE DISCUSSION     """
    
def discu(request): #OK
    if not 'iddiscu' in request.GET.keys():
        return render(request,'search_error.tmpl',{})
    iddiscu = request.GET['iddiscu']
    try  :
        iddiscu = int(iddiscu)
    except :
        return render(request,'search_error.tmpl',{})
    emails = mails.objects.filter(discu=iddiscu).order_by('-date')
    return render(request,'mess1.tmpl',{'emails':emails})
    
    
    
    
    
''' RECHERCHE '''


def recherche(request):
    if not 'glob' in request.GET.keys():
        return render(request,'search_error.tmpl',{})
    else:
        choix = request.GET["glob"]
        debut = request.GET["from"]
        fin = request.GET["to"]
        emails = mails.objects.filter(Q(date__gte=debut),Q(date__lte=fin)).order_by('-date')
        if choix == "glob1" :
            return recherche_tous(request,emails)
        elif choix == "glob2" :
            return recherche_emp(request,emails)
        elif choix == "glob3" :
            return recherche_discu(request,emails)          
    return render(request, 'search_error.tmpl',{})



# TYPES DE RECHERCHE
    

def recherche_tous(request,emails):     #OK
    aff = request.GET['aff1']
    if aff == "messages":
        return render(request,'mess1.tmpl',{'emails':emails}) #OK
    elif aff == "relations":
        res = {}
        for m in emails:
            res[m]=destinataires.objects.filter(mail=m)
        return render(request,'rela1.tmpl',{'emails':res})
    elif aff == "discussions":
        return render(request,'discu1.tmpl',{'emails':emails})
    return render(request,'search_error.tmpl',{}) #OK
    
    
    
def recherche_emp(request,emails):
    aff = request.GET['aff2']
    try :
        log = request.GET['login2']
        id_prs = employes.objects.get(login=log).id
    except :
        return render(request,'search_error.tmpl',{})
    adr = adresses.objects.filter(employe=id_prs) # Adresses de l'employé
    res = {}
    L = []
    M = []
    if aff == "env":
        for a in adr :
            res[a.adresse] = emails.filter(expe=a)
        return render(request,'mess3.tmpl',{'emails':res}) #OK
    elif aff == "rec":
        for a in adr:
            L.append(destinataires.objects.filter(Q(desti=a),Q(en_tant_que='TO')))
        for i in L:
            for j in i:
                M.append(j.mail)
        return render(request,'mess2.tmpl',{'dest':M})
    elif aff == "cc":
        for a in adr:
            L.append(destinataires.objects.filter(Q(desti=a),Q(en_tant_que='CC')))
        for i in L:
            for j in i:
                M.append(j.mail)
        return render(request,'mess2.tmpl',{'dest':M})
    elif aff == "bcc":
        for a in adr:
            L.append(destinataires.objects.filter(Q(desti=a),Q(en_tant_que='BCC')))
        for i in L:
            for j in i:
                M.append(j.mail)
        return render(request,'mess2.tmpl',{'dest':M})
    elif aff == "tous":
        for a in adr:
            L.append(destinataires.objects.filter(Q(desti=a),Q(en_tant_que='BCC')))
            res[a.adresse] = emails.filter(expe=a)
        for i in L:
            for j in i:
                M.append(j.mail)
        return render(request,'mess4.tmpl',{'dest1':res,
                                            'dest2':M})
    return render(request,'search_error.tmpl',{})
    
    
    
def recherche_discu(request,emails): #OK
    iddiscu = request.GET["discu3"]
    try  :
        iddiscu = int(iddiscu)
    except :
        return render(request,'search_error.tmpl',{})
    emails = emails.filter(discu=iddiscu)
    res = {}
    for m in emails:
        res[m]=destinataires.objects.filter(mail=m)
    return render(request,'rela2.tmpl',{'id':iddiscu,
                                        'emails':res}) #OK







