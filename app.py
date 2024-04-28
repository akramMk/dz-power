from flask import Flask, render_template, request
from views import submit_knowledge_base_logic
from attacks import *
from graph import *
from burden import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_knowledge_base', methods=['GET', 'POST'])
def submit_knowledge_base():
    return render_template('submit_knowledge_base.html')

@app.route('/generate_attacks', methods=['POST'])
def generate_attacks():
    context = submit_knowledge_base_logic(request)

    # Générer les attaques en utilisant les fonctions fournies
    all_arguments = context['arguments']
    rebuts_attacks = generate_all_rebuts_with_sub_args(all_arguments)
    undercuts = generate_all_undercut(all_arguments)
    all_rebuts = generate_argument_preference(rebuts_attacks)
    all_defeats = generate_all_defeats(all_rebuts, undercuts)

    # Genere les graphs
    generate_graph(all_arguments, all_defeats)
    generate_histogram(all_arguments, all_defeats)

    # Genere les burden
    all_burden = calc_all_burden(all_arguments, all_defeats)

    # Convertir les données de burden en une liste de tuples (argument, burden)
    burden_data = [(arg, data) for arg, data in all_burden.items()]


    #Affiche les preferences
    preference = compare(all_burden)
    
    return render_template('attacks_template.html',
                           image_file_graph='graph.png',
                           image_file_histogram='histogram.png',
                           rebuts_attacks=rebuts_attacks,
                           defeats=all_defeats,
                           rebuts=all_rebuts,
                           undercuts=undercuts,
                           burden=burden_data,  # Transmettre les données de burden au template
                           preference=preference,
                           **context)


# if __name__ == '__main__':
#     app.run(debug=True)
