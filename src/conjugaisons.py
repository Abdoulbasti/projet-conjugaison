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
        verbes_sujets_lower = {k: v.lower() for k, v in verbes_sujets.items()}
        
        phrase_conjugue = replace_verbs_in_sentence(phrase, temps, modele_langue, verbes_sujets_lower)
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
    
"""
PHRASES AUX PRÉSENTS : 
il vas à l'école et j'étudie le français
ils jouent au football, marquent des buts et célèbrent leurs victoires
J'aime les mangues bio, ils donnent des vitamines
alors que le monde avance sans relâche, je médite à travers l'écriture et la méditation
alors que les vagues s'écrasent contre les rochers, je contemple l'immensité de l'océan et je me sens bien
pendant que la ville s'agite, je me promène tranquillement dans les ruelles étroites, observant les détails architecturaux
alors que le soleil se lève à l'horizon, les oiseaux entament leur symphonie matinale


PHRASES À L'IMPARFAIT:
pendant que le vent soufflait doucement à travers les arbres, les feuilles dansaient gracieusement au sol
je lisais un livre pendant que mon ami écoutait de la musique
pendant que la vieille maison craquait sous le poids des années, les souvenirs s'entremêlaient dans chaque recoin
alors que la lune éclairait la scène, les acteurs improvisaient avec passion et créativité sur scène
nous avancions vers le parc, mangions des glaces et jouions ensemble
mon patron me confiait régulièrement de nouveaux projets
pendant que les étoiles scintillaient dans le ciel nocturne, les amoureux se promenaient main dans la main le long de la rivière
alors que la brume enveloppait la forêt, les oiseaux entonnaient un chant mystérieux et envoûtant


PHRASES AUX PASSÉ SIMPLE :
Tu achetas un nouveau livre pour enrichir ta collection
Dès que je reçus la lettre, je courus à la poste pour envoyer une réponse
Quand il vit le chien dans la rue, il s'arrêta, le regarda, et lui offrit un morceau de son sandwich


PHRASES AUX FUTUR:
les amis de mes amis arriveront demain
elle achètera les ingrédients nécessaires et préparera un dîner spécial pour nous
ils arriveront à l'aéroport, prendront un taxi, et nous rejoindront à l'hôtel
il fera ses valises et prendra le premier avion pour Paris
"""