from pynk import isotopes as i

li2o = i.compound(constituents={'Li': 2, 'O': 1})

for row in li2o.abundance_table:
    print row
