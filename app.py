from flask import Flask, request, render_template, session, redirect, url_for,flash
import random
from flask_mail import Mail, Message
import google.generativeai as genai
import time
import mysql.connector


def create_db_connection():
    return mysql.connector.connect(
        host="mainline.proxy.rlwy.net",
        user="root",
        password="hAVcUuqmaYCGjasjfFZUrEQaSkdqrIYO",
        database="railway",
        port=20797
    )

genai.configure(api_key="AIzaSyCXWcN9zWhx7qYARfieyryTzPgMygYVKlk")

#app = Flask(__name__)
#app.config['SECRET_KEY'] = 'Sekhar@26'  

app = Flask(__name__)
app.secret_key = "Sekhar@26"  # for session management ?


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'lvrajasekharareddy.2007@gmail.com'  
app.config['MAIL_PASSWORD'] = 'uiyt torw peym xlvb'  

mail = Mail(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        #session['string_lst'] = []
        #session['acc_lst'] = []
        email = session['email']
        otp = session['otp']
        print("*******************************otp: ",otp)
        conn = create_db_connection()
        cursor = conn.cursor(dictionary=True)  
        cursor.execute("SELECT * FROM users_md WHERE email=%s", (email,))
        result = cursor.fetchone()
        if result and 'email' and 'otp' in session :
            print("////////in result//////")
            return redirect(url_for('levels', level_no = session['level_no']))
        error_message = None
        if request.method == 'POST':
            session['string_lst'] = []
            session['acc_lst'] = []
            name = request.form['name']
            mobile_number = request.form['mobile_number']
            password = request.form['password'] 
            email = request.form['email'] 
            session['email'] = email
            try:
                conn = create_db_connection()
                cursor = conn.cursor()

                # Check if username already exists
                cursor.execute("SELECT * FROM users_md WHERE name = %s", (name,))
                existing_user = cursor.fetchone()

                if existing_user:
                    # Username already exists
                    flash("Username already exists. Please choose a different one.")
                    return render_template("register.html", error_message="Username already exists. Please choose a different one.")
  # or wherever your registration form is
                else:
                    # Insert new user
                    cursor.execute("""
                        INSERT INTO users_md 
                        (name, mobile_number, password, email, level, accuracy, total, correct, incorrect) 
                        VALUES (%s, %s, %s, %s, 1, 0, 0, 0, 0)
                    """, (name, mobile_number, password, email))
                    conn.commit()

                #cursor.execute("SELECT level FROM users_md WHERE email=%s",(email,))
                #level_no = cursor.fetchone()
                #session['level_no'] = level_no[0]
                conn = create_db_connection()
                cursor = conn.cursor(dictionary=True)  
                cursor.execute("SELECT level FROM users_md WHERE email=%s", (email,))
                level_no = cursor.fetchone()
                session['level_no'] = level_no['level']
            
                
                return redirect(url_for('send'))
            except mysql.connector.IntegrityError:
                error_message = "User already exists! Try logging in."
            
            conn.close() 
        print("ah!shock ayyava")
        return render_template("register.html", error_message=error_message)
    except:
        if 'otp' in session :
            return redirect(url_for('levels', level_no = session['level_no']))
        error_message = None
        if request.method == 'POST':
            session['string_lst'] = []
            session['acc_lst'] = []
            name = request.form['name']
            mobile_number = request.form['mobile_number']
            password = request.form['password'] 
            email = request.form['email'] 
            session['email'] = email
            try:
                conn = create_db_connection()
                cursor = conn.cursor()

                # Check if username already exists
                cursor.execute("SELECT * FROM users_md WHERE name = %s", (name,))
                existing_user = cursor.fetchone()

                if existing_user:
                    # Username already exists
                    flash("Username already exists. Please choose a different one.")
                    return render_template("register.html", error_message="Username already exists. Please choose a different one.")
  # or wherever your registration form is
                else:
                    # Insert new user
                    cursor.execute("""
                        INSERT INTO users_md 
                        (name, mobile_number, password, email, level, accuracy, total, correct, incorrect) 
                        VALUES (%s, %s, %s, %s, 1, 0, 0, 0, 0)
                    """, (name, mobile_number, password, email))
                    conn.commit()

                #cursor.execute("SELECT level FROM users_md WHERE email=%s",(email,))
                #level_no = cursor.fetchone()
                #session['level_no'] = level_no[0]
                conn = create_db_connection()
                cursor = conn.cursor(dictionary=True)  
                cursor.execute("SELECT level FROM users_md WHERE email=%s", (email,))
                level_no = cursor.fetchone()
                session['level_no'] = level_no['level']
            
                
                return redirect(url_for('send'))
            except mysql.connector.IntegrityError:
                error_message = "User already exists! Try logging in."
            
            conn.close() 

        return render_template("register.html", error_message=error_message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        passwordd = request.form['password']

        conn = create_db_connection()
        cursor = conn.cursor(dictionary=True)  
        cursor.execute("SELECT email, name, password FROM users_md WHERE email=%s", (email,))
        user = cursor.fetchone()  
        cursor.execute("SELECT level FROM users_md WHERE email=%s",(email,))
        level_no = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and passwordd == user['password']:  
            session['email'] = user['email']
            session['name'] = user['name']
            session['level_no'] = level_no['level']
            return redirect(url_for('levels', level_no = session['level_no']))
        else:
            return "Invalid Credentials"

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
@app.route('/profile', methods=["POST", "GET"])
def profile_info():
    if 'otp' not in session:
        return redirect(url_for('login'))

    email = session.get('email')

    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT name, level FROM users_md WHERE email=%s", (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        name = user.get('name', "Guest")
        level = user.get('level', "Unknown")

        conn = create_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT accuracy FROM users_md WHERE email=%s", (email,))
        accuracy_db = cursor.fetchone()
        accuracy = accuracy_db['accuracy'] if accuracy_db else 0

        cursor.execute("SELECT * FROM users_md WHERE email=%s", (email,))
        det_db = cursor.fetchone()
        correct = det_db['correct']
        incorrect = det_db['incorrect']
        total = det_db['total']

        if level == 1:
            badge = "ASSOCIATE"
        elif level == 2:
            badge = "SPECIALIST"
        elif level == 3:
            badge = "ADVISOR"
        elif level == 4:
            badge = "CONSULTANT"
        elif level == 5:
            badge = "STRATEGIST"
        elif level == 6:
            badge = "EXPERT"
        elif level == 7:
            badge = "ANALYST"
        elif level == 8:
            badge = "SENIOR"
        elif level == 9:
            badge = "PRINCIPAL"
        else:
            badge = "PIONEER"

        cursor.close()
        conn.close()

        return render_template('profile.html', name=name, level=level, accuracy=accuracy,
                               total=total, correct=correct, incorrect=incorrect, badge=badge)

    else:
        return "User not found. Please log in again."

   

@app.route('/')
def home():
    session['sum'] = 0
    session['acc_lst'] = []
    return render_template("index.html")

@app.route('/home_again', methods=['GET', 'POST'])
def home_again():
    print("🧪 Method used:", request.method)
    return render_template("index.html")

@app.route('/Start', methods=["POST"])
def Start():
    return render_template("email_form.html")

@app.route('/send', methods=['GET', 'POST'])
def send():
    #if request.method == 'POST':
        email = session['email']
        if not email:
            return 'Email is required!', 400

        otp = random.randint(100000, 999999)
        session['otp'] = otp
        session['email'] = email

        msg = Message("Your OTP", sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = f"Your OTP is: {otp}"
        mail.send(msg)

        return redirect(url_for('verify'))

    #return render_template('email_form.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        stored_otp = session.get('otp')

        if entered_otp and stored_otp and entered_otp == str(stored_otp):
            #session.pop('otp', None)
            #session.pop('email', None)
            return redirect(url_for('levels', level_no = session['level_no']))
        else:
            return 'Invalid OTP. Try again!'

    return render_template('verify_otp.html')

@app.route('/levels')
def levels():
    return render_template('levels.html', level_no = session['level_no'])
    

@app.route('/level1')
def level1():
    #ai_answers = "dummy"
    return render_template('level1.html', status1="display", question = "display")


@app.route('/level2')
def level2():
    return render_template('level2.html', status1="display", question = "display") 

@app.route('/level3')
def level3():
    return render_template('level3.html', status1="display", question = "display")

@app.route('/level4')
def level4():
    return render_template('level4.html', status1="display", question = "display")

@app.route('/level5')
def level5():
    return render_template('level5.html', status1="display", question = "display")

@app.route('/level6')
def level6():
    return render_template('level6.html', status1="display", question = "display")

@app.route('/level7')
def level7():
    return render_template('level7.html', status1="display", question = "display")

@app.route('/level8')
def level8():
    return render_template('level8.html', status1="display", question = "display")

@app.route('/level9')
def level9():
    return render_template('level9.html', status1="display", question = "display")

@app.route('/level10')
def level10():
    return render_template('level10.html', status1="display", question = "display")


# AI Gemini Route
@app.route('/gemini', methods=["POST"])
def gemini():
    
    l = request.form.get('level')
    q = request.form.get('form_id')
    string = l+q
    if session['string_lst'] == [] or string not in session['string_lst']:
        print("********************************************************************************")
        conn = create_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users_md SET total = total + 1 WHERE email=%s',(session['email'],))
        conn.commit()
    #session['string_lst'].append(string)
    #my_dict = session['my_dict']
    print("----------------",session['string_lst'])
    
    
    answer = request.form.get("answer")
    question = request.form.get("question")
    print("----question----", question)
    print("----answer----", answer)
    session['sum'] = 0
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # First AI call: Checking if answer is correct
    prompt = f"question is {question} and answer is {answer}. Is the answer correct for given question? YES OR NO ONLY."
    response = model.generate_content(prompt)
    command = f"question is {question} and answer is {answer}. Give the accuracy of the answer between 1 to 10. If answer is wrong then accuracy is 0. Just provide the value no extras"
    acc = model.generate_content(command)
    acc_text = acc.candidates[0].content.parts[0].text.strip().upper()
    print("acc: ",acc_text)
    email = session['email']
    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True) 
    cursor.execute("SELECT level FROM users_md WHERE email=%s", (email,))
    pres_level = cursor.fetchone()
    pres_level_no = pres_level['level']
    if session['level_no'] < pres_level_no:
        print("Nothing changed")
    else:
        session['acc_lst'].append(acc_text)
        for i in session['acc_lst']:
            session['sum'] = session['sum'] + int(i)
            avg = session['sum'] / len(session['acc_lst'])

        session['avg'] = avg
        conn = create_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users_md SET accuracy = %s WHERE email=%s',(avg, session['email'],))
        conn.commit()
        print("Sum: ",session['sum'])
        print("Length: ", len(session['acc_lst']))
        print("Average = ",avg)
        response_text = response.candidates[0].content.parts[0].text.strip().upper()
        print('list: ',session['acc_lst'])
        
    ai_answers = ""
    
    if response_text == "NO":
        # Second AI call: Getting the correct answer
        prompt = f"Provide the correct answer for: {question} in maximum of 3 lines. Since this for public to understand, provide answer in simple words and in funny manner and use indian english only english no hindi. IT SHOULD BE UNDERSTOOD BY INDIAN PUBLIC EASILY. ALSO SAY ONE POPULAR MEDICINE NAME and A HOME REMIDY FOR THAT PROBLEM do not use * in answer"
        ai_answer = model.generate_content(prompt)
        if ai_answer and ai_answer.candidates:
            ai_answers = ai_answer.candidates[0].content.parts[0].text.strip()
        else:
            ai_answers = "Error generating response"
    
    session['ai_answers'] = ai_answers
    form_id = request.form.get("form_id")
    status = "display"
    statusn = "status" + form_id
    print("Status number: ",statusn)
    status_dict = {
        f"status{form_id}" : "display"
    }
    level = request.form.get('level')
    print("Level: ", level)
    level = "level" + str(level) + ".html"
            
    if ai_answers:
        if session['string_lst'] == [] or string not in session['string_lst']:
            conn = create_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE users_md SET incorrect = incorrect + 1 WHERE email=%s',(session['email'],))
            conn.commit()
            session['string_lst'].append(string)
            return render_template(level, **status_dict, ai_answers=ai_answers, question = "hide" )  
        else:
              return render_template(level, **status_dict, ai_answers=ai_answers, question = "hide" )
    else:
        if session['string_lst'] == [] or string not in session['string_lst']:
            conn = create_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE users_md SET correct = correct + 1 WHERE email=%s',(session['email'],))
            conn.commit()
            session['string_lst'].append(string)
            return render_template(level, **status_dict, ai_answers=ai_answers, question = "hide" )
            #return render_template("level1.html", **status_dict, ai_answers=ai_answers )
        else:
            return render_template(level, **status_dict, ai_answers=ai_answers, question = "hide" )

@app.route('/next', methods=["POST", "GET"])
def next_question():
    if request.method == "POST":
        form_id = request.form.get("form_id")
        print("Form id: ",form_id)
        

        if form_id is None:
            return "Error: No form ID received", 400

        try:
            form_id = int(form_id) + 1
            prev_form = form_id - 1
            level = request.form.get('level')
            print("Level: ", level)
            level = "level" + str(level) + ".html"
            
            session["form_id"] = form_id
            

            # Ensure that form_id doesn't exceed the number of questions.
            if form_id > 10:
                level = request.form.get('level')
                level = int(level) 
                conn = create_db_connection()
                cursor = conn.cursor(dictionary=True)
                #level_no = session['level_no']
                print("email: ",session['email'])
                email = session['email']
                cursor.execute("SELECT level FROM users_md WHERE email=%s", (email,))
                pres_level = cursor.fetchone()
                pres_level_no = pres_level['level']
                if level < pres_level_no:
                    return render_template("bad1.html", level=level)
                    #return render_template("level_complete.html", level = level) 
                else:
                    session['level_no'] = session['level_no'] + 1
                    cursor.execute('UPDATE users_md SET level = level + 1 WHERE email=%s',(session['email'],))
                    conn.commit()
                    #session['level_no'] = level_no  + 1
                    print("Current level is: ", level)
                    #return render_template("level_complete.html", level = level) 
                    return render_template("bad1.html", level=level)

            #Dynamically set status variables.
            status_dict = {
                f"status{prev_form}": "hidden",
                f"status{form_id}": "display"
            }
            print("Level: ", level)
            return render_template(level, **status_dict, question = "display")

        except ValueError:
            return "Error: Invalid form ID", 400
        

    return redirect(url_for('level1'))  

@app.route('/complete', methods=['POST'])
def complete():
    return render_template("level_complete.html", level = session['level_no']) 


@app.route('/show_answer', methods = ["POST", "GET"])
def show_answer():
    status = "ok"
    ai_answers = session.get('ai_answers')
    type = "hidden"
    #value = session['form_id']
    value = int(request.form.get('form_id'))
    level = request.form.get('level')
    print("Value is: ",value)
    question = request.form.get('question')
    return render_template("show_answer.html", status = status, ai_answers = ai_answers, type = type, value = value, question = question, level = level)

@app.route('/rewrite', methods=["POST", "GET"])
def rewrite():
    form_id = request.form.get("form_id")
    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)
    email = session['email']
    cursor.execute("SELECT name, level FROM users_md WHERE email=%s", (email,))
    user = cursor.fetchone()  # ✅ Fetch name & level in a single query

    cursor.close()
    conn.close()
    level = user.get('level', "Unknown")


    if form_id is None:
        return "Error: No form ID received", 400  

    try:
        next_question_number = int(form_id)
    except ValueError:
        return "Error: Invalid form ID", 400
    print(f"status{next_question_number}") 
    level = "level"+str(level)+".html"
    print("level: ",level)
    
    return render_template(level, **{f"status{next_question_number}": "display"}, question = "display")

allowed_levels = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

@app.route('/next_level', methods=["POST"])
def next_level():
    level = int(request.form.get('level')) + 1
    level = str(level)
    print("Level in next_level: ", level)

    if level and level in allowed_levels:
        new_level = "level" + level + ".html"
        return render_template(new_level, status1 = "display", question = "display")
    else:
        # Handle invalid level input (e.g., return an error page)
        return "No level present rey!"    

def get_leaderboard_data():
    conn = create_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True) #return results as dictionary
        cursor.execute("""
            SELECT name, total, correct, incorrect, accuracy 
            FROM users_md
            ORDER BY total DESC, correct DESC, accuracy DESC, name ASC;
        """)
        results = cursor.fetchall()
        conn.close()
        return results
    return []

@app.route('/leaderboard')
def leaderboard():
    leaderboard_data = get_leaderboard_data()
    return render_template('leaderboard.html', leaderboard_data=leaderboard_data)


if __name__ == '__main__':
    app.run(debug=True)

