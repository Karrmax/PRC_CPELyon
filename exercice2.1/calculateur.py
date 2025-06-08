


#Calculateur
def calculateur(queue_demandes, queue_retour):
    while True:
        item = queue_demandes.get()
        if item == "Fin de demande":
            break
        value1, value2, operator, demandeur_id = item
            
        match operator:
            case "+":
                res = value1 + value2
            case "-":
                res = value1 - value2
            case "*":
                res = value1 * value2               
            case "/":
                res = value1 / value2
                # if value2 == 0:   # Plus très car on retiré la possibilité d'avoir 0 au dénominateur
                #     raise ZeroDivisionError

        queue_retour[demandeur_id].put(res)