n1 = raw_input("insectar numero uno")
n2 = raw_input("insectar numero dos")
n3 = raw_input("insectar numero tres")

if n1 > n2:
if n1 > n3:
if n2 > n3:
print str(n1)+ " - "+ str(n2)+ " - "+ str(n3)
else:
print str(n1)+ " - "+ str(n3)+ " - "+ str(n2)
else:
print str(n3)+ " - "+ str(n1)+ " - "+ str(n2)
else:
if n2 > n3:
if n1 > n3:
print str(n2)+ " - "+ str(n1)+ " - "+ str(n3)
else:
print str(n2)+ " - "+ str(n3)+ " - "+ str(n1)
else:
print str(n3)+ " - "+ str(n2)+ " - "+ str(n1)