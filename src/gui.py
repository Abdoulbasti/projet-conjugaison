from tkinter import *
import conjugaisons

BACKGROUND_COLOR_1 = "#e6e9f2"
BACKGROUND_COLOR_2 = "#dbdee7"
THEME_COLOR_1 = "#183798" # bleu marine
BUTTON_COLOR = "#f2f2f2"
BUTTON_COLOR_ACTIVE = "#ececec"
BUTTON_COLOR_SELECTED = "#8b9fe0"
BUTTON_COLOR_SELECTED_ACTIVE = "#788dd3"
BUTTON_HB_COLOR = "#9fa4b4"
POLICE = "Liberation Sans"

SOURCE_SELECTED = 'présent'
TARGET_SELECTED = 'imparfait'

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

def switch_buttons(old_selected : Button, old_selected_frame : Frame,
                   new_selected : Button, new_selected_frame : Frame):
    # un-set selected
    old_selected.config(bg=BUTTON_COLOR)
    old_selected.config(font=(POLICE, '12'))
    old_selected.config(activebackground=BUTTON_COLOR_ACTIVE)
    old_selected_frame.config(highlightbackground=BUTTON_HB_COLOR)
    old_selected_frame.config(highlightthickness=1)
    
    # set selected
    new_selected.config(bg=BUTTON_COLOR_SELECTED)
    new_selected.config(font=(POLICE, '12', 'bold'))
    new_selected.config(activebackground=BUTTON_COLOR_SELECTED_ACTIVE)
    new_selected_frame.config(highlightbackground=THEME_COLOR_1)
    new_selected_frame.config(highlightthickness=3)

def imparfait_source():
    global SOURCE_SELECTED, TARGET_SELECTED
    # insérer appel traduction
    if SOURCE_SELECTED != 'imparfait' :
        switch_buttons(present_source_button, present_source_button_frame,
                       imparfait_source_button, imparfait_source_button_frame)
        switch_buttons(imparfait_target_button, imparfait_target_button_frame,
                    present_target_button, present_target_button_frame)
        SOURCE_SELECTED = 'imparfait'
        TARGET_SELECTED = 'present'
        
def present_source():
    global SOURCE_SELECTED, TARGET_SELECTED
    # insérer appel traduction
    if SOURCE_SELECTED != 'present' :
        switch_buttons(imparfait_source_button, imparfait_source_button_frame,
                    present_source_button, present_source_button_frame)
        switch_buttons(present_target_button, present_target_button_frame,
                       imparfait_target_button, imparfait_target_button_frame)
        SOURCE_SELECTED = 'present'
        TARGET_SELECTED = 'imparfait'
        
def imparfait_target():
    global SOURCE_SELECTED, TARGET_SELECTED
    # insérer appel traduction
    if TARGET_SELECTED != 'imparfait' :
        switch_buttons(present_target_button, present_target_button_frame,
                       imparfait_target_button, imparfait_target_button_frame)
        switch_buttons(imparfait_source_button, imparfait_source_button_frame,
                    present_source_button, present_source_button_frame)
        SOURCE_SELECTED = 'present'
        TARGET_SELECTED = 'imparfait'
        
def present_target():
    global SOURCE_SELECTED, TARGET_SELECTED
    # insérer appel traduction
    if TARGET_SELECTED != 'present' :
        switch_buttons(imparfait_target_button, imparfait_target_button_frame,
                    present_target_button, present_target_button_frame)
        switch_buttons(present_source_button, present_source_button_frame,
                       imparfait_source_button, imparfait_source_button_frame)
        SOURCE_SELECTED = 'imparfait'
        TARGET_SELECTED = 'present'
        
    
#-----------------------création fenêtre

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

imparfait_source_button_frame = Frame(source_buttons_frame, bg=BACKGROUND_COLOR_2,  
                         highlightbackground = BUTTON_HB_COLOR, highlightthickness = 1)

imparfait_source_button = Button(imparfait_source_button_frame, text='imparfait',
                         font=(POLICE, '12'), bg=BUTTON_COLOR, relief='flat',
                         command=imparfait_source)

imparfait_source_button.pack()


present_source_button_frame = Frame(source_buttons_frame, bg=BACKGROUND_COLOR_2, 
                         highlightbackground = THEME_COLOR_1, highlightthickness = 3)

present_source_button = Button(present_source_button_frame, text='présent',
                         bg=BUTTON_COLOR_SELECTED, activebackground=BUTTON_COLOR_SELECTED_ACTIVE, 
                         font=(POLICE, '12', 'bold'), relief='flat', command=present_source)

present_source_button.pack()

source_buttons_frame.columnconfigure(1, weight=1, pad=10)

imparfait_source_button_frame.grid(row=0, column=0)
present_source_button_frame.grid(row=0, column=1)

source_buttons_frame.pack()
source_pick_frame.pack()

source_text = Text(source_frame, width=45, height=13, relief='sunken', padx=10, pady=10)
source_text.pack()

## target

target_frame = Frame(trad_frame, bg=BACKGROUND_COLOR_2)

target_pick_frame = Frame(target_frame, bg=BACKGROUND_COLOR_2, padx=10, pady=10)

target_label = Label(target_pick_frame, text="Cible", bg=BACKGROUND_COLOR_2,
                     fg="grey", font=(POLICE, '12', 'italic'))
target_label.pack()

target_buttons_frame = Frame(target_pick_frame, bg=BACKGROUND_COLOR_2, pady=15)

imparfait_target_button_frame = Frame(target_buttons_frame, bg=BACKGROUND_COLOR_2, 
                         highlightbackground = THEME_COLOR_1, highlightthickness = 3)

imparfait_target_button = Button(imparfait_target_button_frame, text='imparfait',
                         bg=BUTTON_COLOR_SELECTED, activebackground=BUTTON_COLOR_SELECTED_ACTIVE, 
                         font=(POLICE, '12', 'bold'), relief='flat', 
                         command=imparfait_target)

imparfait_target_button.pack()


present_target_button_frame = Frame(target_buttons_frame, bg=BACKGROUND_COLOR_2,  
                         highlightbackground = BUTTON_HB_COLOR, highlightthickness = 1)

present_target_button = Button(present_target_button_frame, text='présent',
                         font=(POLICE, '12'), bg=BUTTON_COLOR, relief='flat',command=present_target)

present_target_button.pack()

target_buttons_frame.columnconfigure(1, weight=1, pad=10)

imparfait_target_button_frame.grid(row=0, column=0)
present_target_button_frame.grid(row=0, column=1)

target_buttons_frame.pack()
target_pick_frame.pack()

target_text = Text(target_frame, height=13, width=45, padx=10, pady=10)
target_text.insert(END, "texte exemple")
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

traduire_button = Button(traduire_border, text="Traduire",
                         bg=BUTTON_COLOR, font=(POLICE, '14', 'bold'))
traduire_button.pack()

traduire_border.pack()

traduire_frame.pack()

root.pack(expand=YES)
fenetre.mainloop()








