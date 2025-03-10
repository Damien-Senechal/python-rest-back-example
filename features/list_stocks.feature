Feature: Consulter tous les articles
    En tant que gestionnaire de stock
    Je veux voir la liste de tous les articles en stock
    Afin de suivre les niveaux d'inventaire

    Scenario: Liste avec plusieurs articles
        Given les articles suivants existent dans la base:
            | name   | quantity | price |
            | Crayon | 100      | 0.99  |
            | Cahier | 50       | 2.99  |
        When je fais une requête GET "/api/stocks"
        Then le code de statut est 200
        And la réponse contient 2 articles
        And l'article "Crayon" a une quantité de 100
        And l'article "Cahier" a une quantité de 50

    Scenario: Liste vide
        Given la base données est vide
        When je fais une requête GET "/api/stocks"
        Then le code de statut est 200
        And la réponse est une liste vide

Feature: Consulter un article spécifique
    En tant que gestionnaire de stock
    Je veux voir les details d'un article precis
    Afin de verifier son etat actuel

    Scenario: Consulter un article existant
        Given un article exsite avec:
            | name   | quantity | price |
            | Crayon | 100      | 0.99  |
        When je fais une requete GET "/api/stocks/1"
        Then le code de statut est 200
        And la reponse contient les details:
            | name     | Crayon |
            | quantity | 100    |
            | price    | 0.99   |

    Scenario: Consulter un article inexistant
        When je fais une requete GET "/api/stocks/999"
        Then le code de statut est 404