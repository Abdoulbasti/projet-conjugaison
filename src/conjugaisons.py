import spacy
from mlconjug3 import Conjugator
                    
def sujet_de_verbe(modele_francais, phrase) : 
    # Analyser une phrase
    #doc = modele_francais("Le chat mange la souris.")
    doc = modele_francais(phrase)

    subjects = {}
    # Parcourir les tokens de la phrase
    for token in doc:
        # Vérifier si le token est un verbe
        if token.pos_ == "VERB":
            # Parcourir les enfants du verbe
            for child in token.children:
                # Vérifier si le rôle du token enfant est 'sujet'
                if child.dep_ in ["nsubj", "nsubjpass"]:
                    # Enregistrer le sujet du verbe
                    subjects[token.text] = child.text

            # Si le verbe n'a pas de sujet direct, essayer de trouver le sujet du verbe conjugué le plus proche à gauche
            if token.text not in subjects:
                for left_token in reversed(doc[:token.i]):
                    if left_token.pos_ == "VERB" and left_token.text in subjects:
                        subjects[token.text] = subjects[left_token.text]
                        break
    return subjects
    


def sujet_de_verbe_infinitif(modele_francais, phrase) : 
    # Analyser une phrase
    #doc = modele_francais("Le chat mange la souris.")
    doc = modele_francais(phrase)

    subjects = {}
    # Parcourir les tokens de la phrase
    for token in doc:  
        # Vérifier si le token est un verbe
        if token.pos_ == "VERB":
            # Parcourir les enfants du verbe
            for child in token.children:
                # Vérifier si le rôle du token enfant est 'sujet'
                if child.dep_ in ["nsubj", "nsubjpass"]:
                    # Enregistrer le sujet du verbe
                    subjects[token.lemma_] = child.text

            # Si le verbe n'a pas de sujet direct, essayer de trouver le sujet du verbe conjugué le plus proche à gauche
            if token.lemma_ not in subjects:
                for left_token in reversed(doc[:token.i]):
                    if left_token.pos_ == "VERB" and left_token.lemma_ in subjects:
                        subjects[token.lemma_] = subjects[left_token.lemma_]
                        break
    return subjects
    
    



def get_number(sujet, modele):
    doc = modele(sujet)
    
    # Si le texte représente une entité nommée
    if doc.ents:
        for token in doc.ents[0]:
            if 'Number=Plur' in token.morph:
                return 'Plural'
        return 'Singular'
    # Sinon, le texte est considéré comme un nom simple ou composé
    else:
        if 'Number=Sing' in doc[0].morph:
            return 'Singular'
        elif 'Number=Plur' in doc[0].morph:
            return 'Plural'
        else:
            return 'Unknown'       
        
        

# Fonction pour remplacer tous les verbes dans une phrase
def replace_verbs_in_sentence(sentence, temps, modele, verbes_sujets):
    sujets = ['je', "j'", 'tu', 'il', 'on', 'elle', 'nous', 'vous', 'ils', 'elles']
    doc = modele(sentence)
    new_sentence = []
    
    
    for token in doc:
        
        if token.pos_ == "VERB":
            verbes = verbes_sujets.keys()
            for verb in verbes :
                #if verb == token.pos_ :
                if verb == token.lemma_ : #token.lemma_ -> verbe à l'infinitif
                    
                    
                    #On fait la conjugaison classic
                    if verbes_sujets[verb] in sujets :
                        #on fait une congugaison classique
                        if verbes_sujets[verb] == "j'" :
                            new_verb = conjugate_verb(verb, temps,"je")
                            new_sentence.append(new_verb)
                        elif verbes_sujets[verb] == 'on' or verbes_sujets[verb] == 'il' or verbes_sujets[verb] == 'elle':
                            new_verb = conjugate_verb(verb, temps,"il (elle, on)")
                            new_sentence.append(new_verb)
                        
                        elif verbes_sujets[verb] == 'ils' or verbes_sujets[verb] == 'elles':
                            new_verb = conjugate_verb(verb, temps,"ils (elles)")
                            new_sentence.append(new_verb)
                            
                        else :
                            new_verb = conjugate_verb(verb, temps, verbes_sujets[verb])
                            new_sentence.append(new_verb)
                      
                      
                    #Cette veut dire que le sujet n'est pas un pronom personnel classic, on doit alors faire les traitement necessaire     
                    elif verbes_sujets[verb] not in sujets : 
                        if get_number(verbes_sujets[verb], modele) == "Singular" :
                            new_verb = conjugate_verb(verb, temps,"il (elle, on)")
                            new_sentence.append(new_verb)
                        
                        elif get_number(verbes_sujets[verb], modele) == "Unknown" :
                            new_verb = conjugate_verb(verb, temps,"il (elle, on)")
                            new_sentence.append(new_verb)
                        
                        elif get_number(verbes_sujets[verb], modele) == "Plural" :
                            new_verb = conjugate_verb(verb, temps,"ils (elles)")
                            new_sentence.append(new_verb)
        
        else:
            new_sentence.append(token.text)
    
            
    return ' '.join(new_sentence)




#Conjugaison de verbe est correct !!!!
#conjugate_verb('manger', 'Présent', 'je')

def conjugate_verb(verb, tense, subject):
    # Créer une instance de Conjugator pour le français
    conjugator = Conjugator(language='fr')
    # Obtenir la conjugaison du verbe spécifié
    conjugated_verb = conjugator.conjugate(verb)
    # Récupérer la forme spécifiée du verbe conjugué
    # Afficher le contenu de conjugated_verb.conjug_info['Indicatif']
    #print(conjugated_verb.conjug_info['Indicatif'])
    conjugated_form = conjugated_verb.conjug_info['Indicatif'][tense][subject]
    return conjugated_form




def conjugaison_phrase(phrase, temps, modele_langue) :
    try:
        verbes_sujets = sujet_de_verbe_infinitif(modele_langue, phrase)
        phrase_conjugue = replace_verbs_in_sentence(phrase, temps, modele_langue, verbes_sujets)
        return phrase_conjugue
        
        
    except AttributeError as e1:
        message_erreur = str(e1)
        return "Erreur AttributeError :" + message_erreur
    except TypeError as e2:
        message_erreur = str(e2)
        return "Erreur TypeError :" + message_erreur
    except ValueError as e3:
        message_erreur = str(e3)
        return "Erreur ValueError :" + message_erreur
    except NameError as e4:
        message_erreur = str(e4)
        return "Erreur NameError :" + message_erreur
    except IndexError as e5: 
        message_erreur = str(e5)
        return "Erreur AttributeError :" + message_erreur
    except KeyError as e6: 
        message_erreur = str(e6) 
        return "Erreur KeyError :" + message_erreur 
    
    
    
    
    
    
    
    
    
    
    
    
#modele_francais = spacy.load('fr_dep_news_trf')
modele_francais = spacy.load('fr_core_news_sm')

p_present0 = "je vais à l'école et j'étudie le français." #OK
p_present1 = "tu manges, tu bois et tu discutes avec tes amis." #OK, probleme avec le petit modele
p_present2 = "tes voisins lui prêtent souvent leur voiture." #Ok , probleme avec le petit modele
p_present5 = "ils jouent au football, marquent des buts et célèbrent leurs victoires." #Ok
p_present4 = "alors que le monde avance sans relâche, je médite à travers l'écriture et la méditation." #OK
p_present3 = "pendant qu'il court doucement, les fleurs s'épanouissent et embaument l'air de leur parfum enivrant." #OK, probleme avec le petit modele
p_present6 = "alors que les vagues s'écrasent contre les rochers, je contemple l'immensité de l'océan et je me sens bien." #OK 
p_present7 = "pendant que la ville s'agite, je me promène tranquillement dans les ruelles étroites, observant les détails architecturaux." #OK
p_present8 = "alors que le soleil se lève à l'horizon, les oiseaux entament leur symphonie matinale." #OK
textes_presents = [p_present0, p_present1, p_present2, p_present3, p_present4, p_present5, p_present6, p_present7, p_present8 ]


p_imparfait0 = "pendant que le vent soufflait doucement à travers les arbres, les feuilles dansaient gracieusement au sol." #OK
p_imparfait1 = "je lisais un livre pendant que mon ami écoutait de la musique." #OK
p_imparfait2 = "pendant que la vieille maison craquait sous le poids des années, les souvenirs s'entremêlaient dans chaque recoin." #OK
p_imparfait3 = "alors que la lune éclairait la scène, les acteurs improvisaient avec passion et créativité sur scène." #OK
p_imparfait4 = "nous avancions vers le parc, mangions des glaces et jouions ensemble."#OK
p_imparfait5 = "mon patron me confiait régulièrement de nouveaux projets." #OK
p_imparfait6 = "elles étudiaient à la bibliothèque, lisaient des livres et prenaient des notes." #OK
p_imparfait7 = "pendant que les étoiles scintillaient dans le ciel nocturne, les amoureux se promenaient main dans la main le long de la rivière."#OK
p_imparfait8 = "alors que la brume enveloppait la forêt, les oiseaux entonnaient un chant mystérieux et envoûtant."#OK
textes_imparfaits = [p_imparfait0, p_imparfait1, p_imparfait2, p_imparfait3, p_imparfait4, p_imparfait5, p_imparfait6, p_imparfait7, p_imparfait8]         


# Ceci est la forme utilisé -> 'il (elle, on)' et 'ils (elles)'

"""
def main(modele):
    print("Bonjour, bienvenue dans mon programme !!!!...................")
    temps1 = "Présent"
    temps2 = "Imparfait"
    temps3 = "Passé Simple"
    #print(conjugate_verb('manger', temps1, 'ils (elles)'))  # Résultat : 'mange'
    #conjugate_verb('manger', temps1, '1s')
    conjugaison_phrase(textes_presents[8], temps2, modele)
    

# Ceci permet d'exécuter la fonction main() seulement si ce fichier est exécuté directement (et non importé comme un module)
if __name__ == "__main__":
    main(modele_francais)"""