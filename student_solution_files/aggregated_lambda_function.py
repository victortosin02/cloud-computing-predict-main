
"""
    Final AWS Lambda function skeleton. 
    
    Author: Explore Data Science Academy.
    
    Note:
    ---------------------------------------------------------------------
    The contents of this file should be added to a AWS  Lambda function 
    created as part of the EDSA Cloud-Computing Predict. 
    For further guidance around this process, see the README instruction 
    file which sits at the root of this repo.
    ---------------------------------------------------------------------

"""

# Lambda dependencies
import boto3 
import json
import base64
import random   
from botocore.exceptions import ClientError 
import numpy as np

# key phrases function
def key_phrase_finder(list_of_important_phrases, list_of_extracted_phrases):

    listing = []
    PhraseChecker = None

    res = str(list_of_extracted_phrases).split()

    for important_word in list_of_important_phrases:
        names = res
        names2 = [word for word in names if important_word in word]
        isnot_empty = np.array(names2).size > 0
        
        if isnot_empty == True:
            listing = np.append(listing, names2)
            
        else:
            listing = listing
            
    if np.array(listing).size > 0:
        PhraseChecker = True
        
    else:
        PhraseChecker = False
    
    return listing, PhraseChecker

# ** Insert sentiment extraction function **
def find_max_sentiment(Comprehend_Sentiment_Output):
    
    sentiment_score = 0

    if Comprehend_Sentiment_Output['Sentiment'] == 'POSITIVE':
        sentiment_score = Comprehend_Sentiment_Output['SentimentScore']['Positive']

    elif Comprehend_Sentiment_Output['Sentiment'] == 'NEGATIVE':
        sentiment_score = Comprehend_Sentiment_Output['SentimentScore']['Negative']

    elif Comprehend_Sentiment_Output['Sentiment'] == 'NEUTRAL':
        sentiment_score = Comprehend_Sentiment_Output['SentimentScore']['Neutral']

    else:
        sentiment_score = Comprehend_Sentiment_Output['SentimentScore']['Mixed']

    print(sentiment_score, Comprehend_Sentiment_Output['Sentiment'])
    
    return Comprehend_Sentiment_Output['Sentiment'], sentiment_score

 
# -----------------------------

# email responses function
def email_response(name, critical_phrase_list, list_of_extracted_phrases, AWS_Comprehend_Sentiment_Dump):

    # Function Constants
    SENDER_NAME = 'Victor'
    
    # --- Check for the sentiment of the message and find dominant sentiment score ---
    Sentiment_finder = find_max_sentiment(AWS_Comprehend_Sentiment_Dump)
    overwhelming_sentiment = Sentiment_finder[0]
    overwhelming_sentiment_score = Sentiment_finder[1]
    
    # --- Check for article critical phrases ---
    Phrase_Matcher_Article = key_phrase_finder(critical_phrase_list,  list_of_extracted_phrases)
    Matched_Phrases_Article = Phrase_Matcher_Article[0]
    Matched_Phrases_Checker_Article = Phrase_Matcher_Article[1]
    
    # --- Check for project phrases ---
    Phrase_Matcher_Project = key_phrase_finder(['github', 'git', 'Git', 
                                                'GitHub', 'projects', 
                                                'portfolio', 'Portfolio'],  
                                                list_of_extracted_phrases)
    Matched_Phrases_Project = Phrase_Matcher_Project[0]
    Matched_Phrases_Checker_Project = Phrase_Matcher_Project[1]
    
    # --- Check for C.V phrases ---
    Phrase_Matcher_CV = key_phrase_finder(['C.V', 'resume', 'Curriculum Vitae',
                                           'Resume', 'CV'],  
                                           list_of_extracted_phrases)
    Matched_Phrases_CV = Phrase_Matcher_CV[0]
    Matched_Phrases_Checker_CV = Phrase_Matcher_CV[1]
    
    # --- Generate standard responses ---
    # === DO NOT MODIFY THIS TEXT FOR THE PURPOSE OF PREDICT ASSESSMENT ===
    Greetings_text = f'Good day {name},'
    

    CV_text = 'I see that you mentioned my C.V in your message. \
               I am happy to forward you my C.V in response. \
               If you have any other questions or C.V related queries please do get in touch. '

    Project_Text = 'The projects I listed on my site only include \
                    the ones not running in production. I have \
                    several other projects that might interest you.'
    
    Article_Text = 'In your message you mentioned my blog posts and data science articles. \
                   I have several other articles published in academic journals. \
                   Please do let me know if you are interested - I am happy to forward them to you'
  
    Negative_Text = f'I see that you are unhappy in your response. \
                    Can we please set up a session to discuss why you are not happy, \
                    be it with the website, my personal projects or anything else. \
                    \n\nLooking forward to our discussion. \n\nKind Regards, \n\nMy Name'
 
    Neutral_Text = f'Thank you for your email. Let me know if you need any additional information.\
                    \n\nKind Regards, \n\n{SENDER_NAME}'
    
    Farewell_Text = f'Thank you for your email.\n\nIf there is anything else I can assist \
                     you with please let me know and I will set up a meeting for us to meet\
                     in person.\n\nKind Regards, \n\n{SENDER_NAME}'
    # =====================================================================
    
    # --- Email Logic --- 
    if overwhelming_sentiment == 'POSITIVE':
        if  ((Matched_Phrases_Checker_CV == True) & \
            (Matched_Phrases_Checker_Article == True) & \
            (Matched_Phrases_Checker_Project == True)):
            
            mytuple = (Greetings_text, CV_text, Article_Text, Project_Text, Farewell_Text)
            Text = "\n \n".join(mytuple)
            
        elif ((Matched_Phrases_Checker_CV == True) & \
             (Matched_Phrases_Checker_Article == False) & \
             (Matched_Phrases_Checker_Project == True)):
            
            mytuple = (Greetings_text, CV_text, Project_Text, Farewell_Text)
            Text = "\n \n".join(mytuple)
            
        elif ((Matched_Phrases_Checker_CV == True) & \
             (Matched_Phrases_Checker_Article == False) & \
             (Matched_Phrases_Checker_Project == False)):
            
            mytuple = (Greetings_text, CV_text, Farewell_Text)
            Text = "\n \n".join(mytuple)
            
        elif ((Matched_Phrases_Checker_CV == False) & \
             (Matched_Phrases_Checker_Article == True) & \
             (Matched_Phrases_Checker_Project == False)):
            
            mytuple = (Greetings_text, Article_Text, Farewell_Text)
            Text = "\n \n".join(mytuple)       
            
        elif ((Matched_Phrases_Checker_CV == False) & \
             (Matched_Phrases_Checker_Article == False) & \
             (Matched_Phrases_Checker_Project == False)):

            mytuple = (Greetings_text, Farewell_Text)
            Text = "\n \n".join(mytuple)   
            
        elif ((Matched_Phrases_Checker_CV == False) & \
             (Matched_Phrases_Checker_Article == False) & \
             (Matched_Phrases_Checker_Project == True)):
            
            mytuple = (Greetings_text, Project_Text ,Farewell_Text)
            Text = "\n \n".join(mytuple)   
            
        elif  ((Matched_Phrases_Checker_CV == True) & \
              (Matched_Phrases_Checker_Article == True) & \
              (Matched_Phrases_Checker_Project == False)):
            
            mytuple = (Greetings_text, CV_text, Article_Text, Farewell_Text)
            Text = "\n \n".join(mytuple)
            
        else:
            mytuple = (Greetings_text, Project_Text, Article_Text, Farewell_Text)
            Text = "\n \n".join(mytuple)
            
    elif overwhelming_sentiment == 'NEGATIVE':
            mytuple = (Greetings_text, Negative_Text)
            Text = "\n \n".join(mytuple)
            
    else:
            mytuple = (Greetings_text, Neutral_Text)
            Text = "\n \n".join(mytuple)
    
    return Text

# -----------------------------

# Lambda function orchestrating the entire predict logic
def lambda_handler(event, context):
    
    # Perform JSON data decoding 
    body_enc = event['body']
    dec_dict = json.loads(base64.b64decode(body_enc))
    

    # Write to dynamodb
    rid = random.randint(1, 1000000000) # random id
    
    dynamodb = boto3.resource('dynamodb')

    # Instantiate the table. Pass the name of the DynamoDB table created in step 4
    table = dynamodb.Table('victorportfolio')
    
    # ** Write the responses to the table using the put_item method. **

    db_response = table.put_item(Item={'ResponsesID': rid, 
                        'Name': dec_dict['name'],
                        'Email': dec_dict['email'],
                        'Cell': dec_dict['phone'], 
                        'Message': dec_dict['message']
    })


    # --- Amazon Comprehend ---
    comprehend = boto3.client(service_name='comprehend')
    
    # Message to encode
    enquiry_text = dec_dict['message']
    
    # --- get the sentiment with AWS comprehend ---
    sentiment = comprehend.detect_sentiment(Text=enquiry_text, LanguageCode='en')
    # -----------------------------
    
    # --- get the key phrases with AWS comprehend ---
    key_phrases = comprehend.detect_key_phrases(Text=enquiry_text, LanguageCode='en')
    # -----------------------------
    
    # Get list of phrases in numpy array
    phrase = []
    for i in range(0, len(key_phrases['KeyPhrases'])-1):
        phrase = np.append(phrase, key_phrases['KeyPhrases'][i]['Text'])


    # generate the text for your email response
    topics=['github', 'git', 'Git', 'GitHub', 'projects', 'portfolio', 'Portfolio', 'CV', 'Projects', 'articles']
    email_text = email_response(dec_dict['name'], critical_phrase_list=topics, list_of_extracted_phrases=phrase, AWS_Comprehend_Sentiment_Dump=sentiment) 
    # -----------------------------
            

    # ** SES Functionality **
    # sender email address
    SENDER = 'victortosin01@gmail.com'
    # -----------------------------

    # recipient
    RECIPIENT = dec_dict['email']
    # -----------------------------
    
    # Email Subject.
    # --- DO NOT MODIFY THIS CODE ---
    SUBJECT = f"Data Science Portfolio Project Website - Hello {dec_dict['name']}"
    # -------------------------------

    # The email body for recipients with non-HTML email clients
    BODY_TEXT = (email_text)

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES service resource
    client = boto3.client('ses')

    # Try to send the email.
    try:
        #Provide the contents of the email.
        ses_response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                    'edsa.predicts@explore-ai.net', 
                ],
            },
            Message={
                'Body': {

                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )

    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(ses_response['MessageId'])

    # ** Create a response object to inform the website that the 
    #    workflow executed successfully. Note that this object is 
    #    used during predict marking and should not be modified.**
    # --- DO NOT MODIFY THIS CODE ---
    lambda_response = {
        'statusCode': 200,
        'body': json.dumps({
        'Name': dec_dict['name'],
        'Email': dec_dict['email'],
        'Cell': dec_dict['phone'], 
        'Message': dec_dict['message'],
        'DB_response': db_response,
        'SES_response': ses_response,
        'Email_message': email_text
        })
    }
    # -----------------------------
    
    return lambda_response  
    




