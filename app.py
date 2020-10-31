from flask import Flask, render_template, make_response
import spacy
import json
import plotly.offline as opy
import plotly.express as px
import pandas as pd
from helpers import get_coord_same_type



app = Flask(__name__)

@app.route('/')
def index():

    #track of the dialog
    whole_dialog = ""
    # take track of entity number
    entity_counter = 0
    # take track of number of coordinated entities with the same type
    coord_type_counter = 0
    # take track of frequency of single entities
    ent_dict = {}
    # take track of frequency of entity types
    ent_type_dict = {}
    # take track of frequency of types among coordinated named-entities
    coord_dict = {}

    # read the data
    jsonFile = open('data/data.json', 'r')
    values = json.load(jsonFile)
    jsonFile.close()

    # load the model
    nlp = spacy.load('en_core_web_sm', disable=['tagger', 'textcat'])

    # extract all the dialogues in the dataset as a whole text
    for dialogue in values:
        # extracting dialogue text
        for log in values[dialogue]['log']:
            whole_dialog += log['text'] + " "
        whole_dialog += "\n"

    # analyze the dialogues in batches of 500 to speed up the process
    for doc in nlp.pipe(whole_dialog.split("\n"), batch_size=500):
        # sentence level analysis
        for sentence in doc.sents:
            c_t_entities = get_coord_same_type(sentence)
            for list in c_t_entities:
                # add the type of the coordinated entities if it was not already discovered
                if list[0].label_ not in coord_dict:
                    coord_dict[list[0].label_] = 0
                # counting frequency of coordinated entity of the same type using dictionaries
                coord_dict[list[0].label_] += len(list)
                # counting number of entities that are coordinated and of the same type
                coord_type_counter += len(list)

            for entity in sentence.ents:
                # counting number of entities
                entity_counter += 1
                # add the type of the entity if it was not already "discovered"
                if entity.label_ not in ent_type_dict:
                    ent_type_dict[entity.label_] = 0
                # add the text of the entity if it was not already "discovered"
                if entity.text not in ent_dict:
                    ent_dict[entity.text] = 0
                # counting frequency of entity type by using dictionaries
                ent_type_dict[entity.label_] += 1
                # counting frequency of single entities
                ent_dict[entity.text] += 1


    # creating the dataframes to display data with plotly library

    ent_d = {'Entity text': ent_dict.keys(), 'Frequency': ent_dict.values()}
    dfent = pd.DataFrame(ent_d).sort_values(by=['Frequency'], ascending=False).head(30)
    fig = px.bar(dfent, x='Entity text', y='Frequency', width=1200, height=800)
    fig.update_layout(bargap=0.02)
    graphent = opy.plot(fig, auto_open=False, output_type='div')

    ent_type_d = {'Type': ent_type_dict.keys(), 'Frequency': ent_type_dict.values() }
    dfte =  pd.DataFrame(ent_type_d).sort_values(by=['Frequency'],ascending=False)
    fig2 = px.bar(dfte, x='Type', y='Frequency', width=1200, height=600)
    fig2.update_layout(bargap=0.05)
    graphte = opy.plot(fig2, auto_open=False, output_type='div', )

    coord_d = {'Type': coord_dict.keys(), 'Frequency': coord_dict.values()}
    dfco = pd.DataFrame(coord_d).sort_values(by=['Frequency'], ascending=False)
    fig3 = px.bar(dfco, x='Type', y='Frequency', color_discrete_sequence= px.colors.qualitative.Plotly, width=1200, height=600)
    fig3.update_layout(bargap=0.05)
    graphco = opy.plot(fig3, auto_open=False, output_type='div')

    freq_coord = round((coord_type_counter/entity_counter) * 100 , 2)

    response = make_response(render_template('home.html', graphte=graphte, graphent = graphent,
                                             graphco = graphco, entity_counter=entity_counter, coord_type_counter = coord_type_counter,
                                             freq_coord = freq_coord))
    return response


if __name__ == '__main__':

	app.run(debug=False)