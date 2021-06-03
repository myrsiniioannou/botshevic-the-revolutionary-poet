import nltk
import random
from nltk.tokenize import TweetTokenizer
import os
import tweepy

### 1. Read & Tokenize a text file - function

def read_and_tokenize(filePath):
    poem_lines=[]
    input_text = open(filePath, encoding="utf8")
    for line in input_text:
        line = line.lower()
        line_strip=line.strip()
        line_strip = line_strip.replace("â€™", "'")
        line_strip = line_strip.replace("â€”", "-")
        line_strip = line_strip.replace("\'s", "'s")
        tokenizer_words = TweetTokenizer()
        poem_lines.append(tokenizer_words.tokenize(line_strip))        
    return poem_lines


### 2. Analyse the files and tokenize them
def analyseAndTokenize(directory):
    all_file_tokens=[]
    for file in os.listdir(directory):
        # Tokenize
        tokens_sentences=read_and_tokenize(directory+file)
        tagged_tokens=[None] * len(tokens_sentences)
        # Analyze
        for sentence in tokens_sentences:
            tagged_tokens[tokens_sentences.index(sentence)]=nltk.pos_tag(sentence)

        all_file_tokens.append(tagged_tokens)
    return all_file_tokens


### 3. Create a dictionary including all the grammatical symbols
### &  Create a dictionary of sequences of grammatical symbols

def grammarSymbolsAndSequences(tokens):

    grammar_symbols = {}
    sequences = []

    for poem in tokens:
        #print("------------POEM-------",poem)
        for line in poem:
            # Create a list for the sequence of the specific line
            lineSequence=[]
            #print("------------Line-------",line)
            try:
                for index, word_and_symbol in enumerate(line):
                    key = word_and_symbol[1]
                    value = word_and_symbol[0]
                    # if the key is not in grammar dictionary add it and append it after
                    if key not in grammar_symbols:
                        grammar_symbols[key]=[]
                    if value not in grammar_symbols[key]:
                        grammar_symbols[key].append(value)
                    # Add the value to the sequence list of the line
                    lineSequence.append(key)
                # Add the value to the sequence general list
                sequences.append(lineSequence)
            except:
                #print('error index:',index, word_and_symbol)
                pass
    return grammar_symbols, sequences


### 5. Generate random sequences

def lineGenerator(n, gm, seq):
    # inputs:
    # n: number of lines
    # gm: grammar symbols
    # seq: all sequences of symbols
    
    generated_poem=""
    
    
    # Pick a random number for n line-sequence , meaning a range between 0 and len(seq)-n
    random_sequence = random.randint(0, len(seq)-n)

    
    for sequence in seq[random_sequence:random_sequence+n]:
        generated_line=""
        for symbol in sequence:
            random_word = random.choice(gm[symbol])
            generated_line+=random_word+" "
        
        #twitter character limit - 280
        if (len(generated_poem)+len(generated_line))<=280:
            generated_poem+=generated_line
        else:
            #print('----280 CHARACTERS LIMIT', len(generated_poem+generated_line))
            #print('length without this sentence:', len(generated_poem))
            break
        
    generated_poem = generated_poem.replace(" ,", ",")
    generated_poem = generated_poem.replace(" .", ".")
    generated_poem = generated_poem.replace(" !", "!")
    generated_poem = generated_poem.replace(" ?", "?")
    generated_poem = generated_poem.replace(" ;", ";")
    generated_poem = generated_poem.replace(" :", ":")
    generated_poem = generated_poem.replace(" i ", " I ")
    generated_poem = generated_poem.replace("\'s", "'s")
    generated_poem = generated_poem.replace(" -", "-")
    generated_poem = generated_poem.replace(" 's", "'s")
    generated_poem = generated_poem[:-1]
            
    #if (generated_poem[-1]==",") or "?" or ":" or ";" or "-")):
    if (generated_poem[-1]==",") or (generated_poem[-1]=="-") or (generated_poem[-1]==":") or (generated_poem[-1]==";"):
        generated_poem=generated_poem[:-1]
        generated_poem=generated_poem+"."        

        
    generated_poem = generated_poem.replace("“", "")
    
    
    # transform it into list for capitalization
    sample_list=list(generated_poem)                                           

    


    for index, letter in enumerate(generated_poem):
        if ((letter == "?") or (letter == ".") or (letter == "!")):
            try:
                #generated_poem = generated_poem[:index+2] + generated_poem[index+2:].upper()
                sample_list[:index+2]=sample_list[:index+2].upper()
                generated_poem = ''.join(str(i) for i in sample_list)
                print("index", generated_poem[index+2])
            except:
                pass
    return generated_poem

### 6. Generate a poem (directory, number of lines)

def poem_generator(direct, number_of_lines):
    all_tokens = analyseAndTokenize(direct)
    grammar_symbols, sequences = grammarSymbolsAndSequences(all_tokens)
    
    poem = lineGenerator(number_of_lines,grammar_symbols, sequences).capitalize()
    for index, character in enumerate(poem):
        if (character=="?") or (character==".") or (character=="!"):
            try:
                poem = poem[:index+2] + poem[index+2:].capitalize()
            except:
                pass
        
        if (character=="\\"):
            poem = poem[:index] + poem[index+1:]
    try:
        poem=poem.replace(' i ', " I ")
        poem=poem.replace(" i'm ", " I'm ")
        poem=poem.replace("\\", "")
    except:
        pass
    return poem




# RUN THE SCRIPT

directory= 'Corpus/'
#print(poem_generator(directory,5))



# Twitter
CONSUMER_KEY = 'mDgBJy8f4FP511hBId8sPp94a'
CONSUMER_SECRET = '2bEYAtiKj9db2G9GfWzkju2NKjznmrTJAy5RJHJLiDydmT3bEK'
ACCESS_KEY = '1399298847143251969-xfcOHTbvXbQcwiwogIxmhSpHF8SEgM'
ACCESS_SECRET = 'tYlYRHd7y1cHcSYau4dJnhcPIi9XqIMnl8tj1BfX8tfcI'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

# Create API object
api = tweepy.API(auth)

# Create a tweet
#api.update_status("Hello Tweepy")

poem_tweet = poem_generator(directory,random.randint(1,5))
api.update_status(poem_tweet)