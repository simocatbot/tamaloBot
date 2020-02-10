from statistics import mean

total_scores = {}

def arrange_scores(scores): #funzione per riordinare i punteggi e update del total score, insieme a medie.

    global total_scores

    scores = scores.upper() #per evitare il problema di case sensitivity
    current_score = scores.split() #creazione di una lista con l'input degli ultimi scores
    it = iter(current_score) 
    res_dict = dict(zip(it,it)) #creazione del dict che matcha persona con il suo punteggio grazioe all'iteratore iter
    for key in res_dict:
        res_dict[key] = int(res_dict[key]) #trasformazione in int 

    result = {key: res_dict.get(key, 0) + total_scores.get(key, 0) 
        for key in set(res_dict) | set(total_scores)} #Risultati sommati di tutta la partita   
    
    reply = {k: v for k, v in sorted(result.items(), key=lambda item: item[1])}

    somma=sum(res_dict.values()) #calcolo di alcune statistiche della mano
    reply_1 = round(somma/len(result), 2)
    reply_2 = round(mean(result[k] for k in result),2)
    reply_3 = round((reply_2/15),2)
    reply_4 = round((reply_1/15),2)
    reply_out = '\n'.join(str([v, reply[v]]) for v in reply) #creazione della stringa di risposta, iniziando con i risultati totali ordinati 
    reply_out = reply_out + '\n\nLa media totale della partita è: '+ str(reply_2) + '\nOvvero ' + str(reply_3) + ' Tamalo-i' + '\n\nLa media dell ultima partita è: ' + str(reply_1) + '\nOvvero ' + str(reply_4) + ' Tamalo-i'
    reply_out = reply_out.replace('[','')
    reply_out = reply_out.replace(']','')
    reply_out = reply_out.replace("""'""",'')

    for key in result: #check se qualcuno è andato sopr i 100 punti
        if result[key] >= 100:
            reply_out = reply_out +'\n\n' + key + ' è OVER, con un punteggio di ' + str(result[key])

    total_scores = result #update della variabile total score
    #print(total_scores)

    return reply_out

