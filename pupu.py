import re

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import pymorphy2

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
morph = pymorphy2.MorphAnalyzer()

def poc(a,b):
    return a / ((a + b) / 100), b / ((a + b) / 100)

def slovar(a):
    ans = []
    test = 0
    i1 = 0
    for i in a:
        i = i.lower()

    for i in a:
        for j in ans:
            if i == j:
                test = 1
        if test == 0:
            ans.append(i)



    return ans



def spl(s):
    M = []

    w = re.findall(r'([^А-Яа-я])', s)
    print(w)

    for i in range(len(w)):
        if w[i][0] == '':
            M.append(w[i][1])
        else:
            M.append(w[i][0])


    return M




primer = spl(open('text.txt', 'r').read())


o = []
impf = 0
perf = 0

for i in primer:
    tt  = morph.parse(i)[0]
    tt1 = morph.parse(i)[0].tag
    if 'VERB' in tt.tag:
        o.append(i.lower())
        if 'impf' in tt1:
            impf += 1
        if 'perf' in tt1:
            perf += 1

o1 = ['0']*2
for i in range(2):
    o1[i] = [0] * len(o)


test = 0
i1 = 0
kek = 0

for i in o:
    for j in range(len(o)):
        if o1[0][j] == i:
            o1[1][j] += 1
            test = 1
    if test == 0:
        o1[0][i1] = i
        o1[1][i1] += 1
        i1+=1
        test = 0
    test = 0
oo = [0]*2
for i in range(2):
    oo[i] = [0] * i1

for i in range(i1):
    oo[1][i] = o1[0][i]
    oo[0][i] = o1[1][i]



for i in range(i1):
    for j in range(i1):
        if oo[0][i] <= oo[0][j]:
            y = oo[0][i]
            y1 = oo[1][i]
            oo[0][i] = oo[0][j]
            oo[0][j] = y

            oo[1][i] = oo[1][j]
            oo[1][j] = y1



r,t = poc(impf, perf)



ooo= []
for i in range(i1):
    if 'impf' in morph.parse(oo[1][i])[0].tag:
        ooo.append("Несовершенный вид")
    else:
        ooo.append("Совершенный вид")
slovar(primer)
df1 = pd.DataFrame({
    "Вид глагола": ooo,
    "кол-во": oo[0],
    "Вид": oo[1]
})
print(oo)
print(impf)
fig1 = px.bar(df1, x="Вид глагола", y="кол-во", color="Вид",barmode ="group")

df = pd.DataFrame({
    "Вид глагола": ["",""],
    "кол-во": [r,t],
    "Вид": ["impf","perf"]
})


fig = px.bar(df, x="Вид глагола", y="кол-во", color="Вид",barmode ="group")




app.layout = html.Div(children=[
    dcc.Markdown('''
        # Вид глаголов в тексте
    '''),

    html.Div(children='''
        Здравствуйте, я проанализировала текст(text.txt) и написала код, который рисует 2 графика. В качестве материала, я взяла статьи из Википедии про рябчиков, черёмуху, зябликов, гавайскую цветочную и информатику. \n На первом графике, процентное соотношение глаголов совершенного вида и не совершенного. Второй график разделён на 2 части. Слева, находяться глаголы несовершенного вида, справа глаголы совершенного вида. Весь график в целом представляет собой частотный словарь, разбитый на 2 категории для наглядности.
    
    '''),

    dcc.Graph(
        id='example-graph1',
        figure=fig
    ),

    dcc.Graph(
        id='example-graph2',
        figure=fig1
    ),

    dcc.Markdown('''
        **Работу выполнила: Ермакова Екатерина**

    ''')

])


if __name__ == '__main__':
    app.run_server(debug=True)
