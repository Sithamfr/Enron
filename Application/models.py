from django.db import models


class employes(models.Model):
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=20)
    login = models.CharField(max_length=20, unique=True)
    poste = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nom, self.prenom, self.login, self.poste
    

class adresses(models.Model):
    employe = models.IntegerField()
    adresse = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.employe, self.adresse
    
    
class mails(models.Model):
    date = models.DateTimeField()
    expe = models.ForeignKey(adresses, on_delete=models.CASCADE)
    objet = models.CharField(max_length=400, default="")
    corps = models.TextField()
    discu = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.date, self.expe, self.corps, self.discu, self.idmail, self.objet
    

class destinataires(models.Model):
    mail = models.ForeignKey(mails, on_delete=models.CASCADE)
    desti = models.ForeignKey(adresses, on_delete=models.CASCADE)
    en_tant_que = models.CharField(max_length=3) # to, cc, bcc
    
    def __str__(self):
        return self.mail, self.desti, self.en_tant_que
    
    
class references(models.Model):
    mail = models.ForeignKey(mails, on_delete=models.CASCADE)
    dossier = models.CharField(max_length=200, default="")
    id_original = models.CharField(max_length=60, default="")
    
    def __str__(self):
        return self.mail, self.id_original, self.dossier