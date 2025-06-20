


#Calculateur
def calculateur(queue_demandes, queue_retour):
    while True:
        element = queue_demandes.get()
        if element == "Fin de demande":
            break
        value1, value2, operator, demandeur_id = element
            
        match operator:
            case "+":
                res = value1 + value2
            case "-":
                res = value1 - value2
            case "*":
                res = value1 * value2               
            case "/":
                res = value1 / value2
                # if value2 == 0:   # Plus très utile car on a retiré la possibilité d'avoir 0 au dénominateur
                #     raise ZeroDivisionError

        queue_retour[demandeur_id].put(res)