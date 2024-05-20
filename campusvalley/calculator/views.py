from django.shortcuts import render, redirect

# Create your views here.
def calculator(request):
    response= request.session.get('response')
    print(response)
    if 'response' in request.session:
        del request.session['response']
    return render(request, "calculator.html", {"response": response})
    # else:
        # return render(request, "calculator.html")


def evaluation(request):
    if request.method == "POST":
        expression = request.POST.get("expression")
        result= eval(expression)
        # print(eval('print("hello")')) //it allows to run python code
        response= {
            'result':result,
            'expression':expression
        }
        request.session["response"]= response
        return redirect(calculator)