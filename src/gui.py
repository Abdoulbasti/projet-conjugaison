from tkinter import *
import conjugaisons
import spacy
import random

modele_francais = spacy.load('fr_core_news_sm')

BACKGROUND_COLOR_1 = "#e6e9f2"
BACKGROUND_COLOR_2 = "#dbdee7"
THEME_COLOR_1 = "#183798" # bleu marine
BUTTON_COLOR = "#f2f2f2"
BUTTON_COLOR_ACTIVE = "#ececec"
BUTTON_COLOR_SELECTED = "#8b9fe0"
BUTTON_COLOR_SELECTED_ACTIVE = "#788dd3"
BUTTON_HB_COLOR = "#9fa4b4"
POLICE = "Liberation Sans"

SOURCE_SELECTED = None
TARGET_SELECTED = None



def copy_text():
    try:
        sel_start = target_text.tag_ranges("sel")[0]
        sel_end = target_text.tag_ranges("sel")[1]
        selected_text = target_text.get(sel_start, sel_end)
        target_text.clipboard_clear()
        target_text.clipboard_append(selected_text)
    except IndexError:
        pass

def show_context_menu(event):
    context_menu.tk_popup(event.x_root, event.y_root)

def get_button_name(button):
    return button["text"].capitalize()
        
def pick_random_target(exclued):
    temps = None
    while(True):
        temps = random.choice(list(target_buttons.values()))
        if temps["button"]["text"].capitalize() != exclued : break
    return temps

def initialize_button(master, origin, name, is_selected):
    if is_selected :
        frame = Frame(master, bg=BACKGROUND_COLOR_2, 
              highlightbackground = THEME_COLOR_1, highlightthickness = 3) 
        button = Button(frame, text=name,
              bg=BUTTON_COLOR_SELECTED, activebackground=BUTTON_COLOR_SELECTED_ACTIVE, 
              font=(POLICE, '10', 'bold'), relief='flat')
    else :
        frame = Frame(master, bg=BACKGROUND_COLOR_2,  
              highlightbackground = BUTTON_HB_COLOR, highlightthickness = 1)
        button = Button(frame, text=name,
              font=(POLICE, '10'), bg=BUTTON_COLOR, relief='flat') 
        
    return {"origin" : origin, "frame" : frame, "button" : button}
  
def switch_buttons(old_selected, new_selected):
    # un-set selected
    old_selected["button"].config(bg=BUTTON_COLOR)
    old_selected["button"].config(font=(POLICE, '10'))
    old_selected["button"].config(activebackground=BUTTON_COLOR_ACTIVE)
    old_selected["frame"].config(highlightbackground=BUTTON_HB_COLOR)
    old_selected["frame"].config(highlightthickness=1)
    
    # set selected
    new_selected["button"].config(bg=BUTTON_COLOR_SELECTED)
    new_selected["button"].config(font=(POLICE, '10', 'bold'))
    new_selected["button"].config(activebackground=BUTTON_COLOR_SELECTED_ACTIVE)
    new_selected["frame"].config(highlightbackground=THEME_COLOR_1)
    new_selected["frame"].config(highlightthickness=3)

def temps_select(temps):
    global SOURCE_SELECTED, TARGET_SELECTED
    new_selected_name = get_button_name(temps["button"])
    if temps['origin'] == "source": 
        # on vérifie si on ne clique pas sur un temps source déjà sélectionné
        if SOURCE_SELECTED != temps :
            switch_buttons(SOURCE_SELECTED, temps)
            old_tgt_name = get_button_name(TARGET_SELECTED["button"])
            # si le temps source sélectionné est le même que le temps cible
            if old_tgt_name == new_selected_name :
                old_src_name = get_button_name(SOURCE_SELECTED["button"])
                if old_src_name != "⁂" :
                    new_target = target_buttons[old_src_name]
                else :
                    new_target = pick_random_target(new_selected_name)
                switch_buttons(TARGET_SELECTED, new_target)
                TARGET_SELECTED = new_target
            SOURCE_SELECTED = temps    
    else :
        # on vérifie si on ne clique pas sur un temps cible déjà sélectionné
        if TARGET_SELECTED != temps :
            switch_buttons(TARGET_SELECTED, temps)
            old_src_name = get_button_name(SOURCE_SELECTED["button"])
            # si le temps cible sélectionné est le même que le temps source
            if old_src_name == new_selected_name :
                old_tgt_name = get_button_name(TARGET_SELECTED["button"])
                new_source = source_buttons[old_tgt_name]
                switch_buttons(SOURCE_SELECTED, new_source)
                SOURCE_SELECTED = new_source
            TARGET_SELECTED = temps
    # print("source_selected : %s , target_selected : %s"
    #       %(get_button_name(SOURCE_SELECTED["button"]), get_button_name(TARGET_SELECTED["button"])))
                         
def traduire():
    conjugaison_temps = None
    source_temps = get_button_name(SOURCE_SELECTED["button"])
    target_temps = get_button_name(TARGET_SELECTED["button"])
    
    # ⁂ (source uniq.) / Passé simple / Imparfait / Présent / Futur
        
    if target_temps == 'Imparfait' : 
        phrase_a_conjugue = source_text.get("1.0", END)[:-1]
        target_text.config(state='normal')
        target_text.delete("0.0", END)
        phrase_conjugue = conjugaisons.conjugaison_phrase(phrase_a_conjugue, target_temps, modele_francais)
        target_text.insert(END, phrase_conjugue)
        
    elif target_temps == 'Présent' : 
        phrase_a_conjugue = source_text.get("1.0", END)[:-1]
        target_text.config(state='normal')
        target_text.delete("0.0", END)
        phrase_conjugue = conjugaisons.conjugaison_phrase(phrase_a_conjugue, target_temps, modele_francais)
        target_text.insert(END, phrase_conjugue)
        
    elif target_temps == 'Passé simple' : 
        target_temps = "Passé Simple"
        phrase_a_conjugue = source_text.get("1.0", END)[:-1]
        target_text.config(state='normal')
        target_text.delete("0.0", END)
        phrase_conjugue = conjugaisons.conjugaison_phrase(phrase_a_conjugue, target_temps, modele_francais)
        target_text.insert(END, phrase_conjugue)
        
    elif target_temps == 'Futur' : 
        phrase_a_conjugue = source_text.get("1.0", END)[:-1]
        target_text.config(state='normal')
        target_text.delete("0.0", END)
        phrase_conjugue = conjugaisons.conjugaison_phrase(phrase_a_conjugue, target_temps, modele_francais)
        target_text.insert(END, phrase_conjugue)
    
    
    target_text.config(state='disabled')
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------création fenêtre-----------------------------------------------#
fenetre=Tk()

fenetre.title('Traductemps')
fenetre.geometry('1150x630')
fenetre.maxsize(1150,630)
fenetre.config(bg=BACKGROUND_COLOR_1)

root = Frame(fenetre, bg=BACKGROUND_COLOR_1)

#---------------------------title

title = Label(root, text='Traductemps', bg=BACKGROUND_COLOR_1, fg=THEME_COLOR_1,
              font=(POLICE, '22', 'bold'), pady=20)
title.pack(side=TOP)

#---------------------------body

trad_frame_border = Frame(root, bg=THEME_COLOR_1, width=110, padx=2, pady=2)

trad_frame = Frame(trad_frame_border, bg=BACKGROUND_COLOR_2, padx=18, pady=18)

## source

source_frame = Frame(trad_frame, bg=BACKGROUND_COLOR_2)

source_pick_frame = Frame(source_frame, bg=BACKGROUND_COLOR_2, padx=10, pady=10)

source_label = Label(source_pick_frame, text="Source", bg=BACKGROUND_COLOR_2,
                     fg="grey", font=(POLICE, '12', 'italic'))
source_label.pack()


source_buttons_frame = Frame(source_pick_frame, bg=BACKGROUND_COLOR_2, pady=15)

source_buttons = {"Tout" : initialize_button(source_buttons_frame,"source","⁂", True),
                  "Passé simple" : initialize_button(source_buttons_frame,"source","passé simple", False),
                  "Imparfait" : initialize_button(source_buttons_frame,"source","imparfait", False),
                  "Présent" : initialize_button(source_buttons_frame,"source","présent",False),
                  "Futur" : initialize_button(source_buttons_frame,"source","futur",False)}

SOURCE_SELECTED = source_buttons["Tout"]

source_buttons["Tout"]["button"].config( command= lambda :
    temps_select(source_buttons["Tout"]) )
source_buttons["Passé simple"]["button"].config( command= lambda :
    temps_select(source_buttons["Passé simple"]) )
source_buttons["Imparfait"]["button"].config( command= lambda :
    temps_select(source_buttons["Imparfait"]) )
source_buttons["Présent"]["button"].config( command= lambda :
    temps_select(source_buttons["Présent"]) )
source_buttons["Futur"]["button"].config( command= lambda :
    temps_select(source_buttons["Futur"]) )

source_buttons["Tout"]["button"].pack()
source_buttons["Passé simple"]["button"].pack()
source_buttons["Imparfait"]["button"].pack()
source_buttons["Présent"]["button"].pack()
source_buttons["Futur"]["button"].pack()

source_buttons_frame.columnconfigure(1, weight=1)

source_buttons["Tout"]["frame"].grid(row=0, column=0)
source_buttons["Passé simple"]["frame"].grid(row=0, column=1)
source_buttons["Imparfait"]["frame"].grid(row=0, column=2)
source_buttons["Présent"]["frame"].grid(row=0, column=3)
source_buttons["Futur"]["frame"].grid(row=0, column=4)

source_buttons_frame.pack()
source_pick_frame.pack()

source_text = Text(source_frame, width=45, height=13, padx=10, pady=10)
source_text.pack()
#source_text_string = str(source_text) #Phrase à conjugué
#print(source_text_string) #Affichage de ce qui est entrée

## target

target_frame = Frame(trad_frame, bg=BACKGROUND_COLOR_2)

target_pick_frame = Frame(target_frame, bg=BACKGROUND_COLOR_2, padx=10, pady=10)

target_label = Label(target_pick_frame, text="Cible", bg=BACKGROUND_COLOR_2,
                     fg="grey", font=(POLICE, '12', 'italic'))
target_label.pack()


target_buttons_frame = Frame(target_pick_frame, bg=BACKGROUND_COLOR_2, pady=15)

target_buttons = {"Passé simple" : initialize_button(target_buttons_frame, "target", "passé simple", False),
                  "Imparfait" : initialize_button(target_buttons_frame, "target", "imparfait", True),
                  "Présent" : initialize_button(target_buttons_frame, "target", "présent",False),
                  "Futur" : initialize_button(target_buttons_frame, "target", "futur",False)}

target_buttons["Passé simple"]["button"].config( command= lambda :
    temps_select(target_buttons["Passé simple"]) )
target_buttons["Imparfait"]["button"].config( command= lambda :
    temps_select(target_buttons["Imparfait"]) )
target_buttons["Présent"]["button"].config( command= lambda :
    temps_select(target_buttons["Présent"]) )
target_buttons["Futur"]["button"].config( command= lambda :
    temps_select(target_buttons["Futur"]) )

TARGET_SELECTED = target_buttons["Imparfait"]

target_buttons["Passé simple"]["button"].pack()
target_buttons["Imparfait"]["button"].pack()
target_buttons["Présent"]["button"].pack()
target_buttons["Futur"]["button"].pack()

target_buttons_frame.columnconfigure(1, weight=1)

target_buttons["Passé simple"]["frame"].grid(row=0, column=0)
target_buttons["Imparfait"]["frame"].grid(row=0, column=1)
target_buttons["Présent"]["frame"].grid(row=0, column=2)
target_buttons["Futur"]["frame"].grid(row=0, column=3)

target_buttons_frame.pack()
target_pick_frame.pack()

target_text = Text(target_frame, height=13, width=45, padx=10, pady=10)
target_text.insert(END, "RÉSULAT DE LA CONJUGAISON...") # resultat de la conjugaison 
target_text.configure(state='disabled', bd=0, highlightthickness=0, relief='flat')

# Ajouter le menu contextuel avec l'option "Copier"
context_menu = Menu(root, tearoff=0)
context_menu.add_command(label="Copier", command=copy_text)

target_text.bind("<Button-3>", show_context_menu)

target_text.pack()

## milieu

fleche_label = Label(trad_frame, bg=BACKGROUND_COLOR_2, text='→', padx=10,
                     font=(POLICE, '24'))

trad_frame.columnconfigure(1, weight=1)

source_frame.grid(row=0, column=0)
fleche_label.grid(row=0, column=1)
target_frame.grid(row=0, column=2)

trad_frame.pack()
trad_frame_border.pack()

## bottom

traduire_frame = Frame(root, bg=BACKGROUND_COLOR_1, padx=5, pady=25)

traduire_border= Frame(traduire_frame, bg=THEME_COLOR_1, padx=5, pady=5)

traduire_button = Button(traduire_border, text="Traduire", bg=BUTTON_COLOR,
                         font=(POLICE, '14', 'bold'), command=traduire)
traduire_button.pack()

traduire_border.pack()

traduire_frame.pack()

root.pack(expand=YES)
fenetre.mainloop()