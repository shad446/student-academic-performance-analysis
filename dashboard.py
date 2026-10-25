import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Academic Intelligence",page_icon="◆",layout="wide")
NAVY="#0C1627"; GOLD="#D9BC7B"; TEAL="#67C6B6"; BLUE="#91B2EC"; IVORY="#F5F1E8"
st.markdown(f"""<style>
.stApp{{background:linear-gradient(120deg,#0C1627,#13233A);color:{IVORY}}}
[data-testid="stSidebar"]{{background:#0D192B}}
h1,h2,h3{{color:{IVORY}!important}}
.hero{{background:#192B44;border:1px solid #45516A;padding:25px;border-radius:18px;margin-bottom:22px}}
.brand{{font-size:13px;letter-spacing:3px;color:{GOLD};font-weight:700}}
.logo{{display:inline-block;padding:12px;border:1px solid {GOLD};border-radius:12px;color:{GOLD};font-weight:800;font-size:25px;margin-right:15px}}
.kpi{{background:linear-gradient(135deg,#1D3049,#14233A);border:1px solid #3C4D63;border-radius:15px;padding:19px;margin-bottom:12px;min-height:130px}}
.kpi-label{{font-size:12px;letter-spacing:1.4px;color:#A9B8C9;text-transform:uppercase}}
.kpi-number{{font-size:32px;font-weight:800;color:{IVORY};margin:13px 0 5px}}
.kpi-note{{font-size:12px;color:{GOLD}}}
</style>""",unsafe_allow_html=True)
@st.cache_data
def load_data(upload=None):
    if upload is not None: d=pd.read_csv(upload)
    else:
        path=next((p for p in ["StudentsPerformance.csv","Student_Performance.csv"] if Path(p).exists()),None)
        if path is None: raise FileNotFoundError("Place StudentsPerformance.csv beside this Python file or upload it.")
        d=pd.read_csv(path)
    cols=["gender","race/ethnicity","parental level of education","lunch","test preparation course","math score","reading score","writing score"]
    missing=[c for c in cols if c not in d.columns]
    if missing: raise ValueError("Missing columns: "+", ".join(missing))
    for c in cols[-3:]: d[c]=pd.to_numeric(d[c],errors="coerce")
    d=d.dropna(subset=cols[-3:]).copy()
    d["Average Score"]=d[cols[-3:]].mean(axis=1)
    return d
def metric(label,value,note):
    st.markdown(f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-number">{value}</div><div class="kpi-note">{note}</div></div>',unsafe_allow_html=True)
def plot(fig,height=350):
    fig.update_layout(template="plotly_dark",height=height,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color=IVORY,margin=dict(l=12,r=12,t=50,b=12),showlegend=False)
    fig.update_yaxes(gridcolor="rgba(170,190,210,.15)")
    st.plotly_chart(fig,use_container_width=True)
st.sidebar.markdown("### ◆ Academic Intelligence")
st.sidebar.caption("Interactive analysis controls")
upload=st.sidebar.file_uploader("Upload student CSV (optional)",type="csv")
try: df=load_data(upload)
except Exception as e:
    st.error(str(e));st.stop()
filters=[("gender","Gender"),("race/ethnicity","Race / ethnicity"),("parental level of education","Parental education"),("lunch","Lunch type"),("test preparation course","Test preparation")]
data=df.copy()
for col,label in filters:
    choices=sorted(df[col].dropna().astype(str).unique().tolist())
    selected=st.sidebar.multiselect(label,choices,default=choices)
    data=data[data[col].astype(str).isin(selected)]
st.markdown('<div class="hero"><div class="brand"><span class="logo">AI</span>ACADEMIC INTELLIGENCE / EDUCATION ANALYTICS</div><h1>Student Performance Overview</h1><p>Executive insights into academic outcomes and learning factors.</p></div>',unsafe_allow_html=True)
if data.empty: st.warning("No students match your filters. Expand the selection.");st.stop()
means=data[["math score","reading score","writing score"]].mean()
overall=data["Average Score"].mean()
benchmark=60
st.markdown("### Executive scorecard")
a,b,c=st.columns(3)
with a:metric("Students analyzed",f"{len(data):,}","Current filtered cohort")
with b:metric("Overall average",f"{overall:.1f} / 100","Across all three subjects")
with c:metric("Above benchmark",f"{(data['Average Score']>=benchmark).mean()*100:.1f}%","Illustrative 60-point benchmark")
a,b,c=st.columns(3)
with a:metric("Mathematics",f"{means['math score']:.1f}","Average subject score")
with b:metric("Reading",f"{means['reading score']:.1f}","Average subject score")
with c:metric("Writing",f"{means['writing score']:.1f}","Average subject score")
st.divider()
st.markdown("### 01 / Academic performance")
a,b=st.columns(2)
with a:
    avg=pd.DataFrame({"Subject":["Math","Reading","Writing"],"Score":means.values})
    fig=px.bar(avg,x="Subject",y="Score",title="Average score by subject",text="Score",color="Subject",color_discrete_sequence=[GOLD,TEAL,BLUE])
    fig.update_traces(texttemplate="%{y:.1f}",textposition="outside")
    fig.update_yaxes(range=[0,110]);plot(fig)
with b:
    fig=px.histogram(data,x="Average Score",nbins=20,title="Student score distribution",color_discrete_sequence=[TEAL])
    fig.add_vline(x=benchmark,line_dash="dash",line_color=GOLD)
    plot(fig)
st.markdown("### 02 / Performance by student group")
for (c1,t1),(c2,t2) in [(filters[0],filters[4]),(filters[2],filters[3]),(filters[1],filters[0])]:
    a,b=st.columns(2)
    for panel,col,title,color in [(a,c1,t1 if False else dict(filters)[c1],GOLD),(b,c2,dict(filters)[c2],BLUE)]:
        with panel:
            grouped=data.groupby(col,as_index=False)["Average Score"].mean().sort_values("Average Score")
            fig=px.bar(grouped,x="Average Score",y=col,orientation="h",title=f"Average score by {title.lower()}",text="Average Score",color_discrete_sequence=[color])
            fig.update_traces(texttemplate="%{x:.1f}",textposition="outside")
            fig.update_xaxes(range=[0,110])
            plot(fig,390)
st.markdown("### 03 / Subject relationships")
corr=data[["math score","reading score","writing score"]].corr()
fig=px.imshow(corr,text_auto=".2f",zmin=-1,zmax=1,color_continuous_scale=[[0,"#405477"],[.5,"#263B53"],[1,TEAL]],title="Correlation between subject scores")
plot(fig,420)
st.markdown("### 04 / Insights")
best=means.idxmax().replace(" score","").title()
weak=means.idxmin().replace(" score","").title()
st.info(f"Highest-scoring subject: {best} ({means.max():.1f}/100).")
st.info(f"Learning support opportunity: {weak} has the lowest average ({means.min():.1f}/100).")
prep=data.groupby("test preparation course")["Average Score"].mean()
if len(prep)>1:
    st.info(f"Test preparation groups differ by {prep.max()-prep.min():.1f} points in average score. This is an association, not evidence of causation.")
st.caption("The 60-point benchmark is illustrative. This dataset does not contain attendance or study-hours measurements.")
with st.expander("Student data explorer and export"):
    st.dataframe(data,use_container_width=True,hide_index=True)
    st.download_button("Download filtered CSV",data.to_csv(index=False).encode("utf-8"),"filtered_students.csv","text/csv")
