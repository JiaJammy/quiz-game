from tkinter import *
from tkinter import messagebox
import mysql.connector as m

root = Tk()
db = m.connect(host='localhost', user='root', database='quiz_game', password='kurtzy123098')
cursor = db.cursor()

#variables
player_score = 0
highest_score = 0
player_rank = None
current_question = None
selected_answer = StringVar()
used_questions = []
total_questions = 0 

#main window
def window(main):
    main.title('Quiz Game')
    main.update_idletasks()
    width = 600
    height = 500
    x = (main.winfo_screenwidth() // 2) - (width // 2)
    y = (main.winfo_screenheight() // 2) - (height // 2)
    main.geometry('{}x{}+{}+{}'.format(width, height, x, y))

#add function
def add_data():
    global qno, question, answer, opt_A, opt_B, opt_C, opt_D, category
    qno = add_question_no_entry.get()
    question = add_question_entry.get()
    answer = add_answer_entry.get()
    opt_A = add_opt_A_entry.get()
    opt_B = add_opt_B_entry.get()
    opt_C = add_opt_C_entry.get()
    opt_D = add_opt_D_entry.get()
    category = add_category_entry.get()

    cursor = db.cursor()
    cursor.execute("INSERT INTO main (qno, question, option1, option2, option3, option4, answer, category) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                   (qno, question, opt_A, opt_B, opt_C, opt_D, answer, category))
    db.commit()
    messagebox.showinfo("ALL DONE!", "Your question has been added!")

#modify function
def modify_question():
    qno = modify_question_no_entry.get()
    question = question_entry.get()
    answer = answer_entry.get()
    opt_A = opt_A_entry.get()
    opt_B = opt_B_entry.get()
    opt_C = opt_C_entry.get()
    opt_D = opt_D_entry.get()
    category = category_entry.get()

    cursor = db.cursor()
    cursor.execute("UPDATE main SET question=%s, option1=%s, option2=%s, option3=%s, option4=%s, answer=%s, category=%s "
                   "WHERE qno=%s",
                   (question, opt_A, opt_B, opt_C, opt_D, answer, category, qno))
    db.commit()
    messagebox.showinfo("ALL DONE!", "Your updates have been made!")

#display function
def display():
    question_no = display_question_no_entry.get() 
    
    if question_no:
        cursor.execute("SELECT * FROM main WHERE qno = '%s'" % (int(question_no)))
        ma = cursor.fetchall()
        messagebox.showinfo("DISPLAY", "\n".join([f"Question Number: {q[0]} \n  Question: {q[1]} \n  Option A: {q[2]} \n  Option B: {q[3]} \n  Option C: {q[4]} \n  Option D: {q[5]} \n  Answer: {q[6]} \n  Category: {q[7]}" for q in ma]))
    else:
        messagebox.showerror("Error", "Please enter the question number")


#delete function
def delete_question():
    question_no = delete_question_no_entry.get()
    print(f"debug: {question_no}")
    if question_no:
        cursor.execute("DELETE FROM main WHERE qno=%s", (question_no,))
        db.commit()
        messagebox.showinfo("ALL DONE!", "Your question has been deleted!")
    else:
        messagebox.showerror("Error", "Please enter the question number")

                      #game functions

def fetch_total_questions():
    global total_questions
    cursor.execute("SELECT COUNT(*) FROM main")
    total_questions = cursor.fetchone()[0]


def play_quiz():
    global current_question, player_score
    selected_answer.set(None)
    if len(used_questions) == total_questions:
        show_final_score()
        return
    cursor.execute("SELECT * FROM main WHERE qno NOT IN (%s) ORDER BY RAND() LIMIT 1" % ','.join(map(str, used_questions)) if used_questions else "SELECT * FROM main ORDER BY RAND() LIMIT 1")
    current_question = cursor.fetchone()

    if current_question:
        used_questions.append(current_question[0])  # Mark the question as used
        question_label.config(text=current_question[1])
        option_a_radio.config(text=current_question[2], value=current_question[2])
        option_b_radio.config(text=current_question[3], value=current_question[3])
        option_c_radio.config(text=current_question[4], value=current_question[4])
        option_d_radio.config(text=current_question[5], value=current_question[5])
        play_quiz_page.tkraise()
    else:
        messagebox.showinfo("INFO", "No questions available")

def check_answer():
    global player_score, username, password, player_rank, highest_score
    
    if selected_answer.get() == current_question[6]:
        player_score += 5

        #high score
        highest_score()

        query = "update users set score = %s where username = %s and password = %s"
        cursor.execute(query, (player_score, username, password))
        db.commit()
        messagebox.showinfo("CORRECT", "Correct Answer!")

        

        #rank update
        if player_score >= 50:
            query = "update users set player_rank = %s where username = %s and password = %s"
            cursor.execute(query, ("Script Kiddie", username, password))
            player_rank = "Script Kiddie"
            db.commit()
        elif player_score >= 100:
            query = "update users set player_rank = %s where username = %s and password = %s"
            cursor.execute(query, ("Code Ninja", username, password))
            player_rank = "Code Ninja"
            db.commit()
        elif player_score >= 150:
            query = "update users set player_rank = %s where username = %s and password = %s"
            cursor.execute(query, ("Junior Developer", username, password))
            player_rank = "Junior Developer"
            db.commit()
        elif player_score >= 200:
            query = "update users set player_rank = %s where username = %s and password = %s"
            cursor.execute(query, ("Developer", username, password))
            player_rank = "Developer"
            db.commit()
        elif player_score >= 250:
            query = "update users set player_rank = %s where username = %s and password = %s"
            cursor.execute(query, ("Full Stack Developer", username, password))
            player_rank = "Full Stack Developer"
            db.commit()
        elif player_score >= 300:
            query = "update users set player_rank = %s where username = %s and password = %s"
            cursor.execute(query, ("Senior Developer", username, password))
            player_rank = "Senior Developer"
            db.commit()
        elif player_score >= 400:
            query = "update users set player_rank = %s where username = %s and password = %s"
            cursor.execute(query, ("Hacker", username, password))
            player_rank = "Hacker"
            db.commit()
        

    else:
        messagebox.showinfo("WRONG", f"Wrong Answer! Correct answer was {current_question[6]}")

    score_label.config(text=f"Score: {player_score}")
    rank_label.config(text=f"Rank: {player_rank}")
    play_quiz()  # Load the next question

def highest_score():
    global player_score, username, password, player_rank, h_score
    cursor.execute("select MAX(score) from users")
    h_score = cursor.fetchall()
    if player_score > h_score[0][0]:
        messagebox.showinfo("NEW HIGH SCORE!", f'You have a new high score {player_score}')


def show_final_score():
    final_score_label.config(text=f"Congratulations! You've completed the quiz.\nYour final score is: {player_score}")
    final_score_page.tkraise()

#login function
def login():
    global username, password, player_score, player_rank
    username = user_name_entry.get()
    password = password_entry.get()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    player_score = user[4]
    player_rank = user[5]

    if user:
        play_quiz_page.tkraise()
        play_quiz()
    else:
        messagebox.showerror("Login Error", "Invalid username or password.")

def ranks_display():
    ranklist = []
    query = "select username,score from users order by score desc"
    cursor.execute(query)
    data = cursor.fetchall()
    for player_data in data :
        text = f'Player: {player_data[0]}           Score: {player_data[1]}'+'\n'
        ranklist.append(text)
    
         
    messagebox.showinfo("RANKS", ranklist )

   


# Final Score Page
final_score_page = Frame(root)
final_score_page.grid(row=0, column=0, sticky='nsew')

finalscorebg = PhotoImage(file="background.png")
finalscorecanvas = Canvas(final_score_page, width=600, height=500)
finalscorecanvas.pack(fill='both', expand=True)
finalscorecanvas.create_image(0, 0, image=finalscorebg, anchor='nw')

final_score_label = Label(finalscorecanvas, text="", font=("Arial", 16))
finalscorecanvas.create_window(300, 200, window=final_score_label)

exit_button = Button(finalscorecanvas, text="Exit", command=root.quit)
finalscorecanvas.create_window(300, 300, width=100, height=30, window=exit_button)
fetch_total_questions()

ranks_button = Button(finalscorecanvas, text="View Player Ranks" , command=ranks_display)
finalscorecanvas.create_window(300, 400, width=100, height=30, window=ranks_button)

# Starting page
main_page = Frame(root)
main_page.grid(row=0, column=0, sticky='nsew')

mainpagebg = PhotoImage(file="main bg image (2) (1)-logo (1).png")

mainpagecanvas = Canvas(main_page, width=600, height=500)
mainpagecanvas.pack(fill='both', expand=True)
mainpagecanvas.create_image(0, 0, image=mainpagebg, anchor='nw')

menu_button = Button(main_page, text='Open Menu', command=lambda: menu_page.tkraise(), bg='#bb6bfe')
menu_button_place = mainpagecanvas.create_window(300, 260, width=100, height=30, window=menu_button)
main_page.tkraise()

# Menu page
menu_page = Frame(root)
menu_page.grid(row=0, column=0, sticky='nsew')

menupagebg = PhotoImage(file="menu page bg.png")
menupagecanvas = Canvas(menu_page, width=600, height=500)
menupagecanvas.pack(fill='both', expand=True)
menupagecanvas.create_image(0, 0, image=menupagebg, anchor='nw')

add_button = Button(menu_page, text="Add", command=lambda: add_page.tkraise())
menupagecanvas.create_window(300, 150, width=80, height=40, window=add_button)

modify_button = Button(menu_page, text="Modify", command=lambda: modify_page.tkraise())
menupagecanvas.create_window(300, 200, width=80, height=40, window=modify_button)

display_button = Button(menu_page, text="Display", command=lambda: display_page.tkraise())
menupagecanvas.create_window(300, 250, width=80, height=40, window=display_button)

delete_button = Button(menu_page, text="Delete", command=lambda: delete_page.tkraise())
menupagecanvas.create_window(300, 300, width=80, height=40, window=delete_button)

exit_button = Button(menu_page, text="Exit", command=root.quit)
menupagecanvas.create_window(300, 350, width=80, height=40, window=exit_button)

# Add page
add_page = Frame(root)
add_page.grid(row=0, column=0, sticky='nsew')

addpagebg = PhotoImage(file="background.png")
addpagecanvas = Canvas(add_page, width=600, height=500)
addpagecanvas.pack(fill='both', expand=True)
addpagecanvas.create_image(0, 0, image=addpagebg, anchor='nw')

addpagecanvas.create_text(100, 20, text="Please enter the question number:")
add_question_no_entry = Entry(addpagecanvas, width=50)
add_question_no_entry.place(x=200, y=10)

addpagecanvas.create_text(100, 50, text="Please enter the question:")
add_question_entry = Entry(addpagecanvas, width=50)
add_question_entry.place(x=200, y=40)

addpagecanvas.create_text(100, 80, text="Please enter Option A:")
add_opt_A_entry = Entry(addpagecanvas, width=50)
add_opt_A_entry.place(x=200, y=70)

addpagecanvas.create_text(100, 110, text="Please enter Option B:")
add_opt_B_entry = Entry(addpagecanvas, width=50)
add_opt_B_entry.place(x=200, y=100)

addpagecanvas.create_text(100, 140, text="Please enter Option C:")
add_opt_C_entry = Entry(addpagecanvas, width=50)
add_opt_C_entry.place(x=200, y=130)

addpagecanvas.create_text(100, 170, text="Please enter Option D:")
add_opt_D_entry = Entry(addpagecanvas, width=50)
add_opt_D_entry.place(x=200, y=160)

addpagecanvas.create_text(100, 200, text="Please enter the answer:")
add_answer_entry = Entry(addpagecanvas, width=50)
add_answer_entry.place(x=200, y=190)

addpagecanvas.create_text(100, 230, text="Please enter the category:")
add_category_entry = Entry(addpagecanvas, width=50)
add_category_entry.place(x=200, y=220)

add_data_button = Button(addpagecanvas, text='Add data to the database', command=add_data)
addpagecanvas.create_window(300, 300, width=150, height=30, window=add_data_button)

backtomenu_button = Button(addpagecanvas, text='Go Back To Menu', command=lambda: menu_page.tkraise())
addpagecanvas.create_window(300, 350, width=150, height=30, window=backtomenu_button)

# Modify page
modify_page = Frame(root)
modify_page.grid(row=0, column=0, sticky='nsew')

modifypagebg = PhotoImage(file="background.png")
modifypagecanvas = Canvas(modify_page, width=600, height=500)
modifypagecanvas.pack(fill='both', expand=True)
modifypagecanvas.create_image(0, 0, image=modifypagebg, anchor='nw')

modifypagecanvas.create_text(100, 20, text="Please enter the question number:")
modify_question_no_entry = Entry(modifypagecanvas, width=50)
modify_question_no_entry.place(x=200, y=10)

modifypagecanvas.create_text(100, 50, text="Please enter the question:")
question_entry = Entry(modifypagecanvas, width=50)
question_entry.place(x=200, y=40)

modifypagecanvas.create_text(100, 80, text="Please enter Option A:")
opt_A_entry = Entry(modifypagecanvas, width=50)
opt_A_entry.place(x=200, y=70)

modifypagecanvas.create_text(100, 110, text="Please enter Option B:")
opt_B_entry = Entry(modifypagecanvas, width=50)
opt_B_entry.place(x=200, y=100)

modifypagecanvas.create_text(100, 140, text="Please enter Option C:")
opt_C_entry = Entry(modifypagecanvas, width=50)
opt_C_entry.place(x=200, y=130)

modifypagecanvas.create_text(100, 170, text="Please enter Option D:")
opt_D_entry = Entry(modifypagecanvas, width=50)
opt_D_entry.place(x=200, y=160)

modifypagecanvas.create_text(100, 200, text="Please enter the answer:")
answer_entry = Entry(modifypagecanvas, width=50)
answer_entry.place(x=200, y=190)

modifypagecanvas.create_text(100, 230, text="Please enter the category:")
category_entry = Entry(modifypagecanvas, width=50)
category_entry.place(x=200, y=220)

modify_data_button = Button(modifypagecanvas, text='Modify Data', command=modify_question)
modifypagecanvas.create_window(300, 300, width=150, height=30, window=modify_data_button)

backtomenu_button = Button(modifypagecanvas, text='Go Back To Menu', command=lambda: menu_page.tkraise())
modifypagecanvas.create_window(300, 350, width=150, height=30, window=backtomenu_button)

# Display Page
display_page = Frame(root)
display_page.grid(row=0, column=0, sticky='nsew')

displaypagebg = PhotoImage(file="background.png")
displaypagecanvas = Canvas(display_page, width=600, height=500)
displaypagecanvas.pack(fill='both', expand=True)
displaypagecanvas.create_image(0, 0, image=displaypagebg, anchor='nw')

displaypagecanvas.create_text(300, 50, text="Please enter the question number:")
display_question_no_entry = Entry(displaypagecanvas, width = 50)
display_question_no_entry.place(x= 150, y = 80)

display_button = Button(displaypagecanvas, text="Display", command=display)
displaypagecanvas.create_window(300, 200, width=100, height=30, window=display_button)

backtomenu_button = Button(displaypagecanvas, text='Go Back To Menu', command=lambda: menu_page.tkraise())
displaypagecanvas.create_window(300, 300, width=150, height=30, window=backtomenu_button)

# Delete Page
delete_page = Frame(root)
delete_page.grid(row=0, column=0, sticky='nsew')

deletepagebg = PhotoImage(file="background.png")
deletepagecanvas = Canvas(delete_page, width=600, height=500)
deletepagecanvas.pack(fill='both', expand=True)
deletepagecanvas.create_image(0, 0, image=deletepagebg, anchor='nw')

deletepagecanvas.create_text(300, 50, text="Please enter the question number:")
delete_question_no_entry = Entry(deletepagecanvas, width=50)
delete_question_no_entry.place(x=150, y=80)

delete_button = Button(deletepagecanvas, text="Delete", command=delete_question)
deletepagecanvas.create_window(300, 200, width=100, height=30, window=delete_button)

backtomenu_button = Button(deletepagecanvas, text='Go Back To Menu', command=lambda: menu_page.tkraise())
deletepagecanvas.create_window(300, 300, width=150, height=30, window=backtomenu_button)

# Play Quiz Page
start_quiz_button = Button(main_page, text='Start Quiz', command=lambda: login_page.tkraise(), bg='#bb6bfe')
mainpagecanvas.create_window(300, 300, width=100, height=30, window=start_quiz_button)
play_quiz_page = Frame(root)
play_quiz_page.grid(row=0, column=0, sticky='nsew')

quizpagebg = PhotoImage(file="game bg.png")
quizpagecanvas = Canvas(play_quiz_page, width=600, height=500)
quizpagecanvas.pack(fill='both', expand=True)
quizpagecanvas.create_image(0, 0, image=quizpagebg, anchor='nw')

question_label = Label(quizpagecanvas, text="", font=("Arial", 14), bg = "#DEAFFF")
quizpagecanvas.create_window(300, 100, window=question_label)

option_a_radio = Radiobutton(quizpagecanvas, text="", variable=selected_answer, font=("Arial", 12), value="", indicator=0, bg = "#DEAFFF")
quizpagecanvas.create_window(300, 150, window=option_a_radio)

option_b_radio = Radiobutton(quizpagecanvas, text="", variable=selected_answer, font=("Arial", 12), value="", indicator=0, bg = '#E2B9FF')
quizpagecanvas.create_window(300, 200, window=option_b_radio)

option_c_radio = Radiobutton(quizpagecanvas, text="", variable=selected_answer, font=("Arial", 12), value="", indicator=0, bg = '#E2B9FF')
quizpagecanvas.create_window(300, 250, window=option_c_radio)

option_d_radio = Radiobutton(quizpagecanvas, text="", variable=selected_answer, font=("Arial", 12), value="", indicator=0, bg = '#E2B9FF')
quizpagecanvas.create_window(300, 300, window=option_d_radio)

submit_answer_button = Button(quizpagecanvas, text="Submit Answer", command=check_answer, bg = "green")
quizpagecanvas.create_window(200, 400, width=100, height=50 ,window=submit_answer_button)

score_label = Label(quizpagecanvas, text=f"Score: {player_score}", font=("Arial", 12), background = "#E3BCFD")
quizpagecanvas.create_window(550, 30, window=score_label)

rank_label = Label(quizpagecanvas, text=f"Rank: {player_rank}", font=("Arial", 12), background = "#E3BCFD")
quizpagecanvas.create_window(100, 30, window=rank_label)

quit_game_button = Button(quizpagecanvas, text = 'Quit Game',command = show_final_score, bg = "red" )
quizpagecanvas.create_window(400, 400, width=100, height=50 ,  window= quit_game_button)

#login page
login_page = Frame(root)
login_page.grid(row=0, column=0, sticky='nsew')

loginpagebg = PhotoImage(file="login bg.png")
loginpagecanvas = Canvas(login_page, width=600, height=500)
loginpagecanvas.pack(fill='both', expand=True)
loginpagecanvas.create_image(0, 0, image=loginpagebg, anchor='nw')

loginpagecanvas.create_text(200, 210, text="Please enter the username:")
user_name_entry = Entry(loginpagecanvas, width=30)
user_name_entry.place(x=300, y=200)

loginpagecanvas.create_text(200, 250, text="Please enter the password:")
password_entry = Entry(loginpagecanvas, width=30)
password_entry.place(x=300, y=240)

login_button = Button(loginpagecanvas, text='login!', command = login, bg="#71306B") 
loginpagecanvas.create_window(300, 300, width=150, height=30, window=login_button)



main_page.tkraise()    
root.resizable(False,False)
window(root)
mainloop()