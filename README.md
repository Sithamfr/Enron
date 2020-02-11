Mise en place d'une interface Python/Django pour la sélection d'informations dans une base de donnée de mail hébergées sur serveur MySQL.<br>
Les templates ont eux aussi été créé par moi-même.

  Ces données sont publiques et peuvent-être récupérées sur le site enrondata.org

  Nous avons un dossier 'enron' contenant un fichier 'employes.csv' et un sous-dossier 'maildir'.

     .'employes.csv' référence les employés, leurs caractéristiques et leurs adresses mails professionnelles.

     .'maildir' contient tous les mails associés aux employés du fichier csv.

  Nous créons une base de données grâce à l'ORM Django associé à Python.

  Une fois cette base de données créée, nous créons un logiciel à ouvrir dans le navigateur permettant d'interagir avec les données et rechercher des informations particulières.

  Cette application n'est exécutable que localement et n'est donc pas disponible car non hébergée sur internet.
