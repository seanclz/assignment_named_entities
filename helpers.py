


#method to get coordinated entities of the same type in a text [OUTPUT : list of lists]
def get_coord_same_type(doc):

    # This is the function used to get a list of coordinated entities of the same type
    def coord_named_entities(entity, enttype, dict, tobeadded):
        tobeadded.append([entity, entity.label_])
        conj = [tok for tok in entity.rights if tok.right_edge.dep_ == 'conj']
        # if the current entity is not coordinated with anything , return the lists of coordinated entitites of the same type
        if not conj:
            if len(tobeadded) > 1:
                # remove from dictionary all the keys of coordinated entities to avoid visiting them again
                for entity,label in tobeadded:
                    if entity.end_char in dict:
                        del dict[entity.end_char]
                # filter by entity label_ using a lambda function
                values = set(map(lambda x: x[1], tobeadded))
                coord_list = [[y[0] for y in tobeadded if y[1] == x] for x in values]
                return coord_list
            else:
                return []
        else:
            # if the current entity is coordinated with another entity, check if this entity is named or not
            for tk in conj:
                # if the key is not in the dictionary, it means that this is not a named entity
                if (tk.idx+len(tk)) not in dict:
                    found = True
                    conj = [token for token in tk.rights if token.right_edge.dep_ == 'conj']
                    # search the dependency tree for a named entity among the coordinated ones
                    while conj and conj[0].idx + len(conj[0]) not in dict:
                        conj = [token for token in conj[0].rights if token.right_edge.dep_ == 'conj']
                    if not conj:
                        found = False
                    # if no named entity was found , return the lists of coordinated entities of the same type
                    if not found:
                        if len(tobeadded) > 1:
                            # remove from dictionary all the keys of coordinated entities to avoid visiting them again
                            for entity, label in tobeadded:
                                del dict[entity.end_char]
                            # filter by entity label_ using a lambda function
                            values = set(map(lambda x: x[1], tobeadded))
                            coord_list = [[y[0] for y in tobeadded if y[1] == x] for x in values]
                            return coord_list
                        else:
                            return []
                    # a named entity was found
                    else:
                        entity = dict[conj[0].idx + len(conj[0])]
                        return coord_named_entities(entity, enttype, dict, tobeadded)
                else:
                    # the entity is a valid named entity and it can be assigned using the dictionary
                    entity = dict[tk.idx + len(tk)]
                    return coord_named_entities(entity, enttype, dict, tobeadded)

    complete_list = []

    # dictionary used to map a token to an entity (using the position of chars)
    dict = {}
    # create a dictionary that maps every token to an entity
    for ent in doc.ents:
        for token in ent:
            dict[token.idx + len(token)] = ent
    # cycle through the entities
    for ent in doc.ents:
        # filter to avoid entities that are not coordinated with anything
        conj_check = [tok for tok in ent.rights if tok.right_edge.dep_ == 'conj']
        # check if they are coordinated with something and check if they are already visited
        if conj_check and ent.end_char in dict:
            list_tobeadded = []
            list_coord = coord_named_entities(ent, ent.label_, dict, list_tobeadded)
            for list in list_coord:
                # only add sub-lists of coordinated entities of the same type with more than 1 element
                if len(list) > 1:
                    complete_list.append(list)

    return complete_list
