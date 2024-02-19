from flask import Flask, render_template,request
import mysql.connector
from markupsafe import escape
from vsearch import search4letters
app = Flask(__name__)

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
    dbconfig = {
        'host':'127.0.0.1',
        'user':'vsearch',
        'password':'password',
        'database':'vsearchlogDB'
    }
    connection = mysql.connector.connect(**dbconfig)
    cursor = connection.cursor()
    _SQL = """ insert into log (phrase,letters,ip,browser_string,results)
    values (%s,%s,%s,%s,%s)
    """
    cursor.execute(_SQL,(req.form['phrase'],
                         req.form['letters'],
                         req.remote_addr,
                         browser,
                         res))
    connection.commit()
    connection.close()
    cursor.close()
    print(req.user_agent.browser)

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
    log_requestDB(request, results)
    return render_template('results.html',the_phrase=phrase,
                           the_letters=letters,the_results=results,
                           the_title = 'here are your results nerd!',
                           the_footer = footer)

@app.route('/viewlog')
def showlogs() -> str:
    with open('vsearch.log') as log:
        contents = log.read()
    return escape(contents)


if __name__ == '__main__':
    app.run(debug=True)
