# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 18:36:30 2020

@author: muuph
"""
import pandas as pd
import string
import statistics as stats

#df_lengths = pd.read_csv("../letter_lengths.csv")
pale = "So I lied, I cheated, I bribed men to cover the crimes of other men. I am an accessory to murder. But the most damning thing of all, I think I can live with it. And if I had to do it all over again, I would. Garak was right about one thing. A guilty conscience is a small price to pay for the safety of the Alpha Quadrant, so I will learn to live with it. Because I can live with it. I can live with it. "
kahless = "Long ago, a storm was heading for the city of Quin'lat. Everyone took protection within the walls except one man who remained outside. Kahless went to him and asked what he was doing.'I am not afraid,' the man said. 'I will not hide my face behind stone and mortar. I will stand before the wind and make it respect me.' Kahless honored his choice and went back inside. The next day, the storm came, and the man was killed. Kahless replied, 'The wind does not respect a fool'."
doc = "A strange seed was planted on its back at birth. The plant sprouts and grows with this Pokemon. To support the bud’s growing weight, it's legs and trunk grow thick and strong. If it starts spending more time lying in the sunlight, it's a sign that the bud will bloom into a large flower soon. The plant blooms when it is absorbing solar energy. It stays on the move to seek sunlight."
doc = "A strange seed was planted on its back at birth. The plant sprouts and grows with this Pokemon."
# step 1: generate list of values to loop through
# step 2: loop through the list with each run using those values, output to df
# step 3: choose value with smallest mean, use that text

def manuscript_format(doc, width, versal_width):
    # outside of the main loop
    width_list = [n for n in range(width-5,width+6)]
    df_compare = pd.DataFrame(width_list,columns=['range'])
    df_compare["document"] = ''
    df_compare["mean"] = 999
    df_compare["lines"] = 0
    df_compare["line_lengths"] = ''
    
    # create list of letter lengths    
    alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    one_length = ['e','f','i','j','l']
    three_length = ['m','w','g']
    doc = doc.replace("’","'")
    
    w = 0
    while w < len(width_list):
        # initialize objects
        words = doc.split()
        document = list()
        line = list()
        length_list = list()
        line_dist = list()
        # initialize starting variables
        line_length = 0
        word_length = 0
        i = 0
        line_number = 0
        line_width = width_list[w]
        if versal_width > 0:
            versal = True
        else:
            versal = False
        while i < len(words):
            word = words[i]
            word_length = 0
            if word.find("'") > -1:
                word_length = word_length+1
                word = word.translate(str.maketrans('', '', string.punctuation))
            letters = [char for char in word]
            if i == 0 and versal == True:     
                letters.pop(0)
                word_length = versal_width
            for char in letters:
                if char.isupper():
                    word_length = word_length+1
            letters = [char.lower() for char in letters]   
            temp_df = pd.DataFrame(letters, columns=['letter'])
            temp_df['value'] = 2
            j = 0
            while j < len(temp_df):
                if temp_df['letter'].iloc[j] in one_length:
                    temp_df['value'].iloc[j] = 1
                if temp_df['letter'].iloc[j] in three_length:
                    temp_df['value'].iloc[j] = 3  
                j += 1
            #join_df = temp_df.join(df_lengths.set_index('letter'),on='letter')
            values = temp_df['value'].tolist()
            word_length = word_length + (sum(values)+ (1* (values.count(1) // 2)))
            if i < (len(words)-1):
                word_length = word_length+2
            if line_length+word_length <= line_width:
               line.append(word)    
               line_length = line_length+word_length
            else:
                #print(line_length)
                length_list.append(line_length)
                string_line = ' '.join([str(word) for word in line]) 
                document.append(string_line)
                line = list()
                line.append(word)
                line_length = word_length
                line_number = line_number+1
                if line_number == 1 and versal == True:
                    line_length = line_length + versal_width
            i = i+1
        string_line = ' '.join([str(word) for word in line]) 
        document.append(string_line)
        for n in length_list:
            d = line_width - n
            line_dist.append(d)
        df_compare['document'].iloc[w] = document
        df_compare['mean'].iloc[w] = stats.mean(line_dist)
        df_compare['lines'].iloc[w] = len(document)
        df_compare['line_lengths'].iloc[w] = length_list
        w = w+1
    
    mc = df_compare[['mean']].idxmin()[0]
    doc_dict = {
        "document": df_compare['document'].iloc[mc]
        , "num_lines": df_compare['lines'].iloc[mc] 
        , "width": df_compare['range'].iloc[mc]
        , "line_lengths": df_compare['line_lengths'].iloc[mc]
        }
    return doc_dict

final = manuscript_format(kahless, 90, 15)

final["document"]
