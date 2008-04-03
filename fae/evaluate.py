from subprocess import call
from uid import generate

# run_wget(params, uid)
# search for .HTML file
# if .HTML file exists
#     run_ocaml(uid)
# else
#     return (0, uid)
# num_pages = get_pgcount(uid)

# report = UserReport(id=uid, user=request.user, pgcount=num_pages...)
# return (pgcount, uid)

#----------------------------------------------------------------
def evaluate(params):
    for i in range(0, 500000):
        j = i**2
    uid = generate()
    return (True, uid)
