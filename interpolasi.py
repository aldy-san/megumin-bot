def linier(msg):
  msg = msg.split("$interpolLinier ")[1].strip()
  if msg[0] == "x":
      findX = False
      titik = float(msg.split("x=")[1][0])
  else:
      findX = True
      titik = float(msg.split("y=")[1][0])
  titik_1 = [float(y) for y in msg.split("titik_1=")[1].split(" titik_2=")[0].split(",")]
  titik_2 = [float(y) for y in msg.split("titik_2=")[1].split(",")]
  output = "Rumus Interpolasi Linier\n"
  output += "(y-y₁)/(y₂-y₁) = (x-x₁)/(x₂-x₁)\n"
  output += "Subtitusi\n"
  if (findX):
      output += f"({titik:g} - {titik_1[1]:g}) / ({titik_2[1]:g} - {titik_1[1]:g}) = (x - {titik_1[0]:g}) / ({titik_2[0]:g} - {titik_1[0]:g})\n"
      output += f"({titik-titik_1[1]:g}) / ({titik_2[1]-titik_1[1]:g}) = (x - {titik_1[0]:g}) / ({titik_2[0]-titik_1[0]:g})\n"
      output += f"x = (({titik-titik_1[1]:g}) / ({titik_2[1]-titik_1[1]:g}) * ({titik_2[0]-titik_1[0]:g})) + ({titik_1[0]:g})\n"
      output += f"x = {((titik-titik_1[1])/(titik_2[1]-titik_1[1]) * (titik_2[0]-titik_1[0])) + (titik_1[0]):g}\n"
  else:
      output += f"(y - {titik_1[1]:g}) / ({titik_2[1]:g}-{titik_1[1]:g}) = ({titik:g} - {titik_1[0]:g}) / ({titik_2[0]:g}-{titik_1[0]:g}\n)"
      output +=f"(y - {titik_1[1]:g}) / ({titik_2[1]-titik_1[1]:g}) = ({titik-titik_1[0]:g}) / ({titik_2[0]-titik_1[0]:g})\n"
      output +=f"y = (({titik-titik_1[0]:g}) / ({titik_2[0]-titik_1[0]:g}) * ({titik_2[1]-titik_1[1]:g})) + ({titik_1[1]:g})\n"
      output +=f"y = {((titik-titik_1[0])/(titik_2[0]-titik_1[0])*(titik_2[1]-titik_1[1]))+titik_1[1]:g}\n"
  return output