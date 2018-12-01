# Returns: 
# Dict of dicts
#   each sub-dict has 3 timeslot keys
#     each timeslot key has list of names of triagers
#     default is ["?"]
# Ex:
#  reservations = {
#    "m": {
#      "1": ["?"],
#      "2": ["John Doe"],
#      "3": ["Jane Doe", "Joe Sixpack"]
#    },
#    "t": {
#      ...
#    },
#    ...
# }
def get_triager_reservations():
  ts=["1","2","3"]
  days=["m","t","w","h","f"]
  reservations = {d:{t:[] for t in ts} for d in days}
  for d,ts in reservations.items():
    for t,users in ts.items():
      if users==[]:
        reservations[d][t]=["?"]

  return reservations
