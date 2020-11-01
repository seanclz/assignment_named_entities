# Named Entity Analysis

## Description

The project uses **[spaCy](https://spacy.io/)** and a **[spaCy model](https://spacy.io/models/en#en_core_web_sm)** to analyze texts through **Named Entity Recognition** and **Dependency Parsing**. The data collected is displayed through an html page using **Flask**. The graphs are plotted using the **[Plotly library](https://plotly.com/python/)**. Examples of output may be found in the Visuals section.

## Input

The script is currently set to read dialogues from the **[MultiWOZ dataset](https://github.com/budzianowski/multiwoz)** and can only read json files of said format. Be sure to change the part of the program that reads the data files according to your needs if you plan to use this for other formats.

## Installation

Go to **/data** and extract the **data.json** file inside the **data.zip** archive (make sure to leave the file inside the data folder). This data refers to the **[MultiWOZ_2.2 dataset](https://github.com/budzianowski/multiwoz/blob/master/data/MultiWOZ_2.2.zip)** .

Install the dependencies using the following command:

```bash
pip install -r requirements.txt
```
Download the spaCy model :

```bash
python -m spacy download en_core_web_sm
```

## Execution

Issue the following command to start the Flask app :

```bash
python app.py
```
This will launch a basic server, head over to the localhost link that pops up in the console and let the page load.

**Note** : If you plan to run this with the **MultiWOZ_2.2 dataset** as input data, the page will take a few minutes to load (~ 5 minutes in my testing) as the dataset is composed of approximatively ~10000 dialogues each of which sitting at a ~1000 characters size on average.


## Visuals

Example of visuals obtained by running the app using the MultiWOZ_2.2 dataset as input :

![](https://github.com/seanclz/assignment_named_entities/blob/main/imgs/namedentitybarplot.png)
![](https://github.com/seanclz/assignment_named_entities/blob/main/imgs/namedentityfreq.png)
![](https://github.com/seanclz/assignment_named_entities/blob/main/imgs/coordtypebarplot.png)

## Digression about Named Entity dependencies 

## Credits
