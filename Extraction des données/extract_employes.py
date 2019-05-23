from app_enron.models import employes



'''
EMPLOYES
''' 

def extract_employes():
    with open("/users/mmath/echange/enron/employes.csv") as f:
        F = f.readlines()
    F[0] = F[0].replace('\\N','"N/A"')   # correction erreur en première ligne
    for ligne in F:
        tmp = ligne[:-1].replace('"','').split(',')
        emp = employes(nom=tmp[0],prenom=tmp[1],login=tmp[6],poste=tmp[7])
        emp.save()
    
    
if __name__ == '__main__':
    extract_employes()