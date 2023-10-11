__author__ = "Andrew Hughes"
__version__ = "0.1.0"
__license__ = "MIT"

import pandas as pd
import openai
from io import StringIO         #Used for converting to and from string.

def main():

    # Function to log errors in code.
    def log_error(Argument):
        # creating/opening a file
        f = open("logging.txt", "a")
        
        # writing in the file
        f.write("\n")
        f.write(str(Argument)+"\n")
            
        # closing the file
        print(Argument)
        f.close()

    # Function to call the api
    def chat_completion(chat_gpt_input):
        ## Connect to API
        openai.api_key = "YOUR API KEY HERE"            # <-------- Add your API key here

        ## Send to ChatGPT and get back the company and country standard formatted.
        prompt = """
                Fill in the missing values in this table based on your general knowledge of companies.
                Description of the field is in (). 
                RecordId, 
                FirstName, 
                LastName,
                InterestedProduct, 
                Company (correctly spelled and format the company to match the companies common official name), 
                Industry (the industry the company operates in),
                HeadquartersCountry (the country the company headquarters are in),
                HeadquartersCity (the city the company headquarters are in),
                ProductIndustry (the industry the company operates in based on the InterestedProduct and Company).
                Return only the table in the response.
                """ + chat_gpt_input            #variable containing our data.
        print('********************************************')
        print('--------------------------------------------')
        print('Prompt Sent to ChatGPT: \n',prompt)
        print('--------------------------------------------')

        # Query GPT - 
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a data analyst assistant analyzing csv datasets."},         #We can give a role to chatGPT. It will use this role when considering the prompt.
            {"role": "user", "content": prompt} #Here is the prompt variable. So our prompt is here.
        ]
        )

        # getting the response out of the JSON
        assistant_response = response['choices'][0]['message']['content']

        return assistant_response
    
    #Read the csv
    # Read the file into dataframe with pandas
    
    # For Demo Purposes
    data = pd.read_csv('SampleData.csv', delimiter=',', on_bad_lines='skip')
    
    print(data)
    
    # Picking only the fields I need for dataframe. No need to pass all fields unless they are used by CHatGPT
    df = data[["RecordId","FirstName","LastName","Company","InterestedProduct"]]

    #count how many records are in the source table
    num_of_records = len(df)

    dfs = []                               #Empty List for results to land in.

    # Loop over the records in steps of 10 records to stay under the charchter limit of a prompt + response.
    for i in range(0,num_of_records,10):
        
        #Wrap the code in a try block to catch errors and to avoid 
        try:
            ## Select the lead_id & the lead_display_name. Convert to a string to send in chatgpt. Send in smaller batches to not overload chatgpt.
            df_chat_gpt_input = df[["RecordId","FirstName","LastName","Company","InterestedProduct"]].iloc[i:(i+10)].to_csv(index=False)
            
            #Print the input text
            print("Input:")
            print(df_chat_gpt_input)

            #Run the Chat Prompt API
            assistant_response = chat_completion(df_chat_gpt_input)

            #Print the response from ChatGPT
            print("Response:")
            print(assistant_response)
        
            #Convert string response from ChatGPT to Dataframe to append to main dataframe #StringIO creates a "fake csv" for DF to interpret
            df_assistant_response = pd.read_csv(StringIO(assistant_response), on_bad_lines='skip')

            #Print the response
            print("DFResponse:")
            print(df_assistant_response)
            
            #Print out the data into CSVs or however you would like.
            df_assistant_response.to_csv(f'./outputs/sample{i}.csv', index=None, header=True)
            
            print(f'******Loop is on {i}******')

        #Except error handling
        except Exception as Argument:
            log_error(Argument)
            print("Error with Try Block!")
            pass
    
if __name__ == "__main__":
    """ Execution completed! (You will only see this in command line) """
    main()
