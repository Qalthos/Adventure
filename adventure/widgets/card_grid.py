import adventure.model as model
from tw2.jit import SQLARadialGraph

class CardGrid(SQLARadialGraph):
    id = 'card-grid'
    entities = [model.Card]
    excluded_columns = ['id', 'description', 'special', 'backlinks']
    base_url = 'jit_data'
    #width = '920'
    #height = '525'
    depth = 5
    rootObject = model.Card.query.first()
