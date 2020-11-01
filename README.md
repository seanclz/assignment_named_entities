# Named Entity Analysis

## Description

The app uses **[spaCy](https://spacy.io/)** and a **[spaCy model](https://spacy.io/models/en#en_core_web_sm)** to analyze texts through **Named Entity Recognition** and **Dependency Parsing**. <br>
The data collected is displayed through an HTML page using **Flask**. <br> 
The graphs are plotted using the **[Plotly library](https://plotly.com/python/)**. 

In particular, the output will display information about:

* the number of Named Entities
* the most recurrent Named Entity types
* the most recurrent Named Entities 
* the number of Coordinated Entities of the same type
* the frequency of Coordinated Entities of the same type over the total of Named Entities
* the most recurrent Named Entity types among Coordinated Entities of the same type

Examples of output may be found in the **[Visuals section](#visuals)**.

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

## Info about the "get_coord_same_type" function

This section contains more information about **[this function](https://github.com/seanclz/assignment_named_entities/blob/main/helpers.py)** and what it is trying to catch. 

You can test the function on your own by customizing this simple code:

```bash
nlp = spacy.load('en_core_web_sm')
doc = nlp("Your sentences here.")

for sentence in doc.sents:
    print(get_coord_same_type(doc))
```
The function will output a list , in which each element is a list of **coordinated Named Entities of the same type**. <br>
We can define **Coordinated Entities** as entities that are "linked" through the **conj** branch of the **Dependency Tree**.

Input:
```bash
Bill and Melinda Gates come respectively from Seattle and Dallas.
```
The **Named Entities** and the **Dependency Tree** of the above sentence are as follow:

![](https://github.com/seanclz/assignment_named_entities/blob/main/imgs/entities.png)
![](https://github.com/seanclz/assignment_named_entities/blob/main/imgs/deptree.png)

* **"Bill"** and **"Melinda Gates"** are **PERSON** entities that are coordinated.
* **"Seattle"** and **"Dallas"** are **GPE** entities that are coordinated.

Since all the **coordinated Named Entities** are of the **same type**, the output of the function is as follow:

```bash
[[Bill, Melinda Gates], [Seattle, Dallas]]
```
You can visualize the **Named Entities** and the **Dependency Tree** by using **[Displacy](https://spacy.io/universe/project/displacy/)**.
```bash
from spacy import displacy

[...]
# displacy.serve(doc, style="ent")  uncomment to show the Named Entities
# displacy.serve(doc, style="dep")  uncomment to show the Dependency Tree
```

### More examples

Input: "Bill and New York are different entities."

```bash
[]
```
Input: "Europe, New York, Asia, Boston and Africa are 5 named entities."

```bash
[[Europe, Asia, Africa], [New York, Boston]]
```
Input: "John, the dog, the cat and Sarah are in New York."
```bash
[[John, Sarah]] 
```

## Credits
