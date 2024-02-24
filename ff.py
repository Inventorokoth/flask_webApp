from flask import Flask, render_template,request
from DBcm import UseDatabase as db
from markupsafe import escape
from vsearch import search4letters
from flask import session
from time import sleep
from threading import Thread
from check import check_logged_in
app = Flask(__name__)
app.secret_key = 'owenkey'

app.config['dbconfig'] = {
    
        'host':'127.0.0.1',
        'user':'vsearch',
        'password':'password',
        'database':'vsearchlogDB'
    }

def get_browser(user_agent_string):
    if 'Firefox' in user_agent_string:
        return 'Firefox'
    elif 'Chrome' in user_agent_string:
        return 'Chrome'
    elif 'Safari' in user_agent_string:
        return 'Safari'
    # Add more browser checks as needed
    else:
        return 'Unknown'
    


def log_requestDB(req,res:str)->None:
    browser = get_browser(req.user_agent.string)

    with db(app.config['dbconfig']) as cursor:
        sleep(14)
        _SQL = """ insert into log (phrase,letters,ip,browser_string,results)
        values (%s,%s,%s,%s,%s)
        """
        cursor.execute(_SQL,(req.form['phrase'],
                            req.form['letters'],
                            req.remote_addr,
                            browser,
                            res))



@app.route('/login')
def login()->None:
    session['islogin']=True
    return 'you are now logged in'

@app.route('/logout')
def logout()->None:
    session.pop('islogin')
    return 'you are now logged out'



@app.route('/')
@app.route('/entry')
def message() -> 'html':
    return render_template('entry.html',the_title='here we do things!')

@app.route('/search4',methods=['POST'])
def search()-> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search4letters(phrase,letters))
    footer = 'footer here'
    try:
        log_requestDB_Concurrent = Thread(target=log_requestDB , args=(request,results))
        log_requestDB_Concurrent.start()
    except Exception as err:
        print(err)
         
       
    return render_template('results.html',the_phrase=phrase,
                        the_letters=letters,the_results=results,
                        the_title = 'here are your results nerd!',
                        the_footer = footer)
    

@app.route('/viewlog')
@check_logged_in
def showlogs() -> str:
    try:
        with db(app.config['dbconfig']) as cursor:
            SQL = """select  phrase , letters, ip, browser_string, results from log"""
            cursor.execute(SQL)
            contents = cursor.fetchall()
            return escape(contents)
    except Exception as err:
        print(err)
        

    
    

if __name__ == '__main__':
    app.run(debug=True)
