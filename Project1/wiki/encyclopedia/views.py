from django.shortcuts import render,redirect
from django.http import HttpResponse

from . import util

# Decorator for search implementation, just for fun
def implement_search(fun,*args,**kargs):
    search_argumnet = 'q'
    def wrapper(*args,**kargs):
        # TODO: Check if args[0] is what I think it is
        # if q is in argumunets of GET
        if search_argumnet in args[0].GET.keys():
            title, user_search = util.match_title(args[0].GET['q'])
            # Correct search
            if title:
                return redirect('entry', title=title)
            # Page with similar artciles
            else:
                # list with entries that match
                matching_entries = []
                # iterate over all entries in lower case (just to use map)
                for entry_title in list( map( lambda list_entry: list_entry.lower(), util.list_entries() ) ):
                    # if entry title contains user search append to list
                    if user_search.lower() in entry_title:
                        matching_entries.append(entry_title)
                    # Not wotch matching entry content
                    # elif user_search.lower() in util.get_entry(entry_title):
                    #     matching_entries.append(entry_title)

                # TODO: mayble implement search path
                return render(args[0], "encyclopedia/search.html", {
                    "entries": matching_entries
                })
        else:
            return fun(*args,**kargs)


    return wrapper

@implement_search
def index(request):
    # # Search
    # if 'q' in request.GET.keys():
    #     title, user_search = util.match_title(request.GET['q'])
    #     # Correct search
    #     if title:
    #         return redirect('entry', title=title)


    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

@implement_search
def entry(request,title):
    # if 'q' in request.GET.keys():
    #     title, user_search = util.match_title(request.GET['q'])
    #     # Correct search
    #     if title:
    #         return redirect('entry', title=title)

    title,user_title = util.match_title(title)

    return render(request, "encyclopedia/entries.html", {
        "title": title,
        "user_title": user_title,
        "entry_content": util.get_entry(title)
    })


