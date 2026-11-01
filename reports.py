import io
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
def pdf(title,inputs,outputs,warning):
 buf=io.BytesIO();styles=getSampleStyleSheet()
 story=[Paragraph("DIMENSIA | NOTE DE CALCUL PÉDAGOGIQUE",styles["Title"]),Spacer(1,12),Paragraph(title,styles["Heading2"])]
 for label,items in (("Hypothèses et données",inputs),("Résultats",outputs)):
  story.append(Spacer(1,14));story.append(Paragraph(label,styles["Heading3"]))
  rows=[["Paramètre","Valeur"]]+[[str(k),str(v)] for k,v in items.items()]
  t=Table(rows,colWidths=[240,270],repeatRows=1)
  t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#183A54")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.3,colors.lightgrey),("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
  story.append(t)
 story.extend([Spacer(1,20),Paragraph(warning,styles["Italic"])])
 SimpleDocTemplate(buf,pagesize=(595,842),leftMargin=42,rightMargin=42).build(story)
 return buf.getvalue()
