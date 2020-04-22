from chatterbot.trainers import ChatterBotCorpusTrainer
from tools import chatbot_logger
from chatterbot import ChatBot
import chatterbot.response_selection
import chatterbot.comparisons

def main():
    while True:
        print("Input: ")
        ins = input()
        try:
            if ins == 'q':
                break
            else:          
                response = chatbot.get_response(ins)
                print(response)

        except(KeyboardInterrupt, EOFError, SystemExit):
            break

'''Chatbot default response when the confidence of any
response is below the threshhold (confidence_lower_bound)
'''
default_response = 'That is a great question that I do not have an' \
                    ' answer to, to learn more you can reach out to the' \
                    ' Russ College at 740.593.1474 or email Dr. McAvoy' \
                    ' (mcavoy@ohio.edu)' \

confidence_lower_bound = 0.85

'''Chatterbot response selection methods: `get_random_response`
'''
response_selection_ = chatterbot.response_selection.get_random_response

'''Chatterbot statement comparison methods: `levenshtein_distance`
'''
comparison_ = chatterbot.comparisons.levenshtein_distance

'''Chatterbot statement preprocessors:
`clean_whitespace`
`unescape_html`
`convert_to_ascii`
'''
preprocessors_ = [
    "chatterbot.preprocessors.clean_whitespace",
    "chatterbot.preprocessors.unescape_html",
    "chatterbot.preprocessors.convert_to_ascii"
]

'''Chatterbot logic adapters and user-defined
logic adapters to supply non-trained responses:
`BestMatch`
`MathematicalEvaluation`
`WikiLogicAdapter`
`WeatherAdapter`
'''
logic_adapters_ = [
    {
        'import_path': 'chatterbot.logic.BestMatch',
        'default_response': default_response,
        'maximum_similarity_threshold': confidence_lower_bound
    },
    {'import_path': 'logic.logic_adapters.wiki_adapter.WikiLogicAdapter'},
    {'import_path': 'logic.logic_adapters.weather_adapter.WeatherAdapter'},
]

'''Build R²
'''
name = 'Console'
chatbot = ChatBot(name,
            response_selection_method=response_selection_,
            statement_comparison_function=comparison_,
            preprocessors=preprocessors_,
            logic_adapters=logic_adapters_,
            read_only=True)

'''Create a new trainer for R²
'''
trainer = ChatterBotCorpusTrainer(chatbot)

'''Train R² on `responses` folder
'''
trainer.train("responses/unsorted_mod.yml")
trainer.train("responses/unsorted_mod_stemmed.yml")
trainer.train("responses/unsorted_mod_lemmatized.yml")

'''
#################################################
'''

if __name__ == "__main__":
    main()
