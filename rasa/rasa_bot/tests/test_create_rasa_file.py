# ctr = 0
# excel_filename = "yaml_test.csv"
# yaml_filename = excel_filename.replace('csv', 'yaml')
# users = {}
#
# with open(excel_filename, "r") as excel_csv:
#     for line in excel_csv:
#         if ctr == 0:
#             ctr+=1  # Skip the coumn header
#         else:
#             # save the csv as a dictionary
#             user,name,uid,shell = line.replace(' ','').strip().split(',')
#             users[user] = {'name': name, 'uid': uid, 'shell': shell}
#
#
#
# with open(yaml_filename, "w+") as yf :
#     yf.write("users: \n")
#     for u in users:
#         yf.write(f"  {u} : \n")
#         for k,v in users[u].items():
#             yf.write(f"    {k} : {v}\n")
import pandas as pd

def create_rasa_files(path, create_files_path, nlu_file_name, domain_file_name):

    #NLU FILE
    df = pd.read_csv(r"{}".format(path))
    file = open(create_files_path+'nlu'+nlu_file_name+'.yml',"w")

    intents = list(df.columns)
    for item in intents:
        file.write("- intent: {intent_name}\n".format(intent_name=item))
        file.write("  examples: |"+'\n')
        for sent in df[item]:
            file.write("   - {}\n".format(sent))
    file.close()


    #DOMAIN FILE
    file = open(create_files_path+domain_file_name+'.yml',"w")
    file.write("intents:\n")
    file.write("responses:\n")
    for intent_name in intents:
        file.write("   utter_{}:\n".format(intent_name))
        file.write('   - text:\n')
    file.write("actions: []\n")
    # for intent_name in intents:
    #     file.write("  - utter_{}\n".format(intent_name
    file.write('forms: {}\n')
    file.write('e2e_actions: []\n')
    file.close()
    return None

if __name__ == '__main__':
    path = './automated_test.csv'
    create_files_path = './'
    domain_file_name = '\domain'
    nlu_file_name = '\nlu'
    create_rasa_files(path, create_files_path, nlu_file_name, domain_file_name)