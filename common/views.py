from django.shortcuts import render


# Create your views here.

def dropdownSearch(listB, pk):
    str1 = '<select class="form-control" name="branch">'
    str1 += '<option value="0">All</option>'
    for li in listB:
        if str(pk) == str(li.id):
            str1 += '<option value = "' + \
                    str(li.id) + '" selected> ' + \
                    str(li.branch_name) + ' </option >'
        else:
            str1 += '<option value = "' + \
                    str(li.id) + '"> ' + \
                    str(li.branch_name) + ' </option >'

    str1 += '</select>'
    return str(str1)
