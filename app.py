import streamlit as st, yfinance as yf, math, time, requests, plotly.graph_objects as go
st.set_page_config(page_title="GARIS 80", layout="wide")
st.markdown("<h1 style='text-align:center;background:black;color:white;padding:15px;border-radius:15px'>GARIS AI SAKTI 80 ANTI NOISE</h1>", unsafe_allow_html=True)
TOKEN="um5rq6eahrf8EhrmZnKT"; WA="6285182561790"
def get_angle(df):
 df['MA50']=df['Close'].rolling(50).mean(); df=df.dropna()
 if len(df)<21: return 0,0,df
 y1=float(df['MA50'].iloc[-20]); y2=float(df['MA50'].iloc[-1]); ang=abs(math.degrees(math.atan2(y2-y1,20))*10)
 return min(ang,90),float(df['MA50'].iloc[-1]),df
def send_wa(m):
 try: requests.post("https://api.fonnte.com/send",headers={"Authorization":TOKEN},data={"target":WA,"message":m},timeout=10)
 except: pass
c1,c2,c3,c4=st.columns(4); pp=c1.empty(); pa=c2.empty(); pg=c3.empty(); ps=c4.empty(); chart=st.empty(); sig=st.empty()
auto=st.sidebar.checkbox("AUTO RUN 80",True)
if st.sidebar.button("TEST WA"): send_wa("TEST 80 VALID!"); st.sidebar.success("TERKIRIM!")
df=yf.Ticker("GC=F").history(period='2d',interval='5m')
if not df.empty:
 price=float(df['Close'].iloc[-1]); prev=float(df['Close'].iloc[-2]); angle,garis,df2=get_angle(df); sl=garis-2.0; sentuh=prev<=garis and price>=garis
 pp.metric("XAU",f"${price:.2f}"); pa.metric("ANGLE",f"{angle:.1f}"); pg.metric("GARIS 80",f"${garis:.2f}"); ps.metric("SL",f"${sl:.2f}")
 fig=go.Figure(); tail=df2.tail(100)
 fig.add_trace(go.Scatter(y=tail['Close'],name='XAU',line=dict(color='green')))
 fig.add_trace(go.Scatter(y=tail['MA50'],name='MA50',line=dict(color='gold')))
 y_g=[garis-(len(tail)-i)*0.6 for i in range(len(tail))]; y_sl=[g-2 for g in y_g]
 fig.add_trace(go.Scatter(y=y_g,name='GARIS 80',line=dict(color='black',width=3)))
 fig.add_trace(go.Scatter(y=y_sl,name='SL',line=dict(color='red',dash='dash')))
 fig.update_layout(title=f"WHITE 80 {angle:.1f} - {'SENTUH!' if sentuh else 'VALID' if angle>=80 else 'NOISE'}",plot_bgcolor='white',height=380)
 chart.plotly_chart(fig,use_container_width=True)
 if angle>=80 and sentuh: sig.success(f"SENTUH GARIS 80! ${price:.2f} BUY SL ${sl:.2f}"); send_wa(f"SENTUH GARIS 80 ${price:.2f}")
 elif angle>=80: sig.success(f"VALID 80! ${price:.2f} BUY")
 elif angle<30: sig.error(f"NOISE {angle:.1f} SKIP!")
 else: sig.warning(f"WAIT {angle:.1f}")
if auto: time.sleep(10); st.rerun()
