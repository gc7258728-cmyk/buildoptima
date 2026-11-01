import io, json
from dataclasses import asdict
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from dimensia.mechanics import Beam,analyze
from dimensia.foundations import centered_footing
from dimensia.reliability import sample_udl_limit
from dimensia.optimization import search
from dimensia.reports import pdf
from dimensia.datasets import load_table,audit,numeric_stats,linear_fit
from dimensia.loads import LoadCombination
from dimensia.sections import rectangle,circle,hollow_rectangle

st.set_page_config(page_title="DIMENSIA — Structural Studio",page_icon="🏗️",layout="wide")
st.markdown("""<style>
[data-testid="stApp"]{background:#f3f6fa;color:#172c42}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#10263c,#1b4057)}
[data-testid="stSidebar"] *{color:#f2f7fa}
h1,h2,h3{letter-spacing:-.035em}
.hero{background:linear-gradient(110deg,#10283f,#16657c);padding:30px;border-radius:18px;color:white;box-shadow:0 12px 30px #12364d24}
.hero h1{color:white;margin:0}.hero p{color:#d4e8f0}
.kpi{background:white;padding:16px 20px;border-top:4px solid #e7a24d;border-radius:14px;box-shadow:0 5px 16px #12364d0a}
.kpi small{color:#6c8293}.kpi b{font-size:1.55rem;display:block;color:#123650}
</style>""",unsafe_allow_html=True)
def metric(title,value):
 st.markdown(f'<div class="kpi"><small>{title}</small><b>{value}</b></div>',unsafe_allow_html=True)
def plot_line(x,y,title,ylabel,color="#0b7495"):
 fig=go.Figure(go.Scatter(x=x,y=y,mode="lines",line={"color":color,"width":3},fill="tozeroy"))
 fig.update_layout(title=title,xaxis_title="Position x (m)",yaxis_title=ylabel,margin=dict(l=12,r=12,t=50,b=20),height=320)
 st.plotly_chart(fig,use_container_width=True)
with st.sidebar:
 st.title("◢ DIMENSIA")
 st.caption("STRUCTURAL ENGINEERING STUDIO")
 page=st.radio("Explorer",["Vue générale","Analyse des poutres","Pré-dimensionnement semelles","Optimisation des sections","Probabilités & fiabilité","Explorateur de données","Combinaisons de charges","Propriétés des sections","Comprendre & limites"])
 st.divider()
 st.caption("Calculs mécaniques pédagogiques · Pas de certification BAEL/EC2")
st.markdown('<div class="hero"><h1>DIMENSIA <span style="color:#f6b75c">/ Studio</span></h1><p>Analyser. Pré-dimensionner. Comparer. Comprendre les structures.</p></div>',unsafe_allow_html=True)
st.write("")
if "beam" not in st.session_state:
 st.session_state.beam=dict(span_m=5.,width_m=.25,depth_m=.45,e_gpa=30.,udl_kn_m=20.,point_kn=0.,point_x_m=2.5,support="Simplement appuyée")
def beam_form():
 with st.form("beam_form"):
  a,b,c=st.columns(3)
  with a:
   span=st.number_input("Portée L (m)",.2,40.,float(st.session_state.beam["span_m"]),step=.1)
   width=st.number_input("Largeur b (m)",.05,3.,float(st.session_state.beam["width_m"]),step=.05)
  with b:
   depth=st.number_input("Hauteur h (m)",.08,4.,float(st.session_state.beam["depth_m"]),step=.05)
   E=st.number_input("Module E (GPa)",1.,250.,float(st.session_state.beam["e_gpa"]),step=1.)
  with c:
   q=st.number_input("Charge répartie q (kN/m)",0.,500.,float(st.session_state.beam["udl_kn_m"]),step=1.)
   P=st.number_input("Charge ponctuelle P (kN)",0.,10000.,float(st.session_state.beam["point_kn"]),step=1.)
  d,e=st.columns(2)
  with d:x=st.number_input("Position charge P : a (m)",0.,float(span),min(float(st.session_state.beam["point_x_m"]),float(span)),step=.1)
  with e:support=st.selectbox("Appuis",["Simplement appuyée","Console"],index=0 if st.session_state.beam["support"]=="Simplement appuyée" else 1)
  submit=st.form_submit_button("Calculer la poutre",type="primary")
  if submit:
   st.session_state.beam=dict(span_m=span,width_m=width,depth_m=depth,e_gpa=E,udl_kn_m=q,point_kn=P,point_x_m=x,support=support)
   st.rerun()
 return Beam(**st.session_state.beam)
beam=Beam(**st.session_state.beam)
if page=="Vue générale":
 st.subheader("Tableau de bord technique")
 st.info("Version 1 : modèles de poutres d'Euler-Bernoulli et semelles centrées. Les règles complètes de ferraillage BAEL 91/99 et Eurocode 2 ne sont pas encore implémentées.")
 try:
  r=analyze(beam)
  a,b,c,d=st.columns(4)
  with a:metric("Portée",f"{beam.span_m:g} m")
  with b:metric("Moment maximal",f"{r['m_max']:.2f} kN·m")
  with c:metric("Effort tranchant",f"{r['v_max']:.2f} kN")
  with d:metric("Flèche maximale",f"{r['deflection_mm']:.2f} mm")
  plot_line(r["x"],r["M"],"Diagramme du moment fléchissant","M (kN·m)")
 except ValueError as e:st.error(str(e))
 st.caption("Les charges ne sont pas combinées à l'ELU. Aucun calcul de ferraillage normatif n'est fourni.")
elif page=="Analyse des poutres":
 st.header("📐 Analyse mécanique des poutres")
 beam=beam_form()
 try:
  r=analyze(beam)
  a,b,c=st.columns(3)
  with a:metric("Moment max. |M|",f"{r['m_max']:.3f} kN·m")
  with b:metric("Effort max. |V|",f"{r['v_max']:.3f} kN")
  with c:metric("Flèche max.",f"{r['deflection_mm']:.3f} mm")
  st.write("**Réactions aux appuis**",r["reactions"])
  plot_line(r["x"],r["V"],"Effort tranchant","V (kN)","#db8d35")
  plot_line(r["x"],r["M"],"Moment fléchissant","M (kN·m)")
  plot_line(r["x"],r["y_mm"],"Déformée théorique","y (mm)","#6c52b7")
  df=pd.DataFrame({"x_m":r["x"],"V_kN":r["V"],"M_kNm":r["M"],"fleche_mm":r["y_mm"]})
  st.download_button("Exporter les diagrammes (CSV)",df.to_csv(index=False).encode("utf-8-sig"),"dimensia_poutre.csv","text/csv")
  report=pdf("Poutre — analyse élastique",asdict(beam),{"M_max (kN.m)":round(r["m_max"],3),"V_max (kN)":round(r["v_max"],3),"Fleche (mm)":round(r["deflection_mm"],3),"I (m4)":r["inertia_m4"]},"Modèle Euler-Bernoulli à rigidité constante, chargement statique. Ce rapport n'est pas un dimensionnement BAEL ou Eurocode 2.")
  st.download_button("📑 Note de calcul PDF",report,"DIMENSIA_note_poutre.pdf","application/pdf")
 except ValueError as e:st.error(str(e))
elif page=="Pré-dimensionnement semelles":
 st.header("🪨 Pré-dimensionnement d'une semelle isolée")
 st.caption("Semelle centrée sous charge verticale ; vérification de pression moyenne seulement. Pas de poinçonnement, flexion, glissement, tassement ni excentricité.")
 a,b,c=st.columns(3)
 with a:N=st.number_input("Charge verticale de service N (kN)",1.,100000.,900.,step=50.)
 with b:qa=st.number_input("Pression admissible du sol (kPa)",1.,5000.,200.,step=10.)
 with c:ratio=st.number_input("Rapport L/B",.3,4.,1.,step=.1)
 d,e=st.columns(2)
 with d:h=st.number_input("Épaisseur de semelle (m)",.1,3.,.45,step=.05)
 with e:selfweight=st.checkbox("Inclure poids propre estimé",True)
 try:
  r=centered_footing(N,qa,ratio,h,include_self_weight=selfweight)
  cols=st.columns(4)
  for col,title,val in zip(cols,["Surface minimale","Largeur B","Longueur L","Pression calculée"],[f"{r['area_m2']:.2f} m²",f"{r['width_m']:.2f} m",f"{r['length_m']:.2f} m",f"{r['bearing_kpa']:.1f} kPa"]):
   with col:metric(title,val)
  st.warning("Résultat indicatif : faire vérifier la portance géotechnique, les tassements, le poinçonnement, la flexion et les armatures avant toute utilisation.")
  st.download_button("Note de calcul PDF",pdf("Semelle — pression moyenne",{"N (kN)":N,"q adm (kPa)":qa,"L/B":ratio,"epaisseur (m)":h},r,"Vérification très simplifiée sous charge centrée. Non conforme à une procédure normative complète."),"DIMENSIA_semelle.pdf","application/pdf")
 except ValueError as ex:st.error(str(ex))
elif page=="Optimisation des sections":
 st.header("⚖️ Recherche de sections candidates")
 st.caption("Filtre pédagogique sur la flèche et un seuil de moment FOURNI par l'utilisateur. Le seuil de moment n'est pas une résistance calculée du béton armé.")
 a,b,c=st.columns(3)
 with a:lim=st.number_input("Flèche maximale admissible (mm)",.01,500.,beam.span_m*1000/300,step=1.)
 with b:mlim=st.number_input("Seuil de moment |M| (kN·m)",.1,100000.,150.,step=5.)
 with c:step=st.select_slider("Nombre de sections par dimension",options=[4,6,8,10],value=8)
 widths=np.linspace(.15,.6,step);depths=np.linspace(.25,.85,step)
 rows=search(beam,widths,depths,lim,mlim)
 d=pd.DataFrame(rows)
 if not d.empty:
  good=d[d["admissible_selon_criteres_saisis"]]
  if len(good):st.success(f"{len(good)} sections respectent les deux critères saisis. Volume minimum : {good.iloc[0]['volume_m3']:.3f} m³ (b={good.iloc[0]['largeur_cm']:.0f} cm ; h={good.iloc[0]['hauteur_cm']:.0f} cm).")
  else:st.warning("Aucune section ne respecte les seuils saisis.")
  st.dataframe(d,use_container_width=True,hide_index=True)
  st.plotly_chart(px.scatter(d,x="volume_m3",y="fleche_mm",color="admissible_selon_criteres_saisis",hover_data=["largeur_cm","hauteur_cm"],title="Volume et flèche des sections candidates"),use_container_width=True)
  st.download_button("Exporter comparaison CSV",d.to_csv(index=False).encode("utf-8-sig"),"dimensia_sections.csv","text/csv")
 st.info("Important : le modèle n'effectue aucune vérification normative en flexion, cisaillement, ancrage ou fissuration. Les sections sont des candidats à étudier, pas des sections certifiées.")
elif page=="Probabilités & fiabilité":
 st.header("🎲 Simulation probabiliste des sollicitations")
 st.caption("Distribution lognormale positive sur la charge répartie. La probabilité calculée est un dépassement de seuil choisi, pas une probabilité de ruine normative.")
 a,b,c=st.columns(3)
 with a:threshold=st.number_input("Seuil de moment à dépasser (kN·m)",.1,100000.,75.,step=5.)
 with b:cv=st.slider("Coefficient de variation de q (%)",0,80,15)
 with c:n=st.select_slider("Nombre de tirages",options=[1000,5000,10000,25000,50000],value=10000)
 seed=st.number_input("Graine reproductible",0,1000000,42)
 if beam.point_kn:
  st.warning("Pour la simulation, fixez la charge ponctuelle P à 0 dans « Analyse des poutres ».")
 else:
  try:
   r=sample_udl_limit(beam,threshold,cv/100,n,seed)
   a,b,c=st.columns(3)
   with a:metric("P(|M| > seuil)",f"{100*r['probability']:.2f} %")
   with b:metric("Moment au 95e percentile",f"{r['p95']:.2f} kN·m")
   with c:metric("Erreur Monte-Carlo (1σ)",f"{100*r['mc_se']:.2f} pt")
   st.plotly_chart(px.histogram(x=r["moments"],nbins=55,title="Distribution simulée du moment maximal",labels={"x":"|M|max (kN·m)"}),use_container_width=True)
   st.caption("Hypothèses : charge q lognormale de moyenne égale à la valeur saisie, CV imposé ; autres paramètres déterministes.")
  except ValueError as ex:st.error(str(ex))
elif page=="Explorateur de données":
 st.header("📊 Explorateur de données — observations brutes d'abord")
 st.caption("Importez des mesures réelles ou un jeu d'exemple fictif. Les sources et unités doivent être renseignées par l'utilisateur.")
 uploaded=st.file_uploader("Fichier de données",type=["csv","xlsx"])
 source=st.text_input("Source des données (organisme, campagne ou fichier)","Source non renseignée")
 date=st.text_input("Date de collecte ou de publication","Non renseignée")
 units=st.text_input("Unités des variables","À préciser")
 if uploaded:
  try:
   df=load_table(uploaded.getvalue(),uploaded.name)
   st.info(f"Source : {source} | Date : {date} | Unités : {units} | {len(df):,} observations | {len(df.columns)} variables")
   st.subheader("1. Données brutes")
   st.dataframe(df.head(1000),use_container_width=True)
   st.caption("Aperçu limité à 1 000 lignes ; les calculs portent sur toutes les lignes importées.")
   st.subheader("2. Qualité des données")
   st.dataframe(audit(df),use_container_width=True,hide_index=True)
   st.subheader("3. Statistiques descriptives")
   stats=numeric_stats(df)
   if stats.empty:st.warning("Aucune variable numérique disponible.")
   else:
    st.dataframe(stats,use_container_width=True)
    names=list(stats.index)
    col=st.selectbox("Variable à représenter",names)
    st.plotly_chart(px.histogram(df,x=col,nbins=40,title=f"Distribution : {col}"),use_container_width=True)
    if len(names)>=2:
     with st.expander("Régression linéaire exploratoire"):
      x=st.selectbox("Variable explicative X",names,index=0)
      y=st.selectbox("Variable cible Y",names,index=1)
      if x!=y:
       try:
        fit,pairs=linear_fit(df,x,y)
        st.json(fit)
        st.plotly_chart(px.scatter(pairs,x=x,y=y,trendline=None,title="Observations (aucune extrapolation validée)"),use_container_width=True)
       except ValueError as exc:st.warning(str(exc))
    st.download_button("Exporter statistiques (CSV)",stats.to_csv().encode("utf-8-sig"),"dimensia_statistiques.csv","text/csv")
  except Exception as exc:st.error(f"Impossible d'analyser le fichier : {exc}")
elif page=="Combinaisons de charges":
 st.header("⚖️ Combinaisons paramétriques de charges")
 st.warning("Les coefficients sont choisis par l'utilisateur. Aucun préréglage réglementaire BAEL/Eurocode 2 n'est appliqué.")
 c1,c2=st.columns(2)
 with c1:
  G=st.number_input("Charge permanente G (kN/m)",0.,10000.,10.)
  Q=st.number_input("Charge variable Q (kN/m)",0.,10000.,5.)
 with c2:
  gg=st.number_input("Coefficient gamma G",0.,10000.,1.0,step=.05)
  gq=st.number_input("Coefficient gamma Q",0.,10000.,1.0,step=.05)
 try:
  result=LoadCombination(G,Q,gg,gq).evaluate()
  st.metric("Charge combinée",f"{result['q_combine (kN/m)']:.2f} kN/m")
  st.dataframe(pd.DataFrame([result]),hide_index=True)
  st.info("Pour une poutre simplement appuyée sous charge répartie : Mmax=qL²/8 et Vmax=qL/2.")
  L=st.number_input("Portée de calcul L (m)",.2,40.,5.)
  st.metric("Moment maximal correspondant",f"{result['q_combine (kN/m)']*L**2/8:.2f} kN·m")
 except ValueError as exc:st.error(str(exc))
elif page=="Propriétés des sections":
 st.header("📏 Caractéristiques géométriques des sections")
 typ=st.selectbox("Géométrie",["Rectangle plein","Cercle plein","Rectangle creux centré"])
 try:
  if typ=="Rectangle plein":
   b=st.number_input("Largeur b (m)",.01,5.,.25)
   h=st.number_input("Hauteur h (m)",.01,5.,.45)
   result=rectangle(b,h)
  elif typ=="Cercle plein":
   d=st.number_input("Diamètre d (m)",.01,5.,.4)
   result=circle(d)
  else:
   b=st.number_input("Largeur extérieure b (m)",.02,5.,.4)
   h=st.number_input("Hauteur extérieure h (m)",.02,5.,.6)
   bi=st.number_input("Largeur intérieure bi (m)",.01,5.,.25)
   hi=st.number_input("Hauteur intérieure hi (m)",.01,5.,.4)
   result=hollow_rectangle(b,h,bi,hi)
  st.dataframe(pd.DataFrame([result]),use_container_width=True,hide_index=True)
  st.download_button("Exporter résultats JSON",json.dumps(result,indent=2).encode(),"dimensia_section.json","application/json")
 except ValueError as exc:st.error(str(exc))
else:
 st.header("📚 Comprendre les modèles et leurs limites")
 st.markdown("""### 1. Poutre simplement appuyée, charge répartie uniforme
- Réactions : **RA = RB = qL/2**.
- Moment maximal : **Mmax = qL²/8**.
- Effort tranchant maximal : **Vmax = qL/2**.
- Flèche maximale : **5qL⁴/(384EI)**.
- Inertie d'une section rectangulaire : **I = bh³/12**.

### 2. Poutre console
- Moment maximal sous charge répartie : **qL²/2**.
- Flèche maximale sous charge répartie : **qL⁴/(8EI)**.

### 3. Semelle isolée
Pour une charge verticale centrée, **A ≈ N/qadm** ; le poids propre de la semelle peut être inclus.

### 4. Probabilités
Pour une charge répartie aléatoire Q, on simule le moment maximal **M(Q)** et on estime **P(M > Mseuil)**.

### 5. Ce qui n'est PAS implémenté
- **BAEL 91 révisé 99** : aucune vérification complète du ferraillage selon cette norme.
- **Eurocode 2** : aucune vérification complète ELU/ELS selon cette norme.
- Poteaux et dalles : pas encore développés.
- Calcul des armatures, flambement, cisaillement du béton armé, poinçonnement, fissuration, ancrages et tassements : non implémentés.
- Combinaisons réglementaires des actions, imperfections, fluage et effets différés : non implémentés.

Les résultats sont destinés à l'enseignement, à la vérification de formules et à l'exploration des paramètres. **Ne pas utiliser seuls pour construire un ouvrage.**
""")
