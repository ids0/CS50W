from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):

    # Compara url/entryName con una lista de las entradas en minuscula
    # if title.lower() in list( map( lambda list_entry: list_entry.lower(), util.list_entries() ) ):

    # Busca la entrada en la lista de entradas, si no encuentra title = ""
    for correct_title in util.list_entries()+[""]:
        if correct_title.lower() == title.lower():
            title = correct_title
            break
    # Llego al final de la lista y no encontro
    if correct_title == "":
        incorrect_search = title
        title = correct_title
    else:
        incorrect_search = ""



    print(util.list_entries()+[""])
    print(f"title is {title}")
    return render(request, "encyclopedia/entries.html", {
        "title": title,
        "incorrect_search": incorrect_search,
        "entry_content": util.get_entry(title)
    })
